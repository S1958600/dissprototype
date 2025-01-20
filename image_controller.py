from tkinter import filedialog
import cv2
import numpy as np
from region_manager import RegionManager, Status
import math

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
        
        stripped_image, shapes_only_image = self.strip_shapes(denoised)
        
        selected_circles = self.detect_circles(denoised)

            
        for (x, y, r) in selected_circles:
            # Draw the circle in the output image, then draw a rectangle corresponding to the center of the circle
            cv2.circle(resized_image, (x, y), r, (0, 255, 0), 2)
            cv2.rectangle(resized_image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

            cv2.imshow("Detected Circles", resized_image)
        
        return RegionManager([])
    
    def detect_circles(self, image):
        # Use Hough Circle Transform to find circles
        circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=14, param2=25, minRadius=10, maxRadius=600)
        
        if circles is None:
            #throw exception
            return
        
        circles = np.round(circles[0, :]).astype("int")
        filtered_circles = []
        height, width = image.shape[:2]
        
        for (x, y, r) in circles:
            # check the radius does not exceed the image boundaries
            if x - r < 0 or x + r > width or y - r < 0 or y + r > height:
                continue
            filtered_circles.append((x, y, r))
        
        # Sort circles by radius in descending order
        filtered_circles = sorted(filtered_circles, key=lambda c: c[2], reverse=True)
        
        selected_circles = []
        min_distance_factor = 0.15  # Set the minimum distance for x*2r distance between circles
        # smaller factor means circles can be closer together
        
        for circle in filtered_circles:
            if len(selected_circles) >= 3:
                # check if the radius is within set percentage of the selected circles
                if all(abs(circle[2] - selected[2]) / selected[2] <= 0.05 for selected in selected_circles):
                    break
                else:
                    selected_circles.pop(0)
            
            # if the distance between the centers is less than the sum of the radii
            # and greater than the minimum distance factor times the sum of the radii
            if all(np.linalg.norm(np.array(circle[:2]) - np.array(selected[:2])) <= (circle[2] + selected[2]) and
                np.linalg.norm(np.array(circle[:2]) - np.array(selected[:2])) >= min_distance_factor * (circle[2] + selected[2])
                for selected in selected_circles):
                
                selected_circles.append(circle)
        
        return selected_circles

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
