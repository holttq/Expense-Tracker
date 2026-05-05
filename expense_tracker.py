import json
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker - Мои расходы")
        self.root.geometry("800x500")
        
        self.expenses = []
        
        self.load_data()
        
        self.create_widgets()
        
        self.refresh_table()
    
    def create_widgets(self):
        input_frame = tk.LabelFrame(self.root, text="Добавить расход", padx=10, pady=10)
        input_frame.pack(pady=10, padx=10, fill="x")
        
        # Поле Сумма
        tk.Label(input_frame, text="Сумма (руб):").grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(input_frame, width=15)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Категория:").grid(row=0, column=2, padx=5, pady=5)
        self.category_var = tk.StringVar()
        categories = ["Еда", "Транспорт", "Развлечения", "Одежда", "Здоровье", "Другое"]
        self.category_combo = ttk.Combobox(input_frame, textvariable=self.category_var, values=categories, width=15)
        self.category_combo.grid(row=0, column=3, padx=5, pady=5)
        self.category_combo.set("Еда")
        

        tk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=4, padx=5, pady=5)
        self.date_entry = tk.Entry(input_frame, width=15)
        self.date_entry.grid(row=0, column=5, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        add_btn = tk.Button(input_frame, text="Добавить расход", command=self.add_expense, bg="lightgreen")
        add_btn.grid(row=0, column=6, padx=10, pady=5)
        
        filter_frame = tk.LabelFrame(self.root, text="Фильтры", padx=10, pady=10)
        filter_frame.pack(pady=10, padx=10, fill="x")
        
        tk.Label(filter_frame, text="Фильтр по категории:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_category_var = tk.StringVar()
        self.filter_category_combo = ttk.Combobox(filter_frame, textvariable=self.filter_category_var, 
                                                   values=["Все"] + categories, width=15)
        self.filter_category_combo.grid(row=0, column=1, padx=5, pady=5)
        self.filter_category_combo.set("Все")
        

        tk.Label(filter_frame, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=0, column=2, padx=5, pady=5)
        self.filter_date_entry = tk.Entry(filter_frame, width=15)
        self.filter_date_entry.grid(row=0, column=3, padx=5, pady=5)
        
        filter_btn = tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        filter_btn.grid(row=0, column=4, padx=5, pady=5)
        
        reset_btn = tk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter)
        reset_btn.grid(row=0, column=5, padx=5, pady=5)
        
        sum_frame = tk.LabelFrame(self.root, text="Подсчет суммы за период", padx=10, pady=10)
        sum_frame.pack(pady=10, padx=10, fill="x")
        
        tk.Label(sum_frame, text="Дата начала (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5)
        self.start_date_entry = tk.Entry(sum_frame, width=15)
        self.start_date_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(sum_frame, text="Дата конца (ГГГГ-ММ-ДД):").grid(row=0, column=2, padx=5, pady=5)
        self.end_date_entry = tk.Entry(sum_frame, width=15)
        self.end_date_entry.grid(row=0, column=3, padx=5, pady=5)
        
        calc_btn = tk.Button(sum_frame, text="Подсчитать сумму", command=self.calculate_sum)
        calc_btn.grid(row=0, column=4, padx=5, pady=5)
        
        self.sum_label = tk.Label(sum_frame, text="Сумма: 0 руб", font=("Arial", 10, "bold"))
        self.sum_label.grid(row=0, column=5, padx=10, pady=5)
        
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tree = ttk.Treeview(table_frame, columns=("Сумма", "Категория", "Дата"), show="headings")
        
        self.tree.heading("Сумма", text="Сумма (руб)")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Дата", text="Дата")
        
        self.tree.column("Сумма", width=200)
        self.tree.column("Категория", width=200)
        self.tree.column("Дата", width=200)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def is_valid_amount(self, amount_str):
        """Проверка корректности суммы"""
        try:
            amount = float(amount_str)
            if amount > 0:
                return True
            else:
                messagebox.showerror("Ошибка", "Сумма должна быть больше 0")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число в поле 'Сумма'")
            return False
    
    def is_valid_date(self, date_str):
        """Проверка корректности даты"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД (например, 2024-12-25)")
            return False
    
    def add_expense(self):
        """Добавление нового расхода"""
        amount_str = self.amount_entry.get()
        category = self.category_var.get()
        date = self.date_entry.get()
        
        if not self.is_valid_amount(amount_str):
            return
        if not self.is_valid_date(date):
            return
        
        expense = {
            "amount": float(amount_str),
            "category": category,
            "date": date
        }
        
        self.expenses.append(expense)
        self.save_data()
        self.refresh_table()
        
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        messagebox.showinfo("Успех", "Расход добавлен!")
    
    def refresh_table(self, filtered_expenses=None):
        """Обновление таблицы"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if filtered_expenses is None:
            expenses_to_show = self.expenses
        else:
            expenses_to_show = filtered_expenses
        
        for i, expense in enumerate(expenses_to_show, start=1):
            self.tree.insert("", "end", values=(expense["amount"], expense["category"], expense["date"]))
    
    def apply_filter(self):
        """Применение фильтров"""
        filtered = self.expenses.copy()
        
        category_filter = self.filter_category_var.get()
        if category_filter != "Все":
            filtered = [e for e in filtered if e["category"] == category_filter]
        
        date_filter = self.filter_date_entry.get()
        if date_filter:
            if self.is_valid_date(date_filter):
                filtered = [e for e in filtered if e["date"] == date_filter]
            else:
                return
        
        self.refresh_table(filtered)
        
        if len(filtered) == 0:
            messagebox.showinfo("Инфо", "Нет записей, соответствующих фильтру")
    
    def reset_filter(self):
        """Сброс фильтров"""
        self.filter_category_combo.set("Все")
        self.filter_date_entry.delete(0, tk.END)
        self.refresh_table()
    
    def calculate_sum(self):
        """Подсчет суммы за период"""
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        
        if not start_date or not end_date:
            messagebox.showerror("Ошибка", "Введите обе даты для подсчета суммы")
            return
        
        if not self.is_valid_date(start_date) or not self.is_valid_date(end_date):
            return
        
        total = 0
        for expense in self.expenses:
            if start_date <= expense["date"] <= end_date:
                total += expense["amount"]
        
        self.sum_label.config(text=f"Сумма: {total} руб")
        messagebox.showinfo("Результат", f"Сумма расходов с {start_date} по {end_date}: {total} руб")
    
    def save_data(self):
        """Сохранение данных в JSON файл"""
        try:
            with open("expenses.json", "w", encoding="utf-8") as file:
                json.dump(self.expenses, file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")
    
    def load_data(self):
        """Загрузка данных из JSON файла"""
        try:
            with open("expenses.json", "r", encoding="utf-8") as file:
                self.expenses = json.load(file)
        except FileNotFoundError:
            self.expenses = []
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки данных: {e}")
            self.expenses = []

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
