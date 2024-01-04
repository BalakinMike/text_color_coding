
'''
This modul use to coding from literal symbols to 
color hex code. We create dictionary with literal 
symbols as keys and hex color codes as values.
'''
import copy
import json
import os

with open("hex_color.csv") as hc: #reading csv file with hex color code
    hex_color = [line[:-8] for line in hc ] #create codes list
# print(hex_color,'\n', len(hex_color))

# Creation list with ASCII codes of standart and Cyryllic symbols
hex_symbol = [hex(code)[2:] for code in range (1104)]
hex_symbol_rus = copy.deepcopy(hex_symbol)
hex_symbol_rus[128:1040] = [] #cuting greek symbols
hex_symbol_rus[:33] = [] #cuting technical symbols which not using in printing

# print(hex_symbol_rus,'\n',len(hex_symbol_rus) )

#createion dict to translate symbols code into hex color code
color_code_dict = {}
j = 0
for i in hex_symbol_rus:
    color_code_dict[i] = hex_color[j]
    j +=1

# print(color_code_dict,'\n', len(color_code_dict))
    
# writing json file with coding table
# with open ('color_code_dict.json', 'a') as f:
#     json.dump(color_code_dict, f, indent=4)