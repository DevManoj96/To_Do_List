import tkinter as tk
from tkinter import Listbox, Menu, Scrollbar, messagebox
import datetime

FILENAME = "saved_tasks.txt"

class ToDoList:
    def __init__(self, root):   
        self.root = root
        self.root.title("--- To Do List ---")
        self.root.geometry('500x650')
        self.root.resizable(False, False)

        self.is_dark = False

        self.themes = {
            "light": {
                "bg": "#ffffff",
                "fg": "#000000",
                "entry_bg": "#ffffff",
                "entry_fg": "#000000",
                "listbox_bg": "#ffffff",
                "listbox_fg": "#000000",
                "btn_bg": "#f0f0f0"
            },
            "dark": {
                "bg": "#1e1e1e",
                "fg": "#ffffff",
                "entry_bg": "#2d2d2d",
                "entry_fg": "#ffffff",
                "listbox_bg": "#2d2d2d",
                "listbox_fg": "#ffffff",
                "btn_bg": "#444444"
            }
        }

        self.menubar = tk.Menu(self.root)

        option_menu = tk.Menu(self.menubar, tearoff=0)
        
        option_menu.add_command(label="Open Tasks", command=self.load_tasks, accelerator="Ctrl+O")
        option_menu.add_command(label="Clear Tasks", command=self.clear_tasks, accelerator="Ctrl+C")
        option_menu.add_command(label="Toggle Theme", command=self.toggle_theme, accelerator="Ctrl+T")
        option_menu.add_separator()
        option_menu.add_command(label="About", command=self.show_about, accelerator="F1")


        self.menubar.add_cascade(label="Options", menu=option_menu)
        self.root.config(menu=self.menubar)

        self.label1 = tk.Label(self.root, text="To Do List", font=("Arial", 20, "bold"), width=20, height=1)
        self.label1.pack(padx=10, pady=10)

        list_frame = tk.Frame(self.root)
        list_frame.pack(padx=10, pady=10)

        self.listbox = tk.Listbox(
            list_frame, width=50, height=15,
            xscrollcommand=lambda *args: self.xscrollbar.set(*args),
            yscrollcommand=lambda *args: self.yscrollbar.set(*args)
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.yscrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.xscrollbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.listbox.xview)
        self.xscrollbar.pack(fill=tk.X)

        self.listbox.config(yscrollcommand=self.yscrollbar.set, xscrollcommand=self.xscrollbar.set)

        self.entry1 = tk.Entry(self.root, font=("Arial", 12), width=35)
        self.entry1.pack(padx=5, pady=5)

        tk.Button(self.root, text="Save Task", command=self.saved_tasks, font=("Arial", 12), width=20, height=2).pack(padx=5, pady=5)
        
        tk.Button(self.root, text="Task Done", command=self.mark_task_done, font=("Arial", 12), width=20, height=2).pack(padx=5, pady=5)

        tk.Button(self.root, text="Delete Task", command=self.delete_task, font=("Arial", 12), width=20, height=2).pack(padx=5, pady=5)

        tk.Button(self.root, text="Exit", command=self.root.quit, font=("Arial", 12), width=20, height=2).pack(padx=5, pady=5)

  
        self.root.bind('<Return>', lambda event: self.saved_tasks())
        self.root.bind('<Control-o>', lambda event: self.load_tasks())
        self.root.bind('<Control-c>', lambda event: self.clear_tasks())
        self.root.bind('<Control-t>', lambda event: self.toggle_theme())
        self.root.bind('<F1>', lambda event: self.show_about())
        self.root.bind('<Delete>', lambda event: self.delete_task())
        self.root.bind('<Control-m>', lambda event: self.mark_task_done())
        self.root.bind('<Escape>', lambda event: self.root.quit())



    def show_about(self):
        """Display the About dialog with application information"""
        about_text = """
        📝 To-Do List Application
        
        Version: 1.0
        
        A simple and efficient task management application built with Python and Tkinter.
        
        Features:
        • Add and save tasks with timestamps
        • Mark tasks as completed
        • Delete individual tasks
        • Clear all tasks
        • Dark/Light theme toggle
        • Persistent task storage
        
        Keyboard Shortcuts:
        • Enter - Add new task
        • Ctrl+O - Open/Load tasks
        • Ctrl+C - Clear all tasks
        • Ctrl+T - Toggle theme
        • Ctrl+M - Mark task as done
        • Delete - Delete selected task
        • F1 - Show this dialog
        • Escape - Exit application
        
        Created with Python & Tkinter
        """
        
        messagebox.showinfo("About To-Do List", about_text)


    def load_tasks(self):
        try:
            with open(FILENAME, 'r') as file:
                lines = file.readlines()
                self.listbox.delete(0, tk.END)

                if not lines:
                    messagebox.showinfo("Tasks", "No Tasks Found.")
                    return

                for line in lines:
                    self.listbox.insert(tk.END, line.strip())
                self.listbox.yview_moveto(1)

        except FileNotFoundError:
            messagebox.showinfo("Tasks", "No Tasks Found.")

    def saved_tasks(self):
        task = self.entry1.get().strip()
        if not task:
            messagebox.showerror("Error", "Enter a task first.")
            return

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = f"{current_time} | {task}"

        self.listbox.insert(tk.END, content)
        self.listbox.yview_moveto(1)

        with open(FILENAME, "a") as file:
            file.write(f"{content}\n")

        self.entry1.delete(0, tk.END)

    def clear_tasks(self):
        try:
            with open(FILENAME, 'r') as file:
                lines = file.readline()
                if not lines:
                    messagebox.showinfo("Task", "Tasks are already cleared")
                    return

        except FileNotFoundError:
            messagebox.showinfo("Task", "Tasks are already cleared")
            return

        confirm = messagebox.askyesno("Confirm", "Do you want to delete all tasks?")

        if confirm:
            with open(FILENAME, 'w') as file:
                file.write("")

            self.listbox.delete(0, tk.END)
            messagebox.showinfo("Tasks", "All Tasks Cleared.")

    def delete_task(self):
        selected = self.listbox.curselection()

        if not selected:
            messagebox.showerror("Error", "No task selected.")
            return

        index = selected[0]
        task = self.listbox.get(index)

        confirm = messagebox.askyesno("Delete Task", f"Delete this task?\n\n{task}")
        
        if confirm:
            self.listbox.delete(index)
            with open(FILENAME, 'r') as file:
                lines = file.readlines()

            with open(FILENAME, 'w') as file:
                for line in lines:
                    if line.strip() != task:
                        file.write(line)

    def mark_task_done(self):
        selected = self.listbox.curselection()

        if not selected:
            messagebox.showerror("Error", "No task selected.")
            return

        index = selected[0]
        task = self.listbox.get(index)

        if task.startswith("✅"):
            messagebox.showinfo("Task", "This task is already marked as done.")
            return

        done_task = f"✅ {task}"
        self.listbox.delete(index)
        self.listbox.insert(index, done_task)

        with open(FILENAME, 'r') as file:
            lines = file.readlines()

        with open(FILENAME, 'w') as file:
            for line in lines:
                if line.strip() == task:
                    file.write(f"{done_task}\n")
                else:
                    file.write(line)

    def toggle_theme(self):
        self.is_dark = not self.is_dark

        theme = self.themes["dark"] if self.is_dark else self.themes["light"]

        self.root.config(bg=theme["bg"])
        self.label1.config(bg=theme["bg"], fg=theme["fg"])
        self.listbox.config(bg=theme["listbox_bg"], fg=theme["listbox_fg"])
        self.entry1.config(bg=theme["entry_bg"], fg=theme["entry_fg"])
        
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg=theme["btn_bg"], fg=theme["fg"])

if __name__ == '__main__':
    root = tk.Tk()
    app = ToDoList(root)
    root.mainloop()
