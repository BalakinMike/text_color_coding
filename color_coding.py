import PySimpleGUI as sg
import json
import os

NAME_SIZE = 23
SIZE_W = 600 # wokr window size (width)
SIZE_H = 100

def json_to_dict(name):
   '''Converting json table to coding dictionary'''
   with open(name) as f:
        color_code_dict = json.load(f)
   return color_code_dict


rightclick=['&Edit', ['C&ut', '&Copy','&Paste', '&Undo']]
menu_def = [['&File', ['&New', '&Open', '&Save', 'E&xit', ]], ['Edit', ['Cut', 'Copy', 'Paste', 'Undo'], ],  ['Help', 'About...'], ]

# ----- Full layout -----
layout = [[
            sg.Text("Searching code table:"),
            sg.In(size=(25, 1), enable_events=True, key="-FILE-"),
            sg.FileBrowse('Обзор'),
           ],
          [sg.Menu(menu_def)],
          [sg.Text("Text, which going to translate in color code:")],
          [sg.Multiline("", key='-IN-', expand_x=True, expand_y=True, right_click_menu = rightclick)],
          [sg.Graph(canvas_size=(SIZE_W,SIZE_H),graph_bottom_left=(0,0), 
                    graph_top_right=(SIZE_W,SIZE_H), background_color='#ffffff', 
                    enable_events=True, key = 'graph')],
          [sg.Text("Window for providing technical information:")],  
          [sg.Multiline("", key='-OUT-', expand_x=True, expand_y=True)],
          [sg.Button('Coding', key='-TRANSFORM-', expand_x=True)],
]

window = sg.Window("Color coder", layout, right_click_menu=rightclick, finalize=True)
graph = window['graph']
input:sg.Multiline = window['-IN-']

while True:
    event, values = window.read()
    
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == '-FILE-': #Searching json file with coding table
        pth = window['-FILE-'].get()
        color_code_dict = json_to_dict(pth)
    if event == 'Paste': #Input text with help of right click mouse
        input.Widget.insert(sg.tk.INSERT, window.TKroot.clipboard_get())
    if event == '-TRANSFORM-': #Transforming text to color line
        txt = window['-IN-'].get()
        j = 0 #lines counter
        for i in range(len(txt)):
            hex_code_sym = f'{hex(ord(txt[i]))[2:]}'
            try:
                h=10*((10*i)//SIZE_W) #transition counter to new line Y
                rectangle = graph.draw_rectangle((10*j,(SIZE_H-h)), (10*j+10,(SIZE_H-h)-10), line_color=f'{color_code_dict[hex_code_sym]}')
                graph.TKCanvas.itemconfig(rectangle, fill= f'{color_code_dict[hex_code_sym]}')
                j +=1
                if j == (SIZE_W/10): #transition counter to new line X
                    j = 0
            except KeyError:
                window['-OUT-'].update(f'Key {hex_code_sym} not found in color_code_dict')
            
            # graph.TKCanvas.itemconfig(rectangle, fill= f'{color_code_dict[hex_code_sym]}')
    
        # print(event, values)
window.close()