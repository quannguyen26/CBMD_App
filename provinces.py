import tkinter as tk
province_districts={
    "Lai Châu":["Phong Thổ","Tam Đường","Tp.Lai Châu","Tân Uyên","Than Uyên","Sìn Hồ","Nậm Nhùn","Mường Tè"],
    "Điện Biên":["Điện Biên","Điện Biên Đông","Tp.Điên Biên Phủ","Mường Ảng","Tuần Giáo","Tủa Chùa","Mường Chà","Tx.Mường Lay","Nậm Pồ","Mường Nhé"],
    "Sơn La":["Quỳnh Nhai","Thuận Châu","Sông Mã","Sốp Cộp","Mường La","Tp.Sơn La","Mai Sơn","Yên Châu","Bắc Yên","Phù Yên","Mộc Châu","Vân Hồ"],
    "Hòa Bình":["Mai Châu","Đà Bắc","Tân Lạc","Cao Phong","Tp.Hòa Bình","Kì Sơn","Lương sơn","Kim Bôi","Lạc Sơn","Yên Thủy","Lạc Thủy"],
    "Lào Cai":["Bát Xát","Sa Pa","Văn Bàn","Tp.Lào Cai","Bảo Thắng","Bảo Yên","Bắc Hà","Mường Khương","Si Ma Cai"],
    "Yên Bái":["Mù Căng Chải","Văn Yên","Lục Yên","Trạm Tấu","Văn Chấn","Trấn Yên","Tx.Nghĩa Lộ","Tp.Yên Bái","Yên Bình"]
    }
def check_district(pro_var,agu_pro,all_check,all_check2):
    n=0
    for i in range(0,len(pro_var)):
        if pro_var[i].get():
            agu_pro[i].configure(state="disabled")
            n=n+1
        else:
            agu_pro[i].configure(state="normal")
    if n<len(pro_var):
        all_check.deselect()
        all_check2.configure(state="normal")
    else:
        all_check.select()
        all_check2.configure(state="disabled")


def check_all(all,pro_lists,pro_lists_13hs,ckbt_all):
    if all.get():
        for pro_list,pro_list_13h in zip(pro_lists,pro_lists_13hs):
            pro_list.configure(state="normal")
            pro_list.select()
            pro_list_13h.deselect()
            pro_list_13h.configure(state="disabled")
        ckbt_all.configure(state="disabled")
    else:
        for pro_list,pro_list_13h in zip(pro_lists,pro_lists_13hs):
            pro_list.deselect()
            pro_list_13h.configure(state="normal")
        ckbt_all.configure(state="normal")

def even_check_buttons(name_province,frame_now,frame_13h,chks,chks_13h,extra_i,for_clear,for_clear_all,padx_):    
    n=0
    pro_lists_now=[]
    pro_lists_13h=[]
    for i in range(0,extra_i):
        for j in range(0,4):
            pro_now=tk.Checkbutton(frame_now,text=province_districts[name_province][n],variable=chks[n],
                                   command=lambda:check_district(chks[:],pro_lists_13h[:],ckbt_all_now,ckbt_all_13h))
            pro_13=tk.Checkbutton(frame_13h,text=province_districts[name_province][n],variable=chks_13h[n],
                                  command=lambda:check_district(chks_13h[:],pro_lists_now[:],ckbt_all_13h,ckbt_all_now))
            pro_lists_now.append(pro_now)
            pro_lists_13h.append(pro_13)
            for_clear.append(pro_now)
            for_clear.append(pro_13)
            pro_now.grid(row=i,column=j,sticky="w",padx=padx_)
            pro_13.grid(row=i,column=j,sticky="w",padx=padx_)
            n+=1

    all_now=tk.BooleanVar()
    all_13h=tk.BooleanVar()
    ckbt_all_now=tk.Checkbutton(frame_now, text="Tất cả",variable=all_now,
                                   command=lambda:check_all(all_now,pro_lists_now,pro_lists_13h,ckbt_all_13h))
    ckbt_all_now.grid(row=1, column=4, sticky="w")
    ckbt_all_13h=tk.Checkbutton(frame_13h, text="Tất cả",variable=all_13h,
                               command=lambda:check_all(all_13h,pro_lists_13h,pro_lists_now,ckbt_all_now))
    ckbt_all_13h.grid(row=1, column=4, sticky="w")
    for_clear_all.append(all_now)
    for_clear_all.append(all_13h)
    for_clear.append(ckbt_all_now)
    for_clear.append(ckbt_all_13h)
def odd_check_buttons(name_province,frame_now,frame_13h,chks,chks_13h,extra_j,for_clear,for_clear_all,padx_):
    n=0
    pro_lists_now=[]
    pro_lists_13h=[]
    for i in range(0,3):
            if i==2:
                for j in range(0,extra_j):
                    pro_now=tk.Checkbutton(frame_now,text=province_districts[name_province][n],variable=chks[n],
                                       command=lambda:check_district(chks[:],pro_lists_13h[:],ckbt_all_now,ckbt_all_13h))
                    pro_13h=tk.Checkbutton(frame_13h,text=province_districts[name_province][n],variable=chks_13h[n],
                                       command=lambda:check_district(chks_13h[:],pro_lists_now[:],ckbt_all_13h,ckbt_all_now))
                    pro_lists_now.append(pro_now)
                    pro_lists_13h.append(pro_13h)
                    for_clear.append(pro_now)
                    for_clear.append(pro_13h)
                    pro_now.grid(row=i,column=j,sticky="w",padx=padx_)
                    pro_13h.grid(row=i,column=j,sticky="w",padx=padx_)
                    n+=1
            else:
                for j in range(0,4):
                    pro_now=tk.Checkbutton(frame_now,text=province_districts[name_province][n],variable=chks[n],
                                       command=lambda:check_district(chks[:],pro_lists_13h[:],ckbt_all_now,ckbt_all_13h))
                    pro_13h=tk.Checkbutton(frame_13h,text=province_districts[name_province][n],variable=chks_13h[n],
                                        command=lambda:check_district(chks_13h[:],pro_lists_now[:],ckbt_all_13h,ckbt_all_now))
                    pro_lists_now.append(pro_now)
                    pro_lists_13h.append(pro_13h)
                    for_clear.append(pro_now)
                    for_clear.append(pro_13h)
                    pro_now.grid(row=i,column=j,sticky="w",padx=padx_)
                    pro_13h.grid(row=i,column=j,sticky="w",padx=padx_)
                    n+=1
    all_now=tk.BooleanVar()
    all_13h=tk.BooleanVar()
    ckbt_all_now=tk.Checkbutton(frame_now, text="Tất cả",variable=all_now,
                   command=lambda:check_all(all_now,pro_lists_now,pro_lists_13h,ckbt_all_13h))
    ckbt_all_now.grid(row=1, column=4, sticky="w")
    ckbt_all_13h=tk.Checkbutton(frame_13h, text="Tất cả",variable=all_13h,
                  command=lambda:check_all(all_13h,pro_lists_13h,pro_lists_now,ckbt_all_now))
    ckbt_all_13h.grid(row=1, column=4, sticky="w")
    for_clear_all.append(all_now)
    for_clear_all.append(all_13h)
    for_clear.append(ckbt_all_now)
    for_clear.append(ckbt_all_13h)
