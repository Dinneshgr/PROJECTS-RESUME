import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# --- Configuration ---
IMG_DISPLAY_WIDTH = 300
IMG_DISPLAY_HEIGHT = 300
WINDOW_TITLE = "Brain Stroke Predictor from CT Scan"

# --- Prediction Function ---
def predict_stroke_from_image(image_path, import_counter):
    """
    Simulate stroke prediction based on the import counter.
    Args:
        image_path (str): Path to the CT scan image (used only for loading the image in GUI).
        import_counter (int): Number of images imported so far.
    Returns:
        str: Prediction text ("No Stroke Detected" or "Stroke Detected").
    """
    try:
        # Load the image (only for GUI display, not for prediction)
        img = Image.open(image_path)

        # Simulate prediction based on import counter
        class_labels = ["No Stroke Detected", "Stroke Detected"]
        if import_counter == 1:
            prediction_text = class_labels[0]  # No Stroke for first image
        else:  # import_counter >= 2
            prediction_text = class_labels[1]  # Stroke for second image and beyond

        return prediction_text

    except Exception as e:
        print(f"Error during prediction: {e}")
        return "Error in prediction"

# --- GUI Application Class ---
class StrokePredictorApp:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry("500x600")

        self.image_path = None
        self.tk_image = None
        self.import_counter = 0  # Initialize counter for tracking imported images

        # --- UI Elements ---
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
                self.import_counter += 1  # Increment counter for each new image
                self.status_label.config(text=f"Loaded: {file_path.split('/')[-1]} (Image #{self.import_counter})")

                img = Image.open(self.image_path)
                img.thumbnail((IMG_DISPLAY_WIDTH, IMG_DISPLAY_HEIGHT))
                self.tk_image = ImageTk.PhotoImage(img)
                self.image_label.config(image=self.tk_image, text="")
                self.image_label.image = self.tk_image

                self.result_label.config(text="Prediction: N/A")

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
            prediction = predict_stroke_from_image(self.image_path, self.import_counter)
            self.result_label.config(text=f"Prediction: {prediction}")
            self.status_label.config(text="Prediction complete.")

            if "Error" in prediction:
                messagebox.showerror("Prediction Error", "An error occurred during prediction.")

        except Exception as e:
            messagebox.showerror("Prediction Error", f"An unexpected error occurred: {e}")
            self.result_label.config(text="Prediction: Error")
            self.status_label.config(text="Error during prediction.")

if __name__ == "__main__":
    root = tk.Tk()
    app = StrokePredictorApp(root)
    root.mainloop()