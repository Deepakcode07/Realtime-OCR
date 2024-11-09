#This code can read text in real time from camera and has good accuracy.

import tkinter as tk
import cv2
import pytesseract as tess
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import numpy as np
import easyocr

# Set Tesseract path
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class CameraApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Camera OCR App")

        # Create a label for displaying camera feed
        self.camera_label = tk.Label(self.window)
        self.camera_label.pack(padx=10, pady=10)

        # Create a button to capture an image
        self.capture_button = tk.Button(self.window, text="Capture Image", command=self.capture_image)
        self.capture_button.pack(padx=10, pady=10)

        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        self.update_camera()

        # Initialize EasyOCR Reader
        self.reader = easyocr.Reader(['en'])

    def update_camera(self):
        # Update camera feed
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=img)
            self.camera_label.img = img
            self.camera_label.config(image=img)
        self.window.after(10, self.update_camera)

    def capture_image(self):
        # Capture current frame from camera
        ret, frame = self.cap.read()
        if ret:
            # Convert frame to PIL Image
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            # Perform OCR on the captured image
            self.perform_ocr(img)

    def perform_ocr(self, img):
        try:
            # Apply filters to enhance image quality
            img = img.convert('L')  # Convert to grayscale
            img = img.filter(ImageFilter.MedianFilter())  # Apply median filter for noise reduction
            img = ImageEnhance.Contrast(img).enhance(2)  # Enhance contrast
            img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # Enhance edges

            # Optional: Convert to numpy array for further OpenCV processing
            open_cv_image = np.array(img)
            open_cv_image = cv2.threshold(open_cv_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  # Apply binary thresholding
            img = Image.fromarray(open_cv_image)

            # Option 1: Perform OCR using Tesseract with enhanced configurations
            tesseract_text = tess.image_to_string(img, lang='eng', config='--oem 1 --psm 6')

            # Option 2: Perform OCR using EasyOCR
            easyocr_result = self.reader.readtext(np.array(img), detail=0)
            easyocr_text = "\n".join(easyocr_result)

            # Combine results or choose the best one
            combined_text = f"Tesseract OCR:\n{tesseract_text}\n\nEasyOCR:\n{easyocr_text}"
            
            # Display the extracted text
            self.display_text(combined_text)

        except Exception as e:
            print(f"Error during OCR: {e}")

    def display_text(self, text):
        # Create a new window to display OCR results
        result_window = tk.Toplevel(self.window)
        result_window.title("OCR Result")

        # Display OCR result
        text_label = tk.Label(result_window, text=text, wraplength=400, justify="left")
        text_label.pack(padx=10, pady=10)

# Main function to start the application
def main():
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()


 





# import pytesseract as tess
# from PIL import Image

# # Set Tesseract path
# tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# # Open the image
# img_path = r'C:\Users\deepa\Documents\Downloads\testing.jpg'
# try:
#     img = Image.open(img_path)
#     print(f"Image loaded successfully: {img_path}")

#     # Perform OCR
#     text = tess.image_to_string(img, lang='eng', config='--psm 6')

#     # Print the extracted text
#     print(f"Extracted Text:\n{text}")

# except Exception as e:
#     print(f"Error occurred: {e}")