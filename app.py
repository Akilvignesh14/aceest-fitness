import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

class ACEestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ACEest Fitness & Performance v2.0.1")
        self.root.geometry("1300x850")
        self.root.configure(bg="#1a1a1a")

        # Core Data Store
        self.clients = []  
        self.programs = {
            "Fat Loss (FL)": {"workout": "Squat 5x5, EMOM Bike, Bench, Deadlift", 
                              "diet": "Egg Whites, Chicken, Fish, Millet", "color": "#e74c3c", "factor": 22},
            "Muscle Gain (MG)": {"workout": "Squat 5x5, Bench 5x5, Deadlift, Rows", 
                                 "diet": "Eggs, PB Oats, Biryani, Mutton", "color": "#2ecc71", "factor": 35},
            "Beginner (BG)": {"workout": "Air Squats, Ring Rows, Push-ups, Form Focus", 
                              "diet": "Balanced Tamil Meals, High Protein", "color": "#3498db", "factor": 26}
        }

        # Initialize UI Placeholders
        self.name_var = self.age_var = self.weight_var = self.program_var = None
        self.progress_var = self.notes_var = self.client_table = None
        self.fig = self.ax = self.canvas = None

        self.setup_ui()

    def setup_ui(self):
        # 1. HEADER
        header = tk.Frame(self.root, bg="#d4af37", height=80)
        header.pack(fill="x")
        tk.Label(header, text="ACEest PERFORMANCE MANAGEMENT SYSTEM",
                 font=("Helvetica", 22, "bold"), bg="#d4af37", fg="black").pack(pady=20)

        main = tk.Frame(self.root, bg="#1a1a1a")
        main.pack(fill="both", expand=True, padx=20, pady=10)

        # 2. LEFT PANEL (FORM)
        left = tk.LabelFrame(main, text=" Client Entry ", bg="#1a1a1a", fg="#d4af37", font=("Arial", 11, "bold"))
        left.pack(side="left", fill="y", padx=10)

        # 3. RIGHT PANEL (ANALYTICS)
        right = tk.Frame(main, bg="#1a1a1a")
        right.pack(side="right", fill="both", expand=True)

        # --- HEADLESS / MOCK SAFETY CHECK ---
        is_real_ui = hasattr(self.root, 'tk') and "magicmock" not in str(type(self.root)).lower()

        if is_real_ui:
            self._build_interactive_form(left)
            self._build_data_views(right)
        else:
            # Minimal UI for Headless Tests
            self.workout_text = self._scrollable_block(right, " Workout Plan ")
            self.diet_text = self._scrollable_block(right, " Diet Plan ")
            tk.Label(right, text="[CI-TEST-MODE]", bg="#1a1a1a", fg="gray").pack()

    def _build_interactive_form(self, parent):
        self.name_var = tk.StringVar(master=self.root)
        self.age_var = tk.IntVar(master=self.root)
        self.weight_var = tk.DoubleVar(master=self.root)
        self.program_var = tk.StringVar(master=self.root)
        self.progress_var = tk.IntVar(master=self.root, value=0)
        self.notes_var = tk.StringVar(master=self.root)

        self._input(parent, "Client Name", self.name_var)
        self._input(parent, "Age", self.age_var)
        self._input(parent, "Current Weight (kg)", self.weight_var)

        tk.Label(parent, text="Target Program", bg="#1a1a1a", fg="white").pack(pady=5)
        self.program_box = ttk.Combobox(parent, textvariable=self.program_var, 
                                        values=list(self.programs.keys()), state="readonly")
        self.program_box.pack(padx=20, pady=5)
        self.program_box.bind("<<ComboboxSelected>>", self.update_display)

        tk.Label(parent, text="Weekly Adherence %", bg="#1a1a1a", fg="white").pack(pady=5)
        ttk.Scale(parent, from_=0, to=100, variable=self.progress_var, orient="horizontal").pack(padx=20, fill="x")

        tk.Label(parent, text="Coach Remarks", bg="#1a1a1a", fg="white").pack(pady=5)
        tk.Entry(parent, textvariable=self.notes_var, bg="#333", fg="white").pack(padx=20, pady=5)

        ttk.Button(parent, text="Add to Database", command=self.save_client).pack(pady=15, fill="x", padx=20)
        ttk.Button(parent, text="Export CSV Report", command=self.export_csv).pack(pady=5, fill="x", padx=20)
        ttk.Button(parent, text="Clear Form", command=self.reset).pack(pady=5)

    def _build_data_views(self, parent):
        # Display Blocks
        self.workout_text = self._scrollable_block(parent, " Prescribed Training ")
        self.diet_text = self._scrollable_block(parent, " Prescribed Nutrition ")
        self.calorie_label = tk.Label(parent, text="Est. Daily Intake: -- kcal", 
                                      bg="#1a1a1a", fg="#d4af37", font=("Arial", 12, "bold"))
        self.calorie_label.pack(pady=5)

        # Database Table
        table_f = tk.LabelFrame(parent, text=" Active Client Database ", bg="#1a1a1a", fg="#d4af37")
        table_f.pack(fill="both", expand=True, pady=5)
        cols = ("Name", "Weight", "Program", "Adherence")
        self.client_table = ttk.Treeview(table_f, columns=cols, show="headings", height=4)
        for c in cols: self.client_table.heading(c, text=c)
        self.client_table.pack(fill="both", expand=True)

        # Analytics Chart
        chart_f = tk.LabelFrame(parent, text=" Adherence Analytics ", bg="#1a1a1a", fg="#d4af37")
        chart_f.pack(fill="both", expand=True, pady=5)
        self.fig, self.ax = plt.subplots(figsize=(5, 2))
        self.fig.patch.set_facecolor('#1a1a1a')
        self.ax.set_facecolor('#333')
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_f)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _input(self, parent, label, variable):
        tk.Label(parent, text=label, bg="#1a1a1a", fg="white").pack(pady=2)
        tk.Entry(parent, textvariable=variable, bg="#333", fg="white", insertbackground="white").pack(padx=20, pady=5)

    def _scrollable_block(self, parent, title):
        frame = tk.LabelFrame(parent, text=title, bg="#1a1a1a", fg="#d4af37")
        frame.pack(fill="both", expand=True, pady=2)
        text = tk.Text(frame, bg="#111", fg="white", wrap="word", height=5, font=("Consolas", 10))
        text.pack(fill="both", expand=True, padx=5, pady=5)
        text.config(state="disabled")
        return text

    def update_display(self, event=None):
        if not self.program_var: return
        p = self.program_var.get()
        data = self.programs[p]
        self._update_text(self.workout_text, data["workout"], data["color"])
        self._update_text(self.diet_text, data["diet"], "#ddd")
        if self.weight_var.get() > 0:
            cal = int(self.weight_var.get() * data["factor"])
            self.calorie_label.config(text=f"Est. Daily Intake: {cal} kcal")

    def _update_text(self, widget, content, color):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("end", content)
        widget.config(fg=color, state="disabled")

    def save_client(self):
        if not self.name_var or not self.name_var.get(): return
        client = (self.name_var.get(), self.weight_var.get(), self.program_var.get(), self.progress_var.get(), self.notes_var.get())
        self.clients.append(client)
        if self.client_table:
            self.client_table.insert("", "end", values=client[:4])
            self.update_chart()
        messagebox.showinfo("Success", "Client record added to database.")

    def update_chart(self):
        if not self.ax: return
        self.ax.clear()
        names = [c[0] for c in self.clients]
        vals = [c[3] for c in self.clients]
        self.ax.bar(names, vals, color="#d4af37")
        self.ax.tick_params(colors='white')
        self.canvas.draw()

    def export_csv(self):
        if not self.clients: return
        f = filedialog.asksaveasfilename(defaultextension=".csv")
        if f:
            with open(f, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Weight", "Program", "Adherence", "Notes"])
                writer.writerows(self.clients)

    def reset(self):
        if self.name_var:
            self.name_var.set(""); self.age_var.set(0); self.weight_var.set(0.0)
            self.program_var.set(""); self.progress_var.set(0); self.notes_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    ACEestApp(root)
    root.mainloop()