from tkinter import *
import tkinter.messagebox
from PIL import Image, ImageTk
from tkinter import ttk
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
hostSegOne = {"H1":1,"H2":2,"H3":3,"H4":3, "H5":3, "H6":3, "H7":3}
hostSegTwo = {"H1":1,"H2":1,"H3":2,"H4":3,"H5":4, "H6":5, "H7":5}
hostSegThree = {"H1":1,"H2":1,"H3":1,"H4":1,"H5":1,"H6":2,"H7":3}
#转发表
S1 = {}
S2 = {}
S3 = {}
dataIO = []
i = 0
# 下拉菜单的选择事件
# def chooseSrc(*args):
#     print(cbSrcAddr.get())
#保存数据
def tableSave(dataIO):
    colName = ['发送的帧','S1地址','S1接口','S2地址','S2接口','S3地址','S3接口','S1的处理','S2的处理','S3的处理']
    csvFile = pd.DataFrame(columns = colName, data = dataIO)
    csvFile.to_csv('testcsv.csv',encoding='gbk',index_label = "序号")
#重置事件
def btnReset():
    #lbdata.destory()
    global i
    i = 0
    for widget in lbdata.winfo_children():
        widget.destroy()
    S1.clear()
    S2.clear()
    S3.clear()
#发送事件
def btnSend():
    global i
    if(i == 7):
        return
    dataChip = ["","","","","","","","","",""]
    srcAddr = varSrc.get()
    desAddr = varDes.get()
    if(srcAddr == desAddr):
        return
    handleB1 = ""
    handleB2 = ""
    handleB3 = ""
    seqS = [0,0,0]
    loc = 0
    if(srcAddr in lan1):
        seqS = [1,2,3]
    elif(srcAddr in lan2):
        seqS = [2,1,3]
    elif(srcAddr in lan3):
        seqS = [3,2,1]
    else:
        return
    count = 0
    #核心部分算法
    while(count!=3):
        if(seqS[count] == 1):
            if(srcAddr in S1):
                handleB1 = "转发,不登记"
            else:
                S1[srcAddr] = hostSegOne[srcAddr]
                handleB1 = "转发,登记"
                Label(lbdata, text=S1[srcAddr]).place(x=60,y=20*i)#.grid(row=8 + i,column=3)
                Label(lbdata, text=srcAddr).place(x=120,y=20*i)#.grid(row=8 + i,column=2)
                dataChip[2 * count + 1] = srcAddr
                dataChip[2 * count + 2] = S1[srcAddr]
            if(desAddr in S1):
                if(desAddr in lan1):
                    for c in range(count + 1, 3):
                        seqS[c] = 0
                    
        elif(seqS[count] == 2):
            if(srcAddr in S2):
                handleB2 = "转发,不登记"
            else:
                S2[srcAddr] = hostSegTwo[srcAddr]
                handleB2 = "转发,登记"
                Label(lbdata, text=S2[srcAddr]).place(x=170,y=20*i)
                Label(lbdata, text=srcAddr).place(x=230,y=20*i)
                dataChip[2 * count + 1] = srcAddr
                dataChip[2 * count + 2] = S2[srcAddr]
            if(desAddr in S2):
                q = 2
                if(desAddr in lan1):
                    q = 3
                elif(desAddr in lan3):
                    q = 1
                for c in range(count, 3):
                    if(seqS[c] == q):
                        seqS[c] = 0
                    if(q == 2):
                        seqS[c] = 0
            #if(desAddr in S2):
        elif(seqS[count] == 3):
            if(srcAddr in S3):
                handleB3 = "转发,不登记"
            else:
                S3[srcAddr] = hostSegThree[srcAddr]
                handleB3 = "转发,登记"
                Label(lbdata, text=S3[srcAddr]).place(x=280,y=20*i)
                Label(lbdata, text=srcAddr).place(x=330,y=20*i)
                dataChip[2 * count + 1] = srcAddr
                dataChip[2 * count + 2] = S3[srcAddr]
            if(desAddr in S3):
                if(desAddr in lan3):
                    for c in range(count + 1, 3):
                        seqS[c] = 0
        count = count + 1
    Label(lbdata, text=srcAddr + "->" + desAddr).place(x=0,y=20*i)
    Label(lbdata, text=handleB1).place(x=380,y=20*i)
    Label(lbdata, text=handleB2).place(x=450,y=20*i)
    Label(lbdata, text=handleB3).place(x=520,y=20*i)
    dataChip[0] = srcAddr + "->" + desAddr
    dataChip[7] = handleB1
    dataChip[8] = handleB2
    dataChip[9] = handleB3
    dataIO.append(dataChip)
    i = i + 1
    if(i == 7):
        i = i - 1
        boolSave=tkinter.messagebox.askokcancel('提示', '要是否进行保存?')
        if(boolSave):
            tableSave(dataIO)
        

if __name__ == "__main__":
    varSrc = StringVar()
    varDes = StringVar()
    img = Image.open('VLN1.png')  # 打开图片
    photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
    imglabel = Label(lbPic, image=photo)
    imglabel.place(x=0,y=0)
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
    btn.place(x=580,y=5)
    #重置按钮
    bt = Button(sendfm,text="重置",command=btnReset)
    bt.place(x=650,y=5)
    #表头
    Label(lbhead, text="发送的帧").place(x=0,y=12)
    Label(lbhead, text="S1的转发表").place(x=70,y=2)
    Label(lbhead, text="地址").place(x=60,y=20)
    Label(lbhead, text="接口").place(x=120,y=20)
    Label(lbhead, text="S2的转发表").place(x=180,y=2)
    Label(lbhead, text="地址").place(x=170,y=20)
    Label(lbhead, text="接口").place(x=230,y=20)
    Label(lbhead, text="S3的转发表").place(x=290,y=2)
    Label(lbhead, text="地址").place(x=280,y=20)
    Label(lbhead, text="接口").place(x=330,y=20)
    Label(lbhead, text="S1的处理").place(x=380,y=12)
    Label(lbhead, text="S2的处理").place(x=450,y=12)
    Label(lbhead, text="S3的处理").place(x=520,y=12)
    mainloop()
