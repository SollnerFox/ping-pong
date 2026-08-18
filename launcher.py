import os
import subprocess
import sys
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Launcher(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Пінг-Понг")
        self.geometry("420x420")
        self.resizable(False, False)

        self.host = "localhost"
        self.port = "8080"
        self.name = "Гравець"

        ctk.CTkLabel(self, text="ПІНГ-ПОНГ", font=("Arial", 40, "bold")).pack(pady=40)
        ctk.CTkLabel(self, text="Лаунчер гри", text_color="gray", font=("Arial", 16)).pack(pady=(0, 30))

        ctk.CTkButton(self, text="Грати", height=50, font=("Arial", 18, "bold"), command=self.show_play).pack(fill="x", padx=40, pady=8)
        ctk.CTkButton(self, text="Налаштування", height=50, font=("Arial", 18), command=self.show_settings).pack(fill="x", padx=40, pady=8)
        ctk.CTkButton(self, text="Вихід", height=50, font=("Arial", 18), fg_color="#D64545", command=self.destroy).pack(fill="x", padx=40, pady=8)

    def show_play(self):
        window = ctk.CTkToplevel(self)
        window.title("Гра")
        window.geometry("320x260")
        window.resizable(False, False)

        ctk.CTkLabel(window, text="Введи своє ім'я:", font=("Arial", 16)).pack(pady=(20, 6))
        self.name_entry = ctk.CTkEntry(window, width=240, height=40)
        self.name_entry.insert(0, self.name)
        self.name_entry.pack(pady=(0, 10))

        ctk.CTkLabel(window, text=f"Сервер: {self.host}:{self.port}", text_color="gray").pack(pady=(0, 10))
        ctk.CTkButton(window, text="Почати гру", height=44, font=("Arial", 16, "bold"), command=self.start_game).pack(padx=30, fill="x", pady=6)

    def start_game(self):
        self.name = self.name_entry.get().strip() or "Гравець"
        subprocess.Popen(
            [sys.executable, "client.py", self.host, self.port, self.name],
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )

    def show_settings(self):
        window = ctk.CTkToplevel(self)
        window.title("Налаштування")
        window.geometry("320x280")
        window.resizable(False, False)

        host_entry = ctk.CTkEntry(window, height=36)
        host_entry.insert(0, self.host)
        port_entry = ctk.CTkEntry(window, height=36)
        port_entry.insert(0, self.port)

        ctk.CTkLabel(window, text="Адреса сервера (IP)", font=("Arial", 14)).pack(padx=30, pady=(20, 4))
        host_entry.pack(padx=30, fill="x")
        ctk.CTkLabel(window, text="Порт", font=("Arial", 14)).pack(padx=30, pady=(12, 4))
        port_entry.pack(padx=30, fill="x")

        def save():
            if host_entry.get().strip():
                self.host = host_entry.get().strip()
            if port_entry.get().strip().isdigit():
                self.port = port_entry.get().strip()
            window.destroy()

        ctk.CTkButton(window, text="Зберегти", height=40, command=save).pack(padx=30, fill="x", pady=20)


if __name__ == "__main__":
    Launcher().mainloop()
