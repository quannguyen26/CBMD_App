import tkinter as tk
from tkcalendar import DateEntry
from docx.shared import Mm
from tkinter.ttk import Combobox
from tkinter import messagebox
from PIL import Image,ImageTk
from datetime import datetime
import os
import io
import sys
import shutil
from docxtpl import DocxTemplate,InlineImage
import provinces as pr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders,utils
import mysql.connector
import subprocess

#----------------------------------------------------------------------------------
def connection_sql():
   cbmd_db=mysql.connector.connect(
      host="localhost",
      user="root",
      password="quanlam26",
      database="custorm"
   )
   return cbmd_db
###### Search in database   
###### Def for searching news from Database ###
def check_in_sql(myresult_now,myresult_13h,districts,checkbutton_now,checkbutton_13h): 
   if myresult_now =="Tất cả":
      for i in range(0,len(checkbutton_now)):checkbutton_now[i].select(),checkbutton_13h[i].configure(state="disabled")  
   elif myresult_13h =="Tất cả":
      for i in range(0,len(checkbutton_13h)):checkbutton_13h[i].select(),checkbutton_now[i].configure(state="disabled")
   else:
      for name in myresult_now.split(", "):
         for name_var,chk1,chk2 in zip(districts,checkbutton_now[:-1],checkbutton_13h[:-1]): 
            if name ==name_var:chk1.select(),chk2.configure(state="disabled")
      for name in myresult_13h.split(", "):
         for name_var,chk1,chk2 in zip(districts,checkbutton_13h[:-1],checkbutton_now[:-1]): 
            if name ==name_var:chk1.select(),chk2.configure(state="disabled") 
def searh():
   clear_button(for_=1)
   cbmd_db=connection_sql()
   mycursor = cbmd_db.cursor()
   mycursor.execute("SELECT MAX(id_news) FROM cbmd_database")
   id_news=mycursor.fetchone()[0] + 1
   if searh_ent_var.get()>= id_news:
      messagebox.showerror('Lỗi',"Không có bản tin số " + str(searh_ent_var.get()))
      cbmd_db.close()
   else:
      #clear_button()
      try:
         query="SELECT * FROM cbmd_database WHERE id_news= %s"
         mycursor.execute(query,(searh_ent_var.get(),))
         myresult = mycursor.fetchone()
         number_news_ent_var.set(myresult[0])
         h_weather_now_var.set(myresult[1][:2])
         m_weather_now_var.set(myresult[1][3:5])
         date_now_ent_var.set(myresult[2])
         kind_news_cbb.set(myresult[3])
         direc_cbb.set(myresult[4])
         velo_cbb.set(myresult[5])
         zmax_spin_var.set(myresult[6])
         for chk in chks_max:chk.set(False)
         for name in myresult[7].split(", "):
            for name_var, chk in zip(province_names,chks_max): 
               if name ==name_var:chk.set(True) 
         charac_pre.set(myresult[8]) 
         hail_var.set(myresult[9])
         h_time_send_var.set(myresult[10][:2])
         m_time_send_var.set(myresult[10][3:5])
         day_time_send_var.set(myresult[11])
         person_send_var.set(myresult[12])
         binary_data = myresult[13]
         img = Image.open(io.BytesIO(binary_data))
         img.save(resource_path("radar_images\\"+str(myresult[0])+".png"))
         img=img.resize((520,460))
         img=ImageTk.PhotoImage(img)
         image_label.configure(image=img)
         image_label.image=img
         link_pic.insert(0,"radar_images\\"+str(myresult[0])+".png")
         check_in_sql(myresult[14],myresult[15],pr.province_districts["Lai Châu"],checkbutton_lc_now,checkbutton_lc_13h)
         check_in_sql(myresult[16],myresult[17],pr.province_districts["Điện Biên"],checkbutton_db_now,checkbutton_db_13h)
         check_in_sql(myresult[18],myresult[19],pr.province_districts["Sơn La"],checkbutton_sl_now,checkbutton_sl_13h)
         check_in_sql(myresult[20],myresult[21],pr.province_districts["Hòa Bình"],checkbutton_hb_now,checkbutton_hb_13h)
         check_in_sql(myresult[22],myresult[23],pr.province_districts["Lào Cai"],checkbutton_lcai_now,checkbutton_lcai_13h)
         check_in_sql(myresult[24],myresult[25],pr.province_districts["Yên Bái"],checkbutton_yb_now,checkbutton_yb_13h)
         cbmd_db.close()
         update = dict_update()
         dict1.update(update)
         obser=person_idnews()
         if obser!=person_send_var.get():
            update_news["state"] ="disabled"
            send_ttram["state"]="disabled"
            send_all["state"]="disabled"
            save_news["state"]="disabled"
         else:
            update_news["state"] ="normal"
            send_ttram["state"]="normal"
            send_all["state"]="normal"
            save_news["state"]="normal"
      except:
         messagebox.showerror('Lỗi',"Không có bản tin số " + str(searh_ent_var.get()))
         cbmd_db.close()

#### Def for save information in database #######      
def byte_string(image_name):
   with open(image_name, 'rb') as image_file:
      encoded_string = image_file.read()
   return encoded_string
def save_provinces(all_chk,districts): 
   lst_now = [districts[i] for i, chk in enumerate(all_chk) if chk.get()]
   if len(lst_now)==0:
            lc=""
   elif len(lst_now)!=0 and len(lst_now)<len(districts[:]):
            lc=', '.join(lst_now)
   elif len(lst_now)==len(districts[:]):
            lc="Tất cả"
   return lc
def saving_database():
   cbmd_db=connection_sql()
   mycursor = cbmd_db.cursor()
   query='''INSERT INTO cbmd_database (id_news,time_now,date_now,kind_news,Derection,Velocity,Zmax,location_zmax,
                                       weather13next,hail,time_send,day_send,observer,image,laichau_now,laichau_13h,
                                       dienbien_now,dienbien_13h,sonla_now,sonla_13h,hoabinh_now,hoabinh_13h,
                                       laocai_now,laocai_13h,yenbai_now,yenbai_13h,name_file) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
         '''
   val=(number_news_ent_var.get(),h_weather_now_var.get()+":"+m_weather_now_var.get(),
         date_now_ent_var.get(),kind_news_cbb.get(),direc_cbb.get(),velo_cbb.get(),
         zmax_spin_var.get(),', '.join([province_names[i] for i, chk in enumerate(chks_max) if chk.get()]),
         charac_pre.get(),hail_var.get(),h_time_send_var.get()+":"+m_time_send_var.get(),
         day_time_send_var.get(),person_send_var.get(),byte_string(resource_path("radar_images\\"+str(number_news_ent_var.get())+".png")),
         save_provinces(chks_lc,pr.province_districts["Lai Châu"]),save_provinces(chks_lc_13h,pr.province_districts["Lai Châu"]),
         save_provinces(chks_db,pr.province_districts["Điện Biên"]),save_provinces(chks_db_13h,pr.province_districts["Điện Biên"]),
         save_provinces(chks_sl,pr.province_districts["Sơn La"]),save_provinces(chks_sl_13h,pr.province_districts["Sơn La"]),
         save_provinces(chks_hb,pr.province_districts["Hòa Bình"]),save_provinces(chks_hb_13h,pr.province_districts["Hòa Bình"]),
         save_provinces(chks_lcai,pr.province_districts["Lào Cai"]),save_provinces(chks_lcai_13h,pr.province_districts["Lào Cai"]),
         save_provinces(chks_yb,pr.province_districts["Yên Bái"]),save_provinces(chks_yb_13h,pr.province_districts["Yên Bái"]),
         path_file_news
        )
   mycursor.execute(query,val)
   cbmd_db.commit()
   cbmd_db.close() 

####Def for get path file news from database##
#Hàm để lấy link của file_name đã lưu sử dụng trong việc xóa file cũ thay fiel mới
def get_linkfile_database():
   cbmd_db=connection_sql()
   mycursor = cbmd_db.cursor()
   query="SELECT name_file FROM cbmd_database WHERE id_news= %s"
   mycursor.execute(query,(number_news_ent_var.get(),))
   link_news = mycursor.fetchone()[0]
   cbmd_db.close()
   return link_news

#### Def for update in database #####
def update_database(for_=0):
   if for_==1:
      try:
         old_file_path=get_linkfile_database()
         os.remove(old_file_path)
         save_file()
      except:
         save_file()
         
   cbmd_db=mysql.connector.connect(
      host="localhost",
      user="root",
      password="quanlam26",
      database="custorm")
   mycursor = cbmd_db.cursor()
   query='''UPDATE cbmd_database SET time_now = %s,date_now = %s,kind_news = %s,Derection = %s,Velocity = %s,Zmax = %s,location_zmax = %s,
               weather13next = %s,hail = %s,time_send = %s,day_send = %s,observer = %s,image = %s,laichau_now = %s,laichau_13h = %s,
               dienbien_now = %s,dienbien_13h = %s,sonla_now = %s,sonla_13h = %s,hoabinh_now = %s,hoabinh_13h = %s,
               laocai_now = %s,laocai_13h = %s,yenbai_now = %s,yenbai_13h = %s, name_file= %s WHERE id_news= %s 
           '''
   val=(h_weather_now_var.get()+":"+m_weather_now_var.get(),
         date_now_ent_var.get(),kind_news_cbb.get(),direc_cbb.get(),velo_cbb.get(),
         zmax_spin_var.get(),', '.join([province_names[i] for i, chk in enumerate(chks_max) if chk.get()]),
         charac_pre.get(),hail_var.get(),h_time_send_var.get()+":"+m_time_send_var.get(),
         day_time_send_var.get(),person_send_var.get(),byte_string(resource_path("radar_images\\"+str(number_news_ent_var.get())+".png")),
         save_provinces(chks_lc,pr.province_districts["Lai Châu"]),save_provinces(chks_lc_13h,pr.province_districts["Lai Châu"]),
         save_provinces(chks_db,pr.province_districts["Điện Biên"]),save_provinces(chks_db_13h,pr.province_districts["Điện Biên"]),
         save_provinces(chks_sl,pr.province_districts["Sơn La"]),save_provinces(chks_sl_13h,pr.province_districts["Sơn La"]),
         save_provinces(chks_hb,pr.province_districts["Hòa Bình"]),save_provinces(chks_hb_13h,pr.province_districts["Hòa Bình"]),
         save_provinces(chks_lcai,pr.province_districts["Lào Cai"]),save_provinces(chks_lcai_13h,pr.province_districts["Lào Cai"]),
         save_provinces(chks_yb,pr.province_districts["Yên Bái"]),save_provinces(chks_yb_13h,pr.province_districts["Yên Bái"]),path_file_news,
         number_news_ent_var.get()
        )
   mycursor.execute(query,val)
   cbmd_db.commit()
   cbmd_db.close()
   #clear_button()
#### Def for get lastest id_news
def lastest_idnews():
   cbmd_db=mysql.connector.connect(
         host="localhost",
         user="root",
         password="quanlam26",
         database="custorm")
   mycursor = cbmd_db.cursor()
   mycursor.execute("SELECT MAX(id_news) FROM cbmd_database")
   id_news=mycursor.fetchone()[0]
   cbmd_db.close()
   return id_news
##Def for change lastesr news from fill new_entry_var ######
def update_label_img(event):
    try:
        value = number_news_ent_var.get()
        lastest_id=lastest_idnews()
        # Kiểm tra nếu giá trị lớn hơn 10
        if value > lastest_id:
            image_label.config(image='')
            link_pic.insert(0,"capture.png")
            observer=person_idnews()
            person_send1.set(observer)
            if observer==person_send_var.get():
               update_news["state"]="normal"
               send_ttram["state"]="normal"
               send_all["state"]="normal"
               save_news["state"]="normal"
               searh_ent_var.set("")
        else:
            pass
    except:
        pass
        # Xử lý trường hợp nếu giá trị không phải là số
         #messagebox.showerror("Lỗi","Giá trị nhập vào không đúng")
    
## Def for change betwee now/1_3h weather button ######
def change_to_now():
   weather_now_frame1.grid(row=1,column=0,sticky="W",pady=(5,0))
   weather_1_3h.grid_forget()
   now_button.configure(bg='lightblue')
   h_1_3_next.configure(bg="#f0f0f0")
def change_to_1_3h_next():
   weather_1_3h.grid(row=1,column=0,sticky="W",pady=(5,0))
   weather_now_frame1.grid_forget()
   h_1_3_next.configure(bg='lightblue')
   now_button.configure(bg="#f0f0f0")

##### Def to get relative_path
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path) 

def sniping_image():
   ##### Def to snipping images #########
   window.withdraw()
   sub=subprocess.Popen(['python' , 'sniping.py'],stdout=subprocess.PIPE)
   sub.wait()
   new_name=str(number_news_ent_var.get())+".png"
   try:
      os.rename('capture.png', new_name)
      try:
         os.remove(resource_path("radar_images\\"+new_name))
         shutil.move(new_name,resource_path("radar_images\\"))
      except OSError:
         shutil.move(new_name,resource_path("radar_images\\"))
      
      link_pic.insert(0,"radar_images\\"+new_name)
      img=Image.open(resource_path("radar_images\\"+new_name),"r")
      img=img.resize((520,460))
      img=ImageTk.PhotoImage(img)
      image_label.configure(image=img)
      image_label.image=img  
   except:
      pass
   window.deiconify()

def my_upd(*args):
    #Funtion to update now date for sending date
    day_time_send_var.set(date_now_ent_var.get())

def person_idnews():
   ######## Def to update for require must save ######
   cbmd_db=mysql.connector.connect(
         host="localhost",
         user="root",
         password="quanlam26",
         database="custorm")
   mycursor = cbmd_db.cursor()
   mycursor.execute("SELECT name_login FROM cbmd_login ORDER BY date_login DESC LIMIT 1")
   observer=mycursor.fetchone()[0]
   #number_news_ent_var.set(id_news)
   cbmd_db.close()
   return observer

def dict_update():
   ######## Def to update for require must save ######
   now_update=[]
   to_13h_update=[]
   def append_list_update(all_chks_agument,n):  
      for j,all_chks in enumerate(all_chks_agument):
         lst_now = [pr.province_districts[province_names[j]][i] for i, chk in enumerate(all_chks) if chk.get()]
         n.append(lst_now)
   append_list_update(all_chks_now,now_update)
   append_list_update(all_chks_13h,to_13h_update)
   dict={'id_news':number_news_ent_var.get(),'now_date':date_now_ent_var.get(),'kind_news':kind_news_cbb.get(),
                              'h_wea_now':h_weather_now_var.get(),'m_wea_now':m_weather_now_var.get(),
                              'zmax': zmax_spin_var.get(),'loca_max':[province_names[i] for i, chk in enumerate(chks_max) if chk.get()],
                              'velocity': velo_cbb.get(),'direc':direc_cbb.get(),
                              'mc1':now_update,'mc2':to_13h_update,
                              'charac_pre':charac_pre.get(),'hail':hail_var.get(),'send_date':day_time_send_var.get(),
                              'h_send':h_time_send_var.get(),'m_send':m_time_send_var.get(),'per_send':person_send_var.get()}
   return dict
######### Def for saving file docx news ############
def saving_news():
   global name_file
   searh_ent_var.set("") # make search to blank
   lst_max = [province_names[i] for i, chk in enumerate(chks_max) if chk.get()]
   #set for Zmax at provinces
   #######
   all_1_now=[[],[]]
   all_2_now=[[],[]]
   all_1_1=[]
   def append_list(all_chks_agument,n): 
      for j,all_chks in enumerate(all_chks_agument):
         lst_now = [pr.province_districts[province_names[j]][i] for i, chk in enumerate(all_chks) if chk.get()]
         if len(lst_now)!=0 and len(lst_now)<len(pr.province_districts[province_names[j]][:]):
            lc="huyện "+', '.join(lst_now)+" ("+province_names[j]+")"
            all_1_now[n].append(lc)
            all_1_1.append(province_names[j])
         elif len(lst_now)==len(list(pr.province_districts[province_names[j]][:])):
            all_2_now[n].append(province_names[j])      
   def news_finall(all_1,all_2):
      if len(all_1)==0 and len(all_2)!=0:
         mc1=""
         mc2="các huyện thuộc tỉnh "+', '.join(all_2)
      elif len(all_1)>0 and len(all_2)!=0:
         mc2=" và tất cả các huyện thuộc tỉnh "+', '.join(all_2)
         mc1='; '.join(all_1)
      elif len(all_2)==0 and len(all_1)>0:
         mc2=""
         mc1='; '.join(all_1)
      return mc1,mc2
   append_list(all_chks_now,0)
   append_list(all_chks_13h,1)
   
   ###### ERROR Notifications######
   if number_news_ent.get()=="" or len(lst_max)==0 or direc_cbb.get()=="" or len(all_1_1)==0 or link_pic[0]=='capture.png':
      messagebox.showerror("Lỗi","Thiếu trường dữ liệu")
      #fill Document
   else:
      try:
         mc1,mc2=news_finall(all_1_now[0],all_2_now[0])
         mc3,mc4=news_finall(all_1_now[1],all_2_now[1])
         mc5=', '.join(list(set(all_1_1+all_2_now[0]+all_2_now[1])))
      except UnboundLocalError:
         messagebox.showerror("Lỗi","Thiếu trường dữ liệu")
      else:
         if hail_var.get() ==1: hail=", mưa đá" 
         else: hail=""
         doc=DocxTemplate(resource_path("dong_tpl\\dongtpl.docx"))
         context={
               "num_tin":number_news_ent.get(),"day":day_time_send_var.get()[0:2],"mon":day_time_send_var.get()[3:5],
               "year":day_time_send_var.get()[6:10],"kind_news":kind_news_cbb.get(),"h":h_weather_now.get(),"m":m_weather_now.get(),
               "mc1":mc1,"mc2":mc2,"mc3":mc3,"mc4":mc4,"mc5":mc5,
               "dBZ":zmax_spin.get(),"direc":direc_cbb.get(),"velo":velo_cbb.get(),"province_max":', '.join(lst_max),
               "pic":InlineImage(doc,resource_path(link_pic[0]),width=Mm(120),height=Mm(110)),"dayp":date_now_ent_var.get()[0:2],"monp":date_now_ent_var.get()[3:5],
               "yearp":date_now_ent_var.get()[6:10],"charac_pre":charac_pre.get(),"hail":hail,"h_send":h_time_send.get(),
               "m_send":m_time_send.get(),"person_send":person_send1.get()
         } 
         doc.render(context)
            #name file news
         if kind_news_cbb.get() =="CẢNH BÁO MƯA DÔNG":
            title_file="DONG"
         else:
            title_file="MLDR"
         name_file="PDIN_"+title_file+"_"+day_time_send_var.get()[6:10]+day_time_send_var.get()[3:5]+day_time_send_var.get()[0:2]+"_"+h_time_send.get()+"h"+m_time_send.get()+".docx"
         file_path="news\\"+name_file
         try:
            update = dict_update()
            dict1.update(update)
            doc.save(resource_path(file_path))
            messagebox.showinfo("Lưu tin", "Đã lưu bản tin: "+name_file)
         except:
            messagebox.showerror("Lỗi","Không lưu được tin")

########## Def for clear #################
def clear_button(for_=0):
   def clear():
      global dict1,link_pic,name_file
      change_to_now()
      kind_news_cbb.set("CẢNH BÁO MƯA DÔNG")
      lastest_id=lastest_idnews()
      number_news_ent_var.set(lastest_id+1)
      date_now_ent_var.set(datetime.now().strftime("%d/%m/%Y"))
      h_weather_now_var.set('00')
      m_weather_now_var.set('00')
      zmax_spin_var.set(40)
      velo_cbb.set('20 – 25')
      direc_cbb.set('')
      for chk in chks_max:chk.set(False)
      for chks_now,chks_13h in zip(all_chks_now,all_chks_13h):
         for chk_now,chk_13h in zip(chks_now,chks_13h):
            chk_now.set(False)
            chk_13h.set(False)
      list_=[checkbutton_lc_now,checkbutton_lc_13h,checkbutton_db_now,checkbutton_db_13h,checkbutton_sl_now,checkbutton_sl_13h,
         checkbutton_hb_now,checkbutton_hb_13h,checkbutton_lcai_now,checkbutton_lcai_13h,checkbutton_yb_now,checkbutton_yb_13h]     
      for chks in list_:
         for j in chks:
            j.configure(state="normal")  
         #for chk in for_clear_all_var:chk.set(False)
      charac_pre.set("mưa, mưa rào và dông")
      hail_var.set(0)
      day_time_send_var.set(datetime.now().strftime("%d/%m/%Y"))
      h_time_send_var.set('00')
      m_time_send_var.set('00')
      observer=person_idnews()
      person_send1.set(observer)
      image_label.config(image='')
      link_pic=["capture.png"]
      name_file=""
      dict1 = {'id_news':0,'now_date':'','kind_news':'','h_wea_now':'','m_wea_now':'','zmax': 0,'loca_max':'', 'velocity':'', 'direc':'',
            'mc1':'','mc2':'','charac_pre':'','hail':0,'send_date':'','h_send':'','m_send':'','per_send':'','m_wea_now':''}
      update_news["state"]="normal"
      send_ttram["state"]="normal"
      send_all["state"]="normal"
      save_news["state"]="normal"
      def remove_file(link_file,extention):
         for f in os.listdir(link_file):
            if not f.endswith(extention):
               continue
            os.remove(os.path.join(link_file, f))
      remove_file(resource_path("news\\"),".docx")
      remove_file(resource_path("radar_images\\"),".png")
   if for_==0:
      searh_ent_var.set("")
      clear()
   elif for_==1:
      clear()

########### Def to Save file news into folder###########
def save_file():
      global path_file_news
      dict2=dict_update()
      if name_file=="" or dict1 != dict2:
         messagebox.showerror("Lỗi","Chưa lưu bản tin")
      else:
         path_folder=resource_path("D:\\CBMD-"+name_file[10:14]+"\\"+name_file[14:16])
         if not os.path.exists(path_folder):
            os.makedirs(path_folder)
         shutil.move(resource_path("news\\"+name_file), path_folder)
         path_file_news=resource_path(path_folder+"\\"+name_file)

###### Def to Send gmail to adresses ######
def send_mail_button(ed_send):
   def send_mail(email_list):
      pswd = "kyvofwfivxxltzuu" 
      email_from = "radaphadintaybac@gmail.com"
      msg = MIMEMultipart()
      msg['From'] = utils.formataddr(('Ra đa Pha Đin', email_from))
      msg['To'] = email_list
      subject=day_time_send_var.get()[0:2]+"."+day_time_send_var.get()[3:5]+"."+day_time_send_var.get()[6:10]+"- "+"Bản tin cảnh báo mưa dông.RDPD -"+ number_news_ent.get()
      msg['Subject'] = subject
      html = '''<p><i>**************<br>
      Trạm Ra đa thời tiết Pha Đin<br>
      Đài Khí tượng Thủy văn khu vực Miền núi phía Bắc<br>
      Địa chỉ: Xã Tỏa Tình - Huyện Tuần Giáo - Tỉnh Điện Biên<br>
      Điện thoại:  0326 086 288<br>
      Email: radaphadintaybac@gmail.com</i></p>'''
      msg.attach(MIMEText(html, 'html'))
      try:
         attachment= open("news\\"+name_file, 'rb')  # r for read and b for binary
         # Encode as base 64
         attachment_package = MIMEBase('application', 'octet-stream')
         attachment_package.set_payload((attachment).read())
         encoders.encode_base64(attachment_package)
         attachment_package.add_header('Content-Disposition', "attachment; filename= " + name_file)
         msg.attach(attachment_package)
      # Cast as string
         text = msg.as_string()
      # Connect with the server
         TIE_server = smtplib.SMTP("smtp.gmail.com", 587)
         TIE_server.starttls()
         TIE_server.login(email_from, pswd)
         TIE_server.sendmail(email_from, email_list, text)  
      # Close the port
         TIE_server.quit()
      except:
         messagebox.showerror("Lỗi","Chưa lưu bản tin")

   #Read mail edress from dong_tpl\\mail.txt   
   with open(resource_path('dong_tpl\\mail.txt'), 'r') as file:
      content_list = [line.strip() for line in file.readlines() if not line.startswith('#')]
   
   #Chọn tới các địa chỉ: 0=các địa chỉ; 1= trưởng trạm
   if ed_send==0: #Tới các địa chỉ
      dict2=dict_update()
      if dict1 == dict2:
         lastest_id=lastest_idnews()
         if number_news_ent_var.get() > lastest_id:
            #send_mail(", ".join(content_list[:]))
            print("Gửi tới các địa chỉ")
            save_file()
            saving_database()
            clear_button()
         else:
            ask_update=messagebox.askokcancel("Tin này đã được gửi","Bạn có muốn gửi lại?")
            if ask_update:
               #send_mail(", ".join(content_list[:]))
               old_file_path=get_linkfile_database()
               try:
                  os.remove(old_file_path)
               except:
                  pass
               save_file()
               update_database(for_=0)   
               print("Gửi lại tới các địa chỉ")
               clear_button()          
      else:
         messagebox.showerror("Lỗi","Chưa lưu bản tin")
   elif ed_send==1: #tới trưởng trạm
      dict2=dict_update()
      if dict1 == dict2:
         send_mail(content_list[0])
         print("Gửi tới trưởng trạm")
      else:
         messagebox.showerror("Lỗi","Chưa lưu bản tin")
#Def to logout, back to login
def logout():
   window.destroy()
   subprocess.Popen(['python' , 'login.py'],stdout=subprocess.PIPE)
#---------------------------------------------------------------------------------

#name of provinces
province_names =list(pr.province_districts.keys())
name_lchau=list(pr.province_districts.keys())[0]
name_dbien=list(pr.province_districts.keys())[1]
name_sla=list(pr.province_districts.keys())[2]
name_hbinh=list(pr.province_districts.keys())[3]
name_lcai=list(pr.province_districts.keys())[4]
name_ybai=list(pr.province_districts.keys())[5]
#######
window=tk.Tk()
window.title("Phần mềm ra bản tin cảnh báo mưa dông")
window.config(bg="skyblue",padx=0,pady=0)
window.geometry("1200x780+150+0")
window.resizable(False,False)

#### VARS #####
searh_ent_var=tk.IntVar(value="")
number_news_ent_var=tk.IntVar()
date_now_ent_var=tk.StringVar()
day_time_send_var=tk.StringVar()
h_weather_now_var=tk.StringVar()
m_weather_now_var=tk.StringVar()
h_time_send_var=tk.StringVar()
m_time_send_var=tk.StringVar()
zmax_spin_var=tk.IntVar()
chks_max = [tk.BooleanVar() for i in province_names] #var for zmax
hail_var=tk.IntVar()
person_send_var=tk.StringVar()
##All var for provinces
chks_lc = [tk.BooleanVar() for i in pr.province_districts["Lai Châu"]]
chks_lc_13h = [tk.BooleanVar() for i in pr.province_districts["Lai Châu"]]
chks_db = [tk.BooleanVar() for i in pr.province_districts["Điện Biên"]]
chks_db_13h = [tk.BooleanVar() for i in pr.province_districts["Điện Biên"]]
chks_sl = [tk.BooleanVar() for i in pr.province_districts["Sơn La"]]
chks_sl_13h = [tk.BooleanVar() for i in pr.province_districts["Sơn La"]]
chks_hb = [tk.BooleanVar() for i in pr.province_districts["Hòa Bình"]]
chks_hb_13h = [tk.BooleanVar() for i in pr.province_districts["Hòa Bình"]]
chks_lcai = [tk.BooleanVar() for i in pr.province_districts["Lào Cai"]]
chks_lcai_13h = [tk.BooleanVar() for i in pr.province_districts["Lào Cai"]]
chks_yb = [tk.BooleanVar() for i in pr.province_districts["Yên Bái"]]
chks_yb_13h = [tk.BooleanVar() for i in pr.province_districts["Yên Bái"]]
all_chks_now=[chks_lc,chks_db,chks_sl,chks_hb,chks_lcai,chks_yb]
all_chks_13h=[chks_lc_13h,chks_db_13h,chks_sl_13h,chks_hb_13h,chks_lcai_13h,chks_yb_13h]
###########

tk.Label(window, text='BẢN TIN CẢNH BÁO MƯA DÔNG TRÊN KHU VỰC MIỀN NÚI PHÍA BẮC',bg="skyblue",font=("Times New Roman",18)).pack(fill="x",pady=(5,25))
searh_ent_var=tk.IntVar(value="")
searh_ent=tk.Entry(window,textvariable=searh_ent_var,width=15,font=("Times New Roman",16))
searh_ent.place(x=870,y=38)
searh_button=tk.Button(window,text="Tìm kiếm",font=("Times New Roman",11),width=10,command=searh,cursor='hand2')
searh_button.place(x=1050,y=37)
frame=tk.Frame(window,bg="skyblue")
frame.pack(padx=20,pady=10)
#window=> fame
#frame1
information_frame1=tk.Frame(frame,highlightbackground="black", highlightthickness=1)
information_frame1.grid(row=0,column=0,columnspan=2)

tk.Label(information_frame1,text="Số bản tin: ").grid(row=0,column=0,padx=(50,0),pady=10)
number_news_ent=tk.Entry(information_frame1,textvariable=number_news_ent_var,width=10)
number_news_ent.grid(row=0,column=1)
number_news_ent.bind("<KeyRelease>", update_label_img)

tk.Label(information_frame1,text="Ngày:").grid(row=0,column=2, padx=(40,0))
date_now_ent=DateEntry(information_frame1,selectmode='day',date_pattern="dd/mm/yyyy",locale='vi',textvariable=date_now_ent_var)
date_now_ent.grid(row=0,column=3)

tk.Label(information_frame1,text="Loại bản tin: ").grid(row=0,column=4, padx=(40,0))
kind_news_cbb=Combobox(information_frame1,width=32,values=['CẢNH BÁO MƯA DÔNG','CẢNH BÁO MƯA DÔNG DIỆN RỘNG'],state="readonly")
kind_news_cbb.set('CẢNH BÁO MƯA DÔNG')
kind_news_cbb.grid(row=0, column=5)

now_button=tk.Button(information_frame1,text="Hiện tại",width=20,command=change_to_now,cursor='hand2')
now_button.grid(row=0, column=6,padx=(45,0))
h_1_3_next=tk.Button(information_frame1,text="Từ 1-3 giờ tới ",width=20,command=change_to_1_3h_next,cursor='hand2')
h_1_3_next.grid(row=0, column=7,padx=(30,82))

#frame2_left
##weather_now_informations
weather_now_frame1=tk.Frame(frame,highlightbackground="black", highlightthickness=1)
weather_now_frame1.grid(row=1,column=0,sticky="W", pady=(5,0))
##infomation_weather_now
info_wea_now=tk.Frame(weather_now_frame1)
info_wea_now.grid(row=0,column=0,pady=(10,0),padx=10)
tk.Label(info_wea_now,text="Thời gian:").grid(row=0,column=0)

h_weather_now=tk.Spinbox(info_wea_now,from_=0,to=23,textvariable=h_weather_now_var, width=3,format="%02.0f")
h_weather_now.grid(row=0,column=1)
tk.Label(info_wea_now,text=":").grid(row=0,column=2)

m_weather_now=tk.Spinbox(info_wea_now,from_=0,to=50, width=3,textvariable=m_weather_now_var, increment=10,format="%02.0f")
m_weather_now.grid(row=0,column=3)

tk.Label(info_wea_now,text="Zmax:").grid(row=0,column=4, padx=(10,0))
zmax_spin=tk.Spinbox(info_wea_now,from_=40,to=62,textvariable=zmax_spin_var, width=5)
zmax_spin.grid(row=0,column=5)

tk.Label(info_wea_now,text="Hướng dịch chuyển:").grid(row=0,column=6, padx=(10,0))
direc_cbb=Combobox(info_wea_now,values=["Bắc","Bắc Đông Bắc","Đông Bắc","Đông Đông Bắc","Đông",
                                        "Đông Đông Nam","Đông Nam","Nam Đông Nam","Nam","Nam Tây Nam",
                                        "Tây Nam","Tây Tây Nam","Tây","Tây Tây Bắc", "Tây Bắc","Bắc Tây Bắc"],width=15,state="readonly")
direc_cbb.grid(row=0,column=7)

#Velocity
tk.Label(info_wea_now,text="Vận tốc:").grid(row=0,column=8, padx=(10,0))
velo_cbb=Combobox(info_wea_now,values=["10 – 15","15 – 20","20 – 25", "25 – 30","30 – 35","35 – 40"],width=6,state="readonly")
velo_cbb.grid(row=0,column=9)

##location_Max_dbZ
location_max_frame=tk.Frame(weather_now_frame1)
location_max_frame.grid(row=1,column=0,pady=5)
tk.Label(location_max_frame,text="Cực đại PHVT tại:").pack(side='left')
for i, name in enumerate(province_names):
    sks=tk.Checkbutton(location_max_frame, text=name, variable=chks_max[i])
    sks.pack(side='left')

#weather_1_3h_informations
weather_1_3h=tk.Frame(frame,highlightbackground="black", highlightthickness=1)
info_wea_1_3h=tk.Frame(weather_1_3h)
info_wea_1_3h.grid(row=0,column=0,pady=(10,0),padx=10,sticky="w")
tk.Label(info_wea_1_3h,text=" Kiểu thời tiết từ 1-3 giờ tới:").grid(row=0,column=0)

charac_pre=Combobox(info_wea_1_3h,width=40,values=["mưa, mưa rào và dông","mưa, mưa vừa, có nơi mưa to và dông"],state="readonly")
charac_pre.grid(row=0,column=1)

severe_weather=tk.Checkbutton(info_wea_1_3h,text="Mưa đá",variable=hail_var,onvalue=1,offvalue=0)
severe_weather.grid(row=1,column=0,pady=(5,0)) 

#weather_now_frame
provivce_wea_now=tk.Frame(weather_now_frame1)
provivce_wea_now.grid(row=3,column=0,pady=(0,5))
#wether_1_3h_frame
provivce_wea_1_3h=tk.Frame(weather_1_3h)
provivce_wea_1_3h.grid(row=1,column=0,pady=5,padx=(61,61.5))
#Lai_Chau
lchau_frame_now=tk.LabelFrame(provivce_wea_now,text=name_lchau)
lchau_frame_now.grid(row=0,column=0,pady=(0,5),sticky="w")
lchau_frame_13h=tk.LabelFrame(provivce_wea_1_3h,text=name_lchau + " từ 1-3 giờ tới")
lchau_frame_13h.grid(row=0,column=1,pady=(0,5),sticky='w')
checkbutton_lc_now,checkbutton_lc_13h=pr.even_check_buttons(name_lchau,lchau_frame_now,lchau_frame_13h,chks_lc,chks_lc_13h,2,8)
#Dien_Bien
dbien_frame_now=tk.LabelFrame(provivce_wea_now,text=name_dbien)
dbien_frame_now.grid(row=1,column=0,pady=(0,5),sticky="w")
dbien_frame_13h=tk.LabelFrame(provivce_wea_1_3h,text=name_dbien + " từ 1-3 giờ tới")
dbien_frame_13h.grid(row=1,column=1,pady=(0,5),sticky="w")
checkbutton_db_now, checkbutton_db_13h=pr.odd_check_buttons(name_dbien,dbien_frame_now,dbien_frame_13h,chks_db,chks_db_13h,2,0)
#Son_La
sla_frame_now=tk.LabelFrame(provivce_wea_now,text=name_sla)
sla_frame_now.grid(row=2,column=0,pady=(0,5),sticky="w")
sla_frame_13h=tk.LabelFrame(provivce_wea_1_3h,text=name_sla + " từ 1-3 giờ tới")
sla_frame_13h.grid(row=2,column=1,pady=(0,5),sticky="w")
checkbutton_sl_now, checkbutton_sl_13h=pr.even_check_buttons(name_sla,sla_frame_now,sla_frame_13h,chks_sl,chks_sl_13h,3,8)
#Hoa_Binh
hb_frame_now=tk.LabelFrame(provivce_wea_now,text=name_hbinh)
hb_frame_now.grid(row=3,column=0,pady=(0,5),sticky="w")
hb_frame_13h=tk.LabelFrame(provivce_wea_1_3h,text=name_hbinh + " từ 1-3 giờ tới")
hb_frame_13h.grid(row=3,column=1,pady=(0,5),sticky="w")
checkbutton_hb_now, checkbutton_hb_13h=pr.odd_check_buttons(name_hbinh,hb_frame_now,hb_frame_13h,chks_hb,chks_hb_13h,3,9)
#Lao_Cai
lcai_frame_now=tk.LabelFrame(provivce_wea_now,text=name_lcai)
lcai_frame_now.grid(row=4,column=0,pady=(0,5),sticky="w")
lcai_frame_13h=tk.LabelFrame(provivce_wea_1_3h,text=name_lcai + " từ 1-3 giờ tới")
lcai_frame_13h.grid(row=4,column=1,pady=(0,5),sticky="w")
checkbutton_lcai_now, checkbutton_lcai_13h=pr.odd_check_buttons(name_lcai,lcai_frame_now,lcai_frame_13h,chks_lcai,chks_lcai_13h,1,9)
#Yen_Bai
ybai_frame_now=tk.LabelFrame(provivce_wea_now,text=name_ybai)
ybai_frame_now.grid(row=5,column=0,pady=(0,5),sticky="w")
ybai_frame_13h=tk.LabelFrame(provivce_wea_1_3h,text=name_ybai + "  từ 1-3 giờ tới")
ybai_frame_13h.grid(row=5,column=1,pady=(0,5),sticky="w")
checkbutton_yb_now, checkbutton_yb_13h=pr.odd_check_buttons(name_ybai,ybai_frame_now,ybai_frame_13h,chks_yb,chks_yb_13h,1,8)

#frame_2_right
image_save_frame=tk.Frame(frame,bg="skyblue")
image_save_frame.grid(row=1,column=1)
image_frame=tk.Frame(image_save_frame,highlightbackground="black", highlightthickness=1,relief="groove")
image_frame.grid(row=0,column=0,padx=(5,0), pady=(5,0),sticky="n")
#------
image_none=tk.Label(image_frame,text="Ảnh")
image_none.grid(row=0,column=0, padx=250, pady=(255,188))
image_label=tk.Label(image_frame)
image_label.grid(row=0,column=0,sticky="n") 
sniping_but=tk.Button(image_frame,text="Cắt ảnh",bg='lightblue',command=sniping_image,cursor='hand2')
sniping_but.grid(row=1,column=0, pady=5,ipadx=10,ipady=5)


#Save frame
save_frame=tk.Frame(image_save_frame,highlightbackground="black", highlightthickness=1)
save_frame.grid(row=1,column=0,pady=(5,0),padx=(5,0),sticky="news")
#------
h_frame_save=tk.Frame(save_frame)
h_frame_save.grid(row=0,column=0, sticky="news", pady=5,padx=(10,0))

tk.Label(h_frame_save,text="Giờ phát tin:").grid(row=0,column=0)
h_time_send=tk.Spinbox(h_frame_save,textvariable=h_time_send_var,from_=0,to=23, width=3,format="%02.0f")
h_time_send.grid(row=0,column=1)
tk.Label(h_frame_save,text=":").grid(row=0,column=2)
m_time_send=tk.Spinbox(h_frame_save,from_=0,to=55,textvariable=m_time_send_var, width=3, increment=5,format="%02.0f")
m_time_send.grid(row=0,column=3,padx=(0,10))
tk.Label(h_frame_save,text="Ngày:").grid(row=0,column=4)
day_time_send=tk.Entry(h_frame_save,textvariable=day_time_send_var,width=15)
day_time_send.grid(row=0,column=5)
date_now_ent_var.trace('w',my_upd)
tk.Label(h_frame_save,text="Người phát tin:").grid(row=0,column=6, padx=(10,0))
person_send1=Combobox(h_frame_save,textvariable=person_send_var, width=17,state='readonly')
person_send1.grid(row=0,column=7)
#------
frame_save_buttons=tk.Frame(save_frame)
frame_save_buttons.grid(row=1,column=0)

save_news=tk.Button(frame_save_buttons,text="Lưu tin",width=12, height=2,bg='lightblue',command=saving_news,cursor='hand2')
save_news.grid(row=0,column=0,padx=15)
send_ttram=tk.Button(frame_save_buttons,text="Gửi trưởng trạm", height=2,
                     command=lambda:send_mail_button(1),bg='lightblue',cursor='hand2')
send_ttram.grid(row=0,column=1,padx=15)
send_all=tk.Button(frame_save_buttons,text="Gửi tin", width=12,height=2,bg='lightblue', 
                   command=lambda:send_mail_button(0),cursor='hand2')
send_all.grid(row=0,column=2,padx=15)
reset_news=tk.Button(frame_save_buttons,text="Làm mới",width=12, height=2,command=clear_button,
                     bg='lightblue',cursor='hand2')
reset_news.grid(row=1,column=0,padx=15,pady=5)
update_news=tk.Button(frame_save_buttons,text="Cập nhật", height=2,width=12,
                     bg='lightblue',command=lambda:update_database(1),cursor='hand2')
update_news.grid(row=1,column=1,padx=15,pady=5)
logout_news=tk.Button(frame_save_buttons,text="Đăng xuất", height=2,width=12,
                     bg='lightblue',command=logout,cursor='hand2')
logout_news.grid(row=1,column=2,padx=15,pady=5)

#Khóa không cho nhập vào spinbox
def on_click(event):
    # Hủy bỏ sự kiện chuột và thiết lập trạng thái nhập vào giá trị mới
    #event.widget.icursor(tk.END)
    return "break"
spinboxes = [h_weather_now, m_weather_now, h_time_send, m_time_send,zmax_spin]
for spinbox in spinboxes:
    spinbox.bind("<Key>", lambda e: "break")
    spinbox.bind("<FocusIn>", on_click)

clear_button()
window.mainloop()
