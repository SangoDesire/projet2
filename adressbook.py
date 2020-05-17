# -*- coding: utf-8 -*-
#---------------------------------
# Author     :   Younes Derfoufi
# Company    :   CRMEF OUJDA
#--------------------------------
from shutil import copyfile
from tkinter import ttk
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
import os
from PIL import Image, ImageTk
import sqlite3  
Profil = {1:""}



def iExit():
    iExit = tkinter.messagebox.askyesno("Carnet D'Address","Vous Souhaitez Quittez L'Application?")
    if iExit > 0:
        root.destroy()
        return

def add_customer():
    name = entryName.get()
    phone = entryPhone.get()
    more = entryMore.get()
    
    # Create connection
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    #Insert data
    cur.execute("INSERT INTO customers(`name` , `phone`, `moreinfo`) VALUES (?,?,?)", (name , phone, more))
    # commit connection
    conn.commit()
    conn.close()
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    select = cur.execute("SELECT*FROM customers order by id desc")
    select = list(select)
    tree.insert('' , END , values = select[0] )
    conn.close()
    # Photo profile
    filename = entryPhoto.get()
    ext = filename.split(".")
    id = select[0][0]
    copyfile(filename, "images/profil_" + str(id) +"."+ext[len(ext)-1])
    im = Image.open("images/profil_" +str(id) +"."+ext[len(ext)-1])
    rgb_im = im.convert('RGB')
    rgb_im.save ("images/profil_" + str(id) + ".jpg")
    conn.close()    
    
  

def delete_customer():
    idSelect = tree.item(tree.selection())['values'][0]
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    delete = cur.execute("delete from customers where id = {}".format(idSelect))
    conn.commit()
    conn.close()
    tree.delete(tree.selection())
    
def sortByName(): 
    # clear the treeview
    for i in tree.get_children():
        tree.delete(i)
    # create connection
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    select = cur.execute("select*from customers order by `name` asc")
    conn.commit()
    for row in select:
        tree.insert('' , END , values = row)
    conn.close() 

def SearchByName(event):
    for i in tree.get_children():
        tree.delete(i)

    name = entrySearchByName.get()

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    select = cur.execute("SELECT * FROM customers where `name` = (?) " , (name,))
    conn.commit()
    select = list(select)
    for row in select:
        tree.insert('' , END , values = row )

    conn.close()

def SearchByPhone(event):
    for i in tree.get_children():
        tree.delete(i)

    phone = entrySearchByPhone.get()

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    select = cur.execute("SELECT*FROM customers where `phone` = (?) " , (phone,))
    conn.commit()
    select = list(select)
    for row in select:
        tree.insert('' , END , values = row )
    conn.close()
    
def BrowsePhoto():
    entryPhoto.delete(0, END)
    filename = filedialog.askopenfilename(initialdir= "/",title="Select File")
    print(filename)  
    entryPhoto.insert(END , filename)
def treeActionSelect(event):
    # load image
    label_image.destroy()
    idSelect = tree.item(tree.selection())['values'][0]
    nameSelect = tree.item(tree.selection())['values'][1]
    phoneSelect = tree.item(tree.selection())['values'][2]
    moreInfoSelect = tree.item(tree.selection())['values'][3]
    imgProfile = "images/profil_" + str(idSelect) + "." + "jpg"
    load = Image.open(imgProfile)
    load.thumbnail((100,100))
    photo = ImageTk.PhotoImage(load)
    Profil[1] = photo
    lblImage = Label(root ,  image = photo)
    lblImage.place(x=10 , y=350)
    lid = Label(root, text = "ID : " + str(idSelect))
    lid.place(x = 110, y = 350 , width = 50)
    lname = Label(root, text = " name : " + nameSelect)
    lname.place(x=110 , y = 380 , width = 150)
    lphone = Label(root, text = "Phone : " + str(phoneSelect))
    lphone.place(x = 110 , y = 410 , width = 150)
    Tmore = Text(root)
    Tmore.place(x = 260 , y = 360 , width = 280 , height =100)
    Tmore.insert(END , "More Info : " +  moreInfoSelect)

root = Tk()
root.title("MON CARNET D'ADRESSES")
root.iconbitmap('images/icon_Ikw_2.ico')
#root.geometry("550x480")
root.maxsize(1279,750)
root.minsize(650,450)
#root.configure(bg = "green")
#==================================================
# Style
root.configure(background="#e1d8b2")
style=ttk.Style()
style.theme_use("classic")
#..................................................
#insertion d'image de font
mon_image=ImageTk.PhotoImage(Image.open("images/dez.jpg"))
mon_label=Label(image=mon_image)
mon_label.pack(side="right")
# Add Title
lblTitle = Label(root , text = "CARNET D'ADRESSES " , font = ("Arial" , 16) , bg="darkblue" ,fg = "white" )
lblTitle.place(x=0 , y=0 , width=250)

# Search area
lbSearchByName = Label(root , text = "Rechercher par Nom :", bg="darkblue",fg = "white")
lbSearchByName.place(x=280 , y=0 , width=130)
entrySearchByName = Entry(root,bd=2,font=("arial",11),fg="red",cursor="iron_cross")
entrySearchByName.bind("<Return>", SearchByName)
entrySearchByName.place(x=410 , y=0 , width=162)

lbSearchByPhone = Label(root , text = "Rechercher par phone :" , bg="darkblue" ,fg = "white")
lbSearchByPhone.place(x=280,y=20 , width=130)
entrySearchByPhone = Entry(root,bd=2,font=("arial",11),fg="red",cursor="heart")
entrySearchByPhone.place(x=410 , y=20 , width=162)
entrySearchByPhone.bind("<Return>", SearchByPhone)

# Label & Entry name
lblName = Label(root , text = "Nom et Prénoms:" ,  bg="black" , fg = "yellow")
lblName.place(x=5 , y = 50 , width = 155)
entryName = Entry(root,cursor="X_cursor")
entryName.place(x = 170,  y =50 , width=400)

# Label & Entry Phone
lblPhone = Label(root , text = "N° de Téléphone:" , bg="black" , fg = "yellow")
lblPhone.place(x=5 , y=80 ,  width = 155 )
entryPhone = Entry(root,cursor="X_cursor")
entryPhone.place(x = 170,  y =80 , width=400)

# Label & Entry Photo
lblPhoto = Label(root , text = "Photo:" , bg="black" , fg = "yellow")
lblPhoto.place(x=5 , y=110 ,  width = 155 )
bPhoto = Button(root , text = "Charger" , bg="darkblue" , fg = "yellow" ,  command = BrowsePhoto )
bPhoto.place(x= 480 ,  y = 110 , height = 25, width=90)
entryPhoto = Entry(root,cursor="X_cursor")
entryPhoto.place(x = 170,  y =110 , width=300)

#More Info
lblMore = Label(root , text = "Plus d'Info:" , bg="black" , fg = "yellow")
lblMore.place(x=5 , y=140 ,  width = 155 )
entryMore = Entry(root,cursor="X_cursor")
entryMore.place(x = 170,  y =140 , width=400)

#Command Button
bAdd = Button(root , text = "Ajout de Client" , bg="darkblue" , fg = "yellow" , command = add_customer)
bAdd.place(x= 5 ,  y = 170 , width = 155)

bDelete = Button(root , text = "Suppression" , bg="darkblue" , fg = "yellow" , command = delete_customer)
bDelete.place(x= 5 ,  y = 205 , width = 155)

bEdit = Button(root , text = "Edition" , bg="darkblue" , fg = "yellow" )
bEdit.place(x= 5 ,  y = 240 , width = 155)

bSort= Button(root , text = "Trie par Nom" , bg="darkblue" , fg = "yellow" , command = sortByName )
bSort.place(x= 5 ,  y = 275 , width = 155)

bExit= Button(root , text = "Quitez " , bg="darkblue" , fg = "yellow" , command =iExit)
bExit.place(x= 5 ,  y = 310 , width = 155)


# Load Image
load = Image.open("images/profil.jpg")
load.thumbnail((1279,130))
photo = ImageTk.PhotoImage(load)
label_image = Label(root,image=photo)
label_image.place(x=10, y=350)

# Add Treeview
tree = ttk.Treeview(root, columns =(1,2,3), height = 5 , show ="headings")
tree.place(x=170, y=170, width = 400, height = 175)
tree.bind("<<TreeviewSelect>>", treeActionSelect)

# Add scrollbar
vsb = ttk.Scrollbar(root , orient="vertical",command=tree.yview)
vsb.place(x=550, y=205, height=136)
tree.configure(yscrollcommand=vsb.set)

# Add headings
tree.heading(1, text = "ID")
tree.heading(2, text = "NOM")
tree.heading(3, text = "TELEPHONE")

#Define column width
tree.column(1, width=50)
tree.column(2, width=100)
tree.column(3, width=100)

# Display data in treeview object
conn = sqlite3.connect("database.db")
cur = conn.cursor()
select = cur.execute ("select * from customers")
for row in select:
    tree.insert('' , END , values = row)
conn.close()

root.mainloop()