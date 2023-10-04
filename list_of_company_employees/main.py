import tkinter as tk 
from tkinter import ttk 
import sqlite3 
 
# Класс для главного окна, наследуется от класса Frame библиотеки tkinter 
class Main(tk.Frame): 
    def __init__(self, root) -> None: 
        """Создание экземпляра класса Main""" 
 
        super().__init__(root) 
        self.init_main() 
        self.db = db 
        self.view_records() 
 
    def init_main(self) -> None: 
        """Хранение и инициализация графических элементов на главном окне""" 
 
        toolbar = tk.Frame(bg="#d7d8e0", bd=2) 
        toolbar.pack(side=tk.TOP, fill=tk.X) 
 
        # Кнопка для открытия дочернего окна для добавления сотрудника 
        self.add_img = tk.PhotoImage(file="list_of_company_employees/img/add.png") 
        btn_open_dialog = tk.Button( 
            toolbar,  
            bg="#d7d8e0",  
            bd=0,  
            image=self.add_img,  
            command=self.open_add_dialog 
        ) 
        btn_open_dialog.pack(side=tk.LEFT) 
 
        # Таблица данных на главном окне 
        self.tree = ttk.Treeview( 
            self,  
            columns=("ID", "fio", "tel", "email", "salary"),  
            height=45,  
            show="headings" 
        ) 
 
        self.tree.column("ID", width=30, anchor=tk.CENTER) 
        self.tree.column("fio", width=300, anchor=tk.CENTER) 
        self.tree.column("tel", width=150, anchor=tk.CENTER) 
        self.tree.column("email", width=150, anchor=tk.CENTER) 
        self.tree.column("salary", width=150, anchor=tk.CENTER) 
 
        self.tree.heading("ID", text="ID") 
        self.tree.heading("fio", text="ФИО") 
        self.tree.heading("tel", text="Телефон") 
        self.tree.heading("email", text="E-mail") 
        self.tree.heading("salary", text="Зарплата") 
 
        self.tree.pack(side=tk.LEFT) 
 
        # Кнопка для открытия дочернего окна для редактирования данных сотрудника 
        self.update_img = tk.PhotoImage(file="list_of_company_employees/img/update.png") 
        btn_edit_dialog = tk.Button( 
            toolbar, 
            bg="#d7d8e0", 
            bd=0, 
            image=self.update_img, 
            command=self.open_update_dialog, 
        ) 
        btn_edit_dialog.pack(side=tk.LEFT) 
 
        # Кнопка для удаления сотрудника 
        self.delete_img = tk.PhotoImage(file="list_of_company_employees/img/delete.png") 
        btn_delete = tk.Button( 
            toolbar, 
            bg="#d7d8e0", 
            bd=0, 
            image=self.delete_img, 
            command=self.delete_records, 
        ) 
        btn_delete.pack(side=tk.LEFT) 
 
        # Кнопка для поиска сотрудника 
        self.search_img = tk.PhotoImage(file="list_of_company_employees/img/search.png") 
        btn_search = tk.Button( 
            toolbar, 
            bg="#d7d8e0", 
            bd=0, 
            image=self.search_img, 
            command=self.open_search_dialog, 
        ) 
        btn_search.pack(side=tk.LEFT) 
 
    def open_add_dialog(self) -> None: 
        """Метод для открытия дочернего окна для добавления сотрудника""" 
 
        Add() 
 
    def records(self, fio, tel, email, salary) -> None: 
        """Метод для добавления сотрудника""" 
 
        self.db.insert_data(fio, tel, email, salary) 
        self.view_records() 
 
    def view_records(self) -> None: 
        """Метод для обновления таблицы на главном экране""" 
 
        self.db.cursor.execute("SELECT * FROM db") 
        [self.tree.delete(i) for i in self.tree.get_children()] 
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()] 
 
    def open_update_dialog(self) -> None: 
        """Метод для открытия дочернего окна для редактирования данных сотрудника""" 
 
        Update() 
 
    def update_records(self, fio, tel, email, salary) -> None: 
        """Метод для редактирования данных сотрудника""" 
 
        self.db.cursor.execute( 
            """UPDATE db SET fio=?, tel=?, email=?, salary=? WHERE id=?""", 
            (fio, tel, email, salary, self.tree.set(self.tree.selection()[0], "#1")), 
        ) 
        self.db.conn.commit() 
        self.view_records() 
 
    def delete_records(self) -> None:
        """Метод для удаления сотрудника""" 
 
        for selection_items in self.tree.selection(): 
            self.db.cursor.execute( 
                "DELETE FROM db WHERE id=?", (self.tree.set(selection_items, "#1")) 
            ) 
            self.db.conn.commit() 
            self.view_records() 
 
    def open_search_dialog(self): 
        """Метод для открытия дочернего окна для поиска""" 
 
        Search() 
 
    def search_records(self, fio) -> None: 
        """Метод для поиска сотрудника по ФИО""" 
 
        fio = "%" + fio + "%" 
        self.db.cursor.execute("SELECT * FROM db WHERE fio LIKE ?", (fio,)) 
 
        [self.tree.delete(i) for i in self.tree.get_children()] 
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()] 
 
 
# Класс дочернего окна, на котором добавляем нового сотрудника, 
# наследуется от класса Toplevel библиотеки tkinter 
class Add(tk.Toplevel): 
    def __init__(self) -> None: 
        """Метод создания экзмепляра класса Add""" 
 
        super().__init__(root) 
        self.init_add() 
        self.view = app 
 
    def init_add(self) -> None: 
        """Хранение и инициализация графических элементов на дочернем окне""" 
 
        # Настройки окна 
        self.title("Добавить") 
        self.geometry("400x220") 
        self.resizable(False, False) 
 
        # Обработка событий 
        self.grab_set() 
        self.focus_set() 
 
        # форма для записи данных 
        label_fio = tk.Label(self, text="ФИО:") 
        label_fio.place(x=50, y=50) 
        label_tel = tk.Label(self, text="Телефон:") 
        label_tel.place(x=50, y=80) 
        label_email = tk.Label(self, text="E-mail:") 
        label_email.place(x=50, y=110)
        label_salary = tk.Label(self, text="Зарплата:")
        label_salary.place(x=50, y=140) 
 
        self.entry_fio = ttk.Entry(self) 
        self.entry_fio.place(x=200, y=50) 
        self.entry_tel = ttk.Entry(self) 
        self.entry_tel.place(x=200, y=80)
        self.entry_email = ttk.Entry(self) 
        self.entry_email.place(x=200, y=110)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140) 
 
        # Кнопка для закрытия окна 
        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy) 
        self.btn_cancel.place(x=220, y=170) 
 
        # Кнопка для добавления данных в базу данных  
        self.btn_ok = ttk.Button(self, text="Добавить") 
        self.btn_ok.place(x=300, y=170) 
 
        self.btn_ok.bind( 
            "<Button-1>", 
            lambda event: self.view.records( 
                self.entry_fio.get(), self.entry_tel.get(), self.entry_email.get(), self.entry_salary.get() 
                ) 
        ) 
 
 
# Класс дочернего окна, на котором редактируют данные сотрудника, 
# наследуется от класса Add 
class Update(Add): 
    def __init__(self) -> None: 
        """Метод создания экзмепляра класса Update""" 
 
        super().__init__() 
        self.init_update() 
        self.view = app 
        self.db = db 
        self.default_data() 
 
    def init_update(self) -> None: 
        """Метод редактирования данных сотрудника""" 
 
        self.title("Редактирование данных сотрудника") 
 
        # Кнопка для редактирования данных сотрудника и закрытия окна 
        btn_edit = ttk.Button(self, text="Редактировать") 
        btn_edit.place(x=205, y=170) 
 
        btn_edit.bind( 
            "<Button-1>", 
            lambda event: self.view.update_records( 
                self.entry_fio.get(), self.entry_tel.get(), self.entry_email.get(), self.entry_salary.get() 
            ), 
        ) 
 
        btn_edit.bind("<Button-1>", lambda event: self.destroy(), add="+") 
        self.btn_ok.destroy() 
 
    def default_data(self) -> None: 
        """Метод вставки уже имеющихся данных сотрудника в поля редактирования""" 
 
        self.db.cursor.execute( 
            "SELECT * FROM db WHERE id=?", 
            self.view.tree.set(self.view.tree.selection()[0], "#1"), 
        ) 
        row = self.db.cursor.fetchone() 
        self.entry_fio.insert(0, row[1])  
        self.entry_tel.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4]) 
 
 
# Класс дочернего окна для поиска сотрудника по ФИО в базе данных, 
# наследуется от класса Toplevel библиотеки tkinter 
class Search(tk.Toplevel): 
    def __init__(self) -> None: 
        """Метод создания экземпляра класса Search""" 
 
        super().__init__() 
        self.init_search() 
        self.view = app 
 
    def init_search(self): 
        """Метод для поиска сотрудника""" 
 
        # Настройки окна 
        self.title("Поиск сотрудника") 
        self.geometry("300x100") 
        self.resizable(False, False) 
 
        label_search = tk.Label(self, text="ФИО:") 
        label_search.place(x=50, y=20) 
 
        self.entry_search = ttk.Entry(self) 
        self.entry_search.place(x=100, y=20, width=150) 
 
        # Кнопка для закрытия окна 
        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy) 
        btn_cancel.place(x=185, y=50) 
 
        # Кнопка для поиска сотрудника по ФИО и закрытия окна 
        btn_search = ttk.Button(self, text="Найти") 
        btn_search.place(x=105, y=50) 
        btn_search.bind( 
            "<Button-1>", 
            lambda event: self.view.search_records(self.entry_search.get()), 
        ) 
        btn_search.bind("<Button-1>", lambda event: self.destroy(), add="+") 
 
 
# Класс для выполнения действий с базой данных 
class DB: 
    def __init__(self) -> None: 
        """Создание экземпляра класса DB""" 
 
        self.conn = sqlite3.connect("db.db") 
        self.cursor = self.conn.cursor() 
        self.cursor.execute( 
            """CREATE TABLE IF NOT EXISTS db ( 
                id INTEGER PRIMARY KEY, 
                fio TEXT, 
                tel TEXT, 
                email TEXT, 
                salary INTEGER 
            )""" 
        ) 
        self.conn.commit() 
 
    def insert_data(self, fio, tel, email, salary) -> None: 
        """Метод для добавления данных в базу данных""" 
 
        self.cursor.execute( 
            """INSERT INTO db(fio, tel, email, salary) VALUES(?, ?, ?, ?)""", (fio, tel, email, salary) 
        ) 
        self.conn.commit() 
 
 
if __name__ == "__main__": 
    root = tk.Tk() 
    db = DB() 
    app = Main(root) 
    app.pack() 
    root.title("Список сотрудников компании") 
    root.geometry("800x500") 
    root.resizable(False, False) 
    root.mainloop()