import threading
import logging
import os
import time
import PySimpleGUI as sg

layout = [[sg.Text('This is a very basic PySimpleGUI layout')],
          [sg.Image('C:\\Users\\antoniu\\Downloads\\cr.gif', key='a')]]

window = sg.Window('My new window', layout, grab_anywhere=True)

while True:
    window['a'].update_animation('C:\\Users\\antoniu\\Downloads\\cr.gif', 50)


window.close()