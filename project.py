import tkinter as tk
from tkinter import ttk, messagebox
# ==============================
# GPA Calculator — Fixed & Clean
# Semester GPA + Cumulative GPA
# ==============================
class Course:
    def __init__(self, name="", credit_hours=0, grade_percentage=0.0):
        self.name = name
        self.credit_hours = credit_hours
        self.grade_percentage = grade_percentage
        self.letter_grade = ""
        self.grade_points = 0.0
        self.calculate_letter_grade()
        self.calculate_grade_points()

    def calculate_letter_grade(self):
        p = self.grade_percentage
        if p >= 97:
            self.letter_grade = "A+"
        elif p >= 93:
            self.letter_grade = "A"
        elif p >= 89:
            self.letter_grade = "A-"
        elif p >= 84:
            self.letter_grade = "B+"
        elif p >= 80:
            self.letter_grade = "B"
        elif p >= 76:
            self.letter_grade = "B-"
        elif p >= 73:
            self.letter_grade = "C+"
        elif p >= 70:
            self.letter_grade = "C"
        elif p >= 67:
            self.letter_grade = "C-"
        elif p >= 64:
            self.letter_grade = "D+"
        elif p >= 60:
            self.letter_grade = "D"
        else:
            self.letter_grade = "F"

    def calculate_grade_points(self):
        mapping = {
            "A+": 4.0,
            "A": 3.83,
            "A-": 3.7,
            "B+": 3.3,
            "B": 3.0,
            "B-": 2.7,
            "C+": 2.3,
            "C": 2.0,
            "C-": 1.7,
            "D+": 1.3,
            "D": 1.0,
            "F": 0.0,
        }
        self.grade_points = mapping[self.letter_grade]

    def get_quality_points(self):
        """Quality Points = grade_points × credit_hours (used in GPA formula)"""
        return self.grade_points * self.credit_hours


class AcademicSystem:
    def __init__(self):
        self.courses = []
        self.previous_gpa = 0.0
        self.previous_credits = 0
        self.term_number = 1
        self.total_quality_points = 0.0
        self.total_credits = 0
        self.semester_gpa = 0.0
        self.cumulative_gpa = 0.0

    def set_previous_record(self, term_number, previous_gpa, previous_credits):
        self.term_number = term_number
        self.previous_gpa = previous_gpa
        self.previous_credits = previous_credits
        self.calculate_gpa()

    def add_course(self, course):
        if len(self.courses) < 7:
            self.courses.append(course)
            self.calculate_gpa()
            return True
        return False

    def remove_course(self, index):
        if 0 <= index < len(self.courses):
            deleted = self.courses.pop(index)
            self.calculate_gpa()
            return deleted
        return None

    def is_course_duplicate(self, course_name):
        return any(c.name.lower() == course_name.lower() for c in self.courses)

    def calculate_gpa(self):
        self.total_quality_points = sum(c.get_quality_points() for c in self.courses)
        self.total_credits = sum(c.credit_hours for c in self.courses)

        self.semester_gpa = (
            self.total_quality_points / self.total_credits
            if self.total_credits > 0
            else 0.0
        )

        previous_points = self.previous_gpa * self.previous_credits
        all_points = previous_points + self.total_quality_points
        all_credits = self.previous_credits + self.total_credits

        self.cumulative_gpa = all_points / all_credits if all_credits > 0 else 0.0

    def reset_current_semester(self):
        self.courses.clear()
        self.total_quality_points = 0.0
        self.total_credits = 0
        self.semester_gpa = 0.0
        self.calculate_gpa()

    def reset_all(self):
        self.courses.clear()
        self.previous_gpa = 0.0
        self.previous_credits = 0
        self.term_number = 1
        self.total_quality_points = 0.0
        self.total_credits = 0
        self.semester_gpa = 0.0
        self.cumulative_gpa = 0.0

    def get_gpa_status(self):
        gpa = self.cumulative_gpa
        if gpa >= 3.7:
            return "Excellent ⭐"
        elif gpa >= 3.3:
            return "Very Good 👍"
        elif gpa >= 2.7:
            return "Good 🙂"
        elif gpa >= 1.7:
            return "Acceptable ⚠️"
        elif gpa >= 1.0:
            return "Weak ❌"
        else:
            return "N/A"


class GPAApp:
    def __init__(self, root):
        self.system = AcademicSystem()
        self.root = root

        self.root.title("GPA Calculator")
        self.root.configure(bg="#F8FAFC")
        self.root.state("zoomed")  # Full screen (maximised) on Windows
        self.root.resizable(True, True)
        self.setup_style()
        self.build_ui()
        self.root.bind("<Return>", lambda e: self.add_course())

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#0F172A",
            rowheight=36,
            fieldbackground="#FFFFFF",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            background="#1B3D7A",
            foreground="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            padding=8,
        )
        style.map(
            "Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", "#0F172A")],
        )

    # ─────────────────────────────────────────────
    # UI Construction  (ALL inside the class ✅)
    # ─────────────────────────────────────────────
    def build_ui(self):
        # ── Header ──────────────────────────────
        header = tk.Frame(self.root, bg="#1B3D7A", height=110)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🎓 GPA Calculator",
            bg="#1B3D7A",
            fg="white",
            font=("Segoe UI", 30, "bold"),
        ).pack(pady=(16, 2))

        tk.Label(
            header,
            text="Semester GPA + Cumulative GPA Calculator",
            bg="#1B3D7A",
            fg="#DBEAFE",
            font=("Segoe UI", 12),
        ).pack()

        container = tk.Frame(self.root, bg="#F8FAFC")
        container.pack(fill="both", expand=True, padx=28, pady=18)

        # ── Section 1: Previous Record ───────────
        prev_card = tk.Frame(
            container,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1,
        )
        prev_card.pack(fill="x", pady=(0, 14))

        tk.Label(
            prev_card,
            text="📚 Previous Academic Record",
            bg="white",
            fg="#1B3D7A",
            font=("Segoe UI", 14, "bold"),
        ).grid(row=0, column=0, columnspan=4, sticky="w", padx=20, pady=(14, 8))

        self.term_entry = self.create_input(prev_card, "Current Term Number", 0, row=1)
        self.previous_gpa_entry = self.create_input(prev_card, "Previous GPA", 1, row=1)
        self.previous_credits_entry = self.create_input(
            prev_card, "Previous Credits", 2, row=1
        )

        tk.Button(
            prev_card,
            text="💾 Save Previous GPA",
            command=self.save_previous_record,
            bg="#10B981",
            fg="white",
            activebackground="#047857",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            padx=16,
            pady=9,
            cursor="hand2",
        ).grid(row=2, column=3, padx=20, pady=(0, 16), sticky="ew")

        self.term_entry.insert(0, "1")
        self.previous_gpa_entry.insert(0, "0")
        self.previous_credits_entry.insert(0, "0")

        # ── Section 2: Add Course ────────────────
        input_card = tk.Frame(
            container,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1,
        )
        input_card.pack(fill="x", pady=(0, 14))

        tk.Label(
            input_card,
            text="➕ Add Current Semester Course",
            bg="white",
            fg="#1B3D7A",
            font=("Segoe UI", 14, "bold"),
        ).grid(row=0, column=0, columnspan=4, sticky="w", padx=20, pady=(14, 8))

        self.course_name = self.create_input(input_card, "Course Name", 0, row=1)
        self.course_credits = self.create_input(input_card, "Credit Hours", 1, row=1)
        self.course_grade = self.create_input(input_card, "Grade %", 2, row=1)

        tk.Button(
            input_card,
            text="➕ Add Course",
            command=self.add_course,
            bg="#2563EB",
            fg="white",
            activebackground="#1B3D7A",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            padx=16,
            pady=9,
            cursor="hand2",
        ).grid(row=2, column=3, padx=20, pady=(0, 16), sticky="ew")

        tk.Label(
            input_card,
            text="📌 Note: Maximum 7 courses per semester  |  Duplicate course names are not allowed",
            bg="white",
            fg="#64748B",
            font=("Segoe UI", 9),
        ).grid(row=3, column=0, columnspan=4, sticky="w", padx=20, pady=(0, 10))

        # ── Section 3: Courses Table ─────────────
        table_card = tk.Frame(
            container,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1,
        )
        table_card.pack(fill="both", expand=True, pady=(0, 14))

        tk.Label(
            table_card,
            text="📋 Current Semester Courses",
            bg="white",
            fg="#1B3D7A",
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", padx=20, pady=(14, 8))

        # Removed "Points" (raw grade_points) — redundant with Letter Grade
        # "Quality Points" = grade_points × credit_hours (needed for GPA formula)
        columns = ("Course Name", "Credits", "Grade %", "Letter", "Quality Points")
        self.tree = ttk.Treeview(table_card, columns=columns, show="headings", height=5)

        col_widths = {
            "Course Name": 300,
            "Credits": 100,
            "Grade %": 110,
            "Letter": 100,
            "Quality Points": 160,
        }
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths[col], anchor="center")

        scrollbar = ttk.Scrollbar(
            table_card, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(
            side="left", fill="both", expand=True, padx=(20, 0), pady=(0, 14)
        )
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=(0, 14))

        self.tree.tag_configure("odd", background="#F8FAFC")
        self.tree.tag_configure("even", background="#FFFFFF")

        self.tree.bind("<Delete>", self.delete_selected_course)
        self.tree.bind("<Button-3>", self.show_context_menu)

        # ── Section 4: Results ───────────────────
        results_card = tk.Frame(
            container,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1,
        )
        results_card.pack(fill="x", pady=(0, 14))

        tk.Label(
            results_card,
            text="📊 Results",
            bg="white",
            fg="#1B3D7A",
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", padx=20, pady=(14, 10))

        results_inner = tk.Frame(results_card, bg="white")
        results_inner.pack(fill="x", padx=20, pady=(0, 18))

        for i in range(5):
            results_inner.grid_columnconfigure(i, weight=1)

        # 5 result cards — all properly stored as instance variables
        self.semester_gpa_label = self.create_result_card(
            results_inner, "📖 Semester GPA", "0.00", "#2563EB", 0
        )
        self.cumulative_gpa_label = self.create_result_card(
            results_inner, "📚 Cumulative GPA", "0.00", "#0EA5E9", 1
        )
        self.status_label = self.create_result_card(
            results_inner, "🏆 Status", "N/A", "#10B981", 2
        )
        self.credits_label = self.create_result_card(
            results_inner, "📊 Current Credits", "0", "#7C3AED", 3
        )
        self.points_label = self.create_result_card(
            results_inner, "⭐ Quality Points", "0.00", "#F59E0B", 4
        )

        # ── Buttons Row ──────────────────────────
        buttons_row = tk.Frame(container, bg="#F8FAFC")
        buttons_row.pack(fill="x", pady=(0, 8))

        tk.Button(
            buttons_row,
            text="🔄 Reset Current Semester",
            command=self.reset_current_semester,
            bg="#F59E0B",
            fg="white",
            activebackground="#B45309",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            padx=18,
            pady=9,
            cursor="hand2",
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            buttons_row,
            text="🗑️ Reset All",
            command=self.reset_all,
            bg="#EF4444",
            fg="white",
            activebackground="#B91C1C",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            padx=18,
            pady=9,
            cursor="hand2",
        ).pack(side="left")

        tk.Label(
            container,
            text="💡 Tip: Select a course and press 'Delete' key or right-click to remove it",
            bg="#F8FAFC",
            fg="#64748B",
            font=("Segoe UI", 9, "italic"),
        ).pack(pady=(4, 0))

    # ─────────────────────────────────────────────
    # Helper Widgets
    # ─────────────────────────────────────────────
    def create_result_card(self, parent, title, value, color, column):
        card = tk.Frame(parent, bg=color, padx=6, pady=2)
        card.grid(row=0, column=column, padx=6, sticky="ew")

        tk.Label(
            card,
            text=title,
            bg=color,
            fg="#DBEAFE",
            font=("Segoe UI", 9, "bold"),
        ).pack(pady=(10, 0))

        value_label = tk.Label(
            card,
            text=value,
            bg=color,
            fg="white",
            font=("Segoe UI", 16, "bold"),
        )
        value_label.pack(pady=(2, 12))
        return value_label

    def create_input(self, parent, label, column, row):
        tk.Label(
            parent,
            text=label,
            bg="white",
            fg="#0F172A",
            font=("Segoe UI", 10, "bold"),
        ).grid(row=row, column=column, padx=20, pady=(0, 5), sticky="w")

        entry = tk.Entry(
            parent,
            font=("Segoe UI", 11),
            bg="#F8FAFC",
            fg="#0F172A",
            bd=0,
            highlightthickness=1,
            highlightbackground="#CBD5E1",
            highlightcolor="#2563EB",
        )
        entry.grid(
            row=row + 1, column=column, padx=20, pady=(0, 16), ipady=8, sticky="ew"
        )
        parent.grid_columnconfigure(column, weight=1)
        return entry

    # ─────────────────────────────────────────────
    # Logic Handlers
    # ─────────────────────────────────────────────
    def save_previous_record(self):
        try:
            term_number = int(self.term_entry.get().strip())
            previous_gpa = float(self.previous_gpa_entry.get().strip())
            previous_credits = int(self.previous_credits_entry.get().strip())

            if term_number <= 0:
                messagebox.showerror("Input Error", "Term number must be positive.")
                return
            if not (0 <= previous_gpa <= 4):
                messagebox.showerror(
                    "Input Error", "Previous GPA must be between 0 and 4."
                )
                return
            if previous_credits < 0:
                messagebox.showerror(
                    "Input Error", "Previous credits cannot be negative."
                )
                return

            self.system.set_previous_record(term_number, previous_gpa, previous_credits)
            self.update_results()
            messagebox.showinfo("Saved", "Previous academic record saved successfully.")

        except ValueError:
            messagebox.showerror(
                "Input Error", "Please enter valid numbers for term, GPA, and credits."
            )

    def add_course(self):
        try:
            name = self.course_name.get().strip()
            credits_text = self.course_credits.get().strip()
            grade_text = self.course_grade.get().strip()

            if not name:
                messagebox.showerror("Input Error", "Course name cannot be empty.")
                return

            # ── Duplicate check ──────────────────
            if self.system.is_course_duplicate(name):
                messagebox.showerror(
                    "Duplicate Course",
                    f"'{name}' already exists!\nDuplicate course names are not allowed.",
                )
                return

            credits = int(credits_text)
            grade = float(grade_text)

            if credits <= 0:
                messagebox.showerror(
                    "Input Error", "Credit hours must be a positive integer."
                )
                return
            if not (0 <= grade <= 100):
                messagebox.showerror("Input Error", "Grade must be between 0 and 100.")
                return
            if len(self.system.courses) >= 7:
                messagebox.showwarning(
                    "Limit Reached", "You can only add up to 7 courses."
                )
                return

            course = Course(name, credits, grade)
            self.system.add_course(course)

            tag = "even" if len(self.system.courses) % 2 == 0 else "odd"
            self.tree.insert(
                "",
                "end",
                values=(
                    course.name,
                    course.credit_hours,
                    f"{course.grade_percentage:.2f}",
                    course.letter_grade,
                    f"{course.get_quality_points():.2f}",
                ),
                tags=(tag,),
            )

            self.update_results()
            self.clear_course_inputs()

        except ValueError:
            messagebox.showerror(
                "Input Error", "Please enter valid numbers for credits and grade."
            )

    def delete_selected_course(self, event=None):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Delete Course", "Please select a course to delete.")
            return

        item = selected[0]
        values = self.tree.item(item, "values")
        course_name = values[0]
        credits = values[1]

        if not messagebox.askyesno(
            "Confirm Delete",
            f"Delete '{course_name}' ({credits} credits)?",
        ):
            return

        # Remove from model
        for i, course in enumerate(self.system.courses):
            if course.name == course_name:
                self.system.remove_course(i)
                break

        # Remove from view
        self.tree.delete(item)
        self.recolor_treeview()
        self.update_results()
        messagebox.showinfo("Deleted", f"'{course_name}' deleted successfully.")

    def recolor_treeview(self):
        for i, child in enumerate(self.tree.get_children()):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.item(child, tags=(tag,))

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(
                label="🗑️ Delete Course", command=self.delete_selected_course
            )
            menu.post(event.x_root, event.y_root)

    def update_results(self):
        self.semester_gpa_label.config(text=f"{self.system.semester_gpa:.2f}")
        self.cumulative_gpa_label.config(text=f"{self.system.cumulative_gpa:.2f}")
        self.status_label.config(text=self.system.get_gpa_status())
        self.credits_label.config(text=str(self.system.total_credits))
        self.points_label.config(text=f"{self.system.total_quality_points:.2f}")

    def clear_course_inputs(self):
        self.course_name.delete(0, tk.END)
        self.course_credits.delete(0, tk.END)
        self.course_grade.delete(0, tk.END)
        self.course_name.focus()

    def reset_current_semester(self):
        if messagebox.askyesno(
            "Reset Semester", "Clear current semester courses only?"
        ):
            self.system.reset_current_semester()
            for row in self.tree.get_children():
                self.tree.delete(row)
            self.update_results()
            self.clear_course_inputs()

    def reset_all(self):
        if messagebox.askyesno(
            "Reset All", "Clear everything including previous records?"
        ):
            self.system.reset_all()
            for row in self.tree.get_children():
                self.tree.delete(row)
            self.term_entry.delete(0, tk.END)
            self.previous_gpa_entry.delete(0, tk.END)
            self.previous_credits_entry.delete(0, tk.END)
            self.term_entry.insert(0, "1")
            self.previous_gpa_entry.insert(0, "0")
            self.previous_credits_entry.insert(0, "0")
            self.update_results()
            self.clear_course_inputs()
if __name__ == "__main__":
    root = tk.Tk()
    app = GPAApp(root)
    root.mainloop()