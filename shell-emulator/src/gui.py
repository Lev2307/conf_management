import tkinter as tk
from tkinter import ttk

from commands import ShellError, execute, ExitR
from shell_parser import parse


DEF_VFS_NAME = "vfs"
WINDOW_SIZE = "600x600"
FONT = ("Consolas", 11)

class ShellApp:
    def __init__(self, vfs_name = DEF_VFS_NAME):
        self.prompt = f"{vfs_name}$ "
        self.root = tk.Tk()
        self.root.title(f"Эмулятор оболочки — [{vfs_name}]")
        self.root.geometry(WINDOW_SIZE)

        self.output = tk.Text(self.root, state="disabled", bg="black", fg="white", font=FONT)
        self.output.pack(fill="both", expand=True)

        self.entry = tk.Entry(self.root, bg="black", fg="white", insertbackground="white", font=FONT)
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus_set()

    def write(self, text):
        self.output.configure(state="normal")
        self.output.insert(tk.END, text + "\n")
        self.output.configure(state="disabled")
        self.output.see(tk.END)

    def on_enter(self, event=None):
        entry = self.entry.get()
        self.entry.delete(0, tk.END)
        self.run_line(entry)

    def run_line(self, line):
        self.write(self.prompt + line)
        name, args = parse(line)
        if name is None: return True

        try:
            self.write(execute(name, args))
            
        except ShellError as e:
            self.write(str(e))
            return False
        except ExitR:
            self.root.destroy()
        return True

    def run(self):
        self.root.mainloop()