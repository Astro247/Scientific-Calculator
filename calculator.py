from tkinter import *
from math import *
from calculator_lists import *
import re

expression_text = ""
hidden_expression_text = ""

def constants_description():
    text="""π (Pi) = Ratio of a circle's circumference to its diameter.              
          τ (Tau) = Represents a full turn in trigonometry.                            
          δ (Gauss's Delta Constant) = Appears in probability and normal distribution. 
          K (Catalan's Constant) = Found in trigonometric series and combinatorics.    
          φ (Golden Ratio) = Ratio found in nature and art.                            
          σ (Silver Ratio) = Similar to the golden ratio, based on Pell numbers.       
          μ (Lévy's Constant) = Used in stochastic process theory.                     
          ψ (Ramanujan-Soldner Constant) = Zero of the logarithmic integral function.  
          e (Euler's Number) = Base of natural logarithms and exponential growth.
          λ (Golomb-Dickman Constant) = Related to number theory and random algorithms.
          F (Fibonacci Growth Constant) = Closely linked to the golden ratio and exponential growth.
          α (Fine-Structure Constant) = Appears in quantum physics, but has mathematical roots.
          Ω (Chaitin’s Constant) = Related to information theory and randomness.
          Λ (Liouville's Constant) = Used in transcendental number theory.
          β (Twin Prime Constant) = Appears in the distribution of twin primes.
          ρ (Viswanath’s Constant) = Associated with the average growth of random Fibonacci sequences.  
          """
    return text


def move_cursor_left(expression_entry):
    position = expression_entry.index(INSERT)
    if position > 0:
        expression_entry.icursor(position - 1)


def move_cursor_right(expression_entry):
    position = expression_entry.index(INSERT)
    if position < len(expression_entry.get()):
        expression_entry.icursor(position + 1)


def block_typing(event):
    return "break"
    

def on_press_button(s, expression_entry):
    global expression_text, hidden_expression_text

    if str(expression_entry.get()) == "ERROR":
        cancel_everything(expression_entry)

    position = expression_entry.index(INSERT)
    expression_text = str(expression_text) + str(s)
    hidden_expression_text = str(hidden_expression_text) + str(s)
    expression_entry.insert(position, s)


def on_press_operators(s, expression_entry):
    global expression_text, hidden_expression_text

    if str(expression_entry.get()) == "ERROR":
        cancel_everything(expression_entry)

    position = expression_entry.index(INSERT)
    expression_entry.insert(position, OPERATORS_DICTIONARY[str(s)])
    expression_text = str(expression_text) + OPERATORS_DICTIONARY[str(s)]
    hidden_expression_text = expression_text


def cancel_one_element(expression_entry):
    if str(expression_entry.get()) == "ERROR":
        cancel_everything(expression_entry)

    global expression_text, hidden_expression_text
    position = expression_entry.index(INSERT)
    if position>0:
        expression_entry.delete(position-1, position)
    expression_text = expression_entry.get()
    hidden_expression_text = expression_entry.get()


def cancel_everything(expression_entry):
    global expression_text, hidden_expression_text
    expression_entry.delete(0, END)
    hidden_expression_text = expression_text = ""


def convert_constants():
    global hidden_expression_text
    for symbol in CONSTANTS_DICTIONARY:
        if symbol in hidden_expression_text:
            hidden_expression_text = hidden_expression_text.replace(symbol, CONSTANTS_DICTIONARY[str(symbol)])


def convert_operators(expression_entry):
    global hidden_expression_text
    hidden_expression_text = expression_entry.get()
    
    hidden_expression_text = hidden_expression_text.replace("÷", "/")
    hidden_expression_text = hidden_expression_text.replace("•", "*")
    hidden_expression_text = hidden_expression_text.replace("^", "**")
    hidden_expression_text = hidden_expression_text.replace("log", "log10")
    hidden_expression_text = hidden_expression_text.replace("ln", "log")
    hidden_expression_text = re.sub(r'\|([^|]+)\|', r'fabs(\1)', hidden_expression_text) #valore assoluto
    hidden_expression_text = hidden_expression_text.replace("√", "sqrt")
    hidden_expression_text = hidden_expression_text.replace("!", "factorial")


def solve_expression(expression_entry):
    global expression_text, hidden_expression_text
    convert_operators(expression_entry)
    convert_constants()
    try:
        result = eval(str(hidden_expression_text))
        hidden_expression_text = str(result)
        expression_text = str(result)
        expression_entry.delete(0, END)
        expression_entry.insert(0, expression_text)

    except(SyntaxError,ZeroDivisionError,ValueError):
        expression_entry.delete(0, END)
        hidden_expression_text = ""
        expression_text = ""
        expression_entry.insert(0, "ERROR")


def main():
    main_window = Tk()
    main_window.config(bg="#cccbca")
    main_window.title("Astro's Scientific Calculator")

    widgets_frame = Frame(main_window, bg="#cccbca")
    widgets_frame.pack(expand=True)

    expression_area_frame = Frame(widgets_frame, height=50, width=1000, bg="#cccbca")
    expression_area_frame.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

    left_arrow_button = Button(expression_area_frame, text="←", font=("Arial", 20, "bold"), bg="#a3a19d", activebackground="#666564")
    left_arrow_button.config(command=lambda:move_cursor_left(expression_entry))
    left_arrow_button.pack(padx=5, side=LEFT)

    expression_entry = Entry(expression_area_frame, font=("Arial", 20, "bold"), relief=RIDGE, bd=5, width=50, bg="#a3a19d")
    expression_entry.pack(padx=5, side=LEFT)
    expression_entry.bind("<Key>", block_typing)    

    right_arrow_button = Button(expression_area_frame, text="→", font=("Arial", 20, "bold"), bg="#a3a19d", activebackground="#666564")
    right_arrow_button.config(command=lambda:move_cursor_right(expression_entry))
    right_arrow_button.pack(padx=5, side=LEFT)

    constants_frame = Frame(widgets_frame, width=400, height=400, bg="gray", relief="solid", bd=5)
    constants_frame.grid(row=3, column=1, padx=5, pady=5)

    numPad_frame = Frame(widgets_frame, width=400, height=400, bg="gray", relief="solid", bd=5)
    numPad_frame.grid(row=3, column=2, padx=5, pady=5)

    operators_frame = Frame(widgets_frame, width=400, height=400, bg="gray", relief="solid", bd=5)
    operators_frame.grid(row=3, column=3, padx=5, pady=5)

    print_constants = constants_description()
    descriptionConstants_label = Label(widgets_frame, text=print_constants, font=("Arial", 13, "bold"), bg="#98b391", relief="solid", bd=5, anchor="w")
    descriptionConstants_label.grid(row=4, column=1, columnspan=3)

    for (word,row,column) in LABELS_LIST:
        title_label = Label(widgets_frame, text=word, font=("Arial", 20, "bold"), bg="gray", relief=RAISED, bd=5)
        title_label.grid(row=row, column=column)

    for (symbol, row, column) in NUMPAD_BUTTONS_LIST:
        numPad_button = Button(numPad_frame, text=symbol, width=5, height=2, font=("Arial", 20, "bold"), bg="#c2c2be", activebackground="#a3a3a2")
        
        if symbol == "⌫":
            numPad_button.config(command=lambda: cancel_one_element(expression_entry))
        elif symbol == "C":
            numPad_button.config(command=lambda: cancel_everything(expression_entry))
        elif symbol == "=":
            numPad_button.config(command=lambda: solve_expression(expression_entry))
        else:
            numPad_button.config(command=lambda s=symbol:on_press_button(s, expression_entry))
        
        numPad_button.grid(row=row, column=column, padx=5, pady=5) 

    for (symbol, row, column) in CONSTANTS_BUTTONS_LIST:
        constant_button = Button(constants_frame, text=symbol, width=5, height=2, font=("Arial", 20, "bold"), bg="#c2c2be", activebackground="#a3a3a2")
        constant_button.config(command=lambda s=symbol:on_press_button(s, expression_entry))
        constant_button.grid(row=row, column=column, padx=5, pady=5) 

    for (symbol, row, column) in OPERATORS_BUTTONS_LIST:
        operator_button = Button(operators_frame, text=symbol, width=5, height=2, font=("Arial", 20, "bold"), bg="#c2c2be", activebackground="#a3a3a2")
        operator_button.config(command=lambda s=symbol:on_press_operators(s, expression_entry))
        operator_button.grid(row=row, column=column, padx=5, pady=5)
    
    main_window.mainloop()

main()