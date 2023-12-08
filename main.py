import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
# importowanie modułów potrzebnych do działania programów

def update_plot(value):
    # Główna funkcja aktualizująca wykresy reagująca na zmiane wartości na Sliderze
    dc_signal = float(value) * np.ones_like(time)
    # Funkcja prądu stałego niezmienna w czasie
    line.set_ydata(dc_signal)
    ax.relim()
    ax.set_ylim([-10, 10])
    ax.set_xlim([0,5])
    canvas.draw()
    # Wyświetlanie pierwszego wykresu po aktualizacji
    dual_slope = np.zeros_like(time)
    if float(value) > 0:
        indi=1
    else:
        indi=-1
    # Sprawdzanie wartości napięcia stałego i nadanie wartości zmiennej modygikującej napięcie referencyjne.
    Vref = 10 * indi # Napięcie referencyjne
    splitValue = 2.5 # Stały czas pierwszej części ładowania kondensatora
    StopV = splitValue * (float(value)) * indi # Już nie pamiętam co to jest ale jest potrzebne :shrug:

    z = (Vref * splitValue + StopV) / Vref
    x = (z - splitValue) * 400 * indi
    n = (x/400)+splitValue
    m=x/1000*Vref
    # Obliczanie zmiennych potrzebnech w póżniejszych obliczeniach oraz w trakcie ewentualnego rozwoju programu

    for i in range(len(time)):
        if time[i] < splitValue:
            dual_slope[i] = ((-time[i]*float(value))/4)
        else:
            if time[i]<(n):
                 dual_slope[i] = ((-StopV*indi + Vref*(time[i]-splitValue))/4)
            else:
                 dual_slope[i] = 0
                # Funkcje opisujące wygląd lini na wykresie po naładowaniu kondesatora



    line2.set_ydata(dual_slope) # Przypisanie drugiemu wykresowi wartości
    plt.axvline(x=2.5, linestyle='dotted',linewidth= 0.5, color='red') # Linia wskazująca na moment przełączenia z napięcia badanego na referencyjne
    plt.axhline(y=0, color='r', linestyle='dotted' , linewidth= 0.5) # Linia wskazująca wartość y=0 dla łatwaiejszej widoczności pola pod/nad wykresem
    ax2.relim()
    ax2.set_ylim([-10, 10])
    ax2.set_xlim([0, 5])
    canvas2.draw() # Ustalanie limity wykresu drugiego oraz go wywoływanie


    label = tk.Label(app, text="  x = " + "%.0f" % x + "  ",)
    label.after(1, label.destroy)
    label = tk.Label(app, text="  x = " "%.0f" % x + "  ",)
    label1 = tk.Label(app, text="Wartość zmierzonego napięcia ze wzoru to "+ "%.3f" % m)
    label2 = tk.Label(app, text="liczba zliczonych impulsów "+ "%.0f" % x)
    label.grid(row=3, column=3, columnspan=2, padx=10, pady=10)
    label1.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    label2.grid(row=1, column=3, columnspan=2, padx=10, pady=10)
    #ustawianie wszystkich zmiennych tekstów wyświetlających się w oknie Aplikacji

#

# Tworzę tablice od 0 do 5 posiadająca 1000 punktów
time = np.linspace(0, 5, 1000)

# Główne okno aplikacji
app = tk.Tk()
app.title("Praca Inżynierska")

# Pierwsza inicjalizacja oraz ustawianie wyglądu wykresów
fig, ax = plt.subplots()
fig2, ax2 = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=app)
canvas2 = FigureCanvasTkAgg(fig2, master=app)
dc_signal = np.ones_like(time)
line, = ax.plot(time, dc_signal, label='DC Signal')
ax.margins(x=0)
line2, = ax2.plot(time, dc_signal, label='Dual Slope')
plt.tick_params(axis='x', which='both', bottom=True, top=True, labelbottom=False)
plt.xticks(np.arange(0, 5, step=0.05))
plt.margins(x=0)

# tytuły wykresów i osi
ax.set_ylabel('Napięcie')
ax.set_xlabel('Czas')
ax.set_title('Napięcie wejściowe integratora')
ax.set_xticks([])
ax2.set_ylabel('Napięcie')
ax2.set_xlabel('Czas')
ax2.set_title('Napięcie wyjściowe integratora')


# Suwak odpowiedzialny za sterowanie napięcia
# TODO przepisać skale z od -100 do 100 mili voltów
# TODO na wykresie wejściowym dodać napięcie referncyjne o znaku przeciwnym do napięcia wejściowego
amplitude_slider_label = ttk.Label(app, text="Napięcie wejsciowe")
amplitude_slider = ttk.Scale(app, from_=-10, to=10, orient="horizontal", command=update_plot , length=300) # Wygląd i zakres wartości na suwaku
amplitude_slider.set(0)  # Wartość początkowa na suwaku

# Ustawianie lementów UI w siatce
amplitude_slider_label.grid(row=0, column=0, padx=10, pady=10)
amplitude_slider.grid(row=0, column=1, padx=10, pady=10)

# Umiejscowianie wykresów Matplotlib w oknie aplikacji
canvas = FigureCanvasTkAgg(fig, master=app)
# Ustawianie pozycji w oknie aplikacji
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=2, column=0, columnspan=2)
canvas_widget2 = canvas2.get_tk_widget()
canvas_widget2.grid(row=2, column=3, columnspan=2)

# Zapętlanie
app.mainloop()