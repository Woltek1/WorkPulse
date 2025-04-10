from customtkinter import *
from CTkTable import *
import json
import webbrowser
from PIL import Image

def run_app():
    # App setup
    app = CTk()
    app.geometry('1280x720')
    app.title('WorkPulse - Time Tracker')
    app.iconbitmap('icon.ico')
    github = Image.open('github.png')

    def format_time(seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f'{hours}h : {minutes}m : {secs}s'

    def to_seconds(time_str):
        final_time = time_str.split(' : ')
        hours = int(final_time[0].replace('h', ''))
        minutes = int(final_time[1].replace('m', ''))
        seconds = int(final_time[2].replace('s', ''))
        return hours * 3600 + minutes * 60 + seconds

    def link():
        webbrowser.open('https://github.com/Woltek1')


    label = CTkLabel(app, text='Dashboard', font=('Roboto', 32), text_color='#fafcf9')
    label.pack(pady=10)

    with open('timer_data.json', 'r') as f:
        data = json.load(f)

    arr = []
    for i, (app_name, time) in enumerate(data.items()):
        formated_time = format_time(time)
        arr.append([app_name, formated_time])
    arr_sorted = sorted(arr, key=lambda x: to_seconds(x[1]), reverse=True)

    frame = CTkScrollableFrame(app, 500, 500, fg_color='transparent')
    frame.pack()

    table = CTkTable(frame, values=[['Application', 'Time spent']] + arr_sorted, font=('Roboto', 24))
    table.pack(fill='both', expand=True)

    github_image = CTkImage(light_image=github, dark_image=github, size=(32, 32))
    button = CTkButton(app, text='My Github', image=github_image, fg_color='#163832', hover_color='#235347', command=link)
    button.pack(side='bottom', pady=10)

    app.mainloop()

run_app()