from tkinter import filedialog
import cv2
import numpy as np
from region_manager import RegionManager, Status

class ImageController:
    def __init__(self):
        self.premise_image_path = None
        self.conclusion_image_path = None
        self.shape_positions = {
            'triangle': None,
            'square': None,
            'pentagon': None,
            'crosses': []
        }

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
        # Convert to grayscale and apply Gaussian Blur
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 3
        )

        # Perform morphological opening to clean noise
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        # Optional: Perform contour filtering for further noise removal
        contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        mask = np.zeros_like(cleaned)

        for contour in contours:
            if cv2.contourArea(contour) > 50:  # Keep only significant contours
                cv2.drawContours(mask, [contour], -1, (255), thickness=cv2.FILLED)

        return cleaned

    def interpret_venn_image(self, image):
        dimensions = self.determine_image_proportion(image)
        
        # Resize the image to fit within the screen
        resized_image = cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)
        
        denoised = self.binary_denoise(resized_image)
        cv2.imshow("Denoised image", denoised)
        
        #strip the shapes from the image
        stripped_image, shapes_only_image = self.strip_shapes(denoised)
        #cv2.imshow("Stripped Image", stripped_image)
        #cv2.imshow("Shapes Only Image", shapes_only_image)
        
        # Use Hough Circle Transform to find circles
        circles = cv2.HoughCircles(denoised, cv2.HOUGH_GRADIENT, dp=1.2, minDist=20, param1=50, param2=30, minRadius=10, maxRadius=200)
        
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            filtered_circles = []
            height, width = resized_image.shape[:2]
            for (x, y, r) in circles:
                # Filter by radius and ensure the circle is within image boundaries
                if r < 100 or r > 500:
                    continue
                if x - r < 0 or x + r > width or y - r < 0 or y + r > height:
                    continue
                filtered_circles.append((x, y, r))
            
            # Sort circles by radius in descending order
            filtered_circles = sorted(filtered_circles, key=lambda c: c[2], reverse=True)
            
            # Select the top 3 circles that are a set distance away from each other
            selected_circles = []
            min_distance = 100  # Set the minimum distance between circles
            for circle in filtered_circles:
                if len(selected_circles) >= 3:
                    break
                if all(np.linalg.norm(np.array(circle[:2]) - np.array(selected[:2])) >= min_distance for selected in selected_circles):
                    selected_circles.append(circle)
            
            for (x, y, r) in selected_circles:
                # Draw the circle in the output image, then draw a rectangle corresponding to the center of the circle
                cv2.circle(resized_image, (x, y), r, (0, 255, 0), 2)
                cv2.rectangle(resized_image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

            cv2.imshow("Detected Circles", resized_image)
        
        return RegionManager([])

    def detect_shapes(self, image):
        # Create a blank image to draw shapes on
        shapes_image = np.zeros_like(image)
        
        # Define colors for each shape type
        colors = {
            'triangle': (0, 255, 0),  # Green
            'square': (255, 0, 0),    # Blue
            'pentagon': (0, 0, 255),  # Red
            'cross': (255, 255, 0)    # Cyan
        }
        
        # Find contours in the image
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            # Filter contours by area
            area = cv2.contourArea(contour)
            if area < 100 or area > 10000:
                continue
            
            # Approximate the contour
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Determine the shape based on the number of vertices
            if len(approx) == 3:
                self.shape_positions['triangle'] = self.get_contour_center(contour)
                cv2.drawContours(shapes_image, [contour], -1, colors['triangle'], 2)
            elif len(approx) == 4:
                # Check if the shape is a square
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = float(w) / h
                if 0.9 < aspect_ratio < 1.1:
                    self.shape_positions['square'] = self.get_contour_center(contour)
                    cv2.drawContours(shapes_image, [contour], -1, colors['square'], 2)
            elif len(approx) == 5:
                self.shape_positions['pentagon'] = self.get_contour_center(contour)
                cv2.drawContours(shapes_image, [contour], -1, colors['pentagon'], 2)
            elif self.is_cross(contour):
                self.shape_positions['crosses'].append(self.get_contour_center(contour))
                cv2.drawContours(shapes_image, [contour], -1, colors['cross'], 2)
        
        print("Detected shapes:", self.shape_positions)
        
        # Display the shapes image
        cv2.imshow("Shapes Image", shapes_image)
        
        return self.shape_positions

    def get_contour_center(self, contour):
        moments = cv2.moments(contour)
        if moments["m00"] == 0:
            return None
        center_x = int(moments["m10"] / moments["m00"])
        center_y = int(moments["m01"] / moments["m00"])
        
        # Return the center coordinates as a tuple
        return (center_x, center_y)

    def is_cross(self, contour):
        bounding_rect = cv2.boundingRect(contour)
        aspect_ratio = float(bounding_rect[2]) / bounding_rect[3]
        
        # Check if the aspect ratio is close to 1 (square-like)
        if 0.8 < aspect_ratio < 1.2:
            # Check for intersecting lines
            intersections = 0
            for i in range(len(contour)):
                for j in range(i + 1, len(contour)):
                    if np.linalg.norm(contour[i] - contour[j]) < 10:  # Threshold for intersection
                        intersections += 1
            if intersections > 4:  # Threshold for number of intersections
                return True
        return False

    def strip_shapes(self, image):
        # Create a copy of the original image to work on
        stripped_image = image.copy()
        
        # Create a blank image to store the shapes
        shapes_only_image = np.zeros_like(image)
        
        # Detect shapes
        self.detect_shapes(stripped_image)
        
        # Create a mask for the detected shapes
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        for shape, position in self.shape_positions.items():
            if position is not None:
                if shape == 'crosses':
                    for pos in position:
                        cv2.circle(mask, pos, 10, 255, -1)  # Adjust the radius as needed
                else:
                    cv2.circle(mask, position, 10, 255, -1)  # Adjust the radius as needed
        
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
