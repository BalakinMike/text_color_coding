import PySimpleGUI as sg
import json
import os

NAME_SIZE = 23

def json_to_dict(name):
   '''Converting json table to coding dictionary'''
   with open(name) as f:
        color_code_dict = json.load(f)
   return color_code_dict


rightclick=['&Edit', ['C&ut', '&Copy','&Paste', '&Undo']]
menu_def = [['&File', ['&New', '&Open', '&Save', 'E&xit', ]], ['Edit', ['Cut', 'Copy', 'Paste', 'Undo'], ],  ['Help', 'About...'], ]

# ----- Full layout -----
layout = [[
            sg.Text("Папка с исходными файлами"),
            sg.In(size=(25, 1), enable_events=True, key="-FILE-"),
            sg.FileBrowse('Обзор'),
           ],
          [sg.Menu(menu_def)],
          [sg.Text("Text, which going to translate in color code:")],
          [sg.Multiline("", key='-IN-', expand_x=True, expand_y=True)],
          [sg.Graph(canvas_size=(400,100),graph_bottom_left=(0,0), 
                    graph_top_right=(400,100), background_color='light grey', 
                    enable_events=True, key = 'graph')],
          [sg.Text("Window for providing technical information:")],  
          [sg.Multiline("", key='-OUT-', expand_x=True, expand_y=True)],
          [sg.Button('Code', key='-TRANSFORM-')],
]

window = sg.Window("Color coder", layout, right_click_menu=rightclick, finalize=True)
graph = window['graph']
# rectangle = graph.draw_rectangle((0, 0), (100, 100), line_color='purple')

while True:
    event, values = window.read()
    
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == '-FILE-': #Searching json file with coding table
        pth = window['-FILE-'].get()
        color_code_dict = json_to_dict(pth)
    if event == '-TRANSFORM-': #Transforming text to color line
        txt = window['-IN-'].get()
        
        for i in range(len(txt)):
            hex_code_sym = f'{hex(ord(txt[i]))[2:]}'
            try:
                rectangle = graph.draw_rectangle((10*i,100), (10*i+10,90), line_color=f'{color_code_dict[hex_code_sym]}')
            except KeyError:
                window['-OUT-'].update(f'Key {hex_code_sym} not found in color_code_dict')
            
            graph.TKCanvas.itemconfig(rectangle, fill= f'{color_code_dict[hex_code_sym]}')
        print(event, values)
window.close()