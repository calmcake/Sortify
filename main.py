import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

extensions = {
    "docs": ["pdf", "docx", "txt", "xlsx"],
    "images": ["jpg", "png", "gif", "svg"],
    "videos": ["mp4", "avi", "mov", "mkv"],
    "musics": ["mp3", "wav", "flac"],
    "archives": ["zip", "rar", "7z", "tar", "gz"],
    "programmes": ["exe", "msi"]
}

custom_extensions = {}

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def sort_files(path):
    try:
        os.chdir(path)
        current_dir_files = os.listdir()

        all_rules = {**extensions, **custom_extensions}

        folders = {}
        for folder in all_rules:
            folder_path = os.path.join(path, folder.capitalize())
            create_dir(folder_path)
            folders[folder] = folder_path

        other_path = os.path.join(path, "Прочее")
        create_dir(other_path)

        for file in current_dir_files:
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path) and "." in file and not file.startswith("main"):
                ext = file.split(".")[-1].lower()
                placed = False
                for category, exts in all_rules.items():
                    if ext in exts:
                        shutil.move(file_path, folders[category])
                        placed = True
                        break
                if not placed:
                    shutil.move(file_path, other_path)

        messagebox.showinfo("Готово", "Файлы успешно отсортированы!")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def choose_directory():
    path = filedialog.askdirectory()
    if path:
        sort_files(path)

def add_custom_rule():
    folder = folder_entry.get().strip().lower()
    ext_text = extensions_entry.get().strip().lower()
    if not folder or not ext_text:
        messagebox.showwarning("Недостаточно данных", "Введите имя папки и хотя бы одно расширение.")
        return

    exts = [e.strip() for e in ext_text.split(",") if e.strip()]
    if not exts:
        messagebox.showwarning("Неверный формат", "Введите хотя бы одно расширение через запятую.")
        return

    custom_extensions[folder] = exts
    messagebox.showinfo("Добавлено", f"Правило для папки '{folder}' добавлено: {', '.join(exts)}")
    folder_entry.delete(0, tk.END)
    extensions_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Сортировщик файлов")
root.geometry("500x400")
root.resizable(False, False)

tk.Label(root, text="Выберите папку для сортировки файлов", font=("Arial", 12)).pack(pady=10)

tk.Button(root, text="Выбрать папку", command=choose_directory, width=25, height=2, bg="#4CAF50", fg="white").pack(pady=10)

tk.Label(root, text="Добавить свою категорию", font=("Arial", 12, "bold")).pack(pady=(20, 5))

form_frame = tk.Frame(root)
form_frame.pack(pady=5)

tk.Label(form_frame, text="Имя папки:").grid(row=0, column=0, padx=5, sticky="e")
folder_entry = tk.Entry(form_frame, width=20)
folder_entry.grid(row=0, column=1, padx=5)

tk.Label(form_frame, text="Расширения (через ,):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
extensions_entry = tk.Entry(form_frame, width=30)
extensions_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Button(root, text="Добавить правило", command=add_custom_rule, bg="#2196F3", fg="white", width=20).pack(pady=10)

root.mainloop()
