import math
import tkinter as tk
from tkinter import messagebox

from database import Database


class Calculator(object):
    def __init__(self):
        self.db = Database()
        self.field_text = ""
        self.factorial_expression = ""
        self.stats_window = None
        self.window = tk.Tk()
        self.field = tk.Text(self.window, height=2, width=21, font=("Times New Roman", 20))
        self.draw_calculator()


    def log_operation(self, operation, operands, result):
        self.db.log_operation(operation, operands, result)

    def factorial(self):
        self.factorial_expression = self.field_text
        self.field_text += "!"
        self.field.delete("1.0", "end")
        self.field.insert("1.0", self.field_text)

    def calculate(self):
        expression = self.field_text
        try:
            expression = expression.replace("[", "(").replace("]", ")")
            if "(" in expression or ")" in expression:
                result = str(eval(expression))
                self.log_operation('calculation', expression, result)
            elif "+" in expression:
                parts = expression.split("+", 1)
                result = str(eval(parts[0]) + eval(parts[1]))
                self.log_operation('addition', parts[0] + ',' + parts[1], result)
            elif "-" in expression:
                parts = expression.split("-", 1)
                result = str(eval(parts[0]) - eval(parts[1]))
                self.log_operation('subtraction', parts[0] + ',' + parts[1], result)
            elif "*" in expression:
                parts = expression.split("*", 1)
                result = str(eval(parts[0]) * eval(parts[1]))
                self.log_operation('multiplication', parts[0] + ',' + parts[1], result)
            elif "/" in expression:
                parts = expression.split("/", 1)
                result = str(eval(parts[0]) / eval(parts[1]))
                self.log_operation('division', parts[0] + ',' + parts[1], result)
            elif "%" in expression:
                parts = expression.split("%", 1)
                result = str(eval(parts[0]) * eval(parts[1]) / 100)
                self.log_operation('percentage', parts[0] + ',' + parts[1], result)
            elif "!" in expression:
                # Handle factorial specifically
                base = expression.replace("!", "")
                result = str(math.factorial(int(base)))
                self.log_operation('factorial', base, result)
            elif "^" in expression:
                parts = expression.split("^", 1)
                result = str(eval(parts[0]) ** eval(parts[1]))
                self.log_operation('exponentiation', parts[0] + "," + parts[1], result)
            else:
                # Evaluate the entire expression if none of the above cases match
                result = str(eval(expression))
                self.log_operation('calculation', expression, result)

            self.field.delete("1.0", "end")
            self.field.insert("1.0", result)
            self.field_text = result
            self.factorial_expression = ""
        except Exception as e:
            error_message = str(e)
            self.log_operation('error', expression, error_message)
            self.field.delete("1.0", "end")
            self.field.insert("1.0", "Error: " + error_message)
            self.field_text = ""
            self.factorial_expression = ""
            messagebox.showerror('Error', str(e))

    def add_to_field(self, entry):
        if len(self.field_text) < 128:
            self.field_text = self.field_text + str(entry)
            self.field.delete("1.0", "end")
            self.field.insert("1.0", self.field_text)

    def clear(self):
        self.field_text = ""
        self.field.delete("1.0", "end")

    def show_statistics(self):
        if self.stats_window:
            self.stats_window.destroy()

        self.stats_window = tk.Toplevel(self.window)
        self.stats_window.title("Statistics")
        self.stats_window.geometry("400x400")

        # Elementary operations
        total_additions = self.db.cursor.execute(
            "SELECT COUNT(*) FROM operations WHERE operation = 'addition'").fetchone()[0]
        total_subtractions = self.db.cursor.execute(
            "SELECT COUNT(*) FROM operations WHERE operation = 'subtraction'").fetchone()[0]
        total_multiplications = self.db.cursor.execute(
            "SELECT COUNT(*) FROM operations WHERE operation = 'multiplication'").fetchone()[0]

        total_divisions = self.db.cursor.execute(
            "SELECT COUNT(*) FROM operations WHERE operation = 'division'").fetchone()[0]

        # Other operations
        total_composite = \
            self.db.cursor.execute("SELECT COUNT(*) FROM operations WHERE operation = 'calculation'").fetchone()[0]
        total_to_power = \
            self.db.cursor.execute("SELECT COUNT(*) FROM operations WHERE operation = 'exponentiation'").fetchone()[0]
        total_percentage = \
            self.db.cursor.execute("SELECT COUNT(*) FROM operations WHERE operation = 'percentage'").fetchone()[0]
        total_factorial = \
            self.db.cursor.execute("SELECT COUNT(*) FROM operations WHERE operation = 'factorial'").fetchone()[0]

        total_elementary_operations = total_additions + total_subtractions + total_multiplications + total_divisions
        print(f" Total elementary operations: {total_elementary_operations}")

        total_sum_other_operations = total_to_power + total_percentage + total_factorial + total_composite
        print(f" Total other operations: {total_sum_other_operations}")

        total_sum_of_all_operations = total_elementary_operations + total_sum_other_operations
        print(f" Total total_sum_of_all_operations operations: {total_sum_of_all_operations}")

        avg_elementary_operations = total_elementary_operations / total_sum_of_all_operations if total_sum_of_all_operations > 0 else 0

        stats = f"""
                Total Additions:          {total_additions}
                Total Subtractions:       {total_subtractions}
                Total Multiplications:    {total_multiplications}
                Total Divisions:          {total_divisions}

            -------------------------------------

                Total Factorial:         {total_factorial}
                Total Exponential:      {total_to_power}
                Total Percentage:         {total_percentage}
                Total Composite:         {total_composite}

            --------------------------------------
                Average Elementary Operations: {avg_elementary_operations:.2f}
        """
        stats_label = tk.Label(self.stats_window, text=stats, font=("Times New Roman", 14))
        stats_label.pack()

    def draw_calculator(self):
        self.window.geometry("300x400")

        self.field.grid(row=1, column=1, columnspan=4)

        btn_0 = tk.Button(self.window, text="0", command=lambda: self.add_to_field(0), width=5,
                          font=("Times New Roman", 14))
        btn_0.grid(row=5, column=1)
        btn_1 = tk.Button(self.window, text="1", command=lambda: self.add_to_field(1), width=5,
                          font=("Times New Roman", 14))
        btn_1.grid(row=4, column=1)
        btn_2 = tk.Button(self.window, text="2", command=lambda: self.add_to_field(2), width=5,
                          font=("Times New Roman", 14))
        btn_2.grid(row=4, column=2)
        btn_3 = tk.Button(self.window, text="3", command=lambda: self.add_to_field(3), width=5,
                          font=("Times New Roman", 14))
        btn_3.grid(row=4, column=3)
        btn_4 = tk.Button(self.window, text="4", command=lambda: self.add_to_field(4), width=5,
                          font=("Times New Roman", 14))
        btn_4.grid(row=3, column=1)
        btn_5 = tk.Button(self.window, text="5", command=lambda: self.add_to_field(5), width=5,
                          font=("Times New Roman", 14))
        btn_5.grid(row=3, column=2)
        btn_6 = tk.Button(self.window, text="6", command=lambda: self.add_to_field(6), width=5,
                          font=("Times New Roman", 14))
        btn_6.grid(row=3, column=3)
        btn_7 = tk.Button(self.window, text="7", command=lambda: self.add_to_field(7), width=5,
                          font=("Times New Roman", 14))
        btn_7.grid(row=2, column=1)
        btn_8 = tk.Button(self.window, text="8", command=lambda: self.add_to_field(8), width=5,
                          font=("Times New Roman", 14))
        btn_8.grid(row=2, column=2)
        btn_9 = tk.Button(self.window, text="9", command=lambda: self.add_to_field(9), width=5,
                          font=("Times New Roman", 14))
        btn_9.grid(row=2, column=3)
        btn_l_par = tk.Button(self.window, text="(", command=lambda: self.add_to_field("("), width=5,
                              font=("Times New Roman", 14))
        btn_l_par.grid(row=6, column=1)

        btn_l_bra = tk.Button(self.window, text="[", command=lambda: self.add_to_field("["), width=5,
                              font=("Times New Roman", 14))
        btn_l_bra.grid(row=7, column=1)

        btn_r_par = tk.Button(self.window, text=")", command=lambda: self.add_to_field(")"), width=5,
                              font=("Times New Roman", 14))
        btn_r_par.grid(row=6, column=2)

        btn_r_bra = tk.Button(self.window, text="]", command=lambda: self.add_to_field("]"), width=5,
                              font=("Times New Roman", 14))
        btn_r_bra.grid(row=7, column=2)

        btn_equals = tk.Button(self.window, text="=", command=lambda: self.calculate(), width=10,
                               font=("Times New Roman", 14))
        btn_equals.grid(row=8, column=2, columnspan=2)
        btn_point = tk.Button(self.window, text=".", command=lambda: self.add_to_field("."), width=5,
                              font=("Times New Roman", 14))
        btn_point.grid(row=5, column=2)
        btn_clear = tk.Button(self.window, text="C", command=lambda: self.clear(), width=5,
                              font=("Times New Roman", 14))
        btn_clear.grid(row=7, column=4)
        btn_minus = tk.Button(self.window, text="-", command=lambda: self.add_to_field("-"), width=5,
                              font=("Times New Roman", 14))
        btn_minus.grid(row=5, column=4)
        btn_plus = tk.Button(self.window, text="+", command=lambda: self.add_to_field("+"), width=5,
                             font=("Times New Roman", 14))
        btn_plus.grid(row=4, column=4)
        btn_multiply = tk.Button(self.window, text="*", command=lambda: self.add_to_field("*"), width=5,
                                 font=("Times New Roman", 14))
        btn_multiply.grid(row=3, column=4)
        btn_del = tk.Button(self.window, text="/", command=lambda: self.add_to_field("/"), width=5,
                            font=("Times New Roman", 14))
        btn_del.grid(row=2, column=4)
        btn_exp = tk.Button(self.window, text="^", command=lambda: self.add_to_field("^"), width=5,
                            font=("Times New Roman", 14))
        btn_exp.grid(row=6, column=4)
        btn_fact = tk.Button(self.window, text="!", command=lambda: self.factorial(), width=5,
                             font=("Times New Roman", 14))
        btn_fact.grid(row=6, column=3)
        btn_mod = tk.Button(self.window, text="%", command=lambda: self.add_to_field("%"), width=5,
                            font=("Times New Roman", 14))
        btn_mod.grid(row=5, column=3)

        btn_stats = tk.Button(self.window, text="Show Stats", command=lambda: self.show_statistics(), width=20,
                              font=("Times New Roman", 14))
        btn_stats.grid(row=9, column=1, columnspan=4)

        self.window.mainloop()

        self.db.conn.close()


if __name__ == "__main__":
    Calculator()
