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

        return cleaned

    def interpret_venn_image(self, image):
        dimensions = self.determine_image_proportion(image)
        resized_image = cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)
        denoised = self.binary_denoise(resized_image)
        cv2.imshow("Denoised image", denoised)
        
        #stripped_image, shapes_only_image = self.strip_shapes(denoised)
        
        drawing_img = resized_image.copy()
        
        selected_circles = self.detect_circles(denoised, drawing_img)
            
        for (x, y, r) in selected_circles:
            # Draw the circle in the output image, then draw a rectangle corresponding to the center of the circle
            cv2.circle(resized_image, (x, y), r, (0, 255, 0), 2)
            cv2.rectangle(resized_image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        cv2.imshow("Selected Circles", resized_image)
        
        return RegionManager([])
    

    def detect_circles(self, image, drawing_img):
        # Use Hough Circle Transform to find circles
        circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=800, param2=30, minRadius=10, maxRadius=600)
        
        if circles is None:
            print("No circles detected - returning")
            return
        
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
        """

        valid_triplets = []
        # for each circle in the list, find all valid 3 circle combinations
        while filtered_circles:
            circle = filtered_circles.pop(0)
            valid_triplets.extend(self.find_valid_triplets(circle, filtered_circles))
            
        # Select the valid triplet with the greatest confidence
        selected_circles = []
        max_confidence_score = 0
                
        for triplet in valid_triplets:
            confidence_score = self.calculate_circle_confidence(triplet)
            if confidence_score > max_confidence_score:
                max_confidence_score = confidence_score
                selected_circles = triplet
                
        
        # Draw 20 largest radii valid triplets
        triplet_image = drawing_img.copy()
        valid_triplets.sort(key=lambda x: sum([circle[2] for circle in x]), reverse=True)
        triplet_count = min(20, len(valid_triplets))
        for triplet in valid_triplets[:triplet_count]:
            for (x, y, r) in triplet:
                cv2.circle(triplet_image, (x, y), r, (0, 255, 0), 2)
                cv2.rectangle(triplet_image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            cv2.imshow("Triplets - largest", triplet_image)
                
                
        #print 20 most confident triplets
        valid_triplets.sort(key=lambda x: self.calculate_circle_confidence(x), reverse=True)
        triplet_count = min(20, len(valid_triplets))
        for i, triplet in enumerate(valid_triplets[:triplet_count], start=1):
            #print(f"Triplet {i}: confidence={self.calculate_circle_confidence(triplet)}")
            for (x, y, r) in triplet:
                cv2.circle(drawing_img, (x, y), r, (0, 255, 0), 2)
                cv2.rectangle(drawing_img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        cv2.imshow("Triplets - most confident", drawing_img)
        
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
            distances = []
            distances.append(math.sqrt((circle1[0] - circle2[0]) ** 2 + (circle1[1] - circle2[1]) ** 2))
            distances.append(math.sqrt((circle1[0] - circle[0]) ** 2 + (circle1[1] - circle[1]) ** 2))
            distances.append(math.sqrt((circle2[0] - circle[0]) ** 2 + (circle2[1] - circle[1]) ** 2))
                
            for distance in distances:
                if not (min_distance <= distance <= max_distance):
                    triplet_valid = False
                    break
            
            if triplet_valid:
                valid_triplets.append([circle1, circle2, circle])
                
        return valid_triplets
    
    def calculate_circle_confidence(self, triplet):
        w1=0.2 # weight for radius similarity
        w2=0.4 # weight for distance consistency
        w3=0.4 # weight for size bonus
        
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
        max_radius = 600 # Maximum radius of a circle for normalization
        size_bonus = mean_radius / max_radius
        
        # Weighted confidence
        confidence = (
            w1 * radius_similarity +
            w2 * distance_consistency +
            w3 * size_bonus
        )
        
        return max(0, min(confidence, 1))  #clamps to [0, 1]

    def detect_crosses(self, image):
        crosses_image = np.zeros_like(image)
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
        # Search for crosses
        cross_positions = []
        bounding_boxes = []
        for contour in contours:
            if self.is_cross(image, contour):
                center = self.get_contour_center(contour)
                if center is not None:
                    cross_positions.append(center)
                    bounding_boxes.append(cv2.boundingRect(contour))
                    
                    # Draw the bounding box and center of the cross
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(crosses_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    cv2.circle(crosses_image, center, 5, (0, 0, 255), -1)
        
        cv2.imshow("Crosses", crosses_image)
        
        return bounding_boxes, cross_positions

    def is_cross(self, image, contour):
        # Approximate the contour to reduce the number of points
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        #tolerance for the number of points
        if not (3 <= len(approx) <= 16):
            return False
        
        return True

        
    def get_contour_center(self, contour):
        moments = cv2.moments(contour)
        if moments["m00"] == 0:
            return None
        center_x = int(moments["m10"] / moments["m00"])
        center_y = int(moments["m01"] / moments["m00"])
        
        return (center_x, center_y)


    def strip_shapes(self, image):
        # Create a copy of the original image to work on
        stripped_image = image.copy()
        
        # Create a blank image to store the shapes
        shapes_only_image = np.zeros_like(image)
        
        # Detect crosses
        bounding_boxes, cross_positions = self.detect_crosses(image)
        
        # Create a mask for the detected shapes
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        for (x, y, w, h) in bounding_boxes:
            cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)
        
        # Create the shapes only image
        shapes_only_image = cv2.bitwise_and(image, image, mask=mask)
        
        # Invert the mask to remove the shapes from the original image
        inverted_mask = cv2.bitwise_not(mask)
        stripped_image = cv2.bitwise_and(image, image, mask=inverted_mask)
        
        return stripped_image, shapes_only_image

    def dud_return(self):
        premise_manager = RegionManager([])
        premise_manager.set_habitability((1, 1, 1), Status.CONTAINS)
        
        conclusion_manager = RegionManager([])
        conclusion_manager.set_habitability((1, 1, 1), Status.UNINHABITABLE)
        
        return premise_manager, conclusion_manager
