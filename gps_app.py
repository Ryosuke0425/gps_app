import tkinter as tk
from tkinter import messagebox
import folium
from pyicloud import PyiCloudService
import time
import datetime
import threading

root = tk.Tk()
root.geometry("300x300")
root.title("GPS app")

state = 0

def start_record():
    th = threading.Thread(target=record)
    th.start()
    

def record():
    global state
    count = 0
    try:
        api = login()
    except:
        messagebox.showerror("error","ログインに失敗しました。ユーザーネームとパスワードを再度入力してください。")
        return
    start_button['state'] = "disabled"
    end_button['state'] = "active"
    folium_map = folium.Map([35,139],zoom_start=50)
    progress_label['text'] = "記録中..."
    while True:
        try:
            location = api.devices[0].location()
            folium.Marker(location=[location['latitude'],location['longitude']],popup=datetime.datetime.now().replace(microsecond=0)).add_to(folium_map)
            if count == 0:
                folium_map.location = [location['latitude'],location['longitude']]
            if state == 1: raise Exception
        except:
            messagebox.showinfo("終了",str(datetime.datetime.now().replace(microsecond=0)) + "記録を終了しました。")
            folium_map.save(file_name_entry.get() + '.html')
            start_button['state'] = "active"
            end_button['state'] = "disabled"
            progress_label['text'] = ''
            state = 0
            break
        time.sleep(10)
    

def login():
    username = username_entry.get()
    passward = passward_entry.get()
    return PyiCloudService(username,passward)


def end_record():
    global state
    state = 1 


username_label = tk.Label(root,text="iCloudのユーザーネーム")
username_label.pack(expand=True)

username_entry = tk.Entry(root,width=40)
username_entry.pack(expand=True)

passward_label = tk.Label(root,text="パスワード")
passward_label.pack(expand=True)

passward_entry = tk.Entry(root,width=40,show="*")
passward_entry.pack(expand=True)

file_name_label = tk.Label(root,text="保存するファイル名")
file_name_label.pack(expand=True)
file_name_entry = tk.Entry(root,width=40)
file_name_entry.pack(expand=True)

start_button = tk.Button(root,text='記録開始',command=start_record)
start_button.pack(expand=True)

progress_label = tk.Label(root,text="")
progress_label.pack(expand=True)

end_button = tk.Button(root,text='記録終了',state="disabled",command=end_record)
end_button.pack(expand=True)

root.mainloop()