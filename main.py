
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


def update_plot(value):
    dc_signal = float(value) * np.ones_like(time)
    line.set_ydata(dc_signal)
    ax.relim()
    ax.set_ylim([-10, 10])
    ax.set_xlim([0,5])
    canvas.draw()
    dual_slope = np.zeros_like(time)
    if float(value) > 0:
        indi=1
    else:
        indi=-1
    for i in range(len(time)):
        Vref = 10*indi
        splitValue = 2.5
        StopV= splitValue*(float(value))*indi
        if time[i] < splitValue:
            dual_slope[i] = ((-time[i]*float(value))/4)
        else:
            dual_slope[i] = ((-StopV*indi + Vref*(time[i]-splitValue))/4)

    z = (Vref * splitValue + StopV) / Vref
    x = (z - splitValue) * 400 * indi
    n = (x/400)+splitValue
    m=x/1000*Vref
#TODO co ustalam tutaj
    line2.set_ydata(dual_slope)
    ax2.relim()
    ax2.set_ylim([-10, 10])
    ax2.set_xlim([0, 5])
    canvas2.draw()
#TODO Komentarz co tutaj się dzieje
    label = tk.Label(app, text="  x = " + "%.0f" % x + "  ",)
    label.after(1, label.destroy)
    label = tk.Label(app, text="  x = " "%.0f" % x + "  ",)
    label.grid(row=2, column=3, columnspan=2, padx=10, pady=10)

    label1 = tk.Label(app, text="wartość zmierzonego napięcia ze wzoru to "+ "%.3f" % m)
    label1.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
# Create a time array from 0 to 1 with sufficient points
time = np.linspace(0, 5, 1000)

#i want to get rid of the X axis numbers
# Create the main application window
app = tk.Tk()
app.title("DC Signal Plotter")

# Create a figure and axis for the plot
fig, ax = plt.subplots()
fig2, ax2 = plt.subplots()
dc_signal = np.ones_like(time)
line, = ax.plot(time, dc_signal, label='DC Signal')
ax.margins(x=0)
line2, = ax2.plot(time, dc_signal, label='Dual Slope')
plt.tick_params(axis='x', which='both', bottom=True, top=True, labelbottom=False)
plt.xticks(np.arange(0, 5, step=0.05))
plt.margins(x=0)

# Add labels and title
ax.set_ylabel('Voltage')
ax.set_title('DC Signal')
ax2.set_ylabel('Voltage')
ax2.set_title('Dual Slope')


# Add a slider to control the DC signal amplitude
amplitude_slider_label = ttk.Label(app, text="DC Signal Amplitude:")
amplitude_slider = ttk.Scale(app, from_=-10, to=10, orient="horizontal", command=update_plot)
amplitude_slider.set(0)  # Initial amplitude value

# Arrange widgets using grid layout
amplitude_slider_label.grid(row=0, column=0, padx=10, pady=10)
amplitude_slider.grid(row=0, column=1, padx=10, pady=10)

# Embed the Matplotlib plot in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=app)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=2, column=0, columnspan=2)
canvas2 = FigureCanvasTkAgg(fig2, master=app)
canvas_widget2 = canvas2.get_tk_widget()
canvas_widget2.grid(row=2, column=3, columnspan=2)

# Run the Tkinter event loop
app.mainloop()



