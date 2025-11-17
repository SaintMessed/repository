import tkinter as tk
from tkinter import ttk
from datetime import datetime, date

FILENAME = "tasks.txt"


def load_tasks(filename):
    """Читает файл и возвращает список (дата, текст)."""
    tasks = []
    with open(filename, encoding="utf-8") as f:
        for line in f:
            if "|" not in line:
                continue
            date_str, text = line.strip().split("|", 1)
            date_str = date_str.strip()
            text = text.strip()
            try:
                d = datetime.strptime(date_str, "%Y-%m-%d").date()
                tasks.append((d, text))
            except ValueError:
                continue
    return tasks


def classify_tasks(tasks):
    """Возвращает строку для отображения и цвет."""
    today = date.today()
    display = []

    for d, text in tasks:
        diff = (today - d).days

        if diff > 0:
            # прошло X дней
            color = "red"
            line = f"Прошло {diff} дней от {text}"
        elif diff == 0:
            # сегодня
            color = "yellow"
            line = f"Прямо щаз происходит {text}"
        else:
            # будущая задача
            days = -diff
            color = "lightblue"
            line = f"Осталось {days} дней до {text}"

        display.append((line, color))

    return display


# ------------------ GUI ---------------------- #

root = tk.Tk()
root.title("Что мне делать, как мне жить?")
root.geometry("900x650")
root.configure(bg="black")

title = tk.Label(
    root,
    text="Мои текущие задачи",
    font=("Arial", 32, "bold", "underline"),
    fg="yellow",
    bg="black"
)
title.pack(pady=20)

frame = tk.Frame(root, bg="black")
frame.pack()

# загрузка из файла
tasks = load_tasks(FILENAME)
display_lines = classify_tasks(tasks)

for text, color in display_lines:
    tk.Label(
        frame,
        text=text,
        font=("Arial", 20),
        fg=color,
        bg="black"
    ).pack(anchor="w")

root.mainloop()
