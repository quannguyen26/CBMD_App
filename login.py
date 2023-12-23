import tkinter as tk
from PIL import ImageTk
from tkinter import messagebox
window_login=tk.Tk()
window_login.title("Đăng nhập phần mềm")
window_login.geometry("1200x780+85+10")
window_login.resizable(False,False)
background_image=ImageTk.PhotoImage(file='app_images/backgroud_login.png')
bg_label=tk.Label(image=background_image)
bg_label.grid(row=0,column=0)
login_frame=tk.Frame(window_login)
login_frame.place(x=500,y=300)

def login(event=None):
    if user_entry.get()=='' or password_entry.get()=='':
        messagebox.showerror('Lỗi','Chưa nhập thông tin đăng nhập')
    elif user_entry.get()=='nguyenkhacquan' and password_entry.get()=='12345':
        window_login.destroy()
        name_user="Nguyễn Khắc Quân"
        import cbmd
    else:
        messagebox.showerror("Lỗi",'Tài khoản hoặc mật khẩu không đúng')

tk.Label(login_frame,text="ĐĂNG NHẬP",font=('Arial 20')).grid(row=0,column=0,columnspan=2,padx=20,pady=(20,10))
tk.Label(login_frame,text="Tên đăng nhập:",font=('Arial 10')).grid(row=1,column=0,pady=5,padx=(20,0))
tk.Label(login_frame,text='Mật khẩu:',font=('Arial 10')).grid(row=2,column=0,sticky='e',pady=5)
user_entry=tk.Entry(login_frame,font=('Arial 10'))
user_entry.grid(row=1,column=1,pady=5,padx=(0,30))
user_entry.focus()
password_entry=tk.Entry(login_frame,show='*',font=('Arial 10'))
password_entry.grid(row=2,column=1,pady=5,padx=(0,30))
login_button=tk.Button(login_frame,text='Đăng nhập',font=('Arial 10'),command=login,width=15,fg='black',
                       bg='cornflowerblue',activebackground='cornflowerblue',activeforeground='cornflowerblue',cursor='hand2')
window_login.bind('<Return>',login)
login_button.grid(row=3,column=0,columnspan=2,pady=(10,20))
window_login.mainloop()