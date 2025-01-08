from tkinter import filedialog
import cv2
import numpy

from region_manager import RegionManager
from region_struct import Status

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
        
        #placeholder dud return
        premise_venn_manager, conclusion_venn_manager = self.dud_return()
        
        return premise_venn_manager, conclusion_venn_manager


    def interpret_venn_image(self, image):
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise and improve circle detection
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)
        
        # Use Hough Circle Transform to detect circles
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50, param1=50, param2=30, minRadius=20, maxRadius=100)
        
        venn_data = {}
        
        if circles is not None:
            circles = numpy.round(circles[0, :]).astype("int")
            
            # Initialize a blank image for region analysis
            regions = numpy.zeros_like(gray)
            
            for (x, y, r) in circles:
                # Draw the detected circles on the regions image
                cv2.circle(regions, (x, y), r, (255, 255, 255), thickness=-1)
            
            # Analyze the regions formed by the intersections of the circles
            venn_data = self.analyze_regions(regions, circles)
        
        return venn_data

    def analyze_regions(self, regions, circles):
        venn_data = {}
        
        # Placeholder for region analysis logic
        # You can use contours or other methods to analyze the regions formed by the intersections of the circles
        
        # Example: Identify the regions and their status
        for i, (x, y, r) in enumerate(circles):
            venn_data[f"circle_{i}"] = {
                "center": (x, y),
                "radius": r,
                "status": "contains"  # Replace with actual status based on region analysis
            }
        
        return venn_data
    
    
    def dud_return(self):
        premise_manager = RegionManager([])
        premise_manager.set_habitability((1, 1, 1), Status.CONTAINS)
        
        conclusion_manager = RegionManager([])
        conclusion_manager.set_habitability((1, 1, 1), Status.UNINHABITABLE)
        
        return premise_manager, conclusion_manager