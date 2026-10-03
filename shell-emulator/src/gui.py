"""Графический интерфейс эмулятора оболочки на tkinter."""

import tkinter as tk
from pathlib import Path

from commands import ShellError, execute, ExitR
from shell_parser import parse

DEF_VFS_NAME = "vfs"
WINDOW_SIZE = "600x600"
FONT = ("Consolas", 11)


class ShellApp:
    """Окно эмулятора: поле вывода сверху и строка ввода снизу."""

    def __init__(self, vfs_name, script_name):
        """Создать окно, вывести параметры и запланировать скрипт."""
        title_vfs_name = DEF_VFS_NAME
        if vfs_name:
            title_vfs_name = Path(vfs_name).name
        self.prompt = f"{title_vfs_name}$ "
        self.closed = False

        self.root = tk.Tk()
        self.root.title(f"Эмулятор оболочки — [{title_vfs_name}]")
        self.root.geometry(WINDOW_SIZE)
        self.build_widgets()

        self.write(f"[DEBUG] vfs = {vfs_name}")
        self.write(f"[DEBUG] script = {script_name}")
        self.check_vfs(vfs_name)
        self.check_script(script_name)

    def build_widgets(self):
        """Создать поле вывода и строку ввода."""
        self.output = tk.Text(self.root, state="disabled", bg="black",
                              fg="white", font=FONT)
        self.output.pack(fill="both", expand=True)

        self.entry = tk.Entry(self.root, bg="black", fg="white",
                              insertbackground="white", font=FONT)
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus_set()

    def check_vfs(self, vfs_name):
        """Сообщить, найден ли файл VFS (если путь задан)."""
        if not vfs_name:
            return
        vfs_file = Path(vfs_name)
        if vfs_file.exists():
            self.write(f"VFS name: {vfs_file.name}")
        else:
            self.write(f"VFS not found: {vfs_file.name}")

    def check_script(self, script_name):
        """Проверить скрипт и запланировать его запуск после старта окна."""
        if not script_name:
            return
        script_file = Path(script_name)
        if script_file.exists():
            self.write(f"Script name: {script_file.name}")
            self.root.after(0, self.read_script, script_file)
        else:
            self.write(f"script not found: {script_file.name}")

    def write(self, text):
        """Добавить строку текста в поле вывода."""
        self.output.configure(state="normal")
        self.output.insert(tk.END, text + "\n")
        self.output.configure(state="disabled")
        self.output.see(tk.END)

    def on_enter(self, event=None):
        """Обработать Enter: забрать текст из поля ввода и выполнить."""
        entry = self.entry.get()
        self.entry.delete(0, tk.END)
        self.run_line(entry)

    def run_line(self, line):
        """Выполнить одну строку. Вернуть False при ошибке или exit."""
        self.write(self.prompt + line)
        name, args = parse(line)
        if name is None:
            return True

        try:
            self.write(execute(name, args))
        except ShellError as e:
            self.write(str(e))
            return False
        except ExitR:
            self.root.destroy()
            self.closed = True
            return False
        return True

    def run(self):
        """Запустить главный цикл окна."""
        self.root.mainloop()

    def read_script(self, script_file: Path):
        """Выполнить команды скрипта, остановившись на первой ошибке."""
        with script_file.open(encoding="utf-8") as f:
            lines = f.readlines()
        for i, line in enumerate(lines, start=1):
            if self.run_line(line.strip()):
                continue
            if not self.closed:
                self.write(f"Скрипт остановлен на строке {i}")
            break