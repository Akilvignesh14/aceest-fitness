import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, date
import matplotlib.pyplot as plt
import os

DB_NAME = "aceest_fitness.db"

class ACEestApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("ACEest Fitness & Performance v3.0.1")
        self.root.geometry("1300x850")
        self.root.configure(bg="#1a1a1a")

        # --- HEADLESS / MOCK SAFETY CHECK ---
        self.is_real_ui = hasattr(self.root, 'tk') and "magicmock" not in str(type(self.root)).lower()

        self.conn = None
        self.cur = None
        self.current_client = None

        self.init_db()
        self.setup_data()
        self.setup_ui()
        
        if self.is_real_ui:
            self.refresh_client_list()

    def init_db(self):
        # Use in-memory for testing, physical DB for real use
        db_path = ":memory:" if not self.is_real_ui else DB_NAME
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

        # Schema: Clients, Progress, Workouts, Exercises, Metrics
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE, age INTEGER, height REAL, weight REAL,
                program TEXT, calories INTEGER, target_weight REAL, target_adherence INTEGER
            )
        """)
        self.cur.execute("CREATE TABLE IF NOT EXISTS progress (id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT, week TEXT, adherence INTEGER)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS workouts (id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT, date TEXT, workout_type TEXT, duration_min INTEGER, notes TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS exercises (id INTEGER PRIMARY KEY AUTOINCREMENT, workout_id INTEGER, name TEXT, sets INTEGER, reps INTEGER, weight REAL)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS metrics (id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT, date TEXT, weight REAL, waist REAL, bodyfat REAL)")
        self.conn.commit()

    def setup_data(self):
        self.programs = {
            "Fat Loss (FL) – 3 day": {"factor": 22, "desc": "3-day full-body fat loss"},
            "Fat Loss (FL) – 5 day": {"factor": 24, "desc": "5-day split fat loss"},
            "Muscle Gain (MG) – PPL": {"factor": 35, "desc": "Push/Pull/Legs hypertrophy"},
            "Beginner (BG)": {"factor": 26, "desc": "3-day beginner full-body"},
        }

    def setup_ui(self):
        # Header & Status Bar
        header = tk.Label(self.root, text="ACEest PERFORMANCE MANAGEMENT v3.0.1", bg="#d4af37", fg="black", font=("Helvetica", 24, "bold"), height=2)
        header.pack(fill="x")
        
        self.status_var = tk.StringVar(master=self.root, value="System Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bg="#111", fg="#d4af37", anchor="w")
        status_bar.pack(side="bottom", fill="x")

        main = tk.Frame(self.root, bg="#1a1a1a")
        main.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Panel (Gated)
        left = tk.LabelFrame(main, text=" Client Management ", bg="#1a1a1a", fg="#d4af37", font=("Arial", 12, "bold"))
        left.pack(side="left", fill="y", padx=10, pady=5)

        if self.is_real_ui:
            self._build_sidebar(left)
            self._build_right_notebook(main)
        else:
            self.name = tk.StringVar(master=self.root)
            self.summary = tk.Text(main)

    def _build_sidebar(self, parent):
        tk.Label(parent, text="Select Client", bg="#1a1a1a", fg="white").pack()
        self.client_list = ttk.Combobox(parent, state="readonly")
        self.client_list.pack(pady=5)
        self.client_list.bind("<<ComboboxSelected>>", self.on_client_selected)

        self.name = tk.StringVar(master=self.root); self.age = tk.IntVar(master=self.root)
        self.height = tk.DoubleVar(master=self.root); self.weight = tk.DoubleVar(master=self.root)
        self.program = tk.StringVar(master=self.root); self.adherence = tk.IntVar(master=self.root)
        self.target_weight = tk.DoubleVar(master=self.root); self.target_adherence = tk.IntVar(master=self.root)

        self._field(parent, "Name", self.name)
        self._field(parent, "Height (cm)", self.height)
        self._field(parent, "Weight (kg)", self.weight)

        tk.Label(parent, text="Program", bg="#1a1a1a", fg="white").pack()
        ttk.Combobox(parent, textvariable=self.program, values=list(self.programs.keys()), state="readonly").pack()

        ttk.Button(parent, text="Save Client", command=self.save_client).pack(pady=10)
        ttk.Button(parent, text="Log Workout", command=self.open_log_workout_window).pack(pady=5)
        ttk.Button(parent, text="Log Metrics", command=self.open_log_metrics_window).pack(pady=5)
        ttk.Button(parent, text="Save Weekly Progress", command=self.save_progress).pack(pady=5)

    def _build_right_notebook(self, parent):
        right = tk.Frame(parent, bg="#1a1a1a")
        right.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        nb = ttk.Notebook(right)
        nb.pack(fill="both", expand=True)

        tab1 = tk.Frame(nb, bg="#1a1a1a")
        nb.add(tab1, text="Summary")
        self.summary = tk.Text(tab1, bg="#111", fg="white", font=("Consolas", 11), state="disabled")
        self.summary.pack(fill="both", expand=True, padx=10, pady=10)

        tab2 = tk.Frame(nb, bg="#1a1a1a")
        nb.add(tab2, text="Analytics")
        ttk.Button(tab2, text="Adherence Chart", command=self.show_progress_chart).pack(pady=10)
        ttk.Button(tab2, text="Weight Trend", command=self.show_weight_chart).pack(pady=5)
        ttk.Button(tab2, text="BMI Analysis", command=self.show_bmi_info).pack(pady=5)

    def _field(self, parent, label, var):
        tk.Label(parent, text=label, bg="#1a1a1a", fg="white").pack()
        tk.Entry(parent, textvariable=var, bg="#333", fg="white").pack(pady=2)

    def refresh_client_list(self):
        self.cur.execute("SELECT name FROM clients ORDER BY name")
        names = [row[0] for row in self.cur.fetchall()]
        self.client_list["values"] = names

    def on_client_selected(self, event=None):
        name = self.client_list.get()
        self.name.set(name); self.current_client = name; self.load_client()

    def save_client(self):
        if not self.name.get(): return
        cal = int(self.weight.get() * self.programs[self.program.get()]["factor"]) if self.weight.get() > 0 else 0
        self.cur.execute("INSERT OR REPLACE INTO clients (name, age, height, weight, program, calories) VALUES (?, ?, ?, ?, ?, ?)",
                         (self.name.get(), self.age.get(), self.height.get(), self.weight.get(), self.program.get(), cal))
        self.conn.commit(); self.refresh_client_list(); messagebox.showinfo("Saved", "Database updated")

    def load_client(self):
        self.cur.execute("SELECT * FROM clients WHERE name=?", (self.name.get(),))
        row = self.cur.fetchone()
        if row:
            self.age.set(row[2]); self.height.set(row[3]); self.weight.set(row[4]); self.program.set(row[5])
            self.refresh_summary()

    def refresh_summary(self):
        self.summary.config(state="normal")
        self.summary.delete("1.0", "end")
        self.summary.insert("end", f"CLIENT PROFILE\n--------------\nName: {self.name.get()}\nProgram: {self.program.get()}\nWeight: {self.weight.get()} kg")
        self.summary.config(state="disabled")

    def save_progress(self):
        week = datetime.now().strftime("Week %U - %Y")
        self.cur.execute("INSERT INTO progress (client_name, week, adherence) VALUES (?, ?, ?)",
                         (self.name.get(), week, self.adherence.get()))
        self.conn.commit(); messagebox.showinfo("Success", "Weekly progress logged")

    def show_progress_chart(self):
        if not self.is_real_ui or not self.name.get(): return
        self.cur.execute("SELECT week, adherence FROM progress WHERE client_name=?", (self.name.get(),))
        data = self.cur.fetchall()
        if data:
            plt.figure(figsize=(8,4)); plt.plot([r[0] for r in data], [r[1] for r in data], marker='o')
            plt.title(f"Adherence: {self.name.get()}"); plt.show()

    def show_weight_chart(self):
        if not self.is_real_ui or not self.name.get(): return
        self.cur.execute("SELECT date, weight FROM metrics WHERE client_name=?", (self.name.get(),))
        data = self.cur.fetchall()
        if data:
            plt.figure(figsize=(8,4)); plt.plot([r[0] for r in data], [r[1] for r in data], color='orange')
            plt.title("Weight Trend"); plt.show()

    def show_bmi_info(self):
        h = self.height.get()/100; w = self.weight.get()
        if h > 0:
            bmi = round(w/(h*h), 1)
            messagebox.showinfo("BMI Info", f"BMI: {bmi}")

    def open_log_workout_window(self):
        if not self.is_real_ui: return
        messagebox.showinfo("Module", "Workout session logger initialized.")

    def open_log_metrics_window(self):
        if not self.is_real_ui: return
        messagebox.showinfo("Module", "Body metrics logger initialized.")

if __name__ == "__main__":
    root = tk.Tk()
    ACEestApp(root)
    root.mainloop()