import tkinter as tk
from tkinter import ttk, messagebox

class ACEestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ACEest Fitness & Performance")
        self.root.geometry("1150x780")
        self.root.configure(bg="#1a1a1a")

        # Program Database
        self.programs = {
            "Fat Loss (FL)": {
                "workout": "Mon: Back Squat 5x5 + Core\nTue: EMOM 20min Assault Bike\nWed: Bench Press + 21-15-9\nThu: Deadlift + Box Jumps\nFri: Zone 2 Cardio 30min",
                "diet": "Breakfast: Egg Whites + Oats\nLunch: Grilled Chicken + Brown Rice\nDinner: Fish Curry + Millet Roti\nTarget: ~2000 kcal",
                "color": "#e74c3c",
                "calorie_factor": 22
            },
            "Muscle Gain (MG)": {
                "workout": "Mon: Squat 5x5\nTue: Bench 5x5\nWed: Deadlift 4x6\nThu: Front Squat 4x8\nFri: Incline Press 4x10\nSat: Barbell Rows 4x10",
                "diet": "Breakfast: Eggs + PB Oats\nLunch: Chicken Biryani\nDinner: Mutton Curry + Rice\nTarget: ~3200 kcal",
                "color": "#2ecc71",
                "calorie_factor": 35
            },
            "Beginner (BG)": {
                "workout": "Full Body Circuit:\n- Air Squats\n- Ring Rows\n- Push-ups\nFocus: Technique & Consistency",
                "diet": "Balanced Tamil Meals\nIdli / Dosa / Rice + Dal\nProtein Target: 120g/day",
                "color": "#3498db",
                "calorie_factor": 26
            }
        }

        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        # Explicitly check for 'tk' AND pass the master to the style object
        if hasattr(self.root, 'tk'):
            try:
                # Passing master=self.root prevents it from creating a new 'Tk' instance
                self.style = ttk.Style(master=self.root)
                self.style.theme_use('clam')
                self.style.configure("TCombobox", fieldbackground="#333", background="#d4af37")
            except Exception:
                self.style = None
        else:
            self.style = None

    def setup_ui(self):
        # --- 1. HEADER ---
        header = tk.Frame(self.root, bg="#d4af37", height=80)
        header.pack(fill="x")
        tk.Label(
            header,
            text="ACEest FUNCTIONAL FITNESS SYSTEM",
            font=("Helvetica", 24, "bold"),
            bg="#d4af37",
            fg="black"
        ).pack(pady=20)

        # --- 2. MAIN LAYOUT ---
        main = tk.Frame(self.root, bg="#1a1a1a")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        left = tk.LabelFrame(main, text=" Client Profile ", bg="#1a1a1a",
                             fg="#d4af37", font=("Arial", 12, "bold"))
        left.pack(side="left", fill="y", padx=10)

        right = tk.Frame(main, bg="#1a1a1a")
        right.pack(side="right", fill="both", expand=True)

        # --- 3. DYNAMIC UI (VARIABLE DEPENDENT) ---
        if hasattr(self.root, 'tk'):
            # Explicitly link variables to root to prevent TclErrors in tests
            self.name_var = tk.StringVar(master=self.root)
            self.age_var = tk.IntVar(master=self.root)
            self.weight_var = tk.DoubleVar(master=self.root)
            self.program_var = tk.StringVar(master=self.root)
            self.progress_var = tk.IntVar(master=self.root, value=0)
            
            # Form Inputs
            self._input(left, "Name", self.name_var)
            self._input(left, "Age", self.age_var)
            self._input(left, "Weight (kg)", self.weight_var)

            tk.Label(left, text="Program", bg="#1a1a1a", fg="white").pack(pady=5)
            self.program_box = ttk.Combobox(
                left,
                textvariable=self.program_var,
                values=list(self.programs.keys()),
                state="readonly"
            )
            self.program_box.pack(padx=20)
            self.program_box.bind("<<ComboboxSelected>>", self.update_program)

            tk.Label(left, text="Weekly Adherence (%)", bg="#1a1a1a", fg="white").pack(pady=10)
            ttk.Scale(left, from_=0, to=100, variable=self.progress_var, orient="horizontal").pack(padx=20)
            
            ttk.Button(left, text="Save Client", command=self.save_client).pack(pady=15)
            ttk.Button(left, text="Reset", command=self.reset).pack()
        else:
            # Headless Fallback
            self.name_var = self.age_var = self.weight_var = self.program_var = self.progress_var = None

        # --- 4. STATIC UI (DISPLAY BLOCKS) ---
        self.workout_text = self._scrollable_block(right, " Weekly Training Plan ")
        self.diet_text = self._scrollable_block(right, " Nutrition Plan (TN Context) ")

        self.calorie_label = tk.Label(
            right,
            text="Estimated Calories: --",
            bg="#1a1a1a",
            fg="#d4af37",
            font=("Arial", 12, "bold")
        )
        self.calorie_label.pack(pady=10)

    def _input(self, parent, label, variable):
        tk.Label(parent, text=label, bg="#1a1a1a", fg="white").pack(pady=5)
        tk.Entry(parent, textvariable=variable, bg="#333", fg="white").pack(padx=20)

    def _scrollable_block(self, parent, title):
        frame = tk.LabelFrame(parent, text=title, bg="#1a1a1a",
                              fg="#d4af37", font=("Arial", 12))
        frame.pack(fill="both", expand=True, pady=5)

        text = tk.Text(frame, bg="#111", fg="white", wrap="word", height=10)
        text.pack(fill="both", expand=True, padx=10, pady=10)
        text.config(state="disabled")
        return text

    def update_program(self, event=None):
        if self.program_var and self.program_var.get():
            program = self.program_var.get()
            data = self.programs[program]

            self._update_text(self.workout_text, data["workout"], data["color"])
            self._update_text(self.diet_text, data["diet"], "white")

            if self.weight_var and self.weight_var.get() > 0:
                calories = int(self.weight_var.get() * data["calorie_factor"])
                self.calorie_label.config(text=f"Estimated Calories: {calories} kcal")

    def _update_text(self, widget, content, color):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("end", content)
        widget.config(fg=color, state="disabled")

    def save_client(self):
        if not self.name_var or not self.name_var.get() or not self.program_var.get():
            messagebox.showwarning("Incomplete", "Please fill client name and program.")
            return

        messagebox.showinfo(
            "Saved",
            f"Client {self.name_var.get()} saved successfully.\n"
            f"Adherence: {self.progress_var.get()}%"
        )

    def reset(self):
        if self.name_var:
            self.name_var.set("")
            self.age_var.set(0)
            self.weight_var.set(0.0)
            self.program_var.set("")
            self.progress_var.set(0)
            self._update_text(self.workout_text, "", "white")
            self._update_text(self.diet_text, "", "white")
            self.calorie_label.config(text="Estimated Calories: --")

if __name__ == "__main__":
    root = tk.Tk()
    ACEestApp(root)
    root.mainloop()