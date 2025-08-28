import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Store PIL images for saving
images = {"original": None, "sketch": None}
# Store Tkinter PhotoImages to prevent garbage collection
tk_images = {"original": None, "sketch": None}

def open_file():
    filepath = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )
    if not filepath:
        return
    img = cv2.imread(filepath)
    display_img(img, original=True)
    sketch_img = convert_to_sketch(img)
    display_img(sketch_img, original=False)

def convert_to_sketch(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted_img = cv2.bitwise_not(gray_img)
    blurred_img = cv2.GaussianBlur(inverted_img, (21, 21), sigmaX=0, sigmaY=0)
    inverted_blur_img = cv2.bitwise_not(blurred_img)
    sketch_img = cv2.divide(gray_img, inverted_blur_img, scale=256.0)
    return sketch_img

def display_img(img, original):
    if original:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        images["original"] = img_pil
    else:
        img_pil = Image.fromarray(img)
        images["sketch"] = img_pil

    img_tk = ImageTk.PhotoImage(image=img_pil)

    if original:
        tk_images["original"] = img_tk  # keep reference
        original_img_label.config(image=img_tk)
    else:
        tk_images["sketch"] = img_tk  # keep reference
        sketch_img_label.config(image=img_tk)

def save_sketch():
    if images["sketch"] is None:
        messagebox.showerror("Error", "No sketch to save")
        return
    sketch_filepath = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[("JPG files", "*.jpg"), ("PNG files", "*.png")]
    )
    if not sketch_filepath:
        return
    images["sketch"].save(sketch_filepath)
    messagebox.showinfo("Saved", f"Sketch saved to {sketch_filepath}")

# GUI setup
app = tk.Tk()
app.title("Pencil Sketch Converter")

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

original_img_label = tk.Label(frame)
original_img_label.grid(row=0, column=0, padx=5, pady=5)
sketch_img_label = tk.Label(frame)
sketch_img_label.grid(row=0, column=1, padx=5, pady=5)

btn_frame = tk.Frame(app)
btn_frame.pack(pady=10)

open_btn = tk.Button(btn_frame, text="Open Image", command=open_file)
open_btn.grid(row=0, column=0, padx=5)

save_button = tk.Button(btn_frame, text="Save Sketch", command=save_sketch)
save_button.grid(row=0, column=1, padx=5)

app.mainloop()
