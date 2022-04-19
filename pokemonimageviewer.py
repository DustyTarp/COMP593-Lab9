from tkinter import *
from tkinter import ttk
from pokiapi import get_pokemon_image_url, get_pokemon_list
import os
import sys
import ctypes
import requests


def main():    #creating an image directory for pokemon images
    script_dir = sys.path[0]
    images_dir = os.path.join(script_dir, 'images')
    if not os.path.isdir(images_dir):
        os.makedirs(images_dir)

    root = Tk()            #setting up gui with taskbar icon
    root.title('Pokemon Image Viewer')
    app_id = 'pokemonimageviewerapp' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    root.iconbitmap(os.path.join(script_dir, 'pika.ico'))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    frm = ttk.Frame(root)         #setting frame up and telling it to scale correctly
    frm.grid(sticky=(N,S,E,W))
    frm.columnconfigure(0, weight=1)
    frm.rowconfigure(0, weight=1)

    img_pokemon = PhotoImage(file=os.path.join(script_dir, 'pokigroup1.png'))      #setting default photo on the gui with padding
    lbl_image = Label(frm, image=img_pokemon)
    lbl_image.grid(row=0, column=0, padx=10, pady=10)


    pokemon_list = get_pokemon_list(limit=1000)         #creation of box with list of every pokemon in order alphabetically
    pokemon_list.sort()
    cbo_pokemon_sel = ttk.Combobox(frm, values=pokemon_list, state='readonly')
    cbo_pokemon_sel.set('Select a Pokemon')
    cbo_pokemon_sel.grid(row=1, column=0)

    def handle_cbo_pokemon_sel(event):         #take pokemon name selected and shows it on gui while unlocking the button
        pokemon_name = cbo_pokemon_sel.get()
        image_url = get_pokemon_image_url(pokemon_name)
        image_path = os.path.join(images_dir, pokemon_name + '.png')
        if download_image_url(image_url, image_path):
            img_pokemon['file'] = image_path
            btn_set_desktop.state(['!disabled'])
            
        
    cbo_pokemon_sel.bind('<<ComboboxSelected>>', handle_cbo_pokemon_sel)         #binds the combobox to the pokemon selected

    def btn_set_desktop_click():                               #button click command to set background with choosen pokemon
        pokemon_name = cbo_pokemon_sel.get()
        image_path = os.path.join(images_dir, pokemon_name + '.png')
        set_desktop_background_image(image_path)
        
        
    btn_set_desktop = ttk.Button(frm, text='Set as Desktop Image', command=btn_set_desktop_click)       #default button state with text displayed on it
    btn_set_desktop.state(['disabled'])
    btn_set_desktop.grid(row=2, column=0, padx=10, pady=10)

    root.mainloop()
    

def set_desktop_background_image(path):            #setting the desktop backgroud function
    try:
       ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
    except:
        print('Error setting new background')

def download_image_url(url, path):        #download of pokemon image function 

    if os.path.isfile(path):
        return path

    resp_msg = requests.get(url)
    pass
    if resp_msg.status_code == 200:
        try:
            img_data = resp_msg.content
            with open(path, 'wb') as fp:
                fp.write(img_data)
            return path
        except:
            return
    else:
        print('Failed to download image')
        print('Response code: ', resp_msg.status_code)
        print(resp_msg.text)
    
main()
