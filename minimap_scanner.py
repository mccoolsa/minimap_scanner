import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import cv2
import numpy as np
import mss
import pygame

class SnippingTool(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        
        self.attributes('-fullscreen', True)
        self.attributes('-alpha', 0.3)
        self.config(cursor="cross")
        self.configure(background='black')

        self.start_x = None
        self.start_y = None
        self.shape = None 

        self.canvas = tk.Canvas(self, cursor="cross", bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.shape = self.canvas.create_oval(self.start_x, self.start_y, 1, 1, outline='red', width=2)

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        self.canvas.coords(self.shape, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        end_x, end_y = (event.x, event.y)
        
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)

        self.destroy()
        self.callback((x1, y1, x2 - x1, y2 - y1))


class MinimapScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minimap Node Scanner")
        self.root.geometry("350x250")
        self.root.resizable(False, False)

        self.region = None 
        self.audio_path = None
        self.is_scanning = False
        self.scan_thread = None

        pygame.mixer.init()

        # --- UI Elements ---
        self.lbl_region = tk.Label(root, text="Region: Not Selected", fg="red")
        self.lbl_region.pack(pady=(10, 0))
        
        # Changed text from "Select Circular Region" to "Select Region"
        self.btn_region = tk.Button(root, text="Select Region", command=self.select_region)
        self.btn_region.pack(pady=5)

        self.lbl_audio = tk.Label(root, text="Audio: Not Selected", fg="red")
        self.lbl_audio.pack(pady=(10, 0))
        
        self.btn_audio = tk.Button(root, text="Select Audio File", command=self.select_audio)
        self.btn_audio.pack(pady=5)

        self.volume_frame = tk.Frame(root)
        self.volume_frame.pack(pady=5)
        tk.Label(self.volume_frame, text="Volume:").pack(side=tk.LEFT)
        self.volume_slider = tk.Scale(self.volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_volume)
        self.volume_slider.set(50)
        self.volume_slider.pack(side=tk.LEFT)

        self.btn_toggle = tk.Button(root, text="START SCANNING", font=("Helvetica", 12, "bold"), bg="green", fg="white", command=self.toggle_scan)
        self.btn_toggle.pack(pady=15)

    def select_region(self):
        self.root.withdraw()
        SnippingTool(self.root, self.on_region_selected)

    def on_region_selected(self, coords):
        self.root.deiconify()
        self.region = coords
        self.lbl_region.config(text=f"Oval: {self.region[2]}x{self.region[3]} pixels", fg="green")

    def select_audio(self):
        filepath = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
        if filepath:
            self.audio_path = filepath
            filename = filepath.split("/")[-1]
            self.lbl_audio.config(text=f"Audio: {filename}", fg="green")
            pygame.mixer.music.load(self.audio_path)

    def update_volume(self, val):
        volume = int(val) / 100.0
        pygame.mixer.music.set_volume(volume)

    def toggle_scan(self):
        if not self.is_scanning:
            if not self.region:
                messagebox.showwarning("Missing Info", "Please select a region first.")
                return
            if not self.audio_path:
                messagebox.showwarning("Missing Info", "Please select an audio file first.")
                return
            
            self.is_scanning = True
            self.btn_toggle.config(text="STOP SCANNING", bg="red")
            self.scan_thread = threading.Thread(target=self.scan_loop, daemon=True)
            self.scan_thread.start()
        else:
            self.is_scanning = False
            self.btn_toggle.config(text="START SCANNING", bg="green")

    def scan_loop(self):
        lower_yellow = np.array([20, 150, 150]) 
        upper_yellow = np.array([35, 255, 255])

        monitor = {"left": self.region[0], "top": self.region[1], "width": self.region[2], "height": self.region[3]}
        width, height = self.region[2], self.region[3]
        center_x, center_y = width // 2, height // 2
        
        oval_mask = np.zeros((height, width), dtype=np.uint8)
        cv2.ellipse(oval_mask, (center_x, center_y), (center_x, center_y), 0, 0, 360, 255, -1)

        with mss.mss() as sct:
            while self.is_scanning:
                img = np.array(sct.grab(monitor))
                frame_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                frame_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

                color_mask = cv2.inRange(frame_hsv, lower_yellow, upper_yellow)
                final_mask = cv2.bitwise_and(color_mask, color_mask, mask=oval_mask)

                contours, _ = cv2.findContours(final_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                node_found = False
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if 15 < area < 150:
                        node_found = True
                        break 

                if node_found: 
                    if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.play()
                
                # Sleep for 1 second before scanning again to save CPU
                time.sleep(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = MinimapScannerApp(root)
    root.mainloop()