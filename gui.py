import copy
import stuffme as be
import math
from os.path import exists
import PySimpleGUI as sg
from tkinter import font as f
from PIL import Image
from io import BytesIO as BIO
import pickle
import threading as mt
import queue as q
font = ('Arial', 12)
convo = None
#text display and input size
DIsize = 240
messages = []
white = '#FFFFFF'
global cursor
cursor = 0
filetype = [("Image", ".png .jpg .jpeg .gif")]
username = input()
currentFolder = '155251522593'
gifsLoaded = []
global window
##################### wahoo columsn are scrollable
#appends a multiline to the column(heaven)
#rightclickmenu = 

#line hieght is 19
#multilines are appended to the messages list with the key of their position then window refresehs with the updated messages list
def displaymessage(offset = 0):
    gifsLoaded.clear()
    selmessage = []
    keys = []
    for x in range(len(messages)-(1+offset), len(messages)-(20+offset), -1):
        if x >= 0:
            selmessage.append(messages[x])
            keys.append(('a' + str(x)))
    refreshWindow(selmessage)
    a = 0
    for key in keys:
        length = window['-MESSAGES-'].get_size()[0]
        message_num = messages[int(key[1: ])]
        if str(message_num[0]).find('Multiline') != -1:
            textlength = arial.measure(window[key].get())
            height = math.ceil((textlength/length))+1
            width = math.ceil(length/arial.measure('a'))
            window[key].set_size((width, height))
        else:
            maxsize_x = window['-MESSAGES-'].get_size()[0]
            maxsize_y = math.floor(window['-MESSAGES-'].get_size()[1]/4)
            imageSize = window[key].get_size()
            maximageXmult = maxsize_x/imageSize[0]
            if imageSize[0] <= maxsize_x and imageSize[1] <= maxsize_y:
                return
            elif imageSize[1] * maximageXmult <= maxsize_y:
                imageX = imageSize[0] * maximageXmult
                imageY = imageSize[1] * maximageXmult
                window[key].set_size((imageX, imageY))
            else:
                maximageYmult = maxsize_y/imageSize[1]
                imageX = imageSize[0] * maximageYmult
                imageY = imageSize[1] * maximageYmult
                window[key].set_size((imageX, imageY))
        a += 1

'''def loadimage(bytes):
    image = Image.open(bytes)
    maxsize_x = window['-MESSAGES-'].get_size()[0]
    maxsize_y = math.floor(window['-MESSAGES-'].get_size()[1]/4)
    imageSize = image.size
    maximageXmult = maxsize_x/imageSize[0]
    if imageSize[0] <= maxsize_x and imageSize[1] <= maxsize_y:
        return [sg.Image(data =bytes, metadata= bytes, right_click_menu=image_rightclick,k = 'a' + str(len(messages)))]
    elif imageSize[1] * maximageXmult <= maxsize_y:
        imageX = imageSize[0] * maximageXmult
        imageY = imageSize[1] * maximageXmult
        image = image.resize((math.floor(imageX, imageY)))
        return [sg.Image(data = bytes, metadata= bytes, right_click_menu=image_rightclick, k = 'a' + str(len(messages)))]
    else:
        maximageYmult = maxsize_y/imageSize[1]
        imageX = imageSize[0] * maximageYmult
        imageY = imageSize[1] * maximageYmult
        image = image.resize((math.floor(imageX), math.floor(imageY)))
        return [sg.Image(data = bytes, metadata= bytes, right_click_menu=image_rightclick, k = 'a' + str(len(messages)))]'''

def createImage(source):
    key = 'a' + str(len(messages))
    image_rightclick = ['Right', ['Inflate::' + key], 'Copy::' + key]
    image = Image.open(source)
    newImage = image
    maxsize_x = window['-MESSAGES-'].get_size()[0]
    maxsize_y = math.floor(window['-MESSAGES-'].get_size()[1]/4)
    i = 0
    for size in maxsize_x, maxsize_y:
        if image.size[i] >= size:
            proportion = size/image.size[i]
            resized = [math.floor(Size * proportion) for Size in image.size]
            newImage = image.resize(size = (resized[0], resized[1]))
        i+=1
    bio = BIO()
    if str(source).find('.gif') == -1:
        newImage.save(bio, format="PNG")
    else:
        newImage.save(bio, format = 'GIF')
    return [sg.Image(data = bio.getvalue(), metadata= source, right_click_menu= image_rightclick, k = key)]

def loadmessages(when):
    #load messages takes as arguments: c for current, b for backwards and n for next
    global cursor
    if when == 'c':
        displaymessage()
    if when == 'b':
        if cursor - 20 >= 0:
            cursor -= 20
            displaymessage(cursor)
    if when == 'n':
        if cursor < len(messages)-1:
            cursor+=20
            displaymessage(cursor)

def createText(text):
    multiline = sg.Multiline(text, auto_size_text=False, disabled=True, no_scrollbar=True, key = ('a' + str(len(messages))), border_width=0, 
    background_color='white', expand_x=True, auto_refresh=True)
    return [multiline]


def make_window(size, location, messDisplay):
    convos = []
    for elem in convo:
        print(elem)
        convos.append(elem)
    tocenter = [[sg.Text('', size = (0,0), expand_x=True, pad= (0,0),key = '-EXPAND1-'), sg.Button('Invite', k = 'invite'),sg.Input(size = (0,0), k = 'ImageLoad', visible=False), sg.FileBrowse('Import', file_types=filetype, k = 'Import'), sg.Button('<', key = 'back') ,sg.Button('>', k = 'next')], 
            [sg.Column(messDisplay, scrollable=True, vertical_scroll_only=True, size=(DIsize, 60), expand_x=True, expand_y=True, background_color='white', key='-MESSAGES-')],
            [sg.Multiline(key = '-INPUT-', do_not_clear=True, size= (DIsize, 3), enter_submits=True, no_scrollbar=True, auto_size_text=True, font = font, expand_x=True, focus=True), sg.Button("ok", key='-SEND-', bind_return_key=True, visible=False, size=(0,0))]]

    chats = [[sg.Button('REFRESH'), sg.Text(size=(0,0), expand_x=True, k = '-EXPAND1-'), sg.Button('Create', k = 'create'), sg.Button('Add', k='add') ,sg.Button('Open')],
            [sg.Listbox(convos, size=(24, 40), font=font, expand_y=True, expand_x=True, k = 'Chats')]]

    layout = [[sg.Column(chats, expand_x=False, justification='', key = '-EXPAND2-', expand_y=True), sg.Col(tocenter, element_justification='left', expand_x=True, key="-MAIN-")]]
    return sg.Window('My Application', layout, finalize=True, resizable=True, font = font, size=size, location=location, alpha_channel=1)

def refreshWindow(messages):
    global window
    message = copy.deepcopy(messages)
    windowsize = window.size
    windowlocation = window.CurrentLocation(more_accurate=True)
    newwindow = make_window(windowsize, windowlocation, message)
    newwindow.set_min_size((800, 623))
    newwindow["-MAIN-"].expand(True, True, True)
    newwindow["-EXPAND2-"].expand(True, True, True)
    newwindow['-EXPAND1-'].expand(True, False, False)
    if windowsize == (2560, 1377) and windowlocation == (0, 0): newwindow.maximize()
    window.close()
    newwindow.alpha_channel = 1
    window = newwindow

def createWindowImage(key):
    print(key)
    source = window[key].metadata
    image = Image.open(source)
    bio = BIO()
    if str(source).find('.gif') == -1:
        image.save(bio, format="PNG")
        imageL = [[sg.Image(data = bio.getvalue(), metadata= source, k = 0)]]
        window3 = sg.Window(title = 'big', layout= imageL)
        while True:
            event, value = window3.Read()
            if event in (sg.WINDOW_CLOSED, 'Exit'):
                window3.Close()
                break
    else:
        image.save(bio, format = 'GIF')
        imageL = [[sg.Image(data = bio.getvalue(), metadata= source, k = 0)]]
        window3 = sg.Window(title = 'big', layout= imageL)
        while True:
            event, value = window3.Read(timeout = (image.info['duration']))
            if event in (sg.WINDOW_CLOSED, 'Exit'):
                window3.Close()
                break
            window3[0].update_animation(window3[0].metadata, image.info['duration'])

def CheckNewMessages(currentchat):
    oldfolderlen = be.folderLen(currentchat)
    while True:
        if end.qsize() == 1: break
        if be.NewMessage(oldfolderlen, currentchat) == True:
            oldfolderlen = be.folderLen(currentchat)
            message = be.Incoming(oldfolderlen, currentchat)
            newmessages.put(message)

def startLoad():
    messages.clear()
    bigTwenty = be.firstMessages(be.folderLen(currentFolder), currentFolder)
    print(len(bigTwenty))
    for message in bigTwenty:
        if message[0] == 'txt':
            messages.append(createText(message[1])) 
        if message[0] == 'image':
            messages.append(createImage(message[1]))
    loadmessages('c')
    checkmessages = mt.Thread(target = CheckNewMessages, daemon=True, args=(currentFolder, ), name='incoming')
    checkmessages.start()
    

def sendMessage(text, ext):
    be.send(text, username, ext = ext, foldernum = currentFolder)

if __name__ == '__main__':
    convo = be.signin(username)
    window = make_window((0,0), (0,0), messages)
    window.set_min_size((800, 623))
    window["-MAIN-"].expand(True, True, True)
    window["-EXPAND2-"].expand(True, True, True)
    window.alpha_channel = 1
    window.maximize()
    arial = f.Font(family= 'Arial', size=12)
    startLoad()
    newmessages = q.Queue()
    end = q.Queue()
    while True:
        event, values = window.Read(timeout=50)
        if newmessages.empty() == False:
            message = newmessages.get()
            if message[0] == 'txt':
                messages.append(createText(message[1]))
                loadmessages('c')
            if message[0] == 'image':
                messages.append(createImage(message[1]))
                loadmessages('c')
        if event != None and event.find('Inflate') != -1:
            key = event[9:]
            createWindowImage(key)
        if event == 'REFRESH':
            loadmessages('c')
        if window['ImageLoad'].get() != '':
            with open(window['ImageLoad'].get(), 'rb') as f:
                pre, extension = f.name.split('.')
                be.send(f, username, '.'+extension, currentFolder)
            window['ImageLoad'].update(value = '')
        if event == 'invite':
            inviteCode = [[sg.Input(currentFolder, readonly=True ,font = ('Arial', 15))]]
            invite = sg.Window('', layout=inviteCode)
            while True:
                event2, value2 = invite.Read()
                if event2 in [sg.WIN_CLOSED, 'Exit']:
                    break
        if event == 'add':
            chatNumDemand = [[sg.Input(do_not_clear=False)],
                             [sg.Button('Enter', k = 'input'), sg.Exit()]]
            addChat = sg.Window(title = '', layout = chatNumDemand)
            while True:
                event2, value2 = addChat.Read()
                if event2 in [sg.WIN_CLOSED, 'Exit']:
                    break
                if event2 == 'input':
                    break
            addChat.Close()
        if event == 'Open':
            chat = window["Chats"].get()
            if chat == '': continue
            currentFolder = convo[chat]
            for thread in mt.enumerate():
                if 'incoming' in thread.name:
                    end.put('end')
                    thread.join()
                    a = end.get()
            startLoad()
        
        if event in (sg.WIN_CLOSED, "Exit"):
            with open('chats', 'wb') as c:
                pickle.dump(convo, c)
            break
        if event == 'create':
            menu = [[sg.Text('Chat Name'), sg.Input('', k = '-NAME-')], [sg.Button('Create', k = '-CREATE-')]]
            chatCreate = sg.Window('', menu)
            while True:
                event4, value4 = chatCreate.Read()
                if event4 in (sg.WIN_CLOSED, "Exit"):
                    break
                if event4 == '-CREATE-':
                    name = chatCreate['-NAME-'].get()
                    convo = be.createfolder(name, username)
                    chatCreate.Close()
                    loadmessages('c')
        if event == "-SEND-":
            if values["-INPUT-"].strip() != '':
                sendThread = mt.Thread(target=sendMessage, args=(values['-INPUT-'], '.txt', ))
                sendThread.start()
                window['-INPUT-'].update(value = '')
        if event == 'next':
            loadmessages('n')
        if event == 'back':
            loadmessages('b')
    window.Close()