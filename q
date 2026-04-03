[33mtag v2.2.1[m
Tagger: Akil Vignesh L <2025ht66023@wilp.bits-pilani.ac.in>
Date:   Fri Apr 3 09:41:13 2026 -0400

Official Release v2.2.1: Full Analytics Integration

[33mcommit 0c39551df47fb86b07154866e44a08fbc5a7db3a[m[33m ([m[1;36mHEAD[m[33m -> [m[1;32mmain[m[33m, [m[1;33mtag: [m[1;33mv2.2.1[m[33m, [m[1;31morigin/main[m[33m, [m[1;31morigin/HEAD[m[33m)[m
Author: Akil Vignesh L <2025ht66023@wilp.bits-pilani.ac.in>
Date:   Fri Apr 3 09:41:13 2026 -0400

    Release: v2.2.1 - Added SQL-driven Progress Charting

[1mdiff --git a/__pycache__/app.cpython-313.pyc b/__pycache__/app.cpython-313.pyc[m
[1mindex 53f54c9..1f44620 100644[m
Binary files a/__pycache__/app.cpython-313.pyc and b/__pycache__/app.cpython-313.pyc differ
[1mdiff --git a/app.py b/app.py[m
[1mindex 96feb72..7bfc697 100644[m
[1m--- a/app.py[m
[1m+++ b/app.py[m
[36m@@ -2,14 +2,13 @@[m [mimport tkinter as tk[m
 from tkinter import ttk, messagebox[m
 import sqlite3[m
 from datetime import datetime[m
[32m+[m[32mimport matplotlib.pyplot as plt[m
 import os[m
 [m
[31m-DB_NAME = "aceest_fitness.db"[m
[31m-[m
 class ACEestApp:[m
     def __init__(self, root):[m
         self.root = root[m
[31m-        self.root.title("ACEest Fitness & Performance v2.1.2")[m
[32m+[m[32m        self.root.title("ACEest Fitness & Performance v2.2.1")[m
         self.root.geometry("1200x800")[m
         self.root.configure(bg="#1a1a1a")[m
 [m
[36m@@ -21,11 +20,11 @@[m [mclass ACEestApp:[m
         self.setup_ui()[m
 [m
     def init_db(self):[m
[31m-        # SRE FIX: Use in-memory database for headless tests to avoid file permission errors[m
[32m+[m[32m        # Use in-memory DB for headless tests, physical DB for real use[m
         if not self.is_real_ui:[m
             self.conn = sqlite3.connect(":memory:")[m
         else:[m
[31m-            self.conn = sqlite3.connect(DB_NAME)[m
[32m+[m[32m            self.conn = sqlite3.connect("aceest_fitness.db")[m
             [m
         self.cur = self.conn.cursor()[m
         self.cur.execute("""[m
[36m@@ -58,7 +57,7 @@[m [mclass ACEestApp:[m
     def setup_ui(self):[m
         header = tk.Label([m
             self.root,[m
[31m-            text="ACEest Functional Fitness System v2.1.2",[m
[32m+[m[32m            text="ACEest Functional Fitness System v2.2.1",[m
             bg="#d4af37",[m
             fg="black",[m
             font=("Helvetica", 24, "bold"),[m
[36m@@ -97,6 +96,7 @@[m [mclass ACEestApp:[m
             ttk.Button(left, text="Save Client", command=self.save_client).pack(pady=10)[m
             ttk.Button(left, text="Load Client", command=self.load_client).pack(pady=5)[m
             ttk.Button(left, text="Save Progress", command=self.save_progress).pack(pady=5)[m
[32m+[m[32m            ttk.Button(left, text="View Progress Chart", command=self.show_progress_chart).pack(pady=10)[m
         else:[m
             self.name = self.age = self.weight = self.program = self.adherence = None[m
 [m
[36m@@ -140,13 +140,40 @@[m [mclass ACEestApp:[m
         self.summary.insert("end", f"CLIENT PROFILE\n--------------\nName: {name}\nAge: {age}\nWeight: {weight} kg\nProgram: {program}\nCalories: {calories} kcal/day")[m
 [m
     def save_progress(self):[m
[31m-        if not self.name: return[m
[32m+[m[32m        if not self.name or not self.name.get(): return[m
         week = datetime.now().strftime("Week %U - %Y")[m
         self.cur.execute("INSERT INTO progress (client_name, week, adherence) VALUES (?, ?, ?)",[m
                          (self.name.get(), week, self.adherence.get()))[m
         self.conn.commit()[m
         messagebox.showinfo("Progress Saved", "Weekly progress logged")[m
 [m
[32m+[m[32m    def show_progress_chart(self):[m
[32m+[m[32m        if not self.is_real_ui: return # Prevent Matplotlib popups in CI[m
[32m+[m[41m        [m
[32m+[m[32m        if not self.name.get():[m
[32m+[m[32m            messagebox.showwarning("No Client", "Enter client name first")[m
[32m+[m[32m            return[m
[32m+[m
[32m+[m[32m        self.cur.execute("SELECT week, adherence FROM progress WHERE client_name=? ORDER BY id", (self.name.get(),))[m
[32m+[m[32m        data = self.cur.fetchall()[m
[32m+[m
[32m+[m[32m        if not data:[m
[32m+[m[32m            messagebox.showinfo("No Data", "No progress data available")[m
[32m+[m[32m            return[m
[32m+[m
[32m+[m[32m        weeks = [row[0] for row in data][m
[32m+[m[32m        adherence = [row[1] for row in data][m
[32m+[m
[32m+[m[32m        plt.figure(figsize=(8, 4))[m
[32m+[m[32m        plt.plot(weeks, adherence, marker="o", color="#d4af37", linewidth=2)[m
[32m+[m[32m        plt.title(f"Weekly Adherence – {self.name.get()}")[m
[32m+[m[32m        plt.ylabel("Adherence (%)")[m
[32m+[m[32m        plt.ylim(0, 105)[m
[32m+[m[32m        plt.grid(True, linestyle='--', alpha=0.7)[m
[32m+[m[32m        plt.xticks(rotation=45)[m
[32m+[m[32m        plt.tight_layout()[m
[32m+[m[32m        plt.show()[m
[32m+[m
 if __name__ == "__main__":[m
     root = tk.Tk()[m
     ACEestApp(root)[m
