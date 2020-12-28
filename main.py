import cv2
import numpy as np
import types

###################

def encrypt(data,kk):
    """
    Input:
         text to be encrypted
         key of the caesar cypher
    Output: Encrypted text
    """

    key = kk
    key = int(key)
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u','v', 'w', 'x', 'y', 'z']
    encrypted = ''
    data = data.lower()
    for char in data:
        if char == " ":
            encrypted += " "
            continue
        if char == "," or char == "." or char == "#" or char == ";" or char == "&":
            continue
        index = alphabet.index(char)
        shifted_text = (index + key) % 26
        encrypted += alphabet[shifted_text]
    return encrypted


def decrypt(encryptedMsg,kk):
    """
    Input:
         text to be deccrypted
         key of the caesar cypher
    Output: deccrypted text
    """
    key = kk
    key = int(key)
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u','v', 'w', 'x', 'y', 'z']
    decrypted = ''
    encryptedMsg = encryptedMsg.lower()
    for char in encryptedMsg:
        if char == " ":
            decrypted += " "
            continue
        if char == "," or char == "." or char == "#" or char == ";" or char == "&":
            continue
        index = alphabet.index(char)
        shifted_text = (index - key) % 26
        decrypted += alphabet[shifted_text]
    return decrypted

########################

def messege_to_binary(message):
    if type(message) == str:
        return ''.join([format(ord(i), "08b") for i in message])
    elif type(message) == bytes or type(message) == np.ndarray:
        return [format(i, "08b") for i in message]
    elif type(message) == int or type(message) == np.uint8:
        return format(message, "08b")
    else:
        raise TypeError("Unknown Input Type")


def encode(image, new_message):
    number_bytes = image.shape[0] * image.shape[1] * 3 // 8

    if len(new_message) > number_bytes:
        raise ValueError("You need a bigger Image or less data")

    new_message += "#####"

    data_index = 0

    binary_new_message = messege_to_binary(new_message)

    data_len = len(binary_new_message)

    for values in image:
        for pixel in values:
            r, g, b = messege_to_binary(pixel)

            # now we use the LSB method
            # remove last bit of every byte for all rgb's and then append new bit
            # using int to convert the binary into a number again

            if data_index < data_len:
                pixel[0] = int(r[:-1] + binary_new_message[data_index], 2)
                data_index += 1
            if data_index < data_len:
                pixel[1] = int(g[:-1] + binary_new_message[data_index], 2)
                data_index += 1
            if data_index < data_len:
                pixel[2] = int(b[:-1] + binary_new_message[data_index], 2)
                data_index += 1
            if data_index >= data_len:
                break
    return image


def show_data(image):
    binary_data = ""

    for values in image:
        for pixel in values:
            # converting the r,g,b into binary format
            r, g, b = messege_to_binary(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]

    all_bytes = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]

    # converting the bits into characters

    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "#####":
            break
    return decoded_data[:-5]


def encode_text(path,mss,new_path,key):
    path = str(path)
    mss = str(mss)
    new_path = str(new_path)

    image = cv2.imread(path)  # transforming image into matrix of r,g,b

    # print('the shape of the image is :', image.shape)


    encrypted_msg = encrypt(mss,key)



    # if (len(data) == 0):
    #     raise ValueError('there is no message ,, sorry  !!')

    file_name = new_path
    encode_image = encode(image, encrypted_msg)
    cv2.imwrite(file_name, encode_image)


def decode_text(path,textelement,key):
    image_name = path
    image = cv2.imread(image_name)  # transforming image into matrix of r,g,b

    text = show_data(image)
    decrypted_msg = decrypt(text,key)

    textelement.config(state=NORMAL)
    v =textelement.get('1.0', 'end-1c')
    if v != '':
        textelement.delete('1.0', END)
    textelement.insert('1.0', decrypted_msg)
    textelement.config(state=DISABLED)


#########################################################

from tkinter import *
from tkinter import ttk , font
from tkinter import filedialog
import tkinter as tk
from PIL import ImageTk,Image
import os, shutil

##############################################
## functions

###################
# griding
def griding(currenttab):
    m0 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(column=0)
    m1 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(column=1)
    m2 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(column=2)
    m3 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(column=3)
    m4 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(column=4)
    m5 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(column=5)
    m6 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(column=6)
    m7 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(column=7)
    m8 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(column=8)
    m9 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(column=9)
    m10 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(column=10)
    m11 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(column=11)
    m12 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(column=12)
    m13 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(column=13)

    m0 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(row=0)
    m1 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(row=1)
    m2 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(row=2)
    m3 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(row=3)
    m4 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(row=4)
    m5 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(row=5)
    m6 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(row=6)
    m7 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(row=7)
    m8 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(row=8)
    m9 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(row=9)
    m10 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(row=10)
    m11 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(row=11)
    m12 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(row=12)
    m13 = Label(currenttab, text="    ", font=('Bahnschrift SemiBold SemiConden', 15)).grid(row=13)

# positioning
def center_window(element,width=300, height=200):

    # get screen width and height
    screen_width = element.winfo_screenwidth()
    screen_height = element.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    element.geometry('%dx%d+%d+%d' % (width, height, x, y))

##################

def encode_tool(parent):
    parent.withdraw()

    tool = Toplevel()
    tool.title("Echo-Tech")
    center_window(tool,width=550, height=320)

    griding(tool)

    encode_label1 = Label(tool, text="Please select the file you want to encode to",fg="gray",anchor='w').grid(column=1, row=1,columnspan=2,sticky = W)

    encode_label2 = Label(tool, text="Please enter the message you want to hide",fg="gray",anchor='w')
    encode_label2.grid(column=1, row=4,columnspan=2,sticky = W)


    encode_entry2 = Text(tool, bg="white",wrap=WORD,height=8, width=30)
    encode_entry2.grid(column=1, row=5,columnspan=4,rowspan=2,sticky = W)

    scrollb = Scrollbar(tool, command=encode_entry2.yview)
    scrollb.grid(column=3, row=5,rowspan=2, sticky='nse')
    encode_entry2['yscrollcommand'] = scrollb.set

    new_name = Text(tool, bg="white",height = 1, width=15)
    new_name.grid(column=5, row=6, rowspan=1,sticky="w")
    new_name_label = Label(tool, text="Please enter a name for the new image",fg="gray",anchor='w')
    new_name_label.grid(column=5, row=7, columnspan=5,sticky="w")
    value = new_name


    pathfinder = ttk.Button(tool, text="Browse", command=lambda: fileDailog(parent=tool,big=encode_entry2,small=new_name))
    pathfinder.grid(column=1, row=2, sticky=W)

    def on_closing():
        tool.destroy()
        parent.deiconify()


    tool.protocol("WM_DELETE_WINDOW", on_closing)

    tool.mainloop()
################################

def decode_tool(parent):
    parent.withdraw()

    tool = Toplevel()
    tool.title("Echo-Tech")
    center_window(tool,width=550, height=320)

    griding(tool)

    decode_label1 = Label(tool, text="Please select the file you want to decode from",fg="gray",anchor='w').grid(column=1, row=1,columnspan=2,sticky = W)

    decode_label2 = Label(tool, text="Here The message Will appear",fg="gray",anchor='w')
    decode_label2.grid(column=1, row=4,columnspan=2,sticky = W)

    decode_entry2 = Text(tool, bg="white",wrap=WORD,height=8, width=30,state=DISABLED)
    decode_entry2.grid(column=1, row=5,columnspan=4,rowspan=2,sticky = W)

    scrollb = Scrollbar(tool, command=decode_entry2.yview)
    scrollb.grid(column=3, row=5,rowspan=2, sticky='nse')
    decode_entry2['yscrollcommand'] = scrollb.set



    # new_name = Text(tool, bg="white",height = 1, width=15)
    # new_name.grid(column=5, row=6, rowspan=1,sticky="w")
    # new_name_label = Label(tool, text="Please enter a name for the new image",fg="gray",anchor='w')
    # new_name_label.grid(column=5, row=7, columnspan=5,sticky="w")
    # value = new_name
    # print('new name',value)
    #

    pathfinder = ttk.Button(tool, text="Browse", command=lambda: fileDailog2(parent=tool,big=decode_entry2))
    pathfinder.grid(column=1, row=2, sticky=W)

    def on_closing():
        tool.destroy()
        parent.deiconify()

    tool.protocol("WM_DELETE_WINDOW", on_closing)
    tool.mainloop()

################################

def fileDailog(parent,big,small):
    fileName = filedialog.askopenfilename(initialdir = "/", title="Select A File")
    # name = fileName
    # localDrive = name[0]
    # name = name[2:]
    # full_name = '/mnt/' + localDrive + name


    img = ImageTk.PhotoImage(Image.open(fileName).resize((200, 200), Image.ANTIALIAS))
    parent.photo = img
    canvas = Canvas(parent, width = 200, height = 200,highlightthickness=1, highlightbackground="white")
    canvas.grid(row=1, column=5,columnspan=5,rowspan=5, sticky="n")
    canvas.create_image(1, 1, anchor='nw', image=img)


    def get_new():
        return fileName[:fileName.rindex('/') + 1] + small.get('1.0', 'end-1c') + '.png'

    def provide():

        def submit(h):
            val1 = entry2.get('1.0', 'end-1c')
            if val1 == "":
                pass
            else:
                h.quit()
                h.withdraw()

        nav = Toplevel()
        nav.title("Echo-Tech")
        center_window(nav,width=200, height=70)

        label2 = Label(nav, text="Please Insert a key of your choice", fg="gray", anchor='w')
        label2.grid(column=1, row=4, columnspan=2, sticky='we', padx=5, pady=2)

        entry2 = Text(nav, bg="white", height=1, width=10)
        entry2.grid(column=1, row=5, rowspan=2, sticky='e', padx=5, pady=2)

        SubmitBtn = Button(nav, text="Submit", command=lambda:submit(nav))
        SubmitBtn.grid(row=5, column=2, padx=5, pady=2,sticky='e')

        nav.mainloop()

        return entry2.get('1.0', 'end-1c')

    apply_button = Button(parent, text="Apply",height = 1, width = 10, fg="black",command=lambda: encode_text(path=fileName,mss=big.get('1.0', 'end-1c'),new_path=get_new(),key=provide()))
    apply_button.grid(column=5, row=6, rowspan=1,columnspan=5,sticky="e")


    pathfinder_label = ttk.Label(parent, text="")
    pathfinder_label.grid(column=1, row=3,columnspan=4,sticky = W)
    pathfinder_label.configure(text=fileName,anchor='w')

def fileDailog2(parent,big):
    fileName = filedialog.askopenfilename(initialdir = "/", title="Select A File")
    # name = fileName
    # localDrive = name[0]
    # name = name[2:]
    # full_name = '/mnt/' + localDrive + name


    img = ImageTk.PhotoImage(Image.open(fileName).resize((200, 200), Image.ANTIALIAS))
    parent.photo = img
    canvas = Canvas(parent, width = 200, height = 200,highlightthickness=1, highlightbackground="white")
    canvas.grid(row=1, column=5,columnspan=5,rowspan=5, sticky="n")
    canvas.create_image(1, 1, anchor='nw', image=img)

    def provide():

        def submit(h):
            val1 = entry2.get('1.0', 'end-1c')
            if val1 == "":
                pass

            else:
                h.quit()
                h.withdraw()

        nav2 = Toplevel()
        nav2.title("Echo-Tech")
        center_window(nav2, width=200, height=70)

        label2 = Label(nav2, text="Please Provide the secret key...", fg="gray", anchor='w')
        label2.grid(column=1, row=4, columnspan=2, sticky='we', padx=5, pady=2)

        entry2 = Text(nav2, bg="white", height=1, width=10)
        entry2.grid(column=1, row=5, rowspan=2, sticky='e', padx=5, pady=2)

        SubmitBtn = Button(nav2, text="Submit", command=lambda: submit(nav2))
        SubmitBtn.grid(row=5, column=2, padx=5, pady=2, sticky='e')

        nav2.mainloop()

        return entry2.get('1.0', 'end-1c')

    apply_button = Button(parent, text="Apply",height = 1, width = 10, fg="black",command=lambda: decode_text(path=fileName,textelement=big,key=provide()))
    apply_button.grid(column=5, row=6, rowspan=1,columnspan=5,sticky="e")


    pathfinder_label = ttk.Label(parent, text="")
    pathfinder_label.grid(column=1, row=3,columnspan=4,sticky = W)
    pathfinder_label.configure(text=fileName,anchor='w')


window=Tk()

window.title("Echo-Tech")
center_window(window,width=550, height=320)

griding(window)

label1 = Label(window,text= "Welcome To Monalisa", fg="gray",font=('Bahnschrift SemiBold SemiConden',15))
label1.grid(column=5,row=0)

encode_button = Button(window, text="Hide A Message" , fg="black",command= lambda: encode_tool(parent=window)).grid(column=1,row=2)
encode_label = Label(window,text= "Press here to hide \n a message of your choice in\n the media you select", fg="gray").grid(column=1,row=3)

decode_button = Button(window, text="Reveal A Message" , fg="black",command= lambda: decode_tool(parent=window)).grid(column=1,row=5)
decode_label = Label(window,text= "Press here to reveal \n a message hidden in a\n media you select\n (If it exist)", fg="gray").grid(column=1,row=6)

window.mainloop()
