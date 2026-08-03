import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import os
import random

class RobloxBypassApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phyton-app")
        self.root.geometry("320x240")
        self.root.resizable(False, False)
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.input_path = None
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="Roblox decals bypass", font=("Segoe UI", 12, "bold"))
        title_label.pack(pady=(0, 10))
        
        self.status_label = ttk.Label(main_frame, text="No file selected", font=("Segoe UI", 9), foreground="gray")
        self.status_label.pack(pady=(0, 10))
        
        self.btn_load = ttk.Button(main_frame, text="Select Image", command=self.load_image)
        self.btn_load.pack(fill=tk.X, pady=5, ipady=5)
        
        self.btn_process = ttk.Button(main_frame, text="Process & Save", command=self.process_image, state=tk.DISABLED)
        self.btn_process.pack(fill=tk.X, pady=5, ipady=5)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file_path:
            self.input_path = file_path
            file_name = os.path.basename(file_path)
            self.status_label.config(text=f"Selected: {file_name}", foreground="green")
            self.btn_process.config(state=tk.NORMAL)

    def process_image(self):
        if not self.input_path:
            return
            
        try:
            img = Image.open(self.input_path).convert("RGBA")

            canvas = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
            img.thumbnail((300, 300), Image.Resampling.LANCZOS)
            paste_x = (300 - img.width) // 2
            paste_y = (300 - img.height) // 2
            canvas.paste(img, (paste_x, paste_y), img)
            
            base_img = canvas.copy()
            enhancer = ImageEnhance.Brightness(base_img)
            exposed_img = enhancer.enhance(0.1) 

            layer_bottom = exposed_img.copy()
            layer_middle = exposed_img.copy()
            layer_top = exposed_img.copy()

            layer_bottom = ImageOps.grayscale(layer_bottom).convert("RGBA")
            layer_middle = layer_middle.filter(ImageFilter.BoxBlur(12))
            layer_top = layer_top.filter(ImageFilter.GaussianBlur(radius=2))

            def set_opacity(layer, opacity):
                r, g, b, a = layer.split()
                alpha = a.point(lambda i: int(i * (opacity / 255.0)))
                return Image.merge("RGBA", (r, g, b, alpha))

            layer_bottom = set_opacity(layer_bottom, 130)
            layer_middle = set_opacity(layer_middle, 130)
            layer_top = set_opacity(layer_top, 130)

            merged = Image.alpha_composite(layer_bottom, layer_middle)
            merged = Image.alpha_composite(merged, layer_top)

            width, height = merged.size
            noise_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            pixels = noise_img.load()
            for x in range(width):
                for y in range(height):
                    if random.random() < 0.25:
                        val = random.randint(0, 255)
                        pixels[x, y] = (val, val, val, random.randint(20, 35))
            
            merged = Image.alpha_composite(merged, noise_img)
            merged = set_opacity(merged, 235)
            final_img = merged.resize((6500, 300), Image.Resampling.LANCZOS)

            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")],
                initialfile="bypassed.png"
            )
            
            if save_path:
                final_img.save(save_path, "PNG")
                messagebox.showinfo("Success", "Image successfully processed and saved!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RobloxBypassApp(root)
    root.mainloop()