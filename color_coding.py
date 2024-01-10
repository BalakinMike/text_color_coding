import PySimpleGUI as sg
import json
import os

NAME_SIZE = 23
SIZE_W = 600 # work window size (width)
SIZE_H = 100
DESCRIPTION = '''This app lets translate text to color code (array of color rectangle).
1. First of all, You have to choose coding dictionary, clicking button 'Browse'. 
2. After that, you have to input (or Paste) text in special window and click 'Coding'.
3. In case in your text will find non standard symbol you will get special message in lower window.
4. For saving getting color code choose 'Save' in window menu. Code will be save currently folder in file 'color_output_code.txt'.

Author: Mike Balakin.'''

def json_to_dict(name):
   '''Converting json table to coding dictionary'''
   with open(name) as f:
        color_code_dict = json.load(f)
   return color_code_dict


rightclick=['&Edit', ['&Copy','&Paste']]
menu_def = [['&File', ['&New', '&Open', '&Save', 'E&xit', ]], ['Edit', ['Copy', 'Paste'], ],  ['Help', 'About...'], ]

# ----- Full layout -----
layout = [[
            sg.Text("Searching code table:"),
            sg.In(size=(25, 1), enable_events=True, key="-FILE-"),
            sg.FileBrowse('Browse'),
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
output_code = []
while True:
    event, values = window.read()
    
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == '-FILE-': #Searching json file with coding table
        pth = window['-FILE-'].get()
        color_code_dict = json_to_dict(pth)
    if event == 'About...':
        sg.popup('Description', DESCRIPTION)
    if event == 'Paste': #Input text with help of right click mouse
        input.Widget.insert(sg.tk.INSERT, window.TKroot.clipboard_get())
    if event == '-TRANSFORM-': #Transforming text to color line
        txt = window['-IN-'].get()
        j = 0 #lines counter
        for i in range(len(txt)):
            hex_code_sym = f'{hex(ord(txt[i]))[2:]}'
            sym_color_code = color_code_dict[hex_code_sym]
            try:
                h=10*((10*i)//SIZE_W) #transition counter to new line Y
                rectangle = graph.draw_rectangle((10*j,(SIZE_H-h)), (10*j+10,(SIZE_H-h)-10), line_color=f'{sym_color_code}')
                graph.TKCanvas.itemconfig(rectangle, fill= f'{sym_color_code}')
                output_code.append(sym_color_code)
                j +=1
                if j == (SIZE_W/10): #transition counter to new line X
                    j = 0
            except KeyError:
                window['-OUT-'].update(f'Key {hex_code_sym} not found in color_code_dict')
    if event == 'Save':  #saving finally color code in file      
        with open('color_output_code.txt', 'w') as cd: #saving result color cod in txt file
            cd.write('\n'.join(output_code))            
        
window.close()