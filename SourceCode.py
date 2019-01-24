from tkinter import *
import tkinter.messagebox
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import pandas as pd

root = Tk()
root.geometry("700x500")#定义总布局大小
root.resizable(width=False, height=False)#界面大小不可调整
root.title('网桥转发表模拟工具')
#图片部分框架
lbPic=LabelFrame(root, width=700, height=250)
lbPic.grid(row=0,column=0)
#发送部分框架
sendfm = Frame(root, width = 700, height=40)
sendfm.grid(row=1,column=0)
#转发表表头
lbhead = LabelFrame(root, width = 700, height = 50, padx=50)
lbhead.grid(row=2,column=0)
#转发表数据
lbdata = Frame(root, width = 700, height = 160, padx=50)
lbdata.grid(row=3,column=0)
#主机所在局域网
lan1 = ["H1","H2"]
lan2 = ["H3","H4","H5"]
lan3 = ["H6","H7"]
#主机端口记录
hostSegOne = {"H1":1,"H2":1,"H3":2,"H4":2, "H5":2, "H6":2, "H7":2}
hostSegTwo = {"H1":1,"H2":1,"H3":1,"H4":1,"H5":1, "H6":2, "H7":2}
#hostSegThree = {"H1":1,"H2":1,"H3":1,"H4":1,"H5":1,"H6":2,"H7":3}
#转发表
S1 = {}
S2 = {}
#S3 = {}
dataIO = []
srcAddr = ""
desAddr = ""
flag = False#默认为点击读取，
i = 0
# 下拉菜单的选择事件
# def chooseSrc(*args):
#     print(cbSrcAddr.get())
#读取数据
def tableRead():
    #root.withdraw()
    global i
    global flag,srcAddr,desAddr
    if(i > 7):
        tkinter.messagebox.showinfo('提示', '请重置后再进行读取')
        return
    file_path = filedialog.askopenfilename(filetypes = [('CSV', 'csv')])
    if(file_path):
        flag = True
        info=pd.read_csv(file_path,encoding = 'gbk')
        for j in info['发送的帧']:
            if(i < 8):
                srcAddr = j.split('-')[0]
                desAddr = j.split('>')[1]
                btnSend()
        flag = False
#         for i in obj:
#             print(i)
    #except:
        #tkinter.messagebox.showinfo('提示', '文件不存在，请先保存')
# def hello():
#     print("c");

#关于使用
def aboutAuthor():
    top1=tkinter.Toplevel()
    image = Image.open('功能框图.jpg')
    img = ImageTk.PhotoImage(image)
    canvas1 = tkinter.Canvas(top1, width = 500 ,height = 566, bg = 'white')
    canvas1.create_image(0,0,image = img,anchor="nw")
    #canvas1.create_image(image.width,0,image = img,anchor="nw")
    canvas1.pack()
    top1.mainloop()
    
#保存数据
def tableSave():
    global dataIO
    boolSave=tkinter.messagebox.askokcancel('提示', '要是否进行保存?')
    if(boolSave):
        colName = ['发送的帧','S1地址','S1接口','S2地址','S2接口','S1的处理','S2的处理','转发途径']
        csvFile = pd.DataFrame(columns = colName, data = dataIO)
        csvFile.to_csv('test.csv',encoding='gbk',index_label = "序号")
    dataIO = []
#重置事件
def btnReset():
    #lbdata.destory()
    global i, flag, dataIO
    i = 0
    for widget in lbdata.winfo_children():
        widget.destroy()
    S1.clear()
    S2.clear()
    flag = False
    #S3.clear()
    dataIO = []
#发送事件
def btnSend():
    global i,srcAddr,desAddr
    if(i > 7):
        tkinter.messagebox.showinfo('提示','转发信息已到达最大数据')
        return
    dataChip = ["","","","","","","",""]
    if(not flag):
        srcAddr = varSrc.get()
        desAddr = varDes.get()
    if(srcAddr == desAddr):
        return
    handleB1 = ""
    handleB2 = ""
    routPort = ""
    flagb1 = True#表示两个转发表都要转发
    flagb2 = True
    seqS = [0,0,0]
    if(srcAddr in lan1):
        seqS = [0,1]
    elif(srcAddr in lan2):
        seqS = [1,0]
    elif(srcAddr in lan3):
        seqS = [1,0]
    else:
        return
    if(desAddr not in lan1):
        if(desAddr not in lan2):
            if(desAddr not in lan3):
                return
    count = 0
    while(count!=2):
        if(seqS[count] == 0 and flagb1):
            if(srcAddr not in S1):
                S1[srcAddr] = hostSegOne[srcAddr]
                handleB1 = "转发,登记"
                Label(lbdata, text=srcAddr).place(x=65,y=20*i)
                Label(lbdata, text=S1[srcAddr]).place(x=125,y=20*i)
                dataChip[2 * count + 1] = srcAddr
                dataChip[2 * count + 2] = S1[srcAddr]
                if(desAddr in S1):
                    if(S1[desAddr] == hostSegOne[srcAddr]):
                        handleB1 = "登记,丢弃"
                        flagb2 = False
                    else:
                        handleB1 = "登记,转发"
                        routPort += "S1 - >"
                else:
                    routPort += "S1 - >"
            else:
                if(desAddr in S1):
                    if(S1[desAddr] == hostSegOne[srcAddr]):
                        handleB1 = "丢弃"
                        flagb2 = False
                    else:
                        handleB1 = "转发"
                        routPort += "S1 - >"
                else:
                        handleB1 = "转发"
                        routPort += "S1 - >"
        elif(seqS[count] == 1 and flagb2):
            if(srcAddr not in S2):
                S2[srcAddr] = hostSegTwo[srcAddr]
                handleB2 = "转发,登记"
                Label(lbdata, text=srcAddr).place(x=175,y=20*i)
                Label(lbdata, text=S2[srcAddr]).place(x=235,y=20*i)
                dataChip[2 * count + 1] = srcAddr
                dataChip[2 * count + 2] = S2[srcAddr]
                if(desAddr in S2):
                    if(S2[desAddr] == hostSegTwo[srcAddr]):
                        handleB2 = "登记,丢弃"
                        flagb1 = False
                    else:
                        handleB2 = "登记,转发"
                        routPort += "S2 - >"
                else:
                    routPort += "S2 - >"
            else:
                if(desAddr in S2):
                    if(S2[desAddr] == hostSegTwo[srcAddr]):
                        handleB2 = "丢弃"
                        flagb1 = False
                    else:
                        handleB2 = "转发"
                        routPort += "S2 - >"
                else:
                        handleB2 = "转发"
                        routPort += "S2 - >"
            if(srcAddr in lan2):
                flagb1 = True
                
        count = count + 1
    #print(i)
    routPort = routPort[:-4]
    Label(lbdata, text=srcAddr + "->" + desAddr).place(x=0,y=20*i)
    Label(lbdata, text=handleB1).place(x=290,y=20*i)
    Label(lbdata, text=handleB2).place(x=380,y=20*i)
    Label(lbdata, text=routPort).place(x=470,y=20*i)
    dataChip[0] = srcAddr + "->" + desAddr
    dataChip[5] = handleB1
    dataChip[6] = handleB2
    dataChip[7] = routPort
    dataIO.append(dataChip)
    i = i + 1

if __name__ == "__main__":
    varSrc = StringVar()
    varDes = StringVar()
    img = Image.open('vln.jpg')  # 打开图片
    photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
    imglabel = Label(lbPic, image=photo)
    imglabel.place(x=0,y=0)
    #顶部菜单栏
    menubar = Menu(root)
    menubar.add_command(label="读取文件",command=tableRead)
    menubar.add_command(label="保存",command=tableSave)
    menubar.add_command(label="重置",command=btnReset)
    menubar.add_command(label="关于",command=aboutAuthor)
    root['menu']=menubar
    #出发地址Label
    lbStart = Label(sendfm, text= "出发地址:")
    lbStart.place(x=30,y=10)
    #出发地址下拉菜单
    cbSrcAddr=ttk.Combobox(sendfm,textvariable=varSrc) #初始化 
    cbSrcAddr["values"]=("H1","H2","H3","H4","H5","H6","H7")
    cbSrcAddr.current(0)  #选择第一个  
    cbSrcAddr.bind("<<ComboboxSelected>>")  #下拉列表框被选中事件
    cbSrcAddr.place(x=100,y=10)
    #目的地址Label
    lbEnd = Label(sendfm, text= "目的地址:")#.grid(row=7, column = 7)
    lbEnd.place(x=330,y=10)
    #目的地址下拉菜单
    cbDesAddr=ttk.Combobox(sendfm,textvariable=varDes) #初始化 
    cbDesAddr["values"]=("H1","H2","H3","H4","H5","H6","H7")
    cbDesAddr.current(0)  #选择第一个  
    cbDesAddr.bind("<<ComboboxSelected>>")  #下拉列表框被选中事件
    cbDesAddr.place(x=400,y=10)
    #发送按钮
    btn = Button(sendfm,text="发送",command=btnSend)
    btn.place(x=620,y=5)
    #表头
    Label(lbhead, text="发送的帧").place(x=0,y=12)
    Label(lbhead, text="S1的转发表").place(x=70,y=2)
    Label(lbhead, text="地址").place(x=60,y=20)
    Label(lbhead, text="接口").place(x=120,y=20)
    Label(lbhead, text="S2的转发表").place(x=180,y=2)
    Label(lbhead, text="地址").place(x=170,y=20)
    Label(lbhead, text="接口").place(x=230,y=20)
    Label(lbhead, text="S1的处理").place(x=290,y=12)
    Label(lbhead, text="S2的处理").place(x=380,y=12)
    Label(lbhead, text="转发途径").place(x=470,y=12)
    mainloop()
