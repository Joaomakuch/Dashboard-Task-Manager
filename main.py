import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
import psutil
import os
import platform, subprocess, re

running = True
window = tk.Tk()
s = ttk.Style()
s.theme_use('clam')


def on_close(event):
    global running
    running = False


def terminal():
    if platform.system() == "Linux":
        os.system("gnome-terminal")
    if platform.system() == "Windows":
        os.system("start cmd")


def getListOfProcessSortedByMemory():
    while True:
        listOfProcObjects = []
        i = 0
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
                pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
                listOfProcObjects.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['vms'], reverse=True)
        return listOfProcObjects


def cpuinfo():
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        all_info = subprocess.check_output(command, shell=True).decode().strip()
        for line in all_info.split("\n"):
            if "model name" in line:
                return re.sub( ".*model name*.", "", line,1)
    return ""


def version():
    return platform.platform()


def memoryusage():
    return psutil.virtual_memory().percent


def cpuusage():
    i = 0
    plt.ylim([0,100])
    while running:
        cpu_usage = psutil.cpu_percent()
        mem_usage = psutil.virtual_memory().percent
        plt.scatter(i, cpu_usage, color = "red")
        plt.scatter(i, mem_usage, color = "blue")
        i = i+1
        plt.legend(["CPU", "Memory"], loc ="lower right")
        plt.pause(0.05) 


fig = plt.figure()
fig.canvas.mpl_connect('close_event', on_close)


def mem():
    global running
    running = True
    cpuusage()
    fig = plt.figure()
    fig.canvas.mpl_connect('close_event', on_close)


def ArchiveSystem():
    my_w = tk.Tk()
    my_w.geometry("400x300")  
    my_w.title("Sistema de Arquivos")  
    my_dir=''  
    def my_fun(): 
        path = filedialog.askdirectory() 
        l1.config(text=path) 
        root=next(os.walk(path))[0] 
        dirnames=next(os.walk(path))[1] 
        files=next(os.walk(path))[2] 
        for item in trv.get_children():
            trv.delete(item)
        i=1
        f2i=1 
        for d in dirnames:
            trv.insert("", 'end',iid=i,values =d)
            path2=path+'/'+d  
            files2=next(os.walk(path2))[2] 
            for f2 in files2:  
                trv.insert(i, 'end',iid='sub'+str(f2i),values ="-" + f2)
                f2i=f2i+1
            i=i+1

        for f in files:  
            trv.insert("", 'end',iid=i,values =f)
            i=i+1

    b1=tk.Button(my_w,text='Selecione o diretório',font=22,
        command=lambda:my_fun(),bg='lightgreen')
    b1.grid(row=0,column=0,padx=5,pady=10)

    l1=tk.Label(my_w,text=my_dir,bg='yellow',font=16)
    l1.grid(row=0,column=1,padx=0)

    trv=ttk.Treeview(my_w,selectmode='browse',height=9)
    trv.grid(row=1,column=0,columnspan=2,padx=10,pady=5)
    trv["columns"]=("1")
    trv['show']='tree headings'
    trv.column("#0", width = 20, anchor ='c')
    trv.column("1",width=300,anchor='w')
    trv.heading("#0", text ="#")
    trv.heading("1",text="Nome",anchor='w')

    my_w.mainloop() 


def update(newWindow):
    var = getListOfProcessSortedByMemory()
    scrollbar = Scrollbar(newWindow)
    scrollbar.pack( side = RIGHT, fill = Y )
    mylist = Listbox(newWindow, yscrollcommand = scrollbar.set)
    for line in var[:100]:
        mylist.insert(END, line)
    mylist.pack(expand=True,fill = BOTH)
    scrollbar.config( command = mylist.yview )
    


def OpenNewWindow():
    newWindow = Toplevel(window)

    newWindow.title("Processos")
    newWindow.geometry("800x400")
    update(newWindow)


window.title('Dashboard')
window.geometry("600x250")
sistema = tk.Label(window, text="Sistema Operacional:", font=80).place(x=20,y=20)
cpu = tk.Label(window, text="Processador:", font = 80).place(x=20, y=40)
e1= tk.Label(window, text=version(), font = 80).place(x=200, y=20)
e2= tk.Label(window, text=cpuinfo(), font = 80).place(x=130, y=40)
cpuusage_button = ttk.Button(window,command = mem,text = "Memoria/CPU")
terminal_button = ttk.Button(window, command = terminal, text = "Terminal")
process_button = ttk.Button(window, command = OpenNewWindow, text = "Processos")
archive_button = ttk.Button(window, command = ArchiveSystem, text = "Sistema de Arquivos")
cpuusage_button.place(x=20,y=80)
terminal_button.place(x=20,y=110)
process_button.place(x=20,y=140)
archive_button.place(x=20, y=170)

window.mainloop()