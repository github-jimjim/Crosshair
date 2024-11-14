import sys
import configparser
import easygui
from tkinter import Tk, Scale, Button, Label, colorchooser
from PIL import Image, ImageTk

def save_settings_to_ini(size=None, color=None):
    config = configparser.ConfigParser()

    config.read('config.ini')

    if 'Settings' not in config:
        config['Settings'] = {}

    if size is not None:
        config['Settings']['Size'] = str(size)
    else:
        size = config['Settings'].get('Size', '200')

    if color is not None:
        config['Settings']['Color'] = color
    else:
        color = config['Settings'].get('Color', '#FFFFFF')

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def show_size_selector():
    def on_apply():
        size = scale.get()
        save_settings_to_ini(size=size)
        root.destroy()

    root = Tk()
    root.title("Select Size")

    img_path = 'useable_crosshair.png'
    img = Image.open(img_path)
    img_tk = ImageTk.PhotoImage(img.resize((200, 200)))
    img_label = Label(root, image=img_tk)
    img_label.pack()

    scale = Scale(root, from_=25, to=500, orient="horizontal", length=400)
    scale.set(200)
    scale.pack()

    def update_preview(val):
        size = int(val)
        img_resized = img.resize((size, size))
        img_tk_resized = ImageTk.PhotoImage(img_resized)
        img_label.config(image=img_tk_resized)
        img_label.image = img_tk_resized

    scale.bind("<Motion>", lambda event: update_preview(scale.get()))

    apply_button = Button(root, text="Apply", command=on_apply)
    apply_button.pack()

    root.mainloop()

def show_color_selector():
    def on_apply():
        color = color_label.cget("bg")
        save_settings_to_ini(color=color)
        root.destroy()

    def choose_color():
        color_code = colorchooser.askcolor(title="Choose color")[1]
        if color_code:
            color_label.config(bg=color_code)

    root = Tk()
    root.title("Select Color")

    color_label = Label(root, text="Choose Color", bg="white", width=20, height=2)
    color_label.pack(pady=10)

    color_button = Button(root, text="Pick Color", command=choose_color)
    color_button.pack()

    apply_button = Button(root, text="Apply", command=on_apply)
    apply_button.pack()

    root.mainloop()

def main():
    choices = ["Change Color", "Change Size", "Exit"]
    task = easygui.choicebox("Choose your Action", choices=choices, title="Action")

    if task == "Change Size":
        show_size_selector()
    elif task == "Change Color":
        show_color_selector()
    else:
        sys.exit()

if __name__ == "__main__":
    main()
