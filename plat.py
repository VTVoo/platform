import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog
from PyQt5.QtGui import QIcon
import csv
from numpy import *
import pandas as pd
from PIL import ImageTk,Image
import matplotlib.pyplot as plt

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    #UI
    def initUI(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        #openFileDialog & LoadCsv
        openFile = QAction(QIcon('./open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open New File')
        openFile.triggered.connect(self.openFileDialogAndReadCsv)

        #save
        cnvtFile = QAction(QIcon('./save.png'), 'Save', self)
        cnvtFile.setShortcut('Ctrl+S')
        cnvtFile.setStatusTip('Save File')
        cnvtFile.triggered.connect(QApplication.quit)
        
        #quit
        quitApp = QAction(QIcon('./quit.png'), 'Quit', self)
        quitApp.setShortcut('Ctrl+Q')
        quitApp.setStatusTip('Quit App')
        quitApp.triggered.connect(QApplication.quit)      

        #menubar
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(cnvtFile)
        fileMenu.addAction(quitApp)

        #mainWindow
        self.setWindowTitle('File Dialog')
        self.setGeometry(300, 300, 1000, 400)
        self.show()

    def openFileDialogAndReadCsv(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        if  self.fname[0]:
            f = open(self.fname[0], 'r')
            with f:
                data = f.read()
                self.textEdit.setText(data)
        
        with open(self.fname[0]) as csvfile:
            self.df = pd.read_csv(csvfile)

    def save(self):
        pass

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

'''
class Main(Frame):
        self.make_treeview()
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
'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())


