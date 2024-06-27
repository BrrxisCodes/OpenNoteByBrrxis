import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import simpledialog
import webbrowser
import ttkbootstrap as ttk
import re
from PIL import Image, ImageTk

class AdvancedNotepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Notepad")
        self.root.geometry("1000x700")

        self.style = ttk.Style("cosmo")

        self.categories = {}
        self.current_category = None
        self.current_note = None

        # Diretório base para salvar categorias e notas
        self.base_dir = "Categorias"
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        self.icon_dir = "C:\\Users\\Ezno\\Desktop\\PythonProjects\\Caderno"

        self.create_frames()
        self.create_widgets()
        self.load_categories()

    def create_frames(self):
        self.frame_left = ttk.Frame(master=self.root, width=200)
        self.frame_left.pack(side="left", fill="y", padx=10, pady=10)

        self.frame_middle = ttk.Frame(master=self.root, width=200)
        self.frame_middle.pack(side="left", fill="y", padx=10, pady=10)

        self.frame_right = ttk.Frame(master=self.root)
        self.frame_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def create_widgets(self):
        self.category_label = ttk.Label(master=self.frame_left, text="Categories", font=("Arial", 18))
        self.category_label.pack(pady=10)

        self.category_listbox = tk.Listbox(master=self.frame_left)
        self.category_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.category_listbox.bind("<<ListboxSelect>>", self.select_category)

        self.new_category_button = ttk.Button(master=self.frame_left, text="New Category", command=self.new_category)
        self.new_category_button.pack(pady=10)

        self.notebook_label = ttk.Label(master=self.frame_middle, text="Notebooks", font=("Arial", 18))
        self.notebook_label.pack(pady=10)

        self.notebook_listbox = tk.Listbox(master=self.frame_middle)
        self.notebook_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.notebook_listbox.bind("<<ListboxSelect>>", self.select_notebook)

        self.new_notebook_button = ttk.Button(master=self.frame_middle, text="New Notebook", command=self.new_notebook)
        self.new_notebook_button.pack(pady=10)

        self.text_area = tk.Text(master=self.frame_right, wrap='word', font=("Arial", 12))
        self.text_area.pack(fill="both", expand=True, padx=10, pady=10)
        self.text_area.bind("<KeyRelease>", self.detect_links)

        self.text_area.tag_configure("hyperlink", foreground="blue", underline=True)
        self.text_area.tag_bind("hyperlink", "<Enter>", lambda e: self.text_area.config(cursor="hand2"))
        self.text_area.tag_bind("hyperlink", "<Leave>", lambda e: self.text_area.config(cursor=""))
        self.text_area.tag_bind("hyperlink", "<Button-1>", self.open_link)

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")

        self.root.bind_all("<Control-n>", lambda event: self.new_file())
        self.root.bind_all("<Control-o>", lambda event: self.open_file())
        self.root.bind_all("<Control-s>", lambda event: self.save_file())
        self.root.bind_all("<Control-q>", lambda event: self.root.quit())

        # Adding text formatting options
        self.format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)
        self.format_menu.add_command(label="Bold", command=self.make_bold, accelerator="Ctrl+B")
        self.format_menu.add_command(label="Italic", command=self.make_italic, accelerator="Ctrl+I")
        self.format_menu.add_command(label="Underline", command=self.make_underline, accelerator="Ctrl+U")

        self.root.bind_all("<Control-b>", lambda event: self.make_bold())
        self.root.bind_all("<Control-i>", lambda event: self.make_italic())
        self.root.bind_all("<Control-u>", lambda event: self.make_underline())

        # Redimensionando ícones
        self.bold_icon = self.resize_icon("boldico.png")
        self.italic_icon = self.resize_icon("italicico.png")
        self.underline_icon = self.resize_icon("underlineico.png")

        self.bold_button = ttk.Button(master=self.frame_right, image=self.bold_icon, command=self.make_bold)
        self.bold_button.pack(side="left", padx=5)

        self.italic_button = ttk.Button(master=self.frame_right, image=self.italic_icon, command=self.make_italic)
        self.italic_button.pack(side="left", padx=5)

        self.underline_button = ttk.Button(master=self.frame_right, image=self.underline_icon, command=self.make_underline)
        self.underline_button.pack(side="left", padx=5)

    def resize_icon(self, icon_name, size=(20, 20)):
        icon_path = os.path.join(self.icon_dir, icon_name)
        icon_image = Image.open(icon_path)
        icon_image = icon_image.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(icon_image)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, file.read())
                self.detect_links()
            except Exception as e:
                messagebox.showerror("Open File", f"Error opening file: {e}")

    def save_file(self):
        if self.current_category and self.current_note:
            category_path = os.path.join(self.base_dir, self.current_category)
            if not os.path.exists(category_path):
                os.makedirs(category_path)
            note_path = os.path.join(category_path, f"{self.current_note}.txt")
            try:
                with open(note_path, 'w') as file:
                    file.write(self.text_area.get(1.0, tk.END))
                messagebox.showinfo("Save", "Note saved successfully!")
            except Exception as e:
                messagebox.showerror("Save File", f"Error saving file: {e}")
        else:
            messagebox.showwarning("Save", "Please select a category and a note to save.")

    def new_category(self):
        category_name = simpledialog.askstring("New Category", "Enter category name:")
        if category_name and category_name not in self.categories:
            self.categories[category_name] = {}
            self.category_listbox.insert(tk.END, category_name)
            try:
                os.makedirs(os.path.join(self.base_dir, category_name))
            except Exception as e:
                messagebox.showerror("New Category", f"Error creating category: {e}")

    def select_category(self, event):
        selection = self.category_listbox.curselection()
        if selection:
            self.current_category = self.category_listbox.get(selection[0])
            self.update_notebook_listbox()

    def new_notebook(self):
        if self.current_category:
            notebook_name = simpledialog.askstring("New Notebook", "Enter notebook name:")
            if notebook_name and notebook_name not in self.categories[self.current_category]:
                self.categories[self.current_category][notebook_name] = ""
                self.update_notebook_listbox()
                note_path = os.path.join(self.base_dir, self.current_category, f"{notebook_name}.txt")
                try:
                    open(note_path, 'w').close()
                except Exception as e:
                    messagebox.showerror("New Notebook", f"Error creating notebook: {e}")
        else:
            messagebox.showwarning("New Notebook", "Please select a category first.")

    def select_notebook(self, event):
        selection = self.notebook_listbox.curselection()
        if selection:
            self.current_note = self.notebook_listbox.get(selection[0])
            note_path = os.path.join(self.base_dir, self.current_category, f"{self.current_note}.txt")
            try:
                with open(note_path, 'r') as file:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, file.read())
                self.detect_links()
            except Exception as e:
                messagebox.showerror("Select Notebook", f"Error loading notebook: {e}")

    def update_notebook_listbox(self):
        self.notebook_listbox.delete(0, tk.END)
        if self.current_category:
            for notebook in self.categories[self.current_category]:
                self.notebook_listbox.insert(tk.END, notebook)

    def load_categories(self):
        if os.path.exists(self.base_dir):
            for category in os.listdir(self.base_dir):
                category_path = os.path.join(self.base_dir, category)
                if os.path.isdir(category_path):
                    self.categories[category] = {}
                    self.category_listbox.insert(tk.END, category)
                    for note in os.listdir(category_path):
                        if note.endswith(".txt"):
                            note_name = note.replace(".txt", "")
                            self.categories[category][note_name] = ""

    def detect_links(self, event=None):
        """Detect URLs in the text and apply the hyperlink tag."""
        start = "1.0"
        url_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

        self.text_area.tag_remove("hyperlink", "1.0", tk.END)

        while True:
            pos = self.text_area.search(url_pattern, start, stopindex=tk.END, regexp=True)
            if not pos:
                break
            end_pos = f"{pos} + {len(self.text_area.get(pos, f'{pos} lineend').split()[0])}c"
            self.text_area.tag_add("hyperlink", pos, end_pos)
            start = end_pos

    def open_link(self, event):
        """Open the link in a web browser."""
        idx = self.text_area.index("@%s,%s" % (event.x, event.y))
        tag_indices = self.text_area.tag_ranges("hyperlink")
        for start, end in zip(tag_indices[0::2], tag_indices[1::2]):
            if self.text_area.compare(start, "<=", idx) and self.text_area.compare(idx, "<", end):
                url = self.text_area.get(start, end)
                webbrowser.open(url)
                break

    def make_bold(self):
        self.toggle_tag("bold", "bold")

    def make_italic(self):
        self.toggle_tag("italic", "italic")

    def make_underline(self):
        self.toggle_tag("underline", "underline")

    def toggle_tag(self, tag_name, font_style):
        try:
            current_tags = self.text_area.tag_names("sel.first")
            if tag_name in current_tags:
                self.text_area.tag_remove(tag_name, "sel.first", "sel.last")
            else:
                self.text_area.tag_add(tag_name, "sel.first", "sel.last")
            self.apply_tags(font_style)
        except tk.TclError:
            pass

    def apply_tags(self, font_style):
        # Fontes padrão para cada estilo
        bold_font = ("Arial", 12, "bold")
        italic_font = ("Arial", 12, "italic")
        underline_font = ("Arial", 12, "underline")

        # Aplicar formatações conforme as tags
        self.text_area.tag_configure("bold", font=bold_font)
        self.text_area.tag_configure("italic", font=italic_font)
        self.text_area.tag_configure("underline", font=underline_font)

if __name__ == "__main__":
    root = ttk.Window(themename="cosmo")
    notepad = AdvancedNotepad(root)
    root.mainloop()
