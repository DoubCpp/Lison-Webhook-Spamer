import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
from PIL import Image, ImageTk
import requests
import json
import re

def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def upload_image(file_path):
    try:
        response = requests.post("https://api.imgbb.com/1/upload", files={"image": open(file_path, "rb")}, data={"key": "81a5d0530b898df2118987163a958c43"})
        if response.status_code == 200:
            response_json = response.json()
            return response_json["data"]["url"]
        else:
            messagebox.showerror("Erreur", "Erreur lors de l'upload de l'image.")
            return None
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'upload de l'image: {e}")
        return None

def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
    if file_path:
        avatar_url = upload_image(file_path)
        if avatar_url:
            avatar_url_entry.delete(0, tk.END)
            avatar_url_entry.insert(0, avatar_url)

def choose_color():
    color_code = colorchooser.askcolor(title="Choisir une couleur")
    if color_code:
        color_hex = color_code[1]
        embed_color_label.config(bg=color_hex)

def send_webhook():
    url = webhook_url_entry.get()
    avatar_url = avatar_url_entry.get()
    embed_color = embed_color_label["bg"]

    if not url:
        messagebox.showerror("Erreur", "L'URL du webhook est requise.")
        return

    if avatar_url and not is_valid_url(avatar_url):
        messagebox.showerror("Erreur", "L'URL de l'avatar n'est pas valide.")
        return

    payload = {
        "username": username_entry.get(),
        "avatar_url": avatar_url,
        "embeds": [
            {
                "title": embed_title_entry.get(),
                "description": embed_description_entry.get("1.0", "end-1c"),
                "color": int(embed_color.replace("#", ""), 16)
            }
        ] if embed_title_entry.get() else []
    }

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code == 204:
            messagebox.showinfo("Succès", "Webhook envoyé avec succès!")
        else:
            error_message = f"Erreur lors de l'envoi du webhook: {response.status_code}\n{response.text}"
            messagebox.showerror("Erreur", error_message)
            print(error_message)
    except requests.exceptions.RequestException as e:
        error_message = f"Une erreur réseau s'est produite: {str(e)}"
        messagebox.showerror("Erreur", error_message)
        print(error_message)
    except ValueError as e:
        error_message = f"Une erreur de conversion JSON s'est produite: {str(e)}"
        messagebox.showerror("Erreur", error_message)
        print(error_message)

root = tk.Tk()
root.title("Lison | Webhook Embed")
root.geometry("600x665")

# Logo
icon_path = "Logo.ico"
icon_image = Image.open(icon_path)
icon_tk = ImageTk.PhotoImage(icon_image)
root.iconphoto(True, icon_tk)

# ASCII Art Title
ascii_title = """
 ▄█        ▄█     ▄████████  ▄██████▄  ███▄▄▄▄   
███       ███    ███    ███ ███    ███ ███▀▀▀██▄ 
███       ███▌   ███    █▀  ███    ███ ███   ███ 
███       ███▌   ███        ███    ███ ███   ███ 
███       ███▌ ▀███████████ ███    ███ ███   ███ 
███       ███           ███ ███    ███ ███   ███ 
███▌    ▄ ███     ▄█    ███ ███    ███ ███   ███ 
█████▄▄██ █▀    ▄████████▀   ▀██████▀   ▀█   █▀  
▀                                                
"""
ascii_label = tk.Label(root, text=ascii_title, justify="center", font=("Courier", 8))
ascii_label.pack()

# Webhook URL
tk.Label(root, text="URL du webhook:").pack(pady=5)
webhook_url_entry = tk.Entry(root, width=70)
webhook_url_entry.pack(pady=5)

# Username
tk.Label(root, text="Nom d'utilisateur:").pack(pady=5)
username_entry = tk.Entry(root, width=70)
username_entry.pack(pady=5)

# Avatar URL
tk.Label(root, text="URL de l'avatar:").pack(pady=5)
avatar_url_entry = tk.Entry(root, width=70)
avatar_url_entry.pack(pady=5)

browse_button = tk.Button(root, text="Parcourir...", command=browse_image)
browse_button.pack(pady=5)

# Embed Title
tk.Label(root, text="Titre de l'embed:").pack(pady=5)
embed_title_entry = tk.Entry(root, width=70)
embed_title_entry.pack(pady=5)

# Embed Description
tk.Label(root, text="Description de l'embed:").pack(pady=5)
embed_description_entry = tk.Text(root, width=70, height=5)
embed_description_entry.pack(pady=5)

# Embed Color
color_frame = tk.Frame(root)
color_frame.pack(pady=5)

tk.Label(color_frame, text="Couleur de l'embed:").pack(side="left")
embed_color_label = tk.Label(color_frame, bg="white", width=10)
embed_color_label.pack(side="left")
color_button = tk.Button(color_frame, text="Choisir couleur", command=choose_color)
color_button.pack(side="left")

# Send Button
send_button = tk.Button(root, text="Envoyer", command=send_webhook)
send_button.pack(pady=20)

root.mainloop()
