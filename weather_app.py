''' The goal of this project is to create a weather app that shows the current weather conditions and forecast for a specific location.

Here are the steps you can take to create this project:

    Use the requests library to make an API call to a weather service (e.g. OpenWeatherMap) to retrieve the weather data for a specific location.

    Use the json library to parse the JSON data returned by the API call.

    Use the tk library to create a GUI for the app, including widgets such as labels, buttons and text boxes.

    Use the Pillow library to display the weather icons.

    Use the datetime library to display the current time and date. '''

import requests
import json
import tkinter as tk
from PIL import Image, ImageTk
import datetime

def getWeather():
    api = requests.get('https://api.open-meteo.com/v1/forecast?latitude=52.5244&longitude=13.4105&hourly=temperature_2m,precipitation_probability,uv_index,is_day').json()
    hours = api['hourly']['time']
    temp = api['hourly']['temperature_2m']
    prec = api['hourly']['precipitation_probability']
    uv = api['hourly']['uv_index']
    is_day = api['hourly']['is_day']
    forecast = []
    
    for i in range(len(hours)):
        if (i > 1 and forecast[-1][0] == "23:00") or i == 0:
            forecast.append([f"{hours[i][-5:]}\n{hours[i][:10]}", temp[i], prec[i], uv[i], is_day[i]])
        else:
            forecast.append([hours[i][-5:], temp[i], prec[i], uv[i], is_day[i]])
    return(forecast)


def makeUI(forecast):
    
    def on_canvas_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    root = tk.Tk()
    root.title("Weather App")
    root.geometry("800x600")
    location = tk.Label(root, text = "Berlin, DE", padx = 10, pady = 10)
    current_time = tk.Label(root, text = datetime.datetime.now().strftime('%c'), padx = 10, pady = 10)

    location.pack()
    current_time.pack()

    # Create a Canvas as a container
    canvas = tk.Canvas(root)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a Scrollbar and link it to the Canvas
    scrollbar_frame = tk.Frame(root)
    scrollbar_frame.place(relx=0.5, rely=1, relwidth=1, anchor=tk.S)

    scrollbar = tk.Scrollbar(scrollbar_frame, command=canvas.xview, orient=tk.HORIZONTAL, width=10,
                            highlightthickness=0, troughcolor="lightgray", borderwidth=2)
    scrollbar.pack(fill=tk.X, expand=True)

    # Configure the Canvas to use the Scrollbar
    canvas.configure(xscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", on_canvas_configure)

    # Create a Frame inside the Canvas to place your widgets
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    row_titles_frame = tk.Frame(root)
    row_titles_frame.place(x=0, y=325)

    row_titles = ['Temp (C)', 'Prec. (%)', 'UV Index']
    for i, title in enumerate(row_titles):
        tk.Label(row_titles_frame, text=title).grid(row=i, column=0, padx=10, pady=10)

    # Make icons workable in TK

    clear_day = ImageTk.PhotoImage(Image.open("svg/01d.png").convert("RGBA"))
    clear_night = ImageTk.PhotoImage(Image.open("svg/01n.png").convert("RGBA"))
    cloudy_day = ImageTk.PhotoImage(Image.open("svg/02d.png").convert("RGBA"))
    cloudy_night = ImageTk.PhotoImage(Image.open("svg/02n.png").convert("RGBA"))
    rainy_day = ImageTk.PhotoImage(Image.open("svg/03d.png").convert("RGBA"))
    rainy_night = ImageTk.PhotoImage(Image.open("svg/03n.png").convert("RGBA"))
        
    i = 1
    for elem in forecast:
        time = tk.Label(frame, text = elem[0]).grid(row = 4, column = i, padx = 10, pady = 10)
        temp = tk.Label(frame, text = elem[1]).grid(row = 1, column = i, padx = 10, pady = 10)
        prec = tk.Label(frame, text = elem[2]).grid(row = 2, column = i, padx = 10, pady = 10)
        uv = tk.Label(frame, text = elem[3]).grid(row = 3, column = i, padx = 10, pady = 10)
        
        if elem[4] == 1:
            if elem[2] < 25: 
                icon = tk.Label(frame, image = clear_day).grid(row = 0, column = i, padx = 10, pady = 20)
            elif 25 < elem[2] < 75:
                icon = tk.Label(frame, image = cloudy_day).grid(row = 0, column = i, padx = 10, pady = 10)
            else:
                icon = tk.Label(frame, image = rainy_day).grid(row = 0, column = i, padx = 10, pady = 10)
        else:
            if elem[2] < 25: 
                icon = tk.Label(frame, image = clear_night).grid(row = 0, column = i, padx = 10, pady = 10)
            elif 25 < elem[2] < 75:
                icon = tk.Label(frame, image = cloudy_night).grid(row = 0, column = i, padx = 10, pady = 10)
            else:
                icon = tk.Label(frame, image = rainy_night).grid(row = 0, column = i, padx = 10, pady = 10)
        i += 1
        if i > 120: 
            break


    
    root.mainloop()

makeUI(getWeather())