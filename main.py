import os
import re
import tkinter as tk
from tkinter import filedialog



def split(str_variable, sep, pos):
    str_variable = str_variable.split(sep)
    return sep.join(str_variable[:pos]), sep.join(str_variable[pos:])


original_path = filedialog.askdirectory()
cwd_edit = next(os.walk(os.path.join(original_path, '.')))[1]
root = tk.Tk()
root.withdraw()

print(original_path)
print(cwd_edit)
run = False
loop = True

while loop is True:
    if run:
        changed_path = original_path.rsplit("/",1)
        original_path = changed_path[0]+'/'
        cwd_edit = [changed_path[1]]
        loop = False
        print("looping through directory")

    for directory in cwd_edit:
        path_to_dir = os.path.abspath(os.path.join(original_path, directory))
        # print(path_to_dir)
        files = os.listdir(path_to_dir)
        # print(cwd_edit)
        for names in files:
            if names.endswith(".hmt"):
                path_actual = os.path.abspath(os.path.join(path_to_dir, names))
                # try:
                with open(path_actual, 'r', errors='ignore') as file:
                    list_of_channel_title = []
                    data = file.readlines()
                    decoded_read = (' '.join(data)).encode("ascii", "ignore").decode()
                    decoded_replaced = decoded_read.replace('\x00', '')

                    slice_ = (re.split('([])', ((re.split('/[^\x00-\x2F]', decoded_replaced, maxsplit=1))[1]), maxsplit=2))
                    character = slice_[1]
                    channel = re.split('[^a-zA-Z0-9-,.? ]',slice_[4],maxsplit=1)
                    list_of_channel_title.extend([slice_[2],(channel[0])[2:]])

                    count_for_pattern = 0
                    for char in list_of_channel_title[1]:
                        if count_for_pattern == 0:
                            pattern = '[' + char + ']' + '.*'
                            count_for_pattern = count_for_pattern + 1
                            continue
                        pattern1 = pattern + '[' + char + ']' + '.*'
                        if re.search(pattern1, list_of_channel_title[0]) is not None:
                            pattern = pattern1
                        else:
                            pattern = pattern
                            break

                    name = character+(re.split(pattern,list_of_channel_title[0]))[0]
                    full_desc = ((re.search(name+'.*',slice_[4]).group(0))[1:])
                    slice_end = (re.search(
                        '\[AD,S]|\[S]|[\x00-\x1F][\x00-\x1F]|\[S,SL]|HD viewers press red to view in HD|\[AD]|Also in HD',
                        full_desc))
                    final = re.sub('',' ',((full_desc.split((slice_end.group(0)),1))[0]))
                    if final[0:2] == 'i7':
                        final = final[2:]
                    print(final)
    run = True


