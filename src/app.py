import os
import tkinter as tk
from tkinter import ttk, PhotoImage
import customtkinter as ctk
from PIL import Image

BASE_DIR = os.path.dirname(__file__) 
ASSETS_DIR = os.path.join(BASE_DIR, "..", "assets")

class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.configure(fg_color=("#f5f6fa", "#222831"))

        header = ctk.CTkFrame(self, height=60, fg_color=("#273c75", "#393e46"))
        header.pack(fill="x", side="top")
        title = ctk.CTkLabel(header, text="Bus Ji", font=("Arial", 28, "bold"), text_color=("#fff", "#fff"))
        title.pack(pady=10)

        content = ctk.CTkFrame(self, fg_color=("#f5f6fa", "#222831"))
        content.pack(fill="both", expand=True, padx=40, pady=30)

        logo = ctk.CTkImage(light_image=Image.open(f"{ASSETS_DIR}/logo.png"), dark_image=Image.open(f"{ASSETS_DIR}/logo.png"), size=(180,180))
        image_label = ctk.CTkLabel(content, image=logo, text="", width=180, height=180)
        image_label.pack(pady=(10, 20))

        description = ctk.CTkLabel(
            content,
            text="Welcome to Bus Ji!\n\nLorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.",
            font=("Arial", 14),
            wraplength=480,
            justify="center",
            text_color=("#222831", "#f5f6fa")
        )
        description.pack(pady=(0, 30))

        # Get Started Button
        get_start_button = ctk.CTkButton(
            content,
            text="Get Started",
            font=("Arial", 16, "bold"),
            fg_color=("#00adb5", "#00adb5"),
            hover_color=("#008891", "#008891"),
            text_color="#fff",
            corner_radius=8,
            width=180,
            height=48,
            command=lambda: controller.show_frame(HomePage),
        )
        get_start_button.pack(pady=10)

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(fg_color=("#f5f6fa", "#222831"))

        sidebar = ctk.CTkFrame(self, width=120, fg_color=("#393e46", "#393e46"))
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        nav_label = ctk.CTkLabel(sidebar, text="Menu", font=("Arial", 16, "bold"), text_color="#fff")
        nav_label.pack(pady=(30, 10))

        home_btn = ctk.CTkButton(sidebar, text="Home", fg_color=("#00adb5", "#00adb5"), hover_color=("#008891", "#008891"), text_color="#fff", corner_radius=6, command=lambda: controller.show_frame(HomePage))
        home_btn.pack(pady=10, fill="x", padx=10)

        start_btn = ctk.CTkButton(sidebar, text="Start", fg_color=("#393e46", "#393e46"), hover_color=("#222831", "#222831"), text_color="#fff", corner_radius=6, command=lambda: controller.show_frame(StartPage))
        start_btn.pack(pady=10, fill="x", padx=10)

        main_content = ctk.CTkFrame(self, fg_color=("#f5f6fa", "#222831"))
        main_content.pack(side="left", fill="both", expand=True, padx=30, pady=30)

        label = ctk.CTkLabel(main_content, text="Home Page", font=("Arial", 22, "bold"), text_color=("#222831", "#f5f6fa"))
        label.pack(pady=(30, 10))

        info = ctk.CTkLabel(main_content, text="This is the home page of your application.\nAdd your widgets and features here!", font=("Arial", 14), wraplength=400, justify="center", text_color=("#222831", "#f5f6fa"))
        info.pack(pady=10)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bus Ji")
        self.geometry("800x900")
        self.minsize(800, 800)
        self.maxsize(800, 1000)

        container = ctk.CTkFrame(self, height=900, width=800, fg_color=("#f5f6fa", "#222831"))
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames: dict = {}

        for F in (StartPage, HomePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

        self.mainloop()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

if __name__ == "__main__":
    App()