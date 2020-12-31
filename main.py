import cv2
import numpy as np
import types
import time
from threading import Thread
import wave
import soundfile
import random

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders




def send_email(filename,r_email,file_path):
    sender="echotech2022@gmail.com"  #sender gmail address
    reciever = r_email  #reciver gmail address
    msg=MIMEMultipart()
    msg['From']=sender
    msg['To']=reciever
    msg['Subject']="Warning This Is Echo-Tech"
    body="sent from Echo-Team"
    msg.attach(MIMEText(body,'plain'))
    attachment_file = file_path
    attachment=open(attachment_file,"rb") #attachment folder
    p=MIMEBase('application','octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition',"attachment; filename=%s"%filename)
    msg.attach(p)
    s=smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(sender,"Echoteam2020") #enter sender gmail password here
    text=msg.as_string()
    s.sendmail(sender,reciever,text)
    s.quit()

def encrypt(data,kk):
    """
    Input:
         text to be encrypted
         key of the caesar cypher
    Output: Encrypted text
    """
    key = kk
    key=int(key)
    alphabet=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    symbols_num =['!','@','#','$','%','^','&','*','(',')','_','-','+', '=', ',',"'",'\n', '.','/', '?', '{', '}', '[', ']',  '~' , '|', '1', '2', '3', '4', '5', '6', '7', '8', '9','0']
    encrypted = ''
    data = data.lower()
    for char in data:
        if char == " " :
              encrypted += " "
              continue
        if char in symbols_num:
            encrypted += char
            continue
        index = alphabet.index(char)
        shifted_text = (index + key) % 26
        encrypted += alphabet[shifted_text]
    return encrypted

def decrypt(encryptedMsg, kk):
    """
    Input:
         text to be deccrypted
         key of the caesar cypher
    Output: deccrypted text
    """
    key = kk
    key = int(key)
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
    symbols_num = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', ',', "'", '\n', '.', '/', '?',
                   '{', '}', '[', ']', '~', '|', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    decrypted = ''
    encryptedMsg = encryptedMsg.lower()
    for char in encryptedMsg:
        if char == " ":
            decrypted += " "
            continue
        if char in symbols_num:
            decrypted += char
            continue
        index = alphabet.index(char)
        shifted_text = (index - key) % 26
        decrypted += alphabet[shifted_text]
    return decrypted

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

    encrypted_msg = encrypt(mss,key)

    file_name = new_path
    encode_image = encode(image, encrypted_msg)
    cv2.imwrite(file_name, encode_image)

    nav3 = Toplevel()
    nav3.title("Echo-Tech")
    center_window(nav3, width=225, height=80)

    label2 = Label(nav3, text="All Done,You may find the new Image \nin the same directory as the original", fg="gray", anchor='w')
    label2.grid(column=1, row=4, columnspan=2, sticky='we', padx=5, pady=2)

    def open():
        os.system(f"start {new_path[:new_path.rindex('/') + 1]}")

    oopen = Button(nav3, text="Open In Explorer", command=open)
    oopen.grid(row=5, column=1, padx=5, pady=2, columnspan=1, sticky='e')

    def provide_e():

        def submit(h):
            val1 = entry2.get()
            if val1 == "":
                pass
            else:
                h.quit()
                h.withdraw()

        nav = Toplevel()
        nav.title("Echo-Tech")
        center_window(nav,width=225, height=80)

        label2 = Label(nav, text="Enter the reciver email address", fg="gray", anchor='w')
        label2.grid(column=2, row=4, columnspan=4, sticky='we', padx=5, pady=2)

        entry2 = Entry(nav, bg="white", width=35)
        entry2.grid(column=1, row=5,columnspan=4, rowspan=2, sticky='e', padx=5, pady=2)

        SubmitBtn = Button(nav, text="Submit", command=lambda:submit(nav))
        SubmitBtn.grid(row=8, column=4, padx=5, pady=2,sticky='e')

        nav.mainloop()

        return entry2.get()

    em = Button(nav3, text="Send Via Email", command=lambda: send_email(filename=new_path[new_path.rindex('/')+1:],r_email=provide_e(),file_path=new_path))
    em.grid(row=5, column=2, padx=5, pady=2, columnspan=1, sticky='e')

    nav3.mainloop()

def decode_text(path,textelement,key):
    textelement.config(state=NORMAL)
    v =textelement.get('1.0', 'end-1c')
    if v != '':
        textelement.delete('1.0', END)
    textelement.config(state=DISABLED)


    # Starting the mixer
    mixer.init()
    # Loading the song
    mazika = "test.mp3"

    if random.randint(1, 3) == 1:
        mazika = "test.mp3"
    elif random.randint(1, 3) == 2:
        mazika = "test2.mp3"
    elif random.randint(1, 3) == 3:
        mazika = "test3.mp3"

    mixer.music.load(mazika)
    # Setting the volume
    mixer.music.set_volume(0.1)
    # Start playing the song
    mixer.music.play()


    nav4 = Toplevel()
    nav4.title("Echo-Tech")
    center_window(nav4, width=240, height=80)

    label2 = Label(nav4, text="Please wait..processing", fg="gray", anchor='w')
    label2.grid(column=1, row=4, columnspan=2, sticky='we', padx=5, pady=2)

    def l():
        image_name = path
        image = cv2.imread(image_name)  # transforming image into matrix of r,g,b

        text = show_data(image)
        decrypted_msg = decrypt(text, key)

        textelement.config(state=NORMAL)
        textelement.insert('1.0', decrypted_msg)
        textelement.config(state=DISABLED)

        mixer.music.stop()
        nav4.destroy()

    def run():
        nav4.after(1000, l())
    t = Thread(target=run)
    t.start()

    nav4.mainloop()

def encode_audio(path,mss,new_path,key):
    # enter the audio path
    audio_path = path
    # read wave audio file
    song = wave.open(audio_path, mode='rb')
    # Read frames and convert to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))
    # The "secret" text message
    text_msg = mss
    encrypted_msg = encrypt(text_msg,key)
    # Append dummy data to fill out rest of the bytes. Receiver shall detect and remove these characters.
    encrypted_msg = encrypted_msg + '###'
    # Convert text to bit array
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in encrypted_msg])))

    # Replace LSB of each byte of the audio data by one bit from the text bit array
    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit

    # Get the modified bytes
    frame_modified = bytes(frame_bytes)
    # Write bytes to a new wave audio file
    new_name = new_path
    with wave.open(new_name , 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)
    song.close()

    nav6 = Toplevel()
    nav6.title("Echo-Tech")
    center_window(nav6, width=225, height=80)

    label2 = Label(nav6, text="All Done,You may find the new Image \nin the same directory as the original", fg="gray", anchor='w')
    label2.grid(column=1, row=4, columnspan=2, sticky='we', padx=5, pady=2)

    def open():
        os.system(f"start {new_path[:new_path.rindex('/') + 1]}")

    oopen = Button(nav6, text="Open In Explorer", command=open)
    oopen.grid(row=5, column=1, padx=5, pady=2, columnspan=1, sticky='e')

    def provide_e():

        def submit(h):
            val1 = entry2.get()
            if val1 == "":
                pass
            else:
                h.quit()
                h.withdraw()

        nav = Toplevel()
        nav.title("Echo-Tech")
        center_window(nav,width=225, height=80)

        label2 = Label(nav, text="Enter the reciver email address", fg="gray", anchor='w')
        label2.grid(column=2, row=4, columnspan=4, sticky='we', padx=5, pady=2)

        entry2 = Entry(nav, bg="white", width=35)
        entry2.grid(column=1, row=5,columnspan=4, rowspan=2, sticky='e', padx=5, pady=2)

        SubmitBtn = Button(nav, text="Submit", command=lambda:submit(nav))
        SubmitBtn.grid(row=8, column=4, padx=5, pady=2,sticky='e')

        nav.mainloop()

        return entry2.get()

    em = Button(nav6, text="Send Via Email", command=lambda: send_email(filename=new_path[new_path.rindex('/')+1:],r_email=provide_e(),file_path=new_path))
    em.grid(row=5, column=2, padx=5, pady=2, columnspan=1, sticky='e')

    nav6.mainloop()

def decode_audio(path,textelement,key):
    textelement.config(state=NORMAL)
    v = textelement.get('1.0', 'end-1c')
    if v != '':
        textelement.delete('1.0', END)
    textelement.config(state=DISABLED)

    # Starting the mixer
    mixer.init()
    # Loading the song
    mazika = "test.mp3"

    if random.randint(1, 3) == 1:
        mazika = "test.mp3"
    elif random.randint(1, 3) == 2:
        mazika = "test2.mp3"
    elif random.randint(1, 3) == 3:
        mazika = "test3.mp3"

    mixer.music.load(mazika)
    # Setting the volume
    mixer.music.set_volume(0.1)
    # Start playing the song
    mixer.music.play()

    nav4 = Toplevel()
    nav4.title("Echo-Tech")
    center_window(nav4, width=240, height=80)

    label2 = Label(nav4, text="Please wait..processing", fg="gray", anchor='w')
    label2.grid(column=1, row=4, columnspan=2, sticky='we', padx=5, pady=2)

    def l():
        # enter the audio path
        audio_path = path
        song = wave.open(audio_path, mode='rb')
        # Convert audio to byte array
        frame_bytes = bytearray(list(song.readframes(song.getnframes())))
        # Extract the LSB of each byte

        extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
        # Convert byte array back to string
        string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
        # Cut off at the filler characters
        decoded = string.split("###")[0]
        # Print the extracted text
        decrypted_msg = decrypt(decoded, key)

        textelement.config(state=NORMAL)
        textelement.insert('1.0', decrypted_msg)
        textelement.config(state=DISABLED)

        song.close()

        mixer.music.stop()
        nav4.destroy()

    def run():
        nav4.after(1000, l())
    t = Thread(target=run)
    t.start()

    nav4.mainloop()

def encrypt_image(parent,im1,im2,new_path):

    # Starting the mixer
    mixer.init()
    # Loading the song
    mazika = "test.mp3"

    if random.randint(1, 3) == 1:
        mazika = "test.mp3"
    elif random.randint(1, 3) == 2:
        mazika = "test2.mp3"
    elif random.randint(1, 3) == 3:
        mazika = "test3.mp3"

    mixer.music.load(mazika)
    # Setting the volume
    mixer.music.set_volume(0.1)
    # Start playing the song
    mixer.music.play()

    nav4 = Toplevel()
    nav4.title("Echo-Tech")
    center_window(nav4, width=240, height=80)

    label2 = Label(nav4, text="Please wait..processing", fg="gray", anchor='w')
    label2.grid(column=1, row=4, columnspan=2, sticky='we', padx=5, pady=2)

    def l():

        # first resizing the two images in order to be the same size
        img1 = Image.open(im1)
        img1 = img1.resize((500, 600), Image.ANTIALIAS)
        img1.save(fp=im1)
        img2 = Image.open(im2)
        img2 = img2.resize((500, 600), Image.ANTIALIAS)
        img2.save(fp=im2)

        img1 = cv2.imread(im1)
        img2 = cv2.imread(im2)

        for i in range(img2.shape[0]):
            for j in range(img2.shape[1]):
                for l in range(3):
                    # v1 and v2 are 8-bit pixel values
                    # of img1 and img2 respectively
                    v1 = format(img1[i][j][l], '08b')
                    v2 = format(img2[i][j][l], '08b')
                    # Taking 4 MSBs of each image
                    v3 = v1[:4] + v2[:4]
                    img1[i][j][l] = int(v3, 2)
        cv2.imwrite(new_path, img1)


        img_par9 = ImageTk.PhotoImage(Image.open(new_path).resize((200, 200), Image.ANTIALIAS))
        parent.photo_par9 = img_par9
        canvas_par9 = Canvas(parent, width=200, height=200, highlightthickness=1, highlightbackground="white")
        canvas_par9.grid(column=7, row=4, columnspan=3, rowspan=2, sticky="n")
        canvas_par9.create_image(1, 1, anchor='nw', image=img_par9)

        global pathfinder_label_par9
        pathfinder_label_par9 = ttk.Label(parent, text="")
        pathfinder_label_par9.grid(column=7, row=3, columnspan=4, sticky=W)
        pathfinder_label_par9.configure(text=new_path, anchor='w')


        mixer.music.stop()
        nav4.destroy()

############

        nav3 = Toplevel()
        nav3.title("Echo-Tech")
        center_window(nav3, width=225, height=80)

        label2 = Label(nav3, text="All Done,You may find the new Image \nin the same directory as the original",
                       fg="gray",
                       anchor='w')
        label2.grid(column=1, row=4, columnspan=2, sticky='we', padx=5, pady=2)

        def open():
            os.system(f"start {new_path[:new_path.rindex('/') + 1]}")

        oopen = Button(nav3, text="Open In Explorer", command=open)
        oopen.grid(row=5, column=1, padx=5, pady=2, columnspan=1, sticky='e')

        def provide_e():

            def submit(h):
                val1 = entry2.get()
                if val1 == "":
                    pass
                else:
                    h.quit()
                    h.withdraw()

            nav = Toplevel()
            nav.title("Echo-Tech")
            center_window(nav, width=225, height=80)

            label2 = Label(nav, text="Enter the reciver email address", fg="gray", anchor='w')
            label2.grid(column=2, row=4, columnspan=4, sticky='we', padx=5, pady=2)

            entry2 = Entry(nav, bg="white", width=35)
            entry2.grid(column=1, row=5, columnspan=4, rowspan=2, sticky='e', padx=5, pady=2)

            SubmitBtn = Button(nav, text="Submit", command=lambda: submit(nav))
            SubmitBtn.grid(row=8, column=4, padx=5, pady=2, sticky='e')

            nav.mainloop()

            return entry2.get()

        em = Button(nav3, text="Send Via Email",
                    command=lambda: send_email(filename=new_path[new_path.rindex('/') + 1:], r_email=provide_e(),
                                               file_path=new_path))
        em.grid(row=5, column=2, padx=5, pady=2, columnspan=1, sticky='e')

        nav3.mainloop()

    def run():
        nav4.after(1000, l())

    t = Thread(target=run)
    t.start()

    nav4.mainloop()

def decrypt_image(parent,im1,new_path):


    # Starting the mixer
    mixer.init()
    # Loading the song
    mazika = "test.mp3"

    if random.randint(1, 3) == 1:
        mazika = "test.mp3"
    elif random.randint(1, 3) == 2:
        mazika = "test2.mp3"
    elif random.randint(1, 3) == 3:
        mazika = "test3.mp3"

    mixer.music.load(mazika)
    # Setting the volume
    mixer.music.set_volume(0.1)
    # Start playing the song
    mixer.music.play()

    nav4 = Toplevel()
    nav4.title("Echo-Tech")
    center_window(nav4, width=240, height=80)

    label2 = Label(nav4, text="Please wait..processing", fg="gray", anchor='w')
    label2.grid(column=1, row=4, columnspan=2, sticky='we', padx=5, pady=2)

    def l():

        # Encrypted image
        img = cv2.imread(im1)
        width = img.shape[0]
        height = img.shape[1]

        # img1 and img2 are two blank images
        img1 = np.zeros((width, height, 3), np.uint8)
        img2 = np.zeros((width, height, 3), np.uint8)

        for i in range(width):
            for j in range(height):
                for l in range(3):
                    v1 = format(img[i][j][l], '08b')
                    v2 = v1[:4] + chr(random.randint(0, 1) + 48) * 4
                    v3 = v1[4:] + chr(random.randint(0, 1) + 48) * 4
                    # Appending data to img1 and img2
                    img1[i][j][l] = int(v2, 2)
                    img2[i][j][l] = int(v3, 2)
                    # These are two images produced from

        cv2.imwrite(new_path, img2)


        img_par8 = ImageTk.PhotoImage(Image.open(new_path).resize((200, 200), Image.ANTIALIAS))
        parent.photo_par8 = img_par8
        canvas_par8 = Canvas(parent, width=200, height=200, highlightthickness=1, highlightbackground="white")
        canvas_par8.grid(column=7, row=4, columnspan=4, rowspan=2, sticky="n")
        canvas_par8.create_image(1, 1, anchor='nw', image=img_par8)

        global pathfinder_label_par8
        pathfinder_label_par8 = ttk.Label(parent, text="")
        pathfinder_label_par8.grid(column=7, row=3, columnspan=4, sticky=W)
        pathfinder_label_par8.configure(text=new_path, anchor='w')


        mixer.music.stop()
        nav4.destroy()

        nav3 = Toplevel()
        nav3.title("Echo-Tech")
        center_window(nav3, width=225, height=80)

        label2 = Label(nav3, text="All Done,You may find the new Image \nin the same directory as the original",
                       fg="gray",
                       anchor='w')
        label2.grid(column=1, row=4, columnspan=2, sticky='we', padx=5, pady=2)

        def open():
            os.system(f"start {new_path[:new_path.rindex('/') + 1]}")

        oopen = Button(nav3, text="Open In Explorer", command=open)
        oopen.grid(row=5, column=1, padx=5, pady=2, columnspan=1, sticky='e')

        def provide_e():

            def submit(h):
                val1 = entry2.get()
                if val1 == "":
                    pass
                else:
                    h.quit()
                    h.withdraw()

            nav = Toplevel()
            nav.title("Echo-Tech")
            center_window(nav, width=225, height=80)

            label2 = Label(nav, text="Enter the reciver email address", fg="gray", anchor='w')
            label2.grid(column=2, row=4, columnspan=4, sticky='we', padx=5, pady=2)

            entry2 = Entry(nav, bg="white", width=35)
            entry2.grid(column=1, row=5, columnspan=4, rowspan=2, sticky='e', padx=5, pady=2)

            SubmitBtn = Button(nav, text="Submit", command=lambda: submit(nav))
            SubmitBtn.grid(row=8, column=4, padx=5, pady=2, sticky='e')

            nav.mainloop()

            return entry2.get()

        em = Button(nav3, text="Send Via Email",
                    command=lambda: send_email(filename=new_path[new_path.rindex('/') + 1:], r_email=provide_e(),
                                               file_path=new_path))
        em.grid(row=5, column=2, padx=5, pady=2, columnspan=1, sticky='e')

        nav3.mainloop()

    def run():
        nav4.after(1000, l())

    t = Thread(target=run)
    t.start()

    nav4.mainloop()


#########################################################

from tkinter import *
from tkinter import ttk , font
from tkinter import filedialog
import tkinter as tk
from PIL import ImageTk,Image
import os, shutil
from pygame import mixer

##############################################

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

    encode_label1 = Label(tool, text="Select the image you want to hide text in",fg="gray",anchor='w').grid(column=1, row=1,columnspan=2,sticky = W)

    encode_label2 = Label(tool, text="Enter the message you want to hide",fg="gray",anchor='w')
    encode_label2.grid(column=1, row=4,columnspan=2,sticky = W)


    encode_entry2 = Text(tool, bg="white",wrap=WORD,height=8, width=30)
    encode_entry2.grid(column=1, row=5,columnspan=4,rowspan=2,sticky = W)

    scrollb = Scrollbar(tool, command=encode_entry2.yview)
    scrollb.grid(column=3, row=5,rowspan=2, sticky='nse')
    encode_entry2['yscrollcommand'] = scrollb.set

    new_name = Text(tool, bg="white",height = 1, width=15)
    new_name.grid(column=5, row=6, rowspan=1,sticky="w")
    new_name_label = Label(tool, text="Enter a name for the new file",fg="gray",anchor='w')
    new_name_label.grid(column=5, row=7, columnspan=5,sticky="w")
    value = new_name


    pathfinder = ttk.Button(tool, text="Browse", command=lambda: fileDailog(parent=tool,big=encode_entry2,small=new_name))
    pathfinder.grid(column=1, row=2, sticky=W)

    def on_closing():
        tool.destroy()
        parent.deiconify()


    tool.protocol("WM_DELETE_WINDOW", on_closing)

    tool.mainloop()

def decode_tool(parent):
    parent.withdraw()

    tool = Toplevel()
    tool.title("Echo-Tech")
    center_window(tool,width=550, height=320)

    griding(tool)

    decode_label1 = Label(tool, text="Select the image that contain the message",fg="gray",anchor='w').grid(column=1, row=1,columnspan=2,sticky = W)

    decode_label2 = Label(tool, text="Here, The message Will appear..",fg="gray",anchor='w')
    decode_label2.grid(column=1, row=4,columnspan=2,sticky = W)

    decode_entry2 = Text(tool, bg="white",wrap=WORD,height=8, width=30,state=DISABLED)
    decode_entry2.grid(column=1, row=5,columnspan=4,rowspan=2,sticky = W)

    scrollb = Scrollbar(tool, command=decode_entry2.yview)
    scrollb.grid(column=3, row=5,rowspan=2, sticky='nse')
    decode_entry2['yscrollcommand'] = scrollb.set


    pathfinder = ttk.Button(tool, text="Browse", command=lambda: fileDailog2(parent=tool,big=decode_entry2))
    pathfinder.grid(column=1, row=2, sticky=W)

    def on_closing():
        tool.destroy()
        parent.deiconify()

    tool.protocol("WM_DELETE_WINDOW", on_closing)
    tool.mainloop()

def en_aud_tool(parent):
    parent.withdraw()

    tool = Toplevel()
    tool.title("Echo-Tech")
    center_window(tool,width=550, height=320)

    griding(tool)

    encode_label1 = Label(tool, text="Select the image you want to hide text in",fg="gray",anchor='w').grid(column=1, row=1,columnspan=2,sticky = W)

    encode_label2 = Label(tool, text="Enter the message you want to hide",fg="gray",anchor='w')
    encode_label2.grid(column=1, row=4,columnspan=2,sticky = W)


    encode_entry2 = Text(tool, bg="white",wrap=WORD,height=8, width=30)
    encode_entry2.grid(column=1, row=5,columnspan=4,rowspan=2,sticky = W)

    scrollb = Scrollbar(tool, command=encode_entry2.yview)
    scrollb.grid(column=3, row=5,rowspan=2, sticky='nse')
    encode_entry2['yscrollcommand'] = scrollb.set

    new_name = Text(tool, bg="white",height = 1, width=15)
    new_name.grid(column=5, row=6, rowspan=1,sticky="w")
    new_name_label = Label(tool, text="Enter a name for the new file",fg="gray",anchor='w')
    new_name_label.grid(column=5, row=7, columnspan=5,sticky="w")
    value = new_name


    pathfinder = ttk.Button(tool, text="Browse", command=lambda: fileDailog3(parent=tool,big=encode_entry2,small=new_name))
    pathfinder.grid(column=1, row=2, sticky=W)

    def on_closing():
        tool.destroy()
        parent.deiconify()


    tool.protocol("WM_DELETE_WINDOW", on_closing)

    tool.mainloop()

def de_aud_tool(parent):
    parent.withdraw()

    tool = Toplevel()
    tool.title("Echo-Tech")
    center_window(tool,width=550, height=320)

    griding(tool)

    encode_label1 = Label(tool, text="Select the file to reveal the message from ",fg="gray",anchor='w').grid(column=1, row=1,columnspan=2,sticky = W)

    encode_label2 = Label(tool, text="Here The message Will appear",fg="gray",anchor='w')
    encode_label2.grid(column=1, row=4,columnspan=2,sticky = W)


    decode_entry2 = Text(tool, bg="white",wrap=WORD,height=8, width=30,state=DISABLED)
    decode_entry2.grid(column=1, row=5,columnspan=4,rowspan=2,sticky = W)

    scrollb = Scrollbar(tool, command=decode_entry2.yview)
    scrollb.grid(column=3, row=5,rowspan=2, sticky='nse')
    decode_entry2['yscrollcommand'] = scrollb.set


    pathfinder = ttk.Button(tool, text="Browse", command=lambda: fileDailog4(parent=tool,big=decode_entry2))
    pathfinder.grid(column=1, row=2, sticky=W)

    def on_closing():
        tool.destroy()
        parent.deiconify()

    tool.protocol("WM_DELETE_WINDOW", on_closing)

    tool.mainloop()

def en_img_tool(parent):
    parent.withdraw()

    tool = Toplevel()
    tool.title("Echo-Tech")
    center_window(tool,width=800, height=350)

    griding(tool)

    encode_label1 = Label(tool, text="Select the file you want to hide", fg="gray", anchor='w')
    encode_label1.grid(column=1, row=1, columnspan=2, sticky=W)

    encode_label2 = Label(tool, text="Select the image you want to hide text in",fg="gray",anchor='w')
    encode_label2.grid(column=4, row=1,columnspan=2,sticky = W)

    new_name = Text(tool, bg="white", height=1, width=15)
    new_name.grid(column=7, row=2, rowspan=1, sticky="w")
    new_name_label = Label(tool, text="Enter a name for the new file", fg="gray", anchor='w')
    new_name_label.grid(column=7, row=1, columnspan=5, sticky="w")
    value = new_name

    pathfinder = ttk.Button(tool, text="Browse", command=lambda: fileDailog5im(parent=tool,cc=1))
    pathfinder.grid(column=1, row=2, sticky=W)

    pathfinder2 = ttk.Button(tool, text="Browse",command=lambda: fileDailog6im(parent=tool,cc=4))
    pathfinder2.grid(column=4, row=2, sticky=W)

    def get_new():
        nn =pathfinder_label2['text']
        return nn[:nn.rindex('/') + 1] + new_name.get('1.0', 'end-1c') + '.png'


    apply_button = Button(tool, text="Apply",height = 1, width = 10, fg="black",command=lambda: encrypt_image(parent=tool,im1=pathfinder_label1['text'],im2=pathfinder_label2['text'],new_path=get_new()))
    apply_button.grid(column=7, row=2, rowspan=1,columnspan=5,sticky="e")

    def on_closing():
        tool.destroy()
        parent.deiconify()


    tool.protocol("WM_DELETE_WINDOW", on_closing)

    tool.mainloop()

def de_img_tool(parent):
    parent.withdraw()

    tool = Toplevel()
    tool.title("Echo-Tech")
    center_window(tool,width=600, height=350)

    griding(tool)

    encode_label1 = Label(tool, text="Select the image you will extract from", fg="gray", anchor='w')
    encode_label1.grid(column=1, row=1, columnspan=2, sticky=W)


    pathfinder = ttk.Button(tool, text="Browse", command=lambda: fileDailog5im(parent=tool,cc=1))
    pathfinder.grid(column=1, row=2, sticky=W)

    new_name = Text(tool, bg="white", height=1, width=15)
    new_name.grid(column=7, row=2, rowspan=1, sticky="w")
    new_name_label = Label(tool, text="Enter a name for the new file", fg="gray", anchor='w')
    new_name_label.grid(column=7, row=1, columnspan=5, sticky="w")

    def get_new():
        nn =pathfinder_label1['text']
        return nn[:nn.rindex('/') + 1] + new_name.get('1.0', 'end-1c') + '.png'

    apply_button = Button(tool, text="Apply",height = 1, width = 10, fg="black",command=lambda: decrypt_image(parent=tool,im1=pathfinder_label1['text'],new_path=get_new()))
    apply_button.grid(column=7, row=2, rowspan=1,columnspan=5,sticky="e")

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
            val1 = entry2.get()
            if val1 == "":
                pass
            else:
                h.quit()
                h.withdraw()

        nav = Toplevel()
        nav.title("Echo-Tech")
        center_window(nav,width=200, height=70)

        label2 = Label(nav, text="Insert a key of your choice", fg="gray", anchor='w')
        label2.grid(column=1, row=4, columnspan=2, sticky='we', padx=5, pady=2)

        entry2 = Entry(nav, bg="white", show="*", width=10)
        entry2.grid(column=1, row=5, rowspan=2, sticky='e', padx=5, pady=2)

        SubmitBtn = Button(nav, text="Submit", command=lambda:submit(nav))
        SubmitBtn.grid(row=5, column=2, padx=5, pady=2,sticky='e')

        nav.mainloop()

        return entry2.get()

    apply_button = Button(parent, text="Apply",height = 1, width = 10, fg="black",command=lambda: encode_text(path=fileName,mss=big.get('1.0', 'end-1c'),new_path=get_new(),key=provide()))
    apply_button.grid(column=5, row=6, rowspan=1,columnspan=5,sticky="e")


    pathfinder_label = ttk.Label(parent, text="")
    pathfinder_label.grid(column=1, row=3,columnspan=4,sticky = W)
    pathfinder_label.configure(text=fileName,anchor='w')

def fileDailog2(parent,big):
    fileName = filedialog.askopenfilename(initialdir = "/", title="Select A File")

    img = ImageTk.PhotoImage(Image.open(fileName).resize((200, 200), Image.ANTIALIAS))
    parent.photo = img
    canvas = Canvas(parent, width = 200, height = 200,highlightthickness=1, highlightbackground="white")
    canvas.grid(row=1, column=5,columnspan=5,rowspan=5, sticky="n")
    canvas.create_image(1, 1, anchor='nw', image=img)

    def provide(textelement):

        def submit(h):
            val1 = entry2.get()
            if val1 == "":
                pass

            else:
                h.quit()
                h.withdraw()

        nav2 = Toplevel()
        nav2.title("Echo-Tech")
        center_window(nav2, width=200, height=70)

        label2 = Label(nav2, text="Provide the secret key...", fg="gray", anchor='w')
        label2.grid(column=1, row=4, columnspan=2, sticky='we', padx=5, pady=2)

        entry2 = Entry(nav2, bg="white", show="*", width=10)
        entry2.grid(column=1, row=5, rowspan=2, sticky='e', padx=5, pady=2)

        SubmitBtn = Button(nav2, text="Submit", command=lambda: submit(nav2))
        SubmitBtn.grid(row=5, column=2, padx=5, pady=2, sticky='e')

        nav2.mainloop()


        textelement.config(state=NORMAL)
        v = textelement.get('1.0', 'end-1c')
        if v != '':
            textelement.delete('1.0', END)
        textelement.config(state=DISABLED)


        return entry2.get()

    apply_button = Button(parent, text="Apply",height = 1, width = 10, fg="black",command=lambda: decode_text(path=fileName,textelement=big,key=provide(textelement=big)))
    apply_button.grid(column=5, row=6, rowspan=1,columnspan=5,sticky="e")


    pathfinder_label = ttk.Label(parent, text="")
    pathfinder_label.grid(column=1, row=3,columnspan=4,sticky = W)
    pathfinder_label.configure(text=fileName,anchor='w')

def fileDailog3(parent,big,small):
    fileName = filedialog.askopenfilename(initialdir = "/", title="Select A File")

    if fileName[fileName.rindex('.'):] == '.wav':
        print('in')
        data, samplerate = soundfile.read(fileName)
        soundfile.write(fileName, data, samplerate)


    frame = Frame(parent, width = 200, height = 200)
    frame.grid(row=1, column=5, columnspan=5, rowspan=5, sticky="n")

    mixer.init()
    mixer.music.load(fileName)

    def pause():
        mixer.music.pause()

    def play():
        mixer.music.play()

    def resume():
        mixer.music.unpause()


    lll1 = Label(frame, text="Feel free to check the right track here").grid(row=2, column=1, columnspan=3)
    Label(frame, text="                                       ").grid(row=3, column=1, columnspan=3,rowspan=1)
    bbb1 =Button(frame,image=start_bu_img, command=play).grid(row=4, column=1)
    bbb2 =Button(frame,image=pause_bu_img, command=pause).grid(row=4, column=2)
    bbb3 =Button(frame,image=resume_bu_img, command=resume).grid(row=4, column=3)


    def get_new():
        return fileName[:fileName.rindex('/') + 1] + small.get('1.0', 'end-1c') + '.wav'

    def provide():

        def submit(h):
            val1 = entry2.get()
            if val1 == "":
                pass
            else:
                h.quit()
                h.withdraw()

        nav = Toplevel()
        nav.title("Echo-Tech")
        center_window(nav,width=200, height=70)

        label2 = Label(nav, text="Insert a key of your choice", fg="gray", anchor='w')
        label2.grid(column=1, row=4, columnspan=2, sticky='we', padx=5, pady=2)

        entry2 = Entry(nav, bg="white", show="*", width=10)
        entry2.grid(column=1, row=5, rowspan=2, sticky='e', padx=5, pady=2)

        SubmitBtn = Button(nav, text="Submit", command=lambda:submit(nav))
        SubmitBtn.grid(row=5, column=2, padx=5, pady=2,sticky='e')

        nav.mainloop()

        return entry2.get()

    apply_button = Button(parent, text="Apply",height = 1, width = 10, fg="black",command=lambda: encode_audio(path=fileName,mss=big.get('1.0', 'end-1c'),new_path=get_new(),key=provide()))
    apply_button.grid(column=5, row=6, rowspan=1,columnspan=5,sticky="e")

    pathfinder_label = ttk.Label(parent, text="")
    pathfinder_label.grid(column=1, row=3,columnspan=4,sticky = W)
    pathfinder_label.configure(text=fileName,anchor='w')

def fileDailog4(parent,big):
    fileName = filedialog.askopenfilename(initialdir = "/", title="Select A File")

    if fileName[fileName.rindex('.'):] == '.wav':
        print('in')
        data, samplerate = soundfile.read(fileName)
        soundfile.write(fileName, data, samplerate)


    frame = Frame(parent, width = 200, height = 200)
    frame.grid(row=1, column=5, columnspan=5, rowspan=5, sticky="n")

    mixer.init()
    mixer.music.load(fileName)

    def pause():
        mixer.music.pause()

    def play():
        mixer.music.play()

    def resume():
        mixer.music.unpause()

    lll1 = Label(frame, text="Feel free to check the right track here").grid(row=2, column=1, columnspan=3)
    Label(frame, text="                                       ").grid(row=3, column=1, columnspan=3,rowspan=1)
    bbb1 =Button(frame,image=start_bu_img, command=play).grid(row=4, column=1)
    bbb2 =Button(frame,image=pause_bu_img, command=pause).grid(row=4, column=2)
    bbb3 =Button(frame,image=resume_bu_img, command=resume).grid(row=4, column=3)

    def provide(textelement):

        def submit(h):
            val1 = entry2.get()
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

        entry2 = Entry(nav2, bg="white", show="*", width=10)
        entry2.grid(column=1, row=5, rowspan=2, sticky='e', padx=5, pady=2)

        SubmitBtn = Button(nav2, text="Submit", command=lambda: submit(nav2))
        SubmitBtn.grid(row=5, column=2, padx=5, pady=2, sticky='e')

        nav2.mainloop()

        textelement.config(state=NORMAL)
        v = textelement.get('1.0', 'end-1c')
        if v != '':
            textelement.delete('1.0', END)
        textelement.config(state=DISABLED)

        return entry2.get()

    apply_button = Button(parent, text="Apply",height = 1, width = 10, fg="black",command=lambda: decode_audio(path=fileName,textelement=big,key=provide(textelement=big)))
    apply_button.grid(column=5, row=6, rowspan=1,columnspan=5,sticky="e")

    pathfinder_label = ttk.Label(parent, text="")
    pathfinder_label.grid(column=1, row=3,columnspan=4,sticky = W)
    pathfinder_label.configure(text=fileName,anchor='w')

def fileDailog5im(parent,cc):
    fileName = filedialog.askopenfilename(initialdir = "/", title="Select A File")

    img1 = ImageTk.PhotoImage(Image.open(fileName).resize((200, 200), Image.ANTIALIAS))
    parent.photo1 = img1
    canvas1 = Canvas(parent, width = 200, height = 200,highlightthickness=1, highlightbackground="white")
    canvas1.grid(column=cc, row=4,columnspan=2,rowspan=2,sticky = "n")
    canvas1.create_image(1, 1, anchor='nw', image=img1)

    global pathfinder_label1
    pathfinder_label1 = ttk.Label(parent, text="")
    pathfinder_label1.grid(column=cc, row=3,columnspan=4,sticky = W)
    pathfinder_label1.configure(text=fileName,anchor='w')

def fileDailog6im(parent,cc):
    fileName = filedialog.askopenfilename(initialdir = "/", title="Select A File")

    img2 = ImageTk.PhotoImage(Image.open(fileName).resize((200, 200), Image.ANTIALIAS))
    parent.photo2 = img2
    canvas2 = Canvas(parent, width = 200, height = 200,highlightthickness=1, highlightbackground="white")
    canvas2.grid(column=cc, row=4,columnspan=2,rowspan=2,sticky = "n")
    canvas2.create_image(1, 1, anchor='nw', image=img2)

    global pathfinder_label2
    pathfinder_label2 = ttk.Label(parent, text="")
    pathfinder_label2.grid(column=cc, row=3,columnspan=4,sticky = W)
    pathfinder_label2.configure(text=fileName,anchor='w')

window=Tk()
window['background'] = 'black'
window.title("@Echo-Tech")
center_window(window, width=913, height=502)
window.wm_iconbitmap('./assets/logo.ico')
immakilldisguy = "./assets/bg1.png"
canva = tk.Canvas(window, width=910, height=500)
imagez = ImageTk.PhotoImage(file=immakilldisguy)
canva.create_image(0, 0, image=imagez, anchor=NW)
canva.create_rectangle(0, 0, 100, 40)
canva.grid(column=0, row=0, columnspan=13, rowspan=13)
window.resizable(False, False)


def about_us(parent):
    parent.withdraw()
    level = Toplevel()
    level.title("About Us")
    center_window(level, width=825, height=380)
    level.wm_iconbitmap('./assets/logo.ico')
    # griding(level)
    level['background'] = 'grey'
    Omar = PhotoImage(file=r"./assets/omarzain.png")
    omar_x = Omar.subsample(3, 3)
    Diana = PhotoImage(file=r"./assets/diana.png")
    diana_x = Diana.subsample(3, 3)
    Hadi = PhotoImage(file=r"./assets/hadi.png")
    hadi_x = Hadi.subsample(3, 3)
    Aya = PhotoImage(file=r"./assets/aya.png")
    aya_x = Aya.subsample(3, 3)
    omar_pic = Label(level, text="Omar Zain \n I'm a Software Developer", image=omar_x, relief="raised", borderwidth=9,
                     compound=TOP, fg="black").grid(column=1, row=1, padx="8", pady=40)
    diana_pic = Label(level, text="Diana Alshafie\n I'm a Software Developer", image=diana_x, relief="raised",
                      borderwidth=9, compound=TOP, fg="black").grid(column=2, row=1, padx="8", pady=40)
    hadi_pic = Label(level, text="Hadi Aji \n I'm a Software Developer", image=hadi_x, compound=TOP, fg="black",
                     relief="raised", borderwidth=9).grid(column=3, row=1, padx="8", pady=40)
    aya_pic = Label(level, text="Aya Rashed \n I'm a Software Developer", image=aya_x, compound=TOP, fg="black",
                    relief="raised", borderwidth=9).grid(column=4, row=1, padx="8", pady=40)
    Echo_Tech = Label(level, text="Echo Tech Team", font='Helvetica 25 bold', fg="black").grid(column=2, row=2,
                                                                                               rowspan="20",
                                                                                               columnspan=2)
    def on_closing():
        level.destroy()
        parent.deiconify()
    level.protocol("WM_DELETE_WINDOW", on_closing)
    level.mainloop()

start_bu = PhotoImage(file= r"./assets/starti.png")
start_bu_img = start_bu.subsample(3, 3)

pause_bu = PhotoImage(file= r"./assets/pause.png")
pause_bu_img = pause_bu.subsample(3, 3)

resume_bu = PhotoImage(file= r"./assets/resume.png")
resume_bu_img = resume_bu.subsample(3, 3)



about = PhotoImage(file=r"./assets/aboutus.png")
aboutUS = about.subsample(5, 7)

imim = PhotoImage(file=r"./assets/text0.png")
lock = imim.subsample(9, 12)

imim2 = PhotoImage(file=r"./assets/text1.png")
unlock = imim2.subsample(9, 12)

pip1 = PhotoImage(file=r"./assets/pip1.png")
pips1 = pip1.subsample(8, 9)

pip2 = PhotoImage(file=r"./assets/pip2.png")
pips2 = pip2.subsample(8, 9)

imim3 = PhotoImage(file=r"./assets/audio_lock.png")
Audio_1 = imim3.subsample(7, 12)

imim4 = PhotoImage(file=r"./assets/audio_unlock.png")
Audio_2 = imim4.subsample(7, 12)

encode_button = Button(window, text="Hide A Message \n inside image", image=lock, compound=LEFT, fg="black",relief="flat", borderwidth=5, font='Helvetica 9 bold',command=lambda: encode_tool(parent=window))
encode_button.grid(column=1, row=2)

decode_button = Button(window, text="Reveal A Hidden \n Message", image=unlock, compound=LEFT, fg="black",relief="flat", borderwidth=5, font='Helvetica 9 bold',command=lambda: decode_tool(parent=window))
decode_button.grid(column=3, row=2)

encode_audio_o = Button(window, text="Hide a Text \n inside audio ", image=Audio_1, compound=LEFT, fg="black",relief="flat", borderwidth=5, font='Helvetica 9 bold',command=lambda: en_aud_tool(parent=window))
encode_audio_o.grid(column=1, row=3, pady=40)

decode_audio2 = Button(window, text="Reveal a text \n from audio", image=Audio_2, compound=LEFT, fg="black",relief="flat", borderwidth=5, font='Helvetica 9 bold',command=lambda: de_aud_tool(parent=window))
decode_audio2.grid(column=3, row=3, pady=40)

encode_pip = Button(window, text="Hide picture \n inside picture ", image=pips1, compound=LEFT, fg="black",relief="flat", borderwidth=5, font='Helvetica 9 bold',command=lambda: en_img_tool(parent=window))
encode_pip.grid(column=1, row=5)

decode_pip = Button(window, text="Reveal a picture \n from picture", image=pips2, compound=LEFT, fg="black",relief="flat", borderwidth=3, font='Helvetica 9 bold',command=lambda: de_img_tool(parent=window))
decode_pip.grid(column=3, row=5)

about_us_bu = Button(window, image=aboutUS, compound=LEFT, fg="black", relief="flat", borderwidth=6,command=lambda: about_us(parent=window))
about_us_bu.grid(column=1, row=10, columnspan=1, ipadx=8)

window.mainloop()
