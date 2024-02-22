from tkinter import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import xlsxwriter





def disappear(a):
    a.place(x=0,y=0,width=0,height=0)

def disappear_all():
    global labels
    global entries
    global buttons
    for i in labels:
        disappear(i)
    for i in entries:
        disappear(i)
        i.delete(0,END)
    for i in buttons:
        disappear(i)
    disappear(submit_button)
def clear_all():
    for i in entries:
        i.delete(0,END)

def appear():
    label1.place(x=50,y=80,width=150,height=20)
    label2.place(x=50, y=110, width=150, height=20)
    entry1.place(x=200,y=80,width=150,height=20)
    entry2.place(x=200, y=110, width=150, height=20)

def FIFO():
    global k
    k='FIFO'
    disappear_all()
    clear_all()

def LIFO():
    global k
    k='LIFO'
    disappear_all()
    clear_all()

def MSTKf():
    global k
    k='MSTK'
    disappear_all()
    clear_all()


def agora():
    disappear_all()
    appear()
    submit_button.place(x=350,y=140,width=50,height=20)
    global litourgia
    litourgia='agora'

def polisi():
    disappear_all()
    appear()
    submit_button.place(x=350,y=140,width=50,height=20)
    global litourgia
    litourgia='polisi'

def submit():
    q=int(entry1.get())
    p=float(entry2.get())
    clear_all()
    enimerosi_apothematos(q,p)
    if litourgia=='polisi':
        enimerosi_poliseon(q*p)

    disappear_all()
    clear_all()

def enimerosi_apothematos(q,p):
    global inventory_data
    global mstk
    if litourgia=='agora':
        global agores
        agores=agores+q*p
        if k=='MSTK':
            if inventory_data.at[0, 'Τιμή'] == 0:
                inventory_data.at[0, 'Τιμή'] = p
                inventory_data.at[0, 'Ποσότητα']=q
                mstk=p
            else:
                mstk=(inventory_data.at[0, 'Ποσότητα']*mstk+p*q)/(inventory_data.at[0,'Ποσότητα']+q)
                inventory_data.at[0, 'Τιμή']=mstk
                inventory_data.at[0, 'Ποσότητα']+=q
        else:
            if len(inventory_data)==1:
                if inventory_data.at[0, 'Τιμή'] == 0:
                    inventory_data.at[0, 'Τιμή'] = p
            a=0
            i=0
            while a==0 and i<=len(inventory_data)-1:
                if inventory_data.at[i, 'Τιμή'] == p:
                    print('ok')
                    inventory_data.at[i, 'Ποσότητα']+=q
                    a=1
                i+=1
            if a==0:
                inventory_data.loc[len(inventory_data)]=[q,p]

    if litourgia=='polisi':
        global kp
        if k=='FIFO':
            for i in range(0,len(inventory_data)):
                if inventory_data.at[i,'Ποσότητα']>q:
                    inventory_data.at[i, 'Ποσότητα']-=q
                    kp+=q*inventory_data.at[i, 'Τιμή']
                    q=0
                else:
                    kp+=inventory_data.at[i, 'Ποσότητα']*inventory_data.at[i,'Τιμή']
                    q-=inventory_data.at[i,'Ποσότητα']
                    inventory_data=inventory_data.drop(i,axis=0)
            inventory_data.index = range(0, len(inventory_data))
        elif k=='LIFO':
            for i in range(len(inventory_data)-1,-1,-1):
                if inventory_data.at[i,'Ποσότητα']>=q:
                    inventory_data.at[i, 'Ποσότητα']-=q
                    kp+=q*inventory_data.at[i, 'Τιμή']
                    i=len(inventory_data)+1
                else:
                    kp+=inventory_data.at[i, 'Ποσότητα']*inventory_data.at[i,'Τιμή']
                    q-=inventory_data.at[i,'Ποσότητα']
                    inventory_data=inventory_data.drop(i,axis=0)
            inventory_data.index = range(0, len(inventory_data))
        else:
            kp+=mstk*q
            inventory_data.at[0, 'Ποσότητα']-=q


    save_apothemata()
def save_apothemata():
    global inventory_data
    global path
    inventory_data.to_excel(path + 'Απόθεμα.xlsx',index=False)
    print(inventory_data)


def enimerosi_poliseon(polisi):
    month = date.today().month

    if month == 1:
        month = 'Ιανο.'
    elif month == 2:
        month = 'Φεβρ.'
    elif month == 3:
        month = 'Μαρτ.'
    elif month == 4:
        month = 'Απρι.'
    elif month == 5:
        month = 'Μαιο.'
    elif month == 6:
        month = 'Ιουν.'
    elif month == 7:
        month = 'Ιουλ.'
    elif month == 8:
        month = 'Αυγο.'
    elif month == 9:
        month = 'Σεπτ.'
    elif month == 10:
        month = 'Οκτο.'
    elif month == 11:
        month = 'Νοεμ.'
    elif month == 12:
        month = 'Δεκε.'
    global sales_data
    sales_data.loc[month]['Πωλήσεις'] += polisi
    plott(sales_data)
    save(sales_data)
    describe(sales_data)

def plott(df):
    plt.plot(df['Πωλήσεις'], c='r')
    global months
    global path
    plt.savefig(path+'διάγραμμα.png')


def save(df):
    global path
    df.to_excel(path+'Αναλυτικές Πωλήσεις ανά Μήνα.xlsx')
    print(df)

def describe(df):
    global path
    global kp
    global agores
    data2=df.describe()
    list=[]
    list.append(data2.at['mean','Πωλήσεις'])
    list.append(data2.at['min','Πωλήσεις'])
    list.append(data2.at['max', 'Πωλήσεις'])
    list.append(kp)
    list.append(agores)
    indexes=['μέσος αριθμός πωλήσεων ανά μήνα:','ελάχιστος αριθμός πωλήσεων ανά μήνα:','μέγιστος αριθμός πωλήσεων ανά μήνα:', 'κόστος πωλήσεων','αγορές']
    data=pd.DataFrame(np.array(indexes).reshape((5,1)),columns=['Στοιχείο'])
    data['Τιμή']=list
    print(data)
    writer=pd.ExcelWriter(path+'Στατιστικά Στοιχεία.xlsx',engine='xlsxwriter')
    data.to_excel(writer,index=False,sheet_name='Sheet1')
    workbook=writer.book
    worksheet=writer.sheets['Sheet1']
    for i, col in enumerate(data.columns):
        width=max(data[col].apply(lambda x:len(str(x))).max(),len(data[col]))
        worksheet.set_column(i,i,width)
    writer.close()


window=Tk()
window.title('Αποθέματα')
window.geometry('600x600')

menubar=Menu(window)
window.config(menu=menubar)
menubar.add_command(label='Αγορά',command=agora)
menubar.add_command(label='Πώληση',command=polisi)

labels=[]
entries=[]
buttons=[]

label=Label(window,text='Επιλέξτε μέθοδο')
label1=Label(window,text='Ποσότητα')
label2=Label(window,text='Τιμή ανά μονάδα')

labels.append(label)
labels.append(label1)
labels.append(label2)

entry1=Entry(window,font=('Arial',10))
entry2=Entry(window,font=('Arial',10))
entry3=Entry(window,font=('Arial',10))

entries.append(entry1)
entries.append(entry2)

button1=Button(text='FIFO',command=FIFO)
button2=Button(text='LIFO',command=LIFO)
button3=Button(text='ΜΣΤΚ',command=MSTKf)
submit_button=Button(text='OK',command=submit)

buttons.append(button1)
buttons.append(button2)
buttons.append(button3)

label.place(x=250,y=80,width=100,height=20)
button1.place(x=150,y=110,width=100,height=20)
button2.place(x=250,y=110,width=100,height=20)
button3.place(x=350,y=110,width=100,height=20)

global path
path="C:/Users/tsapn/OneDrive/Υπολογιστής/codes/python/finance applications/Αποθέματα/database/"
global sales_data
sales_data=pd.DataFrame(pd.read_excel(path+'Αναλυτικές Πωλήσεις ανά Μήνα.xlsx',header=None,skiprows=[0],usecols=[1]).astype(float))
global months
months=['Ιανο.','Φεβρ.','Μαρτ.','Απρι.','Μαιο.','Ιουν.','Ιουλ.','Αυγο.','Σεπτ.','Οκτο.','Νοεμ.','Δεκε.']
sales_data.index=months
sales_data.columns=['Πωλήσεις']
global inventory_data
inventory_data=pd.DataFrame(pd.read_excel(path+'Απόθεμα.xlsx',header=None,skiprows=[0]).astype(float))
inventory_data.columns=['Ποσότητα','Τιμή']
global kp
global agores
global mstk
mstk=0
global k
data=pd.DataFrame(pd.read_excel(path+'Στατιστικά Στοιχεία.xlsx',header=None,skiprows=[0],usecols=[1]).astype(float))
kp=data.at[3,1]
agores=data.at[4,1]
window.mainloop()