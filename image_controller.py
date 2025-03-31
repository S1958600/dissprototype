from tkinter import filedialog
import cv2
import numpy as np
from region_manager import RegionManager, Status
import math
import itertools

class ImageController:
    def __init__(self):
        self.premise_image_path = None
        self.conclusion_image_path = None

    def upload_premise_image(self):
        self.premise_image_path = filedialog.askopenfilename(title="Select Premise Venn Diagram Image", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        return self.premise_image_path

    def upload_conclusion_image(self):
        self.conclusion_image_path = filedialog.askopenfilename(title="Select Conclusion Venn Diagram Image", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        return self.conclusion_image_path

    def process_images(self):
        if not self.premise_image_path or not self.conclusion_image_path:
            raise ValueError("Both premise and conclusion images must be uploaded before processing.")
        
        premise_image = cv2.imread(self.premise_image_path)
        conclusion_image = cv2.imread(self.conclusion_image_path)
        
        # generate a region manager for both images
        premise_venn_manager = self.interpret_venn_image(premise_image)
        conclusion_venn_manager = self.interpret_venn_image(conclusion_image)
        
        return premise_venn_manager, conclusion_venn_manager

    def determine_image_proportion(self, image, max_dimension=720):
        # Find dimensions of the image
        height, width, _ = image.shape
        
        # Calculate the scale factor to resize the image while maintaining the aspect ratio
        scale_factor = max_dimension / max(height, width)
        
        # Resize dimensions
        new_height = int(height * scale_factor)
        new_width = int(width * scale_factor)

        return (new_width, new_height)
    
    def binary_denoise(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 3)

        #morphological opening to clean noise
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        
        """
        #show each step of image processing for report
        cv2.imshow("input image", image)
        cv2.imshow("Gray image", gray)
        cv2.imshow("gaussian blur", blurred)
        cv2.imshow("Adaptive Threshold", thresh)
        cv2.imshow("Morphological Opening", cleaned)
        #"""

        return cleaned

    def interpret_venn_image(self, image):
        dimensions = self.determine_image_proportion(image)
        resized_image = cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)
        denoised = self.binary_denoise(resized_image)
        
        #cv2.imshow("Denoised image", denoised)
                
        drawing_img = resized_image.copy() # dev purposes only
        
        selected_circles = self.detect_circles(denoised, drawing_img)
        
        #"""
        # display the selected circles    
        for (x, y, r) in selected_circles:
            # Draw the circle in the output image, then draw a rectangle corresponding to the center of the circle
            cv2.circle(resized_image, (x, y), r, (0, 255, 0), 2)
            cv2.rectangle(resized_image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        cv2.imshow("Selected Circles", resized_image)
        #"""
        
        # identify each region and what set(s) it belongs to
        region_masks = self.generate_region_masks(denoised, selected_circles)
        
        #check all region masks and interpret the regions
        region_manager = self.interpret_all_regions(denoised, region_masks)
                
        #region_manager.print_regions()
        
        return region_manager
    

    def detect_circles(self, image, drawing_img):
        # Use Hough Circle Transform to find circles
        circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=800, param2=30, minRadius=10, maxRadius=600)
        
        if circles is None:
            #throw an error if no circles are detected
            raise ValueError("No circles detected in the image")
        
        
        circles = np.round(circles[0, :]).astype("int")
        filtered_circles = []
        height, width = image.shape[:2]
        
        for (x, y, r) in circles:
            # check the radius does not exceed the image boundaries
            if x - r < 0 or x + r > width or y - r < 0 or y + r > height:
                continue
            # check the radius is smaller than 10% of the image dimensions
            if r / max(height, width) < 0.1:
                continue
            filtered_circles.append((x, y, r))
        
        """
        # Print all circles detected
        image_copy = image.copy()
        #enable colour on binary image copy
        image_copy = cv2.cvtColor(image_copy, cv2.COLOR_GRAY2BGR)
        
        for i, (x, y, r) in enumerate(filtered_circles, start=1):
            cv2.circle(image_copy, (x, y), r, (0, 255, 0), 2)
            cv2.rectangle(image_copy, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        cv2.imshow("All Circles", image_copy)
        #"""
        
        
        # remove bottom 20% of circles
        filtered_circles.sort(key=lambda x: x[1], reverse=True)
        filtered_circles = filtered_circles[:int(0.8 * len(filtered_circles))]
        
        """
        # Print 20 largest circles
        filtered_circles.sort(key=lambda x: x[2], reverse=True)
        circle_count = min(20, len(filtered_circles))
        for i, (x, y, r) in enumerate(filtered_circles[:circle_count], start=1):
            print(f"Circle {i}: center=({x}, {y}), radius={r}")
            cv2.circle(drawing_img, (x, y), r, (0, 255, 0), 2)
            cv2.rectangle(drawing_img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            cv2.putText(drawing_img, str(i), (x - 5, y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.imshow("largest circles", drawing_img)
        #"""

        valid_triplets = []
        # for each circle in the list, find all valid 3 circle combinations
        while filtered_circles:
            circle = filtered_circles.pop(0)
            valid_triplets.extend(self.find_valid_triplets(circle, filtered_circles))
            
        # Select the valid triplet with the greatest confidence
        selected_circles = []
        max_confidence_score = 0
                
        for triplet in valid_triplets:
            confidence_score = self.calculate_circle_confidence(triplet, image)
            if confidence_score > max_confidence_score:
                max_confidence_score = confidence_score
                selected_circles = triplet
                
        
        """
        # Draw 20 largest radii valid triplets
        triplet_image = drawing_img.copy()
        valid_triplets.sort(key=lambda x: sum([circle[2] for circle in x]), reverse=True)
        triplet_count = min(20, len(valid_triplets))
        for triplet in valid_triplets[:triplet_count]:
            for (x, y, r) in triplet:
                cv2.circle(triplet_image, (x, y), r, (0, 255, 0), 2)
                cv2.rectangle(triplet_image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            cv2.imshow("Triplets - largest", triplet_image)
        #"""        
        
        """        
        # Print 20 most confident triplets in different colors
        valid_triplets.sort(key=lambda x: self.calculate_circle_confidence(x, image), reverse=True)
        triplet_count = min(20, len(valid_triplets))
        
        # Draw the triplets in reverse order to make the more confident circles more visible
        for i, triplet in enumerate(reversed(valid_triplets[:triplet_count]), start=1):
            confidence = self.calculate_circle_confidence(triplet, image)
            # Calculate color based on confidence rank
            color = (0, int(255 * (1 - (i / triplet_count))), int(255 * (i / triplet_count)))
            
            for (x, y, r) in triplet:
                cv2.circle(drawing_img, (x, y), r, color, 2)
                cv2.rectangle(drawing_img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        
        cv2.imshow("Triplets - most confident", drawing_img)
        #"""
        
        return selected_circles
    
    def find_valid_triplets(self, circle, circles):
        #minimum distance between the circles is some fraction of r
        min_distance_factor = 0.8
        min_distance = min_distance_factor * circle[2]
        
        #maximum distance between the circles is 2r -> not intersecting if radii are equal (they should be)
        max_distance = 2 * circle[2]
        
        radius_tolerance = 0.1  # Set the percentage tolerance for the radius difference between circles
        min_radius = circle[2] - radius_tolerance * circle[2]
        max_radius = circle[2] + radius_tolerance * circle[2]
        
        valid_triplets = []
        #for each pair of circles from the list, check if all 3 circles are valid
        for pair in itertools.combinations(circles, 2):
            circle1, circle2 = pair
            triplet_valid = True
            
            #check if the radii of the 2 circles are within the tolerance
            if not (min_radius <= circle1[2] <= max_radius and min_radius <= circle2[2] <= max_radius):
                triplet_valid = False
                continue
            
            #check if the distance between each of the 3 circles is within the min and max distance
            distance12 = math.sqrt((circle1[0] - circle2[0]) ** 2 + (circle1[1] - circle2[1]) ** 2)
            distance01 = math.sqrt((circle1[0] - circle[0]) ** 2 + (circle1[1] - circle[1]) ** 2)
            distance02 = math.sqrt((circle2[0] - circle[0]) ** 2 + (circle2[1] - circle[1]) ** 2)
            distances =[distance12, distance01, distance02]
            
            for distance in distances:
                if not (min_distance <= distance <= max_distance):
                    triplet_valid = False
                    break
            
            #skips to the next iteration of pairs if the triplet is not valid    
            if not triplet_valid:
                continue
            
            # Calculate the center point of the triangle formed by the centers of the three circles
            centroid_x = (circle1[0] + circle2[0] + circle[0]) / 3
            centroid_y = (circle1[1] + circle2[1] + circle[1]) / 3
            
            # Check if the center point is within a radius distance from each of the three circle centers
            for circle in [circle1, circle2, circle]:
                centroid_distance = math.sqrt((centroid_x - circle[0]) ** 2 + (centroid_y - circle[1]) ** 2)
                if centroid_distance > circle[2]:
                    triplet_valid = False
                    break     
            
            if triplet_valid:
                valid_triplets.append([circle1, circle2, circle])
                
        return valid_triplets
    
    def calculate_circle_confidence(self, triplet, binary_image):
        w1=0.15 # weight for radius similarity              
        w2=0.1 # weight for distance consistency            
        w3=0.35 # weight for size bonus                 
        w4=0.4 # weight for mean highlighted percentage
        
        circle1, circle2, circle3 = triplet
        radii = [circle1[2], circle2[2], circle3[2]]
        distances = [
            math.sqrt((circle1[0] - circle2[0]) ** 2 + (circle1[1] - circle2[1]) ** 2),
            math.sqrt((circle1[0] - circle3[0]) ** 2 + (circle1[1] - circle3[1]) ** 2),
            math.sqrt((circle2[0] - circle3[0]) ** 2 + (circle2[1] - circle3[1]) ** 2)
        ]
        
        # Radius similarity
        mean_radius = np.mean(radii)
        std_radius = np.std(radii)   # standard deviation
        radius_similarity = 1 - (std_radius / mean_radius)  # larger similarity = more similar radii
        
        # Distance consistency
        mean_distance = np.mean(distances)
        std_distance = np.std(distances)
        distance_consistency = 1 - (std_distance / mean_distance)
        
        # Size bonus
        max_radius = 360 # Maximum radius of a circle for normalization
        size_bonus = mean_radius / max_radius
        
        # Highlighted percentage
        highlighted_percentages = [self.calculate_highlighted_percentage(circle, binary_image) for circle in triplet]
        mean_highlighted_percentage = np.mean(highlighted_percentages)
        
        
        # Weighted confidence
        confidence = (
            w1 * radius_similarity +
            w2 * distance_consistency +
            w3 * size_bonus +
            w4 * mean_highlighted_percentage
        )
        
        return max(0, min(confidence, 1))  #clamps to [0, 1]
    
    def calculate_highlighted_percentage(self, circle, binary_image):
        mask = np.zeros(binary_image.shape, dtype=np.uint8) # Create a mask for the circle
        cv2.circle(mask, (circle[0], circle[1]), circle[2], 255, thickness=2)  # Only draw the edge with thickness=2
        highlighted_region = cv2.bitwise_and(binary_image, binary_image, mask=mask)
        total_edge_pixels = cv2.countNonZero(mask)   # Total number of edge pixels in the circles edge
        highlighted_edge_pixels = cv2.countNonZero(highlighted_region)   # Number of highlighted edge pixels
        highlighted_percentage = highlighted_edge_pixels / total_edge_pixels
        return highlighted_percentage
    
    def generate_region_masks(self, image, circles):
        # A is top left, B is top right, C is center - selected by x coord order
        sorted_circles = sorted(circles, key=lambda c: c[0])
        sets = {'A': sorted_circles[0], 'B': sorted_circles[2], 'C': sorted_circles[1]}
        
        # Create a mask for each circle
        height, width = image.shape[:2]
        small_mask_A = np.zeros((height, width), dtype=np.uint8)
        small_mask_B = np.zeros((height, width), dtype=np.uint8)
        small_mask_C = np.zeros((height, width), dtype=np.uint8)
        
        big_mask_A = np.zeros((height, width), dtype=np.uint8)
        big_mask_B = np.zeros((height, width), dtype=np.uint8)
        big_mask_C = np.zeros((height, width), dtype=np.uint8)
        
        # Reduce the radius by a small amount to exclude the edges
        radius_reduction = 10  # Reduce the radius by x pixels
        
        cv2.circle(small_mask_A, (sets['A'][0], sets['A'][1]), sets['A'][2] - radius_reduction, 255, thickness=-1)
        cv2.circle(small_mask_B, (sets['B'][0], sets['B'][1]), sets['B'][2] - radius_reduction, 255, thickness=-1)
        cv2.circle(small_mask_C, (sets['C'][0], sets['C'][1]), sets['C'][2] - radius_reduction, 255, thickness=-1)
        
        # Increase the radius by a small amount for regions outside the circle
        cv2.circle(big_mask_A, (sets['A'][0], sets['A'][1]), sets['A'][2] + radius_reduction, 255, thickness=-1)
        cv2.circle(big_mask_B, (sets['B'][0], sets['B'][1]), sets['B'][2] + radius_reduction, 255, thickness=-1)
        cv2.circle(big_mask_C, (sets['C'][0], sets['C'][1]), sets['C'][2] + radius_reduction, 255, thickness=-1)
        
        
        #masks identified by region tuple - note NULL region is not considered
        #use bitwise and for efficiency
        region_masks = {
            (True, False, False): cv2.bitwise_and(small_mask_A, cv2.bitwise_not(cv2.bitwise_or(big_mask_B, big_mask_C))),  # A
            (False, True, False): cv2.bitwise_and(small_mask_B, cv2.bitwise_not(cv2.bitwise_or(big_mask_A, big_mask_C))),  # B
            (False, False, True): cv2.bitwise_and(small_mask_C, cv2.bitwise_not(cv2.bitwise_or(big_mask_A, big_mask_B))),  # C
            (True, True, False): cv2.bitwise_and(cv2.bitwise_and(small_mask_A, small_mask_B), cv2.bitwise_not(big_mask_C)),  # AB
            (True, False, True): cv2.bitwise_and(cv2.bitwise_and(small_mask_A, small_mask_C), cv2.bitwise_not(big_mask_B)),  # AC
            (False, True, True): cv2.bitwise_and(cv2.bitwise_and(small_mask_B, small_mask_C), cv2.bitwise_not(big_mask_A)),  # BC
            (True, True, True): cv2.bitwise_and(cv2.bitwise_and(small_mask_A, small_mask_B), small_mask_C)  # ABC
        }
        
        #"""
        #dev image for testing, use colour to identify regions in BGR format
        #all_regions = np.zeros((height, width, 3), dtype=np.uint8)
        
        #all regions is a copy of the input image
        all_regions = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        all_regions[region_masks[(True, False, False)] == 255] = (0, 0, 255)  # A is red
        all_regions[region_masks[(False, True, False)] == 255] = (0, 255, 0)  # B is green
        all_regions[region_masks[(False, False, True)] == 255] = (255, 0, 0)  # C is blue
        all_regions[region_masks[(True, True, False)] == 255] = (0, 255, 255)  # other colours are combinations
        all_regions[region_masks[(True, False, True)] == 255] = (255, 0, 255)   
        all_regions[region_masks[(False, True, True)] == 255] = (255, 255, 0)   
        all_regions[region_masks[(True, True, True)] == 255] = (255, 255, 255)  
        cv2.imshow("All Regions", all_regions)
        #"""
        
        return region_masks
    
    
    def get_pixel_region_tuple(self, x, y, circleA, circleB, circleC):
        # check if the pixel is in each circle
        inA = self.is_pixel_in_circle(x, y, circleA)
        inB = self.is_pixel_in_circle(x, y, circleB)
        inC = self.is_pixel_in_circle(x, y, circleC)
        
        return (inA, inB, inC)
    
    def is_pixel_in_circle(self, x, y, circle):
        # uses pythagarean theorem to check if the pixel is within the circle - np is faster than math
        dx = np.array(x) - circle[0]
        dy = np.array(y) - circle[1]
        r = circle[2]
        return np.square(dx) + np.square(dy) < np.square(r)  # True if pixel is less than r away from the center
    
    def interpret_all_regions(self, image, region_masks):
        # for each region mask, interpret the region
        region_manager = RegionManager([])
        
        for region_tuple, region_mask in region_masks.items():
            status = self.interpret_region(image, region_mask)
            region_manager.set_habitability(region_tuple, status)
             
        return region_manager
    
    def interpret_region(self, image, region_mask):
        # check if the region is shaded
        is_shaded = self.check_shaded(image, region_mask)
        if is_shaded:
            return Status.UNINHABITABLE
        
        # check if the region has a cross
        is_checked = self.check_cross(image, region_mask)
        if is_checked:
            return Status.CONTAINS
        
        return Status.HABITABLE
    
    def check_shaded(self, binary_image, region_mask, threshold=0.2):
        #get the region of the image that is within the region mask
        region = cv2.bitwise_and(binary_image, binary_image, mask=region_mask)
        
        #find proportion of shaded pixels
        total_region_pixels = cv2.countNonZero(region_mask)
        shaded_region_pixels = cv2.countNonZero(region)
        shaded_ratio = shaded_region_pixels / total_region_pixels
        
        is_shaded = shaded_ratio > threshold
        #print(f"Region has {shaded_ratio * 100:.2f}% shaded spixels")
        return is_shaded
    
    
    def check_cross(self, binary_image, region_mask):
        # Extract the region using the mask
        region = cv2.bitwise_and(binary_image, binary_image, mask=region_mask)
        edges = cv2.Canny(region, 50, 150)
        
        # Find contours in the region
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        dev_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        
        if len(contours) == 0:
            #print("No contours detected")
            return False
        
        cross_detected = False
        area_threshold_lower = 30
        area_threshold_upper = 300
        
        # Check each contour to see if it resembles a cross
        for contour in contours:
            if cv2.contourArea(contour) < area_threshold_lower:
                continue
            
            #x, y, w, h = cv2.boundingRect(contour)
            #bounding_box_area = w * h
            #if bounding_box_area > area_threshold_upper:
            #    continue
            
            if self.is_cross(contour):
                # Draw the contour in green if it is detected as a cross
                cv2.drawContours(dev_image, [contour], -1, (0, 255, 0), 2)
                cross_detected = True
            else:
                # Draw the contour in red if it is not detected as a cross
                cv2.drawContours(dev_image, [contour], -1, (0, 0, 255), 2)
        
        #if cross_detected:
        #    cv2.imshow("Cross Detection", dev_image)
        
        return cross_detected

    def is_cross(self, contour):
        # Approximate the contour to reduce the number of points
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Check if the contour has a specific number of points (approximate for a cross shape)
        if len(approx) >= 8 and len(approx) <= 14:
            # Additional checks can be added here to verify the shape of the contour
            # For example, checking the aspect ratio, area, etc.
            return True
        
        return False