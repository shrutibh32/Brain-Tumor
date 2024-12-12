import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk  # To display image previews
from db_operations import insert_patient


def browse_image():
    """Open a file dialog to select an image and display the file path."""
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png")])
    if file_path:
        image_var.set(file_path)  # Store file path in the StringVar
        display_image(file_path)  # Display the selected image


def display_image(file_path):
    """Display the selected image in the placeholder label."""
    try:
        img = Image.open(file_path)
        img.thumbnail((150, 150))  # Resize for preview
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk  # Keep a reference to avoid garbage collection
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {e}")


def submit_details():
    """Validate and submit the form details."""
    name = name_entry.get()
    age = age_entry.get()
    gender = gender_var.get()
    diagnosis = diagnosis_var.get()
    image_path = image_var.get()

    if name and age and gender and diagnosis:  # Ensure all fields are filled
        try:
            age = int(age)  # Validate age
            insert_patient(name, age, gender, diagnosis, image_path)
            messagebox.showinfo("Success", "Patient record saved!")
        except ValueError:
            messagebox.showerror("Invalid Data", "Age must be a valid number.")
    else:
        messagebox.showwarning("Incomplete Data", "Please fill all fields before submitting.")


root = tk.Tk()
root.title("Patient Details")
root.geometry("400x600")
root.configure(bg="#f4f4f9")

font = ("Helvetica", 12)

# Title label
title_label = tk.Label(root, text="Enter Patient Details", font=("Helvetica", 16, "bold"), bg="#f4f4f9", fg="#4f4f4f")
title_label.pack(pady=20)

# Name input
name_label = tk.Label(root, text="Name:", font=font, bg="#f4f4f9")
name_label.pack(pady=5)
name_entry = ttk.Entry(root, font=font)
name_entry.pack(pady=5, padx=20, fill='x')

# Age input
age_label = tk.Label(root, text="Age:", font=font, bg="#f4f4f9")
age_label.pack(pady=5)
age_entry = ttk.Entry(root, font=font)
age_entry.pack(pady=5, padx=20, fill='x')

# Gender selection
gender_label = tk.Label(root, text="Gender:", font=font, bg="#f4f4f9")
gender_label.pack(pady=5)
gender_var = tk.StringVar(value="Male")
gender_menu = ttk.OptionMenu(root, gender_var, "Male", "Female", "Other")
gender_menu.pack(pady=5, padx=20, fill='x')

# Diagnosis selection
diagnosis_label = tk.Label(root, text="Diagnosis:", font=font, bg="#f4f4f9")
diagnosis_label.pack(pady=5)
diagnosis_var = tk.StringVar(value="Tumor Detected")
diagnosis_menu = ttk.OptionMenu(root, diagnosis_var, "Tumor Detected", "No Tumor")
diagnosis_menu.pack(pady=5, padx=20, fill='x')

# Image selection
image_label = tk.Label(root, bg="#f4f4f9")
image_label.pack(pady=10)
image_var = tk.StringVar()
image_button = ttk.Button(root, text="Browse Image", command=browse_image)
image_button.pack(pady=10)

# Submit button
submit_button = ttk.Button(root, text="Submit", command=submit_details)
submit_button.pack(pady=20)

# Configure styles
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=6)
style.configure("TEntry", font=("Helvetica", 12))
style.configure("TOptionMenu", font=("Helvetica", 12))

# Start the GUI loop
root.mainloop()
