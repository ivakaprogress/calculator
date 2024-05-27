import sqlite3
import os
import math
import tkinter as tk
from tkinter import messagebox


conn = sqlite3.connect('calculator.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS operations (
                id INTEGER PRIMARY KEY,
                operation TEXT,
                operands TEXT,
                result TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )''')
conn.commit()

field_text = ""
factorial_expression = ""


def add_to_field(entry):
    global field_text
    field_text += str(entry)
    field.delete("1.0", "end")
    field.insert("1.0", field_text)


def log_operation(operation, operands, result):
    c.execute("INSERT INTO operations (operation, operands, result) VALUES (?, ?, ?)",
              (operation, operands, result))
    conn.commit()


def factorial():
    global field_text, factorial_expression
    factorial_expression = field_text
    field_text += "!"
    field.delete("1.0", "end")
    field.insert("1.0", field_text)


def calculate():
    global field_text, factorial_expression
    expression = field_text
    try:
        expression = expression.replace("[", "(").replace("]", ")")
        if "(" in expression or ")" in expression:
            result = str(eval(expression))
            log_operation('calculation', expression, result)
        elif "+" in expression:
            parts = expression.split("+", 1)
            result = str(eval(parts[0]) + eval(parts[1]))
            log_operation('addition', parts[0] + ',' + parts[1], result)
        elif "-" in expression:
            parts = expression.split("-", 1)
            result = str(eval(parts[0]) - eval(parts[1]))
            log_operation('subtraction', parts[0] + ',' + parts[1], result)
        elif "*" in expression:
            parts = expression.split("*", 1)
            result = str(eval(parts[0]) * eval(parts[1]))
            log_operation('multiplication', parts[0] + ',' + parts[1], result)
        elif "/" in expression:
            parts = expression.split("/", 1)
            result = str(eval(parts[0]) / eval(parts[1]))
            log_operation('division', parts[0] + ',' + parts[1], result)
        elif "%" in expression:
            parts = expression.split("%", 1)
            result = str(eval(parts[0]) * eval(parts[1]) / 100)
            log_operation('percentage', parts[0] + ',' + parts[1], result)
        elif "!" in expression:
            # Handle factorial specifically
            base = expression.replace("!", "")
            result = str(math.factorial(int(base)))
            log_operation('factorial', base, result)
        elif "^" in expression:
            parts = expression.split("^", 1)
            result = str(eval(parts[0]) ** eval(parts[1]))
            log_operation('exponentiation', parts[0] + "," + parts[1], result)
        else:
            result = str(eval(expression))
            log_operation('calculation', expression, result)

        field.delete("1.0", "end")
        field.insert("1.0", result)
        field_text = result
        factorial_expression = ""

    except Exception as e:
        error_message = str(e)
        log_operation('error', expression, error_message)
        field.delete("1.0", "end")
        field.insert("1.0", "Error: " + error_message)
        field_text = ""
        factorial_expression = ""
        messagebox.showerror('Error', str(e))


def clear():
    global field_text, factorial_expression
    field_text = ""
    factorial_expression = ""
    field.delete("1.0", "end")


stats_window = None


def show_statistics():
    global stats_window
    if stats_window:
        stats_window.destroy()

    stats_window = tk.Toplevel(window)
    stats_window.title("Statistics")
    stats_window.geometry("400x400")

    total_additions = c.execute("SELECT COUNT(*) FROM operations WHERE operation = 'addition'").fetchone()[0]
    total_subtractions = c.execute("SELECT COUNT(*) FROM operations WHERE operation = 'subtraction'").fetchone()[0]
    total_multiplications = c.execute("SELECT COUNT(*) FROM operations WHERE operation = 'multiplication'").fetchone()[0]
    total_divisions = c.execute("SELECT COUNT(*) FROM operations WHERE operation = 'division'").fetchone()[0]

    total_composite = c.execute("SELECT COUNT(*) FROM operations WHERE operation = 'calculation'").fetchone()[0]
    total_to_power = c.execute("SELECT COUNT(*) FROM operations WHERE operation = 'exponentiation'").fetchone()[0]
    total_percentage = c.execute("SELECT COUNT(*) FROM operations WHERE operation = 'percentage'").fetchone()[0]
    total_factorial = c.execute("SELECT COUNT(*) FROM operations WHERE operation = 'factorial'").fetchone()[0]

    total_elementary_operations = total_additions + total_subtractions + total_multiplications + total_divisions
    total_sum_other_operations = total_to_power + total_percentage + total_factorial + total_composite
    total_sum_of_all_operations = total_elementary_operations + total_sum_other_operations

    avg_elementary_operations = total_elementary_operations / total_sum_of_all_operations if total_sum_of_all_operations > 0 else 0

    stats = f"""
        Total Additions:          {total_additions}
        Total Subtractions:       {total_subtractions}
        Total Multiplications:    {total_multiplications}
        Total Divisions:          {total_divisions}

    -------------------------------------

        Total Factorial:         {total_factorial}
        Total Exponential:       {total_to_power}
        Total Percentage:        {total_percentage}
        Total Composite:         {total_composite}

    --------------------------------------
        Average Elementary Operations: {avg_elementary_operations:.2f}
    """
    stats_label = tk.Label(stats_window, text=stats, font=("Times New Roman", 14))
    stats_label.pack()


window = tk.Tk()
window.geometry("300x400")

field = tk.Text(window, height=2, width=21, font=("Times New Roman", 20))
field.grid(row=1, column=1, columnspan=4)

btn_0 = tk.Button(window, text="0", command=lambda: add_to_field(0), width=5, font=("Times New Roman", 14))
btn_0.grid(row=5, column=1)
btn_1 = tk.Button(window, text="1", command=lambda: add_to_field(1), width=5, font=("Times New Roman", 14))
btn_1.grid(row=4, column=1)
btn_2 = tk.Button(window, text="2", command=lambda: add_to_field(2), width=5, font=("Times New Roman", 14))
btn_2.grid(row=4, column=2)
btn_3 = tk.Button(window, text="3", command=lambda: add_to_field(3), width=5, font=("Times New Roman", 14))
btn_3.grid(row=4, column=3)
btn_4 = tk.Button(window, text="4", command=lambda: add_to_field(4), width=5, font=("Times New Roman", 14))
btn_4.grid(row=3, column=1)
btn_5 = tk.Button(window, text="5", command=lambda: add_to_field(5), width=5, font=("Times New Roman", 14))
btn_5.grid(row=3, column=2)
btn_6 = tk.Button(window, text="6", command=lambda: add_to_field(6), width=5, font=("Times New Roman", 14))
btn_6.grid(row=3, column=3)
btn_7 = tk.Button(window, text="7", command=lambda: add_to_field(7), width=5, font=("Times New Roman", 14))
btn_7.grid(row=2, column=1)
btn_8 = tk.Button(window, text="8", command=lambda: add_to_field(8), width=5, font=("Times New Roman", 14))
btn_8.grid(row=2, column=2)
btn_9 = tk.Button(window, text="9", command=lambda: add_to_field(9), width=5, font=("Times New Roman", 14))
btn_9.grid(row=2, column=3)
btn_l_par = tk.Button(window, text="(", command=lambda: add_to_field("("), width=5, font=("Times New Roman", 14))
btn_l_par.grid(row=6, column=1)

btn_l_bra = tk.Button(window, text="[", command=lambda: add_to_field("("), width=5, font=("Times New Roman", 14))
btn_l_bra.grid(row=7,column=1)

btn_r_bra = tk.Button(window, text="]", command=lambda: add_to_field("]"), width=5, font=("Times New Roman", 14))
btn_r_bra.grid(row=7, column=2)

btn_r_par = tk.Button(window, text=")", command=lambda: add_to_field(")"), width=5, font=("Times New Roman", 14))
btn_r_par.grid(row=6, column=2)
btn_equals = tk.Button(window, text="=", command=lambda: calculate(), width=10, font=("Times New Roman", 14))
btn_equals.grid(row=8, column=2, columnspan=2)
btn_point = tk.Button(window, text=".", command=lambda: add_to_field("."), width=5, font=("Times New Roman", 14))
btn_point.grid(row=5, column=2)
btn_clear = tk.Button(window, text="C", command=lambda: clear(), width=5, font=("Times New Roman", 14))
btn_clear.grid(row=7, column=4)
btn_minus = tk.Button(window, text="-", command=lambda: add_to_field("-"), width=5, font=("Times New Roman", 14))
btn_minus.grid(row=5, column=4)
btn_plus = tk.Button(window, text="+", command=lambda: add_to_field("+"), width=5, font=("Times New Roman", 14))
btn_plus.grid(row=4, column=4)
btn_multiply = tk.Button(window, text="*", command=lambda: add_to_field("*"), width=5, font=("Times New Roman", 14))
btn_multiply.grid(row=3, column=4)
btn_del = tk.Button(window, text="/", command=lambda: add_to_field("/"), width=5, font=("Times New Roman", 14))
btn_del.grid(row=2, column=4)
btn_exp = tk.Button(window, text="^", command=lambda: add_to_field("^"), width=5, font=("Times New Roman", 14))
btn_exp.grid(row=6, column=4)
btn_fact = tk.Button(window, text="!", command=lambda: factorial(), width=5, font=("Times New Roman", 14))
btn_fact.grid(row=6, column=3)
btn_mod = tk.Button(window, text="%", command=lambda: add_to_field("%"), width=5, font=("Times New Roman", 14))
btn_mod.grid(row=5, column=3)

btn_stats = tk.Button(window, text="Show Stats", command=lambda: show_statistics(), width=20,
                      font=("Times New Roman", 14))
btn_stats.grid(row=9, column=1, columnspan=4)

window.mainloop()

# Close the database connection when done
conn.close()
