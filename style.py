import cv2
import gif as gif
import numpy as np
import types
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
def encode_text(path,mss,new_path):
    image_name = path
    image = cv2.imread(image_name)  # transforming image into matrix of r,g,b
    # print('the shape of the image is :', image.shape)
    data = mss
    # if (len(data) == 0):
    #     raise ValueError('there is no message ,, sorry  !!')
    file_name = new_path
    encode_image = encode(image, data)
    cv2.imwrite(file_name, encode_image)
def decode_text():
    image_name = input("Insert an image(with the extention) you want to decode:  ")
    image = cv2.imread(image_name)  # transforming image into matrix of r,g,b
    text = show_data(image)
    return text
#########################################################
from tkinter import *
from tkinter import ttk , font
from tkinter import filedialog
from PIL import ImageTk,Image
import tkinter as tk
import os, shutil
##############################################
## functions
img = 0
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
    print('m13: ', m13)
##################

tool = None

def encode_tool(parent):
    global tool
    parent.withdraw()
    tool = Toplevel()
    tool.title("Echo-Tech")
    tool.geometry("550x320")
    tool.wm_iconbitmap('logo.ico')

    griding(tool)
    encode_label1 = Label(tool, text="Please select the file you want to encode to",fg="gray",anchor='w').grid(column=1, row=1,columnspan=2,sticky = W)
    pathfinder = ttk.Button(tool, text="Browse", command= lambda: fileDailog(parent=tool))
    pathfinder.grid(column=1, row=2,sticky = W)
    # encode_label2 = Label(tool, text="Please enter the message you want to hide",fg="gray",anchor='w').grid(column=1, row=4,columnspan=2,sticky = W)
    # encode_entry2 = Text(tool, bg="white",wrap=WORD,height=8, width=30).grid(column=1, row=5,columnspan=4,rowspan=2,sticky = W)
    # confirm_button = Button(tool, text="confirm", height=2, width=10, fg="black",command=(new_text == encode_entry2)).grid(column=1, row=5,columnspan=4,rowspan=2,sticky = W)


    def on_closing():
        tool.destroy()
        parent.deiconify()
    tool.protocol("WM_DELETE_WINDOW", on_closing)
    tool.mainloop()
################################

def fileDailog(parent):
    global tool
    new_text = None

    encode_label2 = Label(tool, text="Please enter the message you want to hide",fg="gray",anchor='w').grid(column=1, row=4,columnspan=2,sticky = W)
    encode_entry2 = Text(tool, bg="white",wrap=WORD,height=8, width=30).grid(column=1, row=5,columnspan=4,rowspan=2,sticky = W)
    # confirm_button = Button(tool, text="confirm", height=2, width=10, fg="black").grid(column=1, row=5,columnspan=4,rowspan=2,sticky = W, command=(new_text == encode_entry2))

    fileName = filedialog.askopenfilename(initialdir = "/", title="Select A File")
    name = fileName
    localDrive = name[0]
    name = name[2:]
    full_name = '/mnt/' + localDrive + name
    # messagebox = encode_entry2.get('1.0', 'end')
    # new_path = fileName[:fileName.rindex('/') + 1] + new_name.get("1.0", 'end-1c') + fileName[fileName.rindex('.'):]
    img = ImageTk.PhotoImage(Image.open(fileName).resize((200, 200), Image.ANTIALIAS))
    parent.photo = img
    canvas = Canvas(parent, width = 200, height = 200,highlightthickness=1, highlightbackground="white")
    canvas.grid(row=1, column=5,columnspan=5,rowspan=5, sticky="n")
    canvas.create_image(1, 1, anchor='nw', image=img)


    apply_button = Button(parent, text="Apply",height = 1, width = 10, fg="black",command=lambda: encode_text(path=full_name,mss=encode_entry2.get('1.0', 'end'),new_path =fileName[:fileName.rindex('/') + 1] + new_name.get("1.0", 'end-1c') + fileName[fileName.rindex('.'):])).grid(column=5, row=6, rowspan=1,columnspan=5,sticky="e")

    new_name = Text(parent, bg="white",height = 1, width=15).grid(column=5, row=6, rowspan=1,sticky="w")
    new_name_label = Label(parent, text="Please enter a name for the new image",fg="gray",anchor='w').grid(column=5, row=7, columnspan=5,sticky="w")
    pathfinder_label = ttk.Label(parent, text="")
    pathfinder_label.grid(column=1, row=3,columnspan=4,sticky = W)
    pathfinder_label.configure(text=fileName,anchor='w')







window=Tk()
window.title("Echo-Tech")
window.geometry("750x370")
window['background']='grey'
window.wm_iconbitmap('logo.ico')

# window.configure(bg='blue')

# ccanvas = Canvas(window,width="550",height="320")
# ccanvas.create_image(0,0,anchor="nw")
# monaliza = imgX.subsample(1,1)
# background_image = tk.PhotoImage(file="t.png")
# background_label = tk.Label(window, image=background_image )
# background_label.place(x=0, y=0, relwidth=1, relheight=2)

imgX = PhotoImage(file = r"main.png")
img1 = PhotoImage(file = r"lock.png")
lock = img1.subsample(10,12)
img2 = PhotoImage(file = r"unlock.png")
unlock = img2.subsample(10,12)



encode_button = Button(window, text="Hide A Message " ,image = lock,compound = LEFT, fg="black",command= lambda: encode_tool(parent=window)).grid(column=1,row=1)
encode_label = Label(window,text= "Press on Encode to hide \n a message of your choice in\n the media you select", fg="gray").grid(column=1,row=2)
decode_button = Button(window, text="Reveal A Message " ,image = unlock,compound = LEFT, fg="black",command= lambda: encode_tool(parent=window)).grid(column=3,row=1)
decode_label = Label(window,text= "Press on Decode to reveal \n a message hidden in a\n media you select\n (If it exist)", fg="gray").grid(column=3,row=2)
label1 = Label(window,text= "Welcome To Monalisa",image = imgX,compound = BOTTOM,fg="gray",font=('Bahnschrift SemiBold SemiConden',15)).grid(column=2,row=1,rowspan=2,pady="55",padx="100")




# bg = ImageTk.PhotoImage(file="t.png")
# mbkLabel = Label(window, image=bg).grid(column=0,row=0)
# ccanvas = Canvas(window,width="550",height="320")
# ccanvas.pack(fill="both",expand="true")
# ccanvas.create_image(0,0,image=bg,anchor="nw")

# def resizer(e):
#     global bg1, resize_bg,new_bg
#     bg1 = Image.open("t.png")
#     resize_bg = bg1.resize((e.width,e.height), Image.ANTIALIAS)
#     new_bg = ImageTk.PhotoImage(resize_bg)
#     ccanvas.create_image(0, 0, image=new_bg, anchor="nw")
#
#
# window.bind('<Configure>', resizer)



# griding(window)
window.mainloop()


# import tkinter
#
# ssw = tkinter.Tk()
#
# def six():
#     toplvl = tkinter.Toplevel() #created Toplevel widger
#     photo = tkinter.PhotoImage(file = 'test2.gif')
#     lbl = tkinter.Label(toplvl ,image = photo)
#     lbl.image = photo #keeping a reference in this line
#     lbl.grid(row=0, column=0)
#
# def base():
#     la = tkinter.Button(ssw,text = 'yes',command=six)
#     la.grid(row=0, column=0) #specifying row and column values is much better
#
# base()
#
# ssw.mainloop()

# import tkinter as tk
# from PIL import Image, ImageTk
# from itertools import count
#
# class ImageLabel(tk.Label):
#     """a label that displays images, and plays them if they are gifs"""
#     def load(self, im):
#         if isinstance(im, str):
#             im = Image.open(im)
#         self.loc = 0
#         self.frames = []
#
#         try:
#             for i in count(1):
#                 self.frames.append(ImageTk.PhotoImage(im.copy()))
#                 im.seek(i)
#         except EOFError:
#             pass
#
#         try:
#             self.delay = im.info['duration']
#         except:
#             self.delay = 100
#
#         if len(self.frames) == 1:
#             self.config(image=self.frames[0])
#         else:
#             self.next_frame()
#
#     def unload(self):
#         self.config(image="")
#         self.frames = None
#
#     def next_frame(self):
#         if self.frames:
#             self.loc += 1
#             self.loc %= len(self.frames)
#             self.config(image=self.frames[self.loc])
#             self.after(self.delay, self.next_frame)
#
# root = tk.Tk()
# lbl = ImageLabel(root)
# lbl.pack()
# lbl.load('7.gif')
# root.mainloop()