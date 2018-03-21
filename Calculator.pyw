import tkinter #导入tkinter模块
import tkinter.messagebox as mbox
import math
from math import *
import scipy
import scipy.special
from scipy.special import perm as perm, comb as comb
import re

root = tkinter.Tk()

def hello():
    root2 = tkinter.Tk()
menubar = tkinter.Menu(root)
filemenu = tkinter.Menu(menubar,tearoff = 0)
for item in ['Python','PHP','CPP','C','Java','JavaScript','VBScript']:
    filemenu.add_command(label = item,command = hello)
#将menubar的menu属性指定为filemenu，即filemenu为menubar的下拉菜单
menubar.add_cascade(label = '选项',menu = filemenu)
root['menu'] = menubar

root.maxsize(800,520)
root.minsize(800,520)
root.title('Calculator')
root.iconbitmap('.\Calculator.ico')






#1.界面布局
#显示面板
result = tkinter.StringVar()            #显示面板显示结果1，用于显示默认数字0
result.set('')
result2 = tkinter.StringVar()           #显示面板显示结果2，用于显示计算过程
result2.set('')
result3 = tkinter.StringVar()           #显示面板显示结果2，用于显示计算过程
result3.set('')
#显示版
label = tkinter.Label(root,font = ('微软雅黑',15),bg = '#EEE9E9',bd ='9',fg = '#828282',anchor = 'se',textvariable = result2)
label.place(width = 810,height = 80)
label3 = tkinter.Label(root,font = ('微软雅黑',10),bg = '#EEE9E9',bd ='9',fg = '#828282',anchor = 'se',textvariable = result3)
label3.place(width = 810,height = 45)
label2 = tkinter.Label(root,font = ('微软雅黑',30),bg = '#EEE9E9',bd ='9',fg = 'black',anchor = 'se',textvariable = result)
label2.place(y = 80,width = 810,height = 60)

Radix = tkinter.IntVar()
Radix.set(3)
Bin = tkinter.Radiobutton(root,variable = Radix,text = 'Bin',value = 1,command = lambda : RadixCvt('Bin'))
Bin.place(x = 480, y = 145)
Oct = tkinter.Radiobutton(root,variable = Radix,text = 'Oct',value = 2,command = lambda : RadixCvt('Oct'))
Oct.place(x = 555, y = 145)
Dec = tkinter.Radiobutton(root,variable = Radix,text = 'Dec',value = 3,command = lambda : RadixCvt('Dec'))
Dec.place(x = 630, y = 145)
Hex = tkinter.Radiobutton(root,variable = Radix,text = 'Hex',value = 4,command = lambda : RadixCvt('Hex'))
Hex.place(x = 705, y = 145)

Angle = tkinter.IntVar()
Angle.set(2)
Deg = tkinter.Radiobutton(root,variable = Angle,text = 'Deg',value = 1)
Deg.place(x = 110, y = 145)
Rad = tkinter.Radiobutton(root,variable = Angle,text = 'Rad',value = 2)
Rad.place(x = 185, y = 145)
Grad = tkinter.Radiobutton(root,variable = Angle,text = 'Grad',value = 3)
Grad.place(x = 260, y = 145)

#数字键按钮

btn7 = tkinter.Button(root,text = '7',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda : PressExpr('7'))
btn7.place(x = 450,y = 285,width = 60,height = 50)
btn8 = tkinter.Button(root,text = '8',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda : PressExpr('8'))
btn8.place(x = 520,y = 285,width = 60,height = 50)
btn9 = tkinter.Button(root,text = '9',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda : PressExpr('9'))
btn9.place(x = 590,y = 285,width = 60,height = 50)

btn4 = tkinter.Button(root,text = '4',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda : PressExpr('4'))
btn4.place(x = 450,y = 340,width = 60,height = 50)
btn5 = tkinter.Button(root,text = '5',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda : PressExpr('5'))
btn5.place(x = 520,y = 340,width = 60,height = 50)
btn6 = tkinter.Button(root,text = '6',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda : PressExpr('6'))
btn6.place(x = 590,y = 340,width = 60,height = 50)

btn1 = tkinter.Button(root,text = '1',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda : PressExpr('1'))
btn1.place(x = 450,y = 395,width = 60,height = 50)
btn2 = tkinter.Button(root,text = '2',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda : PressExpr('2'))
btn2.place(x = 520,y = 395,width = 60,height = 50)
btn3 = tkinter.Button(root,text = '3',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda : PressExpr('3'))
btn3.place(x = 590,y = 395,width = 60,height = 50)
btn0 = tkinter.Button(root,text = '0',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda : PressExpr('0'))
btn0.place(x = 520,y = 450,width = 60,height = 50)
btnComma = tkinter.Button(root,text = ',',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda : PressExpr(','))
btnComma.place(x = 450,y = 450,width = 60,height = 50)
btnPoint = tkinter.Button(root,text = '.',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda : PressExpr('.'))
btnPoint.place(x = 590,y = 450,width = 60,height = 50)
btnPi = tkinter.Button(root,text = 'π',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda :PressExpr ('π'))
btnPi.place(x = 730,y = 285,width = 60,height = 50)
btne = tkinter.Button(root,text = 'e',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda : PressExpr('e'))
btne.place(x = 730,y = 340,width = 60,height = 50)
btnAns = tkinter.Button(root,text = 'ans',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda : PressExpr('ans'))
btnAns.place(x = 730,y = 395,width = 60,height = 50)


#运算符号按钮
btnAc = tkinter.Button(root,text = 'AC',bd = 0.5,font = ('微软雅黑',12),fg = 'orange',command = lambda : PressCtrl('AC'))
btnAc.place(x = 450,y = 230,width = 60,height = 50)
btnCe = tkinter.Button(root,text = 'CE',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressCtrl('CE'))
btnCe.place(x = 520,y = 230,width = 60,height = 50)
btnBack = tkinter.Button(root,text = '←',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressCtrl('backspace'))
btnBack.place(x = 590,y = 230,width = 60,height = 50)
btnLpar = tkinter.Button(root,text = '(',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('('))
btnLpar.place(x = 660,y = 230,width = 60,height = 50)
btnRpar = tkinter.Button(root,text =')',font = ('微软雅黑',12),fg = "#4F4F4F",bd = 0.5,command = lambda : PressExpr(')'))
btnRpar.place(x = 730,y = 230,width = 60,height = 50)
btnAdd = tkinter.Button(root,text = '+',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('+'))
btnAdd.place(x = 660,y = 285,width = 60,height = 50)
btnSub = tkinter.Button(root,text = '-',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('-'))
btnSub.place(x = 660,y = 340,width = 60,height = 50)
btnMul = tkinter.Button(root,text = '×',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('*'))
btnMul.place(x = 660,y = 395,width = 60,height = 50)
btnDiv = tkinter.Button(root,text = '÷',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('/'))
btnDiv.place(x = 660,y = 450,width = 60,height = 50)
btnCalc = tkinter.Button(root,text = 'Calc',bg = 'orange',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda : PressEqual())
btnCalc.place(x = 730,y = 450,width = 60,height = 50)

btnMc = tkinter.Button(root,text = 'MC',bd = 0.5,font = ('微软雅黑',12),fg = 'orange',command = lambda : PressMem('MC'))
btnMc.place(x = 450,y = 175,width = 60,height = 50)
btnMadd = tkinter.Button(root,text = 'M+',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressMem('M+'))
btnMadd.place(x = 520,y = 175,width = 60,height = 50)
btnMsub = tkinter.Button(root,text = 'M-',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressMem('M-'))
btnMsub.place(x = 590,y = 175,width = 60,height = 50)
btnMst = tkinter.Button(root,text = 'MS',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressMem('MS'))
btnMst.place(x = 660,y = 175,width = 60,height = 50)
btnMrd = tkinter.Button(root,text = 'MR',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('M'))
btnMrd.place(x = 730,y = 175,width = 60,height = 50)

btnSqr = tkinter.Button(root,text = 'x^2',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('^2'))
btnSqr.place(x = 360,y = 175,width = 60,height = 50)
btnCub = tkinter.Button(root,text = 'x^3',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('^3'))
btnCub.place(x = 360,y = 230,width = 60,height = 50)
btnSqrt = tkinter.Button(root,text = '√x',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('^0.5'))
btnSqrt.place(x = 360,y = 285,width = 60,height = 50)
btnRev = tkinter.Button(root,text = '1/x',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('^-1'))
btnRev.place(x = 360,y = 340,width = 60,height = 50)
btnPow10 = tkinter.Button(root,text = '10^x',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('10^'))
btnPow10.place(x = 360,y = 395,width = 60,height = 50)
btnLog10 = tkinter.Button(root,text = 'log10',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('log10('))
btnLog10.place(x = 360,y = 450,width = 60,height = 50)

btnPow = tkinter.Button(root,text = 'x^y',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('^'))
btnPow.place(x = 290,y = 175,width = 60,height = 50)
btnExp = tkinter.Button(root,text = 'e^x',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('e^'))
btnExp.place(x = 290,y = 230,width = 60,height = 50)
btnLn = tkinter.Button(root,text = 'ln',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('ln('))
btnLn.place(x = 290,y = 285,width = 60,height = 50)
btnLog = tkinter.Button(root,text = 'log(b,a)',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('log('))
btnLog.place(x = 290,y = 340,width = 60,height = 50)
btnMod = tkinter.Button(root,text = 'mod',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('mod'))
btnMod.place(x = 290,y = 395,width = 60,height = 50)
btnAbs = tkinter.Button(root,text = 'abs',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('abs('))
btnAbs.place(x = 290,y = 450,width = 60,height = 50)

btnSin = tkinter.Button(root,text = 'sin',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('sin('))
btnSin.place(x = 220,y = 175,width = 60,height = 50)
btnCos = tkinter.Button(root,text = 'cos',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('cos('))
btnCos.place(x = 220,y = 230,width = 60,height = 50)
btnTan = tkinter.Button(root,text = 'tan',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('tan('))
btnTan.place(x = 220,y = 285,width = 60,height = 50)
btnAsin = tkinter.Button(root,text = 'arcsin',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('arcsin('))
btnAsin.place(x = 220,y = 340,width = 60,height = 50)
btnAcos = tkinter.Button(root,text = 'arccos',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('arccos('))
btnAcos.place(x = 220,y = 395,width = 60,height = 50)
btnAtan = tkinter.Button(root,text = 'arctan',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('arctan('))
btnAtan.place(x = 220,y = 450,width = 60,height = 50)

btnFact = tkinter.Button(root,text = 'n!',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('fact('))
btnFact.place(x = 150,y = 175,width = 60,height = 50)
btnPerm = tkinter.Button(root,text = 'P(m,n)',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('perm('))
btnPerm.place(x = 150,y = 230,width = 60,height = 50)
btnComb = tkinter.Button(root,text = 'C(m,n)',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('comb('))
btnComb.place(x = 150,y = 285,width = 60,height = 50)
btnPer = tkinter.Button(root,text = '%',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('%'))
btnPer.place(x = 150,y = 340,width = 60,height = 50)
btnX = tkinter.Button(root,text = 'x',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('x'))
btnX.place(x = 150,y = 395,width = 60,height = 50)
btnY = tkinter.Button(root,text = 'y',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('y'))
btnY.place(x = 150,y = 450,width = 60,height = 50)

btnA = tkinter.Button(root,text = 'A',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('A'))
btnA.place(x = 80,y = 175,width = 60,height = 50)
btnB = tkinter.Button(root,text = 'B',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('B'))
btnB.place(x = 80,y = 230,width = 60,height = 50)
btnC = tkinter.Button(root,text = 'C',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('C'))
btnC.place(x = 80,y = 285,width = 60,height = 50)
btnD = tkinter.Button(root,text = 'D',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('D'))
btnD.place(x = 80,y = 340,width = 60,height = 50)
btnE = tkinter.Button(root,text = 'E',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('E'))
btnE.place(x = 80,y = 395,width = 60,height = 50)
btnF = tkinter.Button(root,text = 'F',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda : PressExpr('F'))
btnF.place(x = 80,y = 450,width = 60,height = 50)


def GetKey(event):
    if event.char == '\b':
        PressCtrl('backspace')
    elif event.char == '\r':
        PressEqual()
    else:
        PressExpr(event.char)
        
root.bind('<Key>', GetKey)

#操作函数

UniSym = ['ans','^2','^3','^0.5','^-1','mod','10^','log10(',
          'e^','ln(','log(','abs(',
          'fact(','perm(','comb(',
          'sin(','cos(','tan(','arcsin(','arccos(','arctan(']

FuncSym = UniSym[6:]

SingleSym = ['+','-','*','/','.',',','%']

NumSym = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f',
          'M','pi','e','ans','x','y','A','B','C','D','E','F']

priorAns = False

curRadix = 'Dec'

A = B = C = D = E = F = M = x = y = ans = 0

#表达式类按键输入
def PressExpr(Sym):                #设置一个数字函数 判断是否按下数字 并获取数字将数字写在显示版上
    global lists
    global priorAns
    if priorAns == True and (Sym in NumSym or Sym in FuncSym):
        result.set('')
    priorAns = False
    oldExpr = result.get()
    if oldExpr != '' and oldExpr[-1] in SingleSym and Sym in SingleSym:
        newExpr = oldExpr[:-1] + Sym
        result.set(newExpr)
    else:
        newExpr = oldExpr + Sym
        result.set(newExpr)         #将按下的数字写到面板中


#控制类按键输入
def PressCtrl(Sym):
    global lists
    global ans
    curExpr = result.get()
    if Sym == 'AC':                 #如果按下的是'AC'按键，则清空列表内容，讲屏幕上的数字键设置为默认数字0
        A = B = C = D = E = F = M = x = y = ans = 0
        result.set('')
        result2.set('')
        result3.set('')
    elif Sym == 'CE':
        result.set('')
    elif Sym == 'backspace':          #如果按下的是退格按键，删除一位数字或是一个整体符号
        if curExpr[-10:] in UniSym:
            result.set(curExpr[0:-10])
        elif curExpr[-9:] in UniSym:
            result.set(curExpr[0:-9])
        elif curExpr[-8:] in UniSym:
            result.set(curExpr[0:-8])
        elif curExpr[-7:] in UniSym:
            result.set(curExpr[0:-7])
        elif curExpr[-6:] in UniSym:
            result.set(curExpr[0:-6])
        elif curExpr[-5:] in UniSym:
            result.set(curExpr[0:-5])
        elif curExpr[-4:] in UniSym:
            result.set(curExpr[0:-4])
        elif curExpr[-3:] in UniSym:
            result.set(curExpr[0:-3])
        elif curExpr[-2:] in UniSym:
            result.set(curExpr[0:-2])
        else:
            result.set(curExpr[0:-1])
    else:
        pass

#角度/弧度切换
def sin(x):
    if Angle.get() == 1:
        return math.sin(x*pi/180)
    elif Angle.get() == 2:
        return math.sin(x)
    else:
        return math.sin(x*pi/200)
    
def cos(x):
    if Angle.get() == 1:
        return math.cos(x*pi/180)
    elif Angle.get() == 2:
        return math.cos(x)
    else:
        return math.cos(x*pi/200)
    
def tan(x):
    if Angle.get() == 1:
        return math.tan(x*pi/180)
    elif Angle.get() == 2:
        return math.tan(x)
    else:
        return math.tan(x*pi/200)
    
def arcsin(x):
    if Angle.get() == 1:
        return math.asin(x)*180/pi
    elif Angle.get() == 2:
        return math.asin(x)
    else:
        return math.asin(x)*200/pi
    
def arccos(x):
    if Angle.get() == 1:
        return math.acos(x)*180/pi
    elif Angle.get() == 2:
        return math.acos(x)
    else:
        return math.acos(x)*200/pi
    
def arctan(x):
    if Angle.get() == 1:
        return math.atan(x)*180/pi
    elif Angle.get() == 2:
        return math.atan(x)
    else:
        return math.atan(x)*200/pi

def ln(x):
    return math.log(x)

def log(b,a):
    return math.log(a,b)

def fact(x):
    return x > 1 and x * fact(x - 1) or 1


#获取运算结果函数
def PressEqual():
    global lists
    global priorAns
    global ans
    global curRadix
    try:
        DispStr = result.get()       #设置当前数字变量，并获取添加到列表
        CompStr = DispStr
        CompStr = CompStr.replace('^','**')
        CompStr = CompStr.replace('%','*0.01')
        CompStr = CompStr.replace('mod','%')
        CompStr = CompStr.replace('π','pi')
        if not(CompStr.find('0**0')):
            raise ValueError
        
        if curRadix == 'Dec':
            FixedExpr = CompStr
        else:
            FixedExpr = RadixFixExpr(CompStr)

        if curRadix != 'Dec':
            ans = int(modf(eval(FixedExpr))[1])
        elif abs(eval(FixedExpr) - int(eval(FixedExpr))) <= 1e-17:
            ans = int(eval(FixedExpr))
        else:
            ans = float('%.16f'% eval(FixedExpr))

        if curRadix == 'Bin':
            if len('{0:b}'.format(ans)) > 32:
                raise OverflowError
            result.set('{0:b}'.format(ans))
        elif curRadix == 'Oct':
            if len('{0:o}'.format(ans)) > 32:
                raise OverflowError
            result.set('{0:o}'.format(ans))
        elif curRadix == 'Hex':
            if len('{0:x}'.format(ans)) > 32:
                raise OverflowError
            result.set('{0:x}'.format(ans).lower())
        elif ans >= 1e17:
            result.set(('{0:.16e}'.format(ans)).lower())
        else:
            result.set(ans)
        result2.set(DispStr)     #将运算过程显示到屏幕2
        priorAns = True
    except ZeroDivisionError:
        #除法时，除数不能为0
        mbox.showerror('除零错误',message = '除法计算时！除数不能为0！')
    except ValueError:
        mbox.showerror('非法运算',message = '结果异常！请检查表达式是否合法！')
    except OverflowError:
        mbox.showerror('上界溢出',message = '结果超过了程序最大可表示范围！')
    except:
        mbox.showerror('语法错误',message = '表达式有误！') 


def PressMem(Sym):
    global M
    global ans
    if Sym == 'MC':
        M = 0
        result3.set('')
    elif Sym == 'MS':
        PressEqual()
        result2.set(result2.get() + '→M')
        M = ans
        if M != 0:
            result3.set('M')
        else:
            result3.set('')
    elif Sym == 'M+':
        PressEqual()
        result2.set('ans M+')
        ans += M
        result.set(ans)
    elif Sym == 'M-':
        PressEqual()
        result2.set('ans M-')
        ans -= M
        result.set(ans)
    else:
        pass

def RadixCvt(Sym):
    global curRadix
    curStr = result.get()
    if curStr != '':
        try:
            if curRadix == 'Bin':
                curVal = int(curStr, 2)
            elif curRadix == 'Oct':
                curVal = int(curStr, 8)
            elif curRadix == 'Dec':
                curVal = int(curStr, 10)
            else:
                curVal = int(curStr, 16)
            if curVal >= 0:
                sign = 0
            else:
                sign = 1
            if Sym == 'Bin':
                curStr = bin(curVal)
                curStr = curStr[0:sign] + curStr[sign + 2:]
            elif Sym == 'Oct':
                curStr = oct(curVal)
                curStr = curStr[0:sign] + curStr[sign + 2:]
            elif Sym == 'Dec':
                curStr = str(curVal)
            else:
                curStr = hex(curVal)
                curStr = curStr[0:sign] + curStr[sign + 2:]
        except ValueError:
            result.set('')
        except:
            mbox.showerror('语法错误',message = '表达式有误！') 
    else:
        pass
    result.set(curStr.lower())
    curRadix = Sym
    if curRadix == 'Bin':
        btn2.config(state = tkinter.DISABLED)
        btn3.config(state = tkinter.DISABLED)
        btn4.config(state = tkinter.DISABLED)
        btn5.config(state = tkinter.DISABLED)
        btn6.config(state = tkinter.DISABLED)
        btn7.config(state = tkinter.DISABLED)
        btn8.config(state = tkinter.DISABLED)
        btn9.config(state = tkinter.DISABLED)
        btnA.config(text = 'A',command = lambda : PressExpr('A'),state = tkinter.DISABLED)
        btnB.config(text = 'B',command = lambda : PressExpr('B'),state = tkinter.DISABLED)
        btnC.config(text = 'C',command = lambda : PressExpr('C'),state = tkinter.DISABLED)
        btnD.config(text = 'D',command = lambda : PressExpr('D'),state = tkinter.DISABLED)
        btnE.config(text = 'E',command = lambda : PressExpr('E'),state = tkinter.DISABLED)
        btnF.config(text = 'F',command = lambda : PressExpr('F'),state = tkinter.DISABLED)
    elif curRadix == 'Oct':
        btn2.config(state = tkinter.NORMAL)
        btn3.config(state = tkinter.NORMAL)
        btn4.config(state = tkinter.NORMAL)
        btn5.config(state = tkinter.NORMAL)
        btn6.config(state = tkinter.NORMAL)
        btn7.config(state = tkinter.NORMAL)
        btn8.config(state = tkinter.DISABLED)
        btn9.config(state = tkinter.DISABLED)
        btnA.config(text = 'A',command = lambda : PressExpr('A'),state = tkinter.DISABLED)
        btnB.config(text = 'B',command = lambda : PressExpr('B'),state = tkinter.DISABLED)
        btnC.config(text = 'C',command = lambda : PressExpr('C'),state = tkinter.DISABLED)
        btnD.config(text = 'D',command = lambda : PressExpr('D'),state = tkinter.DISABLED)
        btnE.config(text = 'E',command = lambda : PressExpr('E'),state = tkinter.DISABLED)
        btnF.config(text = 'F',command = lambda : PressExpr('F'),state = tkinter.DISABLED)
    elif curRadix == 'Dec':
        btn2.config(state = tkinter.NORMAL)
        btn3.config(state = tkinter.NORMAL)
        btn4.config(state = tkinter.NORMAL)
        btn5.config(state = tkinter.NORMAL)
        btn6.config(state = tkinter.NORMAL)
        btn7.config(state = tkinter.NORMAL)
        btn8.config(state = tkinter.NORMAL)
        btn9.config(state = tkinter.NORMAL)
        btnA.config(text = 'A',command = lambda : PressExpr('A'),state = tkinter.NORMAL)
        btnB.config(text = 'B',command = lambda : PressExpr('B'),state = tkinter.NORMAL)
        btnC.config(text = 'C',command = lambda : PressExpr('C'),state = tkinter.NORMAL)
        btnD.config(text = 'D',command = lambda : PressExpr('D'),state = tkinter.NORMAL)
        btnE.config(text = 'E',command = lambda : PressExpr('E'),state = tkinter.NORMAL)
        btnF.config(text = 'F',command = lambda : PressExpr('F'),state = tkinter.NORMAL)
    else:
        btn2.config(state = tkinter.NORMAL)
        btn3.config(state = tkinter.NORMAL)
        btn4.config(state = tkinter.NORMAL)
        btn5.config(state = tkinter.NORMAL)
        btn6.config(state = tkinter.NORMAL)
        btn7.config(state = tkinter.NORMAL)
        btn8.config(state = tkinter.NORMAL)
        btn9.config(state = tkinter.NORMAL)
        btnA.config(text = 'a',command = lambda : PressExpr('a'),state = tkinter.NORMAL)
        btnB.config(text = 'b',command = lambda : PressExpr('b'),state = tkinter.NORMAL)
        btnC.config(text = 'c',command = lambda : PressExpr('c'),state = tkinter.NORMAL)
        btnD.config(text = 'd',command = lambda : PressExpr('d'),state = tkinter.NORMAL)
        btnE.config(text = 'e',command = lambda : PressExpr('e'),state = tkinter.NORMAL)
        btnF.config(text = 'f',command = lambda : PressExpr('f'),state = tkinter.NORMAL)

def RadixFixExpr(Expr):
    global curRadix
    res = ''
    if curRadix == 'Bin':
        listNum = re.findall(r"[0|1]+",Expr)
        prefix = '0b'
    elif curRadix == 'Oct':
        listNum = re.findall(r"[0-7]+",Expr)
        prefix = '0o'
    else:
        listNum = re.findall(r"[0-9|a|b|c|d|e|f]+",Expr)
        prefix = '0x'
    for i in listNum:
        n = Expr.find(i)
        res = res + Expr[0:n] + prefix + i
        Expr = Expr[n+len(i):]
    res = res + Expr
    return res
root.mainloop()
