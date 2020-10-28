# -*- coding: utf-8 -*-
import configparser
import datetime
import tkinter as tk
from tkinter import messagebox
import os
import csv

flag = True
root = tk.Tk()
root.withdraw()

#config.ini read
ini = configparser.ConfigParser()
try:
    ini.read('./config.ini', 'UTF-8')
    hyouzi_PASS = ini['DEFAULTPASS']['hyouzi']
    rog_PASS = ini['DEFAULTPASS']['rog']

    dt_now = datetime.datetime.now()
    td = str(dt_now.day)
    A_hyouzi_Text = ini['A_HYOUZI'][td]
    B_hyouzi_Text = ini['B_HYOUZI'][td]
    C_hyouzi_Text = ini['C_HYOUZI'][td]
except configparser.NoSectionError as err:
    flag = False
    messagebox.showerror('エラー', err)
except configparser.NoOptionError as err:
    flag = False
    messagebox.showerror('エラー', err)
if hyouzi_PASS =='':
    flag = False
    messagebox.showerror('エラー', 'iniファイルのhyouziで\ntxtファイルのパスが指定されていません')

#hyouzi.txt read
while flag == True:
    try:
        with open(hyouzi_PASS, 'r', encoding='UTF-8') as f:
            D_hyouzi_Text = f.read()
    except FileNotFoundError:
        flag = False
        messagebox.showerror('エラー', 'iniファイルで指定したパスの\nテキストファイルが見つかりません')
    except Exception as err:
        flag = False
        messagebox.showerror('エラー', err)
    
    if flag == True:
        if not D_hyouzi_Text:
            messagebox.showerror('エラー', 'txtファイルにデータがありません')
            flag = False
        else:
            #ユーザ名の取得
            user = os.environ.get('USERNAME')
            dt_now = datetime.datetime.now()

            with open(rog_PASS + user +'-rog.csv','a',newline='') as logf:
                writer=csv.writer(logf)
                writer.writerow([dt_now.strftime('%Y%m/%d %H:%M:%S') , user])

            data = A_hyouzi_Text + '\n' + B_hyouzi_Text + '\n'+ C_hyouzi_Text +'\n\n' + D_hyouzi_Text
            messagebox.showinfo(dt_now.strftime('%m/%d %H:%M:%S'),data)
            flag = messagebox.askyesno('更新確認', 'メッセージボックスを更新しますか?')

messagebox.showinfo('終了','プログラムを終了します')
root.destroy()
