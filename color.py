from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import csv
from numpy import *
import pandas as pd
from PIL import ImageTk,Image
import matplotlib.pyplot as plt

class Main(Frame):
    def __init__(self, master):
        self.master = master
        Frame.__init__(self,self.master, bg="red") #Frame을 init 시켰는데 왜 Main에 Tk클래스가 적용되는지
        self.pack(fill='both', expand=True)
        Grid.columnconfigure(self, 0, weight=1)
        Grid.rowconfigure(self, 0, weight=1)
        Grid.rowconfigure(self, 1, weight=1)
        #rowconfig가 rowpropagate에 우선함
        self.init_topmenu(self.master) 
        self.init_topbar()
        self.init_botpanel()
        return

    def init_topmenu(self,master):
        self.the_menu = Menu()
        self.file_menu = Menu(self, tearoff=0)
        self.file_menu.add_command(label="Load", command=(lambda:self.load_csv(master)))
        self.file_menu.add_command(label="Save")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit",command=(lambda:self.quit_app(master)))
        self.the_menu.add_cascade(label="File", menu=self.file_menu)
        master.config(menu=self.the_menu)
        return

    def init_topbar(self):
        self.topbar_frame = Frame(self, height = 50, bg="blue")
        self.topbar_frame.grid(row = 0, column = 0, sticky=E+W+N)
        Grid.rowconfigure(self.topbar_frame, 0, weight=1)   
        self.topbar_frame.propagate(0)

        #Button
        self.save_img = PhotoImage(file = "save.png").subsample(3,3)
        self.save_btn = Button(self.topbar_frame, image= self.save_img, anchor = W)
        self.save_btn.grid(row=0,column=0)
        self.load_img = PhotoImage(file = "load.png").subsample(3,3)
        self.load_btn = Button(self.topbar_frame, image= self.load_img, anchor = W, command = (lambda : self.load_csv(self.master)))
        self.load_btn.grid(row=0,column=1)
        return

    def init_botpanel(self):
        self.botpanwin = PanedWindow(self, bg = 'orange', orient="horizontal")
        self.botpanwin.grid(row = 1, column = 0, sticky=E+W+S+N)
        Grid.rowconfigure(self.botpanwin, 0, weight=1)
        Grid.columnconfigure(self.botpanwin, 0, weight=1)   
        Grid.columnconfigure(self.botpanwin, 1, weight=1)
        Grid.columnconfigure(self.botpanwin, 2, weight=1) 

        self.init_sidebar()
        self.init_rightpanel()     
        return

    def init_sidebar(self):
        self.sidebar_frame = Frame(self.botpanwin, bg="yellow")
        self.sidebar_frame.grid(row = 0, column = 0, sticky = N+S) 

        self.botpanwin.add(self.sidebar_frame)

        self.load_btn = Button(self.sidebar_frame, text = "load", width = 4)
        self.load_btn.grid(row = 0, column = 0)
        self.save_btn = Button(self.sidebar_frame, text = "save", width = 4)
        self.save_btn.grid(row = 1, column = 0)
        self.quit_btn = Button(self.sidebar_frame, text = "quit", width = 4)
        self.quit_btn.grid(row = 2, column = 0)
        return

    def init_rightpanel(self):
        self.right_frame = Frame(self.botpanwin, bg = 'gray')
        self.right_frame.grid(row = 0, column = 2, sticky=S+N)
        self.botpanwin.add(self.right_frame)

        Grid.rowconfigure(self.right_frame, 0, weight=1)
        Grid.columnconfigure(self.right_frame, 0, weight=1)   
        return     
       

    def load_csv(self,master):
        #load csv & make data frame
        master.filename =  filedialog.askopenfilename(initialdir = "dataset", title = "Open file", filetypes = (("all files","*.*"),("csv files","*.csv")))
        with open(master.filename) as csvfile:
            self.df = pd.read_csv(csvfile)
        self.make_treeview()
        return
        
    def quit_app(self, master):
        master.quit()
        return

    def make_treeview(self):
        #make scrollbar & make treeview
        self.treeview_labelframe = LabelFrame(self.botpanwin, text = "treeview", padx=5, pady=5)
        self.treeview_labelframe.grid(row = 0, column = 1, sticky=W+N+S+E)
        
        self.botpanwin.add(self.treeview_labelframe)

        Grid.columnconfigure(self.treeview_labelframe, 0, weight=1) #tree
        Grid.columnconfigure(self.treeview_labelframe, 1, weight=1) #scrollbary
        Grid.rowconfigure(self.treeview_labelframe, 0, weight=1)
       
        self.scrollbary = Scrollbar(self.treeview_labelframe) #Main class는 pack 됐음에도 scrollbar는 grid가 먹힘
        self.scrollbary.grid(row=0, column=2, sticky="ns")
        self.scrollbarx = Scrollbar(self.treeview_labelframe, orient=HORIZONTAL)
        self.scrollbarx.grid(row=1, column=1, sticky="ew")      
        self.indices = tuple(self.df.columns.values)
        self.treeview = ttk.Treeview(self.treeview_labelframe, columns = self.indices, yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set) #height 넣으면 버벅거림
        self.treeview.grid(row=0,column=1)
        self.scrollbary.config(command=self.treeview.yview)
        self.scrollbarx.config(command=self.treeview.xview)

        #input date to treeview
        for n, idx in enumerate(self.indices):
            self.treeview.heading(idx, text = idx, anchor = W)
            self.treeview.column('#'+str(n), stretch = YES, minwidth=50, width=50)
            self.treeview.grid() #col넣을 때 grid 건드리지 말기

        with open(root.filename) as csvfile:
            has_header = csv.Sniffer().has_header(csvfile.read(1024))
            csvfile.seek(0)
            reader = csv.reader(csvfile)
            if has_header:
                next(reader)
            row = []
            for line in reader:
                for elem in range(len(self.indices)):
                    row.append(line[elem])
                self.treeview.insert("",END,values=tuple(row))
                del row[:]
        return

root = Tk()
root.title("Data Analysis Platform")
root.iconbitmap('./a.ico')
root.geometry("800x330")
Main(root)
root.mainloop()


