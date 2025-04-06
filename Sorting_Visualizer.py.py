import tkinter as tk
import random

# Global variables
bars = []
bar_heights = []
sort_generator = None
bar_count = 0

# Swap two bars visually on canvas
def swap_bars(bar1_id, bar2_id):
    x1_start, _, x1_end, _ = canvas.coords(bar1_id)
    x2_start, _, x2_end, _ = canvas.coords(bar2_id)
    canvas.move(bar1_id, x2_start - x1_start, 0)
    canvas.move(bar2_id, x1_end - x2_end, 0)

# Insertion Sort Generator
def insertion_sort_gen():
    global bars, bar_heights
    for i in range(len(bar_heights)):
        current = bar_heights[i]
        current_bar = bars[i]
        j = i
        while j > 0 and bar_heights[j - 1] > current:
            bar_heights[j] = bar_heights[j - 1]
            bars[j], bars[j - 1] = bars[j - 1], bars[j]
            swap_bars(bars[j], bars[j - 1])
            yield
            j -= 1
        bar_heights[j] = current
        bars[j] = current_bar
        swap_bars(bars[j], current_bar)
        yield

# Bubble Sort Generator
def bubble_sort_gen():
    global bars, bar_heights
    for i in range(len(bar_heights) - 1):
        for j in range(len(bar_heights) - i - 1):
            if bar_heights[j] > bar_heights[j + 1]:
                bar_heights[j], bar_heights[j + 1] = bar_heights[j + 1], bar_heights[j]
                bars[j], bars[j + 1] = bars[j + 1], bars[j]
                swap_bars(bars[j + 1], bars[j])
                yield

# Selection Sort Generator
def selection_sort_gen():
    global bars, bar_heights
    for i in range(len(bar_heights)):
        min_idx = i
        for j in range(i + 1, len(bar_heights)):
            if bar_heights[j] < bar_heights[min_idx]:
                min_idx = j
        bar_heights[i], bar_heights[min_idx] = bar_heights[min_idx], bar_heights[i]
        bars[i], bars[min_idx] = bars[min_idx], bars[i]
        swap_bars(bars[min_idx], bars[i])
        yield

# Trigger sort methods
def start_insertion_sort():
    global sort_generator
    sort_generator = insertion_sort_gen()
    run_sort_animation()

def start_selection_sort():
    global sort_generator
    sort_generator = selection_sort_gen()
    run_sort_animation()

def start_bubble_sort():
    global sort_generator
    sort_generator = bubble_sort_gen()
    run_sort_animation()

# Animation runner
def run_sort_animation():
    global sort_generator
    if sort_generator is not None:
        try:
            next(sort_generator)
            window.after(50, run_sort_animation)
        except StopIteration:
            sort_generator = None

# Create bar visuals
def create_bars():
    global bars, bar_heights
    canvas.delete('all')
    bars.clear()
    bar_heights.clear()
    x_start = 5
    x_end = 15
    for _ in range(bar_count):
        y_position = random.randint(20, 360)
        bar = canvas.create_rectangle(x_start, y_position, x_end, 365, fill='yellow')
        bars.append(bar)
        x_start += 10
        x_end += 10

    for bar in bars:
        y1, y2 = canvas.coords(bar)[1], canvas.coords(bar)[3]
        bar_heights.append(y2 - y1)

    for i, height in enumerate(bar_heights):
        if height == min(bar_heights):
            canvas.itemconfig(bars[i], fill='red')
        elif height == max(bar_heights):
            canvas.itemconfig(bars[i], fill='black')

# Input from user
def handle_input_submit():
    global bar_count
    try:
        bar_count = int(entry_box.get())
        if bar_count <= 0:
            raise ValueError
        input_window.destroy()
        launch_sorting_gui()
    except ValueError:
        entry_box.delete(0, tk.END)
        entry_box.insert(0, "Enter a valid positive number")

# Sorting visualizer UI
def launch_sorting_gui():
    global canvas, window
    window = tk.Tk()
    window.title("Sorting Algorithm Visualizer")
    window.geometry("1000x450")

    canvas = tk.Canvas(window, width=1000, height=400)
    canvas.grid(column=0, row=0, columnspan=50)

    tk.Button(window, text="Insertion Sort", command=start_insertion_sort).grid(column=1, row=1)
    tk.Button(window, text="Selection Sort", command=start_selection_sort).grid(column=2, row=1)
    tk.Button(window, text="Bubble Sort", command=start_bubble_sort).grid(column=3, row=1)
    tk.Button(window, text="Shuffle", command=create_bars).grid(column=0, row=1)

    create_bars()
    window.mainloop()

# Intro window
def show_intro_screen():
    intro_win = tk.Tk()
    intro_win.geometry("700x350")
    intro_win.title("Welcome to Sorting Visualizer")

    tk.Label(intro_win, text="SORTING ALGORITHM VISUALIZER", font=("Courier", 14)).pack(pady=10)

    about_text = tk.Text(intro_win, height=5, width=52, bg="lightyellow")
    about_text.insert(tk.END, """MINI PROJECT 
Developed by:
Yaswanth [or your team name]""")
    about_text.pack()

    tk.Button(intro_win, text="NEXT", command=intro_win.destroy).pack(pady=10)
    intro_win.mainloop()

# Prompt for number of bars
def show_input_prompt():
    global entry_box, input_window
    input_window = tk.Tk()
    input_window.geometry("400x200")
    input_window.title("Bar Count Input")

    tk.Label(input_window, text="Enter number of bars to display:").pack(pady=10)
    entry_box = tk.Entry(input_window, width=30)
    entry_box.pack()
    tk.Button(input_window, text="Submit", command=handle_input_submit).pack(pady=10)
    input_window.mainloop()

# Start the program
show_intro_screen()
show_input_prompt()
