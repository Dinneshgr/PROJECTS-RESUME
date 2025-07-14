import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf
import os

# --- Configuration ---
IMG_DISPLAY_WIDTH = 300
IMG_DISPLAY_HEIGHT = 300
WINDOW_TITLE = "Brain Stroke Predictor from CT Scan"

# Load the model
model = tf.keras.models.load_model('E:/code parts/best_brain_stroke_model (1).h5')  # Update path to your .h5 model

# Print model summary to debug input shape
print(model.summary())
print("Expected input shape:", model.input_shape)

# Prediction function
def predict_stroke_from_image(image_path):
    try:
        # Load image in RGB mode (adjust based on model input)
        img = Image.open(image_path).convert('RGB')  # Use 'L' if model expects grayscale
        target_size = (224, 224)
        img_resized = img.resize(target_size)
        img_array = np.array(img_resized) / 255.0  # Shape: (224, 224, 3) for RGB
        img_batch = np.expand_dims(img_array, axis=0)  # Shape: (1, 224, 224, 3)

        # Make prediction
        prediction_scores = model.predict(img_batch)
        predicted_class_index = np.argmax(prediction_scores[0])
        confidence = prediction_scores[0][predicted_class_index]

        class_labels = ["No Stroke Detected", "Stroke Detected"]
        prediction_text = class_labels[predicted_class_index]
        confidence_text = f"Confidence: {confidence:.2%}"

        return prediction_text, confidence_text

    except Exception as e:
        print(f"Error during prediction: {e}")
        return "Error in prediction", str(e)

# GUI Application Class
class StrokePredictorApp:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry("500x600")

        self.image_path = None
        self.tk_image = None

        # UI Elements
        self.title_label = tk.Label(root, text="Brain Stroke Prediction", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=10)

        self.image_frame = tk.Frame(root, width=IMG_DISPLAY_WIDTH, height=IMG_DISPLAY_HEIGHT,
                                   relief="sunken", borderwidth=2)
        self.image_frame.pack(pady=10)
        self.image_frame.pack_propagate(False)

        self.image_label = tk.Label(self.image_frame, text="No Image Selected")
        self.image_label.pack(expand=True, fill="both")

        self.browse_button = tk.Button(root, text="Browse CT Scan Image", command=self.browse_image,
                                      font=("Arial", 12))
        self.browse_button.pack(pady=10)

        self.predict_button = tk.Button(root, text="Predict Stroke", command=self.predict_stroke,
                                       font=("Arial", 14, "bold"), bg="lightblue")
        self.predict_button.pack(pady=15)

        self.result_label = tk.Label(root, text="Prediction: N/A", font=("Arial", 14))
        self.result_label.pack(pady=5)

        self.confidence_label = tk.Label(root, text="Confidence: N/A", font=("Arial", 12))
        self.confidence_label.pack(pady=5)

        self.status_label = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def browse_image(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Select CT Scan Image",
                filetypes=(("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff"),
                          ("All files", "*.*"))
            )
            if file_path:
                self.image_path = file_path
                self.status_label.config(text=f"Loaded: {file_path.split('/')[-1]}")

                img = Image.open(self.image_path)
                img.thumbnail((IMG_DISPLAY_WIDTH, IMG_DISPLAY_HEIGHT))

                self.tk_image = ImageTk.PhotoImage(img)
                self.image_label.config(image=self.tk_image, text="")
                self.image_label.image = self.tk_image

                self.result_label.config(text="Prediction: N/A")
                self.confidence_label.config(text="Confidence: N/A")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")
            self.status_label.config(text="Error loading image")

    def predict_stroke(self):
        if not self.image_path:
            messagebox.showwarning("No Image", "Please select a CT scan image first.")
            return

        self.status_label.config(text="Processing...")
        self.root.update_idletasks()

        try:
            prediction, confidence = predict_stroke_from_image(self.image_path)

            self.result_label.config(text=f"Prediction: {prediction}")
            self.confidence_label.config(text=confidence)
            self.status_label.config(text="Prediction complete.")

            if "Error" in prediction:
                messagebox.showerror("Prediction Error", confidence)

        except Exception as e:
            messagebox.showerror("Prediction Error", f"An unexpected error occurred: {e}")
            self.result_label.config(text="Prediction: Error")
            self.confidence_label.config(text="")
            self.status_label.config(text="Error during prediction.")

if __name__ == "__main__":
    root = tk.Tk()
    app = StrokePredictorApp(root)
    root.mainloop()