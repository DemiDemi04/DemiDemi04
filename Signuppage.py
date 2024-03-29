from tkinter import *
from tkinter import messagebox
import ast
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Darian123123',
    database='matched_faces'
)
cursor = conn.cursor()

window=Tk()
window.title('Signup')
window.geometry('903x603')
window.config(bg="#fff")
window.resizable(False,False)

def signup():
    username=user.get()
    password=code.get()
    confirm_password=codeconfirm.get()
    
    if password==confirm_password:
        try:
            file=open('datasheet.txt','r+')
            d=file.read()
            r=ast.literal_eval(d)
            
            dict2={username:password}
            r.update(dict2)
            file.truncate(0)
            file.close()
            
            file=open('datasheet.txt',"w")
            w=file.write(str(r))
            
            messagebox.showinfo('Signup','Successfully sign up')
            
        except:
            file=open('datasheet.txt','w')
            pp=str({'Username':'password'})
            file.write(pp)
            file.close()
            
    else:
        messagebox.showerror('Invalid',"Both Password should match")
        
def sign():
    window.destroy()   

img = PhotoImage(file="website_images/facerecog,900x600.png")
Label(window,image=img,border=0,bg='white').place(x=1,y=1)

frame=Frame(window,width=400,height=370,bg='white')
frame.place(x=270,y=130)

heading=Label(frame,text='Sign up',fg='#57a1f8',bg='white',font=('Microsoft Yahei UI Light',23,'bold'))
heading.place(x=145,y=5)

##############

def on_enter(e):
    user.delete(0, 'end')
    
def on_leave(e):
    if user.get()=='':
        user.insert(0,'Username')

user = Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
user.place(x=70,y=80)
user.insert(0,'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame,width=250,height=2,bg='black').place(x=70,y=107)




################------------

def on_enter(e):
    code.delete(0, 'end')
    
def on_leave(e):
    if code.get()=='':
        code.insert(0,'Password')
        
code = Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
code.place(x=70,y=150)
code.insert(0,'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

Frame(frame,width=250,height=2,bg='black').place(x=70,y=177)

##########-----------------

def on_enter(e):
    codeconfirm.delete(0, 'end')
    
def on_leave(e):
    if codeconfirm.get()=='':
        codeconfirm.insert(0,'Confirm Password')
        
codeconfirm = Entry(frame,width=25,fg='black',border=0,show='*',bg='white',font=('Microsoft Yahei UI Light',11))
codeconfirm.place(x=70,y=220)
codeconfirm.insert(0,'Confirm Password')
codeconfirm.bind('<FocusIn>', on_enter)
codeconfirm.bind('<FocusOut>', on_leave)

Frame(frame,width=250,height=2,bg='black').place(x=70,y=247)
###############----------------------------------

Button(frame,width=39,pady=7,text='Sign up', bg='#56a1f8',fg='white',border=0,command=signup).place(x=57,y=280)
label=Label(frame,text="I have an account",fg='black',bg='white',font=('Microsoft Yahei UI Light',9))
label.place(x=120,y=330)

signin= Button(frame,width=6,text='Sign in',border=0,bg='white', cursor='hand2',fg='#57a1f8',command=sign)
signin.place(x=220,y=330)

window.mainloop()