import tkinter as tk
from PIL import ImageTk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
import os
import sys
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path) 
window_login=tk.Tk()
window_login.title("Đăng nhập phần mềm")
window_login.geometry("1200x780+170+10")
window_login.resizable(False,False)
background_image=ImageTk.PhotoImage(file=resource_path('app_images\\backgroud_login.png'))
icon_image=ImageTk.PhotoImage(file=resource_path('app_images\\radar.ico'))
bg_label=tk.Label(image=background_image)
window_login.iconphoto(False, icon_image)
bg_label.grid(row=0,column=0)
login_frame=tk.Frame(window_login)
login_frame.place(x=500,y=300)
def saving_login(values):
   cbmd_db=mysql.connector.connect(
      host="localhost",
      user="root",
      password="quanlam26",
      database="custorm")
   mycursor = cbmd_db.cursor()
   query='''INSERT INTO cbmd_login (name_login,date_login) VALUES (%s,%s)'''
   date=datetime.now()
   val=(values,date)
   mycursor.execute(query,val)
   cbmd_db.commit()
   cbmd_db.close()

def login(event=None):
    if user_entry.get()=='' or password_entry.get()=='':
        messagebox.showerror('Lỗi','Chưa nhập thông tin đăng nhập')
    elif user_entry.get()=='nguyenkhacquan' and password_entry.get()=='12345':
        saving_login("Nguyễn Khắc Quân")
        window_login.destroy()
        import main
    elif user_entry.get()=='tranvanquy' and password_entry.get()=='123456':
        saving_login("Trần Văn Quý")
        window_login.destroy()
        import main
    elif user_entry.get()=='vangatung' and password_entry.get()=='1234567':
        saving_login("Vàng A Tùng")
        window_login.destroy()
        import main    
    else:
        messagebox.showerror("Lỗi",'Tài khoản hoặc mật khẩu không đúng')

tk.Label(login_frame,text="ĐĂNG NHẬP",font=('Arial 20')).grid(row=0,column=0,columnspan=2,padx=20,pady=(20,10))
tk.Label(login_frame,text="Tên đăng nhập:",font=('Arial 10')).grid(row=1,column=0,pady=5,padx=(20,0))
tk.Label(login_frame,text='Mật khẩu:',font=('Arial 10')).grid(row=2,column=0,sticky='e',pady=5)
user_var=tk.StringVar
user_entry=tk.Entry(login_frame,font=('Arial 10'),textvariable=user_var)
user_entry.grid(row=1,column=1,pady=5,padx=(0,30))
user_entry.focus()
password_entry=tk.Entry(login_frame,show='*',font=('Arial 10'))
password_entry.grid(row=2,column=1,pady=5,padx=(0,30))
login_button=tk.Button(login_frame,text='Đăng nhập',font=('Arial 10'),command=login,width=15,fg='black',
                       bg='cornflowerblue',activebackground='cornflowerblue',activeforeground='cornflowerblue',cursor='hand2')
window_login.bind('<Return>',login)
login_button.grid(row=3,column=0,columnspan=2,pady=(10,20))
window_login.mainloop()