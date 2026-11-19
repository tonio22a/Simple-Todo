import flet as ft
import sqlite3

# 1. Подключаемся к базе данных и создаем таблицу (если её еще нет)
conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT, is_done INTEGER DEFAULT 0)")
conn.commit()

def main(page: ft.Page):
    page.title = "Мои задачи (Flet + SQLite)"
    page.window.width = 400
    page.window.height = 500

    task_input = ft.TextField(label="Новая задача", expand=True)
    tasks_column = ft.Column()

    # Функция загрузки всех задач из базы данных на экран
    def load_tasks():
        tasks_column.controls.clear()
        cursor.execute("SELECT id, title, is_done FROM tasks")
        for task_id, title, is_done in cursor.fetchall():
            tasks_column.controls.append(
                ft.Row([
                    ft.Checkbox(
                        value=bool(is_done),  # Ставит галочку, если в базе 1
                        on_change=lambda e, tid=task_id: do_task(tid, e.control.value)
                    ),
                    ft.Text(title, expand=True, size=16),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        on_click=lambda e, tid=task_id: delete_task(tid)
                    )
                ])
            )
        page.update()

    # Функция добавления задачи в базу
    def add_task(e):
        if task_input.value.strip():
            cursor.execute("INSERT INTO tasks (title) VALUES (?)", (task_input.value,))
            conn.commit()
            task_input.value = ""
            load_tasks()

    # Функция удаления задачи из базы
    def delete_task(task_id):
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        load_tasks()

    def do_task(task_id, is_checked):
        cursor.execute("UPDATE tasks SET is_done = ? WHERE id = ?", (int(is_checked), task_id))
        conn.commit()
        load_tasks()

    add_btn = ft.Button("Добавить", on_click=add_task)
    
    page.add(ft.Row([task_input, add_btn]), tasks_column)
    load_tasks()  # Загружаем сохраненные задачи при старте программы

ft.run(main)
