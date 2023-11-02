import tkinter as tk
from tkinter import ttk

class Task:
    def __init__(self, description, due_date, priority):
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = False

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")

        self.tasks = []

        self.init_ui()

    def init_ui(self):
        self.style = ttk.Style()

        self.description_label = ttk.Label(root, text="Description:")
        self.description_label.grid(row=0, column=0, padx=10, pady=5)
        self.description_entry = ttk.Entry(root)
        self.description_entry.grid(row=0, column=1, padx=10, pady=5)

        self.due_date_label = ttk.Label(root, text="Due Date (YYYY-MM-DD):")
        self.due_date_label.grid(row=1, column=0, padx=10, pady=5)
        self.due_date_entry = ttk.Entry(root)
        self.due_date_entry.grid(row=1, column=1, padx=10, pady=5)

        self.priority_label = ttk.Label(root, text="Priority:")
        self.priority_label.grid(row=2, column=0, padx=10, pady=5)
        self.priority_combo = ttk.Combobox(root, values=["Low", "Medium", "High"])
        self.priority_combo.grid(row=2, column=1, padx=10, pady=5)

        self.add_button = ttk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.grid(row=3, column=0, padx=10, pady=5, columnspan=2)

        self.task_list = tk.Listbox(root, selectmode=tk.SINGLE)
        self.task_list.grid(row=4, column=0, padx=10, pady=5, columnspan=2)

        self.complete_button = ttk.Button(root, text="Mark as Completed", command=self.mark_completed)
        self.complete_button.grid(row=5, column=0, padx=10, pady=5, columnspan=2)

        self.update_button = ttk.Button(root, text="Update Task", command=self.update_task)
        self.update_button.grid(row=6, column=0, padx=10, pady=5, columnspan=2)

        self.remove_button = ttk.Button(root, text="Remove Task", command=self.remove_task)
        self.remove_button.grid(row=7, column=0, padx=10, pady=5, columnspan=2)

        self.load_button = ttk.Button(root, text="Load Tasks", command=self.load_tasks)
        self.load_button.grid(row=8, column=0, padx=10, pady=5, columnspan=2)

        self.save_button = ttk.Button(root, text="Save Tasks", command=self.save_tasks)
        self.save_button.grid(row=9, column=0, padx=10, pady=5, columnspan=2)

    def add_task(self):
        description = self.description_entry.get()
        due_date = self.due_date_entry.get()
        priority = self.priority_combo.get()
        task = Task(description, due_date, priority)
        self.tasks.append(task)
        self.task_list.insert(tk.END, description)
        self.clear_entries()

    def mark_completed(self):
        selected_index = self.task_list.curselection()
        if selected_index:
            task_index = int(selected_index[0])
            self.tasks[task_index].completed = True
            self.update_task_list()

    def update_task(self):
        selected_index = self.task_list.curselection()
        if selected_index:
            task_index = int(selected_index[0])
            description = self.description_entry.get()
            due_date = self.due_date_entry.get()
            priority = self.priority_combo.get()
            task = self.tasks[task_index]
            task.description = description
            task.due_date = due_date
            task.priority = priority
            self.task_list.delete(task_index)
            self.task_list.insert(task_index, description)
            self.clear_entries()

    def remove_task(self):
        selected_index = self.task_list.curselection()
        if selected_index:
            task_index = int(selected_index[0])
            self.tasks.pop(task_index)
            self.task_list.delete(task_index)
            self.clear_entries()

    def load_tasks(self):
        self.clear_task_list()
        try:
            with open("tasks.txt", "r") as file:
                for line in file:
                    description, due_date, priority, completed = line.strip().split(',')
                    task = Task(description, due_date, priority)
                    task.completed = completed.lower() == 'true'
                    self.tasks.append(task)
                    self.task_list.insert(tk.END, description)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading tasks from file: {str(e)}")

    def save_tasks(self):
        try:
            with open("tasks.txt", "w") as file:
                for task in self.tasks:
                    file.write(f"{task.description},{task.due_date},{task.priority},{task.completed}\n")
        except Exception as e:
            print(f"Error saving tasks to file: {str(e)}")

    def clear_entries(self):
        self.description_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.priority_combo.set("")

    def clear_task_list(self):
        self.task_list.delete(0, tk.END)

    def update_task_list(self):
        self.clear_task_list()
        for task in self.tasks:
            status = "Completed" if task.completed else "Pending"
            self.task_list.insert(tk.END, f"{task.description} ({status})")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()
