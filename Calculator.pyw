import tkinter
from tkinter import *
import tkinter.messagebox as mbox
from numpy import *
from re import *
from numpy.linalg import *

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
import numpy as np
from functools import partial
from math import log, log10,sin,exp,pi,cos

import math
from math import *
import scipy
from scipy.special import perm as perm, comb as comb, factorial as fact

from tkinter import ttk as ttk
import numpy

from matplotlib import pyplot
import pylab as pl

import sympy
from sympy import *

'''*****************************************************************窗体设计部分*****************************************************************'''

root = None

def main():
    global root
    try:
        root.destroy()
    except:
        pass
    root = tkinter.Tk()

    def about():
        tkinter.messagebox.showinfo('关于',message = '组长：阮超逸\n组员：周高超、肖文宗')

    #菜单栏部分
    Menubar = tkinter.Menu(root)

    PlotList = tkinter.Menu(Menubar,tearoff = 0)
    PlotList.add_command(label = '2D绘图',command = lambda:Plot2D())
    PlotList.add_command(label = '3D绘图',command = lambda:Plot3D())

    Preference = tkinter.Menu(Menubar,tearoff = 0)
    Preference.add_command(label = '普通计算',command = lambda:main())
    Preference.add_command(label = '统计数学',command = lambda:Statistics())
    Preference.add_command(label = '微积分',command = lambda:Calculus())
    Preference.add_command(label = '线性代数',command = lambda:LinearAlgebra())
    Preference.add_cascade(label = '绘图',menu = PlotList)

    Preference.add_separator()
    Preference.add_command(label = '退出',command = lambda:root.destroy())

    Edit = tkinter.Menu(Menubar,tearoff = 0)
    Edit.add_command(label = '复制',command = lambda:(root.clipboard_clear(),root.clipboard_append(result.get())))
    Edit.add_command(label = '粘贴',command = lambda:result.set(root.clipboard_get()))

    Help = tkinter.Menu(Menubar,tearoff = 0)
    Help.add_command(label = '关于...',command = lambda:about())

    Menubar.add_cascade(label = '选项',menu = Preference)
    Menubar.add_cascade(label = '编辑',menu = Edit)
    Menubar.add_cascade(label = '帮助',menu = Help)
    root['menu'] = Menubar

    #窗体大小、名称与图标
    root.maxsize(800,520)
    root.minsize(800,520)
    root.resizable(False,False)
    root.title('Calculator')
    root.iconbitmap('.\Calculator.ico')

    #当前表达式（计算结果）、上一次计算的表达式与‘M’累加器显示屏
    result = tkinter.StringVar()    #当前表达式（结果）
    result.set('')
    result2 = tkinter.StringVar()   #上一次计算的表达式
    result2.set('')
    result3 = tkinter.StringVar()   #‘M’记号
    result3.set('')

    #对应的显示屏
    label = tkinter.Label(root,font = ('微软雅黑',15),bg = '#EEE9E9',bd ='9',fg = '#828282',anchor = 'se',textvariable = result2)
    label.place(width = 800,height = 80)
    label3 = tkinter.Label(root,font = ('微软雅黑',10),bg = '#EEE9E9',bd ='9',fg = '#828282',anchor = 'se',textvariable = result3)
    label3.place(width = 800,height = 45)
    label2 = tkinter.Label(root,font = ('微软雅黑',30),bg = '#EEE9E9',bd ='9',fg = 'black',anchor = 'se',textvariable = result)
    label2.place(y = 78,width = 800,height = 60)

    #进制切换单选框
    Radix = tkinter.IntVar()
    Radix.set(3)
    Bin = tkinter.Radiobutton(root,variable = Radix,text = 'Bin',value = 1,command = lambda:RadixCvt('Bin'))
    Bin.place(x = 480, y = 145)
    Oct = tkinter.Radiobutton(root,variable = Radix,text = 'Oct',value = 2,command = lambda:RadixCvt('Oct'))
    Oct.place(x = 555, y = 145)
    Dec = tkinter.Radiobutton(root,variable = Radix,text = 'Dec',value = 3,command = lambda:RadixCvt('Dec'))
    Dec.place(x = 630, y = 145)
    Hex = tkinter.Radiobutton(root,variable = Radix,text = 'Hex',value = 4,command = lambda:RadixCvt('Hex'))
    Hex.place(x = 705, y = 145)

    #角度切换单选框：度（Deg，一周为360度）、弧度（Rad，一周为2π）与梯度（Grad，一周为400梯度）
    Angle = tkinter.IntVar()
    Angle.set(2)
    Deg = tkinter.Radiobutton(root,variable = Angle,text = 'Deg',value = 1,command = lambda:(PressCtrl('↑') , PressCtrl('↑')))
    Deg.place(x = 110, y = 145)
    Rad = tkinter.Radiobutton(root,variable = Angle,text = 'Rad',value = 2,command = lambda:(PressCtrl('↑') , PressCtrl('↑')))
    Rad.place(x = 185, y = 145)
    Grad = tkinter.Radiobutton(root,variable = Angle,text = 'Grad',value = 3,command = lambda:(PressCtrl('↑') , PressCtrl('↑')))
    Grad.place(x = 260, y = 145)

    #常用区数字按键：0-9、百分数‘%’、小数点‘.’、圆周率π、自然对数的底数e和结果寄存器ans
    btn7 = tkinter.Button(root,text = '7',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('7'))
    btn7.place(x = 450,y = 285,width = 60,height = 50)
    btn8 = tkinter.Button(root,text = '8',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('8'))
    btn8.place(x = 520,y = 285,width = 60,height = 50)
    btn9 = tkinter.Button(root,text = '9',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('9'))
    btn9.place(x = 590,y = 285,width = 60,height = 50)
    btn4 = tkinter.Button(root,text = '4',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('4'))
    btn4.place(x = 450,y = 340,width = 60,height = 50)
    btn5 = tkinter.Button(root,text = '5',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('5'))
    btn5.place(x = 520,y = 340,width = 60,height = 50)
    btn6 = tkinter.Button(root,text = '6',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('6'))
    btn6.place(x = 590,y = 340,width = 60,height = 50)
    btn1 = tkinter.Button(root,text = '1',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('1'))
    btn1.place(x = 450,y = 395,width = 60,height = 50)
    btn2 = tkinter.Button(root,text = '2',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('2'))
    btn2.place(x = 520,y = 395,width = 60,height = 50)
    btn3 = tkinter.Button(root,text = '3',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('3'))
    btn3.place(x = 590,y = 395,width = 60,height = 50)
    btn0 = tkinter.Button(root,text = '0',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('0'))
    btn0.place(x = 520,y = 450,width = 60,height = 50)
    btnPer = tkinter.Button(root,text = '%',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('%'))
    btnPer.place(x = 450,y = 450,width = 60,height = 50)
    btnDot = tkinter.Button(root,text = '.',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('.'))
    btnDot.place(x = 590,y = 450,width = 60,height = 50)
    btnPi = tkinter.Button(root,text = 'π',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda :PressExpr ('π'))
    btnPi.place(x = 730,y = 285,width = 60,height = 50)
    btne = tkinter.Button(root,text = 'e',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('e'))
    btne.place(x = 730,y = 340,width = 60,height = 50)
    btnAns = tkinter.Button(root,text = 'ans',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('ans'))
    btnAns.place(x = 730,y = 395,width = 60,height = 50)

    #常用区运算符、控制符按键：AC、CE、BS、左括号‘(’、右括号‘)’、+、-、×、/、计算（Calc）
    btnAc = tkinter.Button(root,text = 'AC',bd = 0.5,font = ('微软雅黑',12),fg = 'orange',command = lambda:PressCtrl('AC'))
    btnAc.place(x = 450,y = 230,width = 60,height = 50)
    btnCe = tkinter.Button(root,text = 'CE',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressCtrl('CE'))
    btnCe.place(x = 520,y = 230,width = 60,height = 50)
    btnBack = tkinter.Button(root,text = '←',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressCtrl('backspace'))
    btnBack.place(x = 590,y = 230,width = 60,height = 50)
    btnLpar = tkinter.Button(root,text = '(',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('('))
    btnLpar.place(x = 660,y = 230,width = 60,height = 50)
    btnRpar = tkinter.Button(root,text =')',font = ('微软雅黑',12),fg = "#4F4F4F",bd = 0.5,command = lambda:PressExpr(')'))
    btnRpar.place(x = 730,y = 230,width = 60,height = 50)
    btnAdd = tkinter.Button(root,text = '+',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('+'))
    btnAdd.place(x = 660,y = 285,width = 60,height = 50)
    btnSub = tkinter.Button(root,text = '-',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('-'))
    btnSub.place(x = 660,y = 340,width = 60,height = 50)
    btnMul = tkinter.Button(root,text = '×',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('×'))
    btnMul.place(x = 660,y = 395,width = 60,height = 50)
    btnDiv = tkinter.Button(root,text = '÷',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('/'))
    btnDiv.place(x = 660,y = 450,width = 60,height = 50)
    btnCalc = tkinter.Button(root,text = 'Calc',bg = 'orange',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressEqual())
    btnCalc.place(x = 730,y = 450,width = 60,height = 50)

    #累加/累减器M控制键：MC、M+、M-、MS、MR
    btnMc = tkinter.Button(root,text = 'MC',bd = 0.5,font = ('微软雅黑',12),fg = 'orange',command = lambda:PressMem('MC'))
    btnMc.place(x = 450,y = 175,width = 60,height = 50)
    btnMadd = tkinter.Button(root,text = 'M+',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressMem('M+'))
    btnMadd.place(x = 520,y = 175,width = 60,height = 50)
    btnMsub = tkinter.Button(root,text = 'M-',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressMem('M-'))
    btnMsub.place(x = 590,y = 175,width = 60,height = 50)
    btnMst = tkinter.Button(root,text = 'MS',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressMem('MS'))
    btnMst.place(x = 660,y = 175,width = 60,height = 50)
    btnMrd = tkinter.Button(root,text = 'MR',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('M'))
    btnMrd.place(x = 730,y = 175,width = 60,height = 50)

    #功能函数键右1:平方、立方、开根号、倒数、10的幂、工程对数
    btnSqr = tkinter.Button(root,text = 'x^2',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('^2'))
    btnSqr.place(x = 360,y = 175,width = 60,height = 50)
    btnCub = tkinter.Button(root,text = 'x^3',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('^3'))
    btnCub.place(x = 360,y = 230,width = 60,height = 50)
    btnSqrt = tkinter.Button(root,text = '√x',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('^0.5'))
    btnSqrt.place(x = 360,y = 285,width = 60,height = 50)
    btnRev = tkinter.Button(root,text = '1/x',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('^-1'))
    btnRev.place(x = 360,y = 340,width = 60,height = 50)
    btnPow10 = tkinter.Button(root,text = '10^x',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('10^'))
    btnPow10.place(x = 360,y = 395,width = 60,height = 50)
    btnLog10 = tkinter.Button(root,text = 'log10',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('log10('))
    btnLog10.place(x = 360,y = 450,width = 60,height = 50)

    #功能函数键右2：x^y，e的幂（注意与10的幂区分）、自然对数、一般对数、求余、绝对值
    btnExp = tkinter.Button(root,text = 'e^x',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('e^'))
    btnExp.place(x = 290,y = 175,width = 60,height = 50)
    btnLn = tkinter.Button(root,text = 'ln',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('ln('))
    btnLn.place(x = 290,y = 230,width = 60,height = 50)
    btnPow = tkinter.Button(root,text = 'x^y',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('^'))
    btnPow.place(x = 290,y = 285,width = 60,height = 50)
    btnLog = tkinter.Button(root,text = 'log(b,a)',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('log('))
    btnLog.place(x = 290,y = 340,width = 60,height = 50)
    btnMod = tkinter.Button(root,text = 'mod',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('mod'))
    btnMod.place(x = 290,y = 395,width = 60,height = 50)
    btnAbs = tkinter.Button(root,text = 'abs',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('abs('))
    btnAbs.place(x = 290,y = 450,width = 60,height = 50)

    #功能函数键右3：（反）三角函数与（反）双曲函数，双曲函数按‘↑’切换
    btnSin = tkinter.Button(root,text = 'sin',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('sin('))
    btnSin.place(x = 220,y = 175,width = 60,height = 50)
    btnCos = tkinter.Button(root,text = 'cos',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('cos('))
    btnCos.place(x = 220,y = 230,width = 60,height = 50)
    btnTan = tkinter.Button(root,text = 'tan',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('tan('))
    btnTan.place(x = 220,y = 285,width = 60,height = 50)
    btnAsin = tkinter.Button(root,text = 'arcsin',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('arcsin('))
    btnAsin.place(x = 220,y = 340,width = 60,height = 50)
    btnAcos = tkinter.Button(root,text = 'arccos',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('arccos('))
    btnAcos.place(x = 220,y = 395,width = 60,height = 50)
    btnAtan = tkinter.Button(root,text = 'arctan',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('arctan('))
    btnAtan.place(x = 220,y = 450,width = 60,height = 50)

    #功能函数键右4：阶乘、排列、组合（均为由欧拉积分函数延拓而得的连续函数），逗号，寄存器x与y
    btnFact = tkinter.Button(root,text = 'n!',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('fact('))
    btnFact.place(x = 150,y = 175,width = 60,height = 50)
    btnPerm = tkinter.Button(root,text = 'P(m,n)',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('perm('))
    btnPerm.place(x = 150,y = 230,width = 60,height = 50)
    btnComb = tkinter.Button(root,text = 'C(m,n)',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('comb('))
    btnComb.place(x = 150,y = 285,width = 60,height = 50)
    btnComma = tkinter.Button(root,text = ',',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr(','))
    btnComma.place(x = 150,y = 340,width = 60,height = 50)
    btnX = tkinter.Button(root,text = 'x',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('x'))
    btnX.place(x = 150,y = 395,width = 60,height = 50)
    btnY = tkinter.Button(root,text = 'y',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('y'))
    btnY.place(x = 150,y = 450,width = 60,height = 50)

    #功能函数键右5：寄存器A-F
    btnA = tkinter.Button(root,text = 'A',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('A'))
    btnA.place(x = 80,y = 175,width = 60,height = 50)
    btnB = tkinter.Button(root,text = 'B',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('B'))
    btnB.place(x = 80,y = 230,width = 60,height = 50)
    btnC = tkinter.Button(root,text = 'C',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('C'))
    btnC.place(x = 80,y = 285,width = 60,height = 50)
    btnD = tkinter.Button(root,text = 'D',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('D'))
    btnD.place(x = 80,y = 340,width = 60,height = 50)
    btnE = tkinter.Button(root,text = 'E',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('E'))
    btnE.place(x = 80,y = 395,width = 60,height = 50)
    btnF = tkinter.Button(root,text = 'F',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('F'))
    btnF.place(x = 80,y = 450,width = 60,height = 50)

    #功能函数键右6：‘↑’、寄存器存储控制、科学计数法转换、结果切换正负号、取整、角度切换
    btnShift = tkinter.Button(root,text = '↑',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressCtrl('↑'))
    btnShift.place(x = 10,y = 175,width = 60,height = 50)
    btnSto = tkinter.Button(root,text = 'sto',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressCtrl('sto'))
    btnSto.place(x = 10,y = 230,width = 60,height = 50)
    btnFE = tkinter.Button(root,text = 'F-E',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressCtrl('F-E'))
    btnFE.place(x = 10,y = 285,width = 60,height = 50)
    btnInt = tkinter.Button(root,text = 'int',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('int('))
    btnInt.place(x = 10,y = 340,width = 60,height = 50)
    btnDms = tkinter.Button(root,text = '→dms',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('ToDms('))
    btnDms.place(x = 10,y = 395,width = 60,height = 50)
    btnRad = tkinter.Button(root,text = 'deg',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('deg('))
    btnRad.place(x = 10,y = 450,width = 60,height = 50)


    '''*****************************************************************功能实现部分*****************************************************************'''


    #整体符号表：每一项都是一个整体，按BS删除时一起删除
    UniSym = ['ans','mod','<<','>>','log10(','comp(',
              'e^','ln(','log(','abs(','int(','ToDms(','DmsTo(',
              'fact(','perm(','comb(','deg(','rad(','grad',
              'sin(','cos(','tan(','arcsin(','arccos(','arctan(',
              'sinh(','cosh(','tanh(','arcsinh(','arccosh(','arctanh(']

    #函数符号表：形如func()型的符号
    FuncSym = UniSym[4:]

    #单字符符号表,规定mod为单字符符号
    SingleSym = ['.',',','%','+','-','×','*','/','^','mod','<<','>>']

    #二元运算符号表
    OperaSym = SingleSym[3:]

    #数值符号表：每一项都能转化为一个数。注意e在十进制中与十六进制中不同的含义
    NumSym = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F',
              'M','pi','ans','x','y']

    NumBtn =    [btn0, btn1, btn2, btn3, btn4, btn5, btn6,  btn7, btn8, btn9,
                 btnA, btnB, btnC, btnD, btnE, btnF, btnPi, btne, btnX, btnY]

    MBtn =      [btnMc, btnMadd, btnMsub, btnMst, btnMrd]

    DecOprBtn = [btnPer, btnDot]

    FuncBtn =   [btnSqr,   btnCub,  btnSqrt, btnRev,  btnPow10, btnLog10,
                 btnExp,   btnLn,   btnPow,  btnLog,  btnMod,   btnAbs,
                 btnSin,   btnCos,  btnTan,  btnAsin, btnAcos,  btnAtan,
                 btnFact,  btnPerm, btnComb, btnComma,
                 btnShift, btnSto,  btnFE,   btnInt,  btnDms,   btnRad]

    #先前是否有答案
    priorAns = False

    #是否按下‘↑’
    isShift = False

    #当前进制。角度制切换后不会自动切换显示，而进制切换会自动切换显示
    curRadix = 'Dec'

    #寄存器
    A = B = C = D = E = F = M = x = y = ans = 0

    #监视键盘的有效输入，以及菜单与快捷键的复制粘贴
    def GetKey(event):
        if event.char == '\b':
            PressCtrl('backspace')
        elif event.char == '\r':
            PressEqual()
        elif curRadix == 'Hex' and event.char.upper() in NumSym[10:15]:
            PressExpr(event.char.upper())
        elif curRadix == 'Dec' and event.char.upper() in NumSym[10:13] + ['F']:
            PressExpr(event.char.upper())
        elif not(event.char in SingleSym or event.char in NumSym):
            pass
        elif curRadix == 'Bin' and not event.char in NumSym[:2] + OperaSym:
            pass
        elif curRadix == 'Oct' and not event.char in NumSym[:8] + OperaSym:
            pass
        elif curRadix == 'Hex' and not event.char.upper() in NumSym[:16] + OperaSym:
            pass
        else:
            PressExpr(event.char)

    def EditExpr(event):   
        Edit.post(event.x_root, event.y_root)

    def Copy(event):
        root.clipboard_clear()
        root.clipboard_append(result.get())

    def Paste(event):
        result.set(root.clipboard_get())

    root.bind('<Control-C>', Copy)
    root.bind('<Control-c>', Copy)
    root.bind('<Control-V>', Paste)
    root.bind('<Control-v>', Paste)
    root.bind('<Key>', GetKey)
    label2.bind('<Button-3>', EditExpr)

    #考虑到角度制转换的（反）三角函数
    def sin(x):
        return Angle.get() == 1 and math.sin(x*pi/180) or Angle.get() == 2 and math.sin(x) or math.sin(x*pi/200)
        
    def cos(x):
        return Angle.get() == 1 and math.cos(x*pi/180) or Angle.get() == 2 and math.cos(x) or math.cos(x*pi/200)
        
    def tan(x):
        return Angle.get() == 1 and math.tan(x*pi/180) or Angle.get() == 2 and math.tan(x) or math.tan(x*pi/200)

    def arcsin(x):
        return Angle.get() == 1 and math.asin(x)*180/pi or Angle.get() == 2 and math.asin(x) or math.asin(x)*200/pi
        
    def arccos(x):
        return Angle.get() == 1 and math.acos(x)*180/pi or Angle.get() == 2 and math.acos(x) or math.acos(x)*200/pi
       
    def arctan(x):
        return Angle.get() == 1 and math.atan(x)*180/pi or Angle.get() == 2 and math.atan(x) or math.atan(x)*200/pi

    #函数转名加壳，方便计算时使用eval()函数
    def arcsinh(x):
        return math.asinh(x)

    def arccosh(x):
        return math.acosh(x)

    def arctanh(x):
        return math.atanh(x)

    def ln(x):
        return math.log(x)

    def log(b,a):
        return math.log(a,b)

    #角度转换
    def deg(x):
        return Angle.get() == 2 and x * 180 / pi or Angle.get() == 3 and x * 180 / 200 or x

    def rad(x):
        return Angle.get() == 1 and x * pi / 180 or Angle.get() == 3 and x * pi / 200 or x
        
    def grad(x):
        return Angle.get() == 1 and x * 200 / 180 or Angle.get() == 2 and x * 200 / pi or x

    #度分秒↔当前角度制
    def ToDms(x):
        x = deg(x)
        x_deg = int(x)
        x_min = (x - x_deg) * 0.6
        x_min = float('%13f'%x_min)
        x_sec = int(x_min * 100)
        x_sec = (x_min * 100 - x_sec) * 0.006
        x_min = int(x_min * 100)/100
        return x_deg + x_min + x_sec

    def DmsTo(x):
        x_deg = int(x)
        x_min = (x - x_deg) / 0.6
        x_min = float('%13f'%x_min)
        x_sec = int(x_min * 100)
        x_sec = (x_min * 100 - x_sec) / 60
        x_min = int(x_min * 100)/100
        res = x_deg + x_min + x_sec
        return Angle.get() == 2 and res * pi / 180 or Angle.get() == 3 and res * 200 / 180 or res

    #求补运算
    def comp(x):
        scale = curRadix == 'Bin' and 1 or curRadix == 'Oct' and 3 or curRadix == 'Hex' and 4
        return x & int("1"*(x >= -2**7 and x < 2**7 and 8 or x >= -2**15 and x < 2**15 and 16 or
                            x >= -2**31 and x < 2**31 and 32 or x >= -2**63 and x < 2**63 and 64), 2)

    #进制转换时切换结果显示屏上的进制、控制部分按钮的使用
    def RadixCvt(Sym):
        nonlocal A,B,C,D,E,F,x,y,M,UniSym,FuncSym,SingleSym,OperaSym,NumBtn,MBtn,DecOprBtn,FuncBtn,priorAns,isShift,curRadix,ans
        curStr = result.get()
        if curStr != '':
            try:
                curVal = curRadix == 'Bin' and int(curStr, 2) or curRadix == 'Oct' and int(curStr, 8) or curRadix == 'Dec' and int(curStr, 10) or int(curStr, 16)
                sign = curVal < 0 and 1 or 0
                curStr = (Sym == 'Bin' and bin(curVal)[0:sign] + bin(curVal)[sign+2:] or Sym == 'Oct' and oct(curVal)[0:sign] + oct(curVal)[sign+2:] or
                          Sym == 'Dec' and str(curVal) or hex(curVal)[0:sign] + hex(curVal)[sign+2:])
                result.set(curStr.upper())
            except ValueError:
                result.set('')
            except:
                tkinter.messagebox.showerror('语法错误',message = '表达式有误！') 
        else:
            pass
        curRadix = Sym
        if curRadix == 'Dec':
            for i in MBtn + DecOprBtn + FuncBtn:
                i.config(state = tkinter.NORMAL)
            isShift = True
            PressCtrl('↑')
            PressSto('sto')
            btnSqr.config(text = 'x^2',command = lambda:PressExpr('^2'))
            btnCub.config(text = 'x^3',command = lambda:PressExpr('^3'))
            btnSqrt.config(text = '√x',command = lambda:PressExpr('^0.5'))
            btnRev.config(text = '1/x',command = lambda:PressExpr('^-1'))
            btnPow10.config(text = '10^x',command = lambda:PressExpr('10^'))
            btnLog10.config(text = 'log10',command = lambda:PressExpr('log10('))
            btnExp.config(text = 'e^x',command = lambda:PressExpr('e^'))
            btnLn.config(text = 'ln',command = lambda:PressExpr('ln('))
            btnLog.config(text = 'log(b,a)',command = lambda:PressExpr('log('))
        else:
            for i in MBtn + DecOprBtn + FuncBtn[12:]:
                i.config(state = tkinter.DISABLED)
            btnSqr.config(text = 'and',command = lambda:PressExpr('&'))
            btnCub.config(text = 'or',command = lambda:PressExpr('|'))
            btnSqrt.config(text = 'neg',command = lambda:PressExpr('~'))
            btnRev.config(text = 'xor',command = lambda:PressExpr('⊕'))
            btnPow10.config(text = '<<1',command = lambda:PressExpr('<<1'))
            btnLog10.config(text = '>>1',command = lambda:PressExpr('>>1'))
            btnExp.config(text = '<<',command = lambda:PressExpr('<<'))
            btnLn.config(text = '>>',command = lambda:PressExpr('>>'))
            btnLog.config(text = 'comp',command = lambda:PressExpr('comp('))
        if curRadix == 'Bin':
            for i in NumBtn[:2]:
                i.config(state = tkinter.NORMAL)
            for i in NumBtn[2:]:
                i.config(state = tkinter.DISABLED)
        elif curRadix == 'Oct':
            for i in NumBtn[:8]:
                i.config(state = tkinter.NORMAL)
            for i in NumBtn[8:]:
                i.config(state = tkinter.DISABLED)
        elif curRadix == 'Dec':
            for i in NumBtn:
                i.config(state = tkinter.NORMAL)
        else:
            for i in NumBtn[:16]:
                i.config(state = tkinter.NORMAL)
            for i in NumBtn[16:]:
                i.config(state = tkinter.DISABLED)

    #去除数字前缀中多余的0，并且给非十进制数加上对应的前缀，保证eval()计算正确
    def RadixFixExpr(Expr):
        nonlocal A,B,C,D,E,F,M,x,y,UniSym,FuncSym,SingleSym,OperaSym,NumBtn,MBtn,DecOprBtn,FuncBtn,priorAns,isShift,curRadix
        res = ''
        if curRadix == 'Bin':
            listNum = findall(r"[0|1]+",Expr)
            prefix = '0b'
        elif curRadix == 'Oct':
            listNum = findall(r"[0-7]+",Expr)
            prefix = '0o'
        elif curRadix == 'Hex':
            listNum = findall(r"[0-9A-F]+",Expr)
            prefix = '0x'
        else:
            listNum = findall(r"\d+\.?\d*",Expr)
            prefix = ''
        for i in listNum:
            n = Expr.find(i)
            l = len(i)
            if i != '0':
                i = i.lstrip('0')
            res = res + Expr[0:n] + prefix + i
            Expr = Expr[n+l:]
        res = res + Expr
        return res


    '''*****************************************************************输入响应部分*****************************************************************'''


    #表达式输入
    def PressExpr(Sym):
        nonlocal A,B,C,D,E,F,x,y,M,UniSym,FuncSym,SingleSym,OperaSym,NumBtn,MBtn,DecOprBtn,FuncBtn,priorAns,isShift,curRadix,ans
        if priorAns == True and (Sym in NumSym or Sym in FuncSym):
            result.set('')
        elif priorAns == True and Sym in ['+','-','×','*','/','%','^','mod']:
            result.set('ans')
        priorAns = False
        curExpr = result.get()
        if curExpr != '' and (curExpr[-1] in ['×','*','/','^'] or curExpr[-3:] == 'mod') and Sym =='-':
            newExpr = curExpr + Sym
            if len(newExpr) > 40:
                result.set(curExpr)
            else:
                result.set(newExpr)
        elif curExpr != '' and curExpr[-1] in SingleSym and Sym in SingleSym:
            newExpr = curExpr[:-1] + Sym
            result.set(newExpr)
        elif len(curExpr) >= 3 and curExpr[-3:] in SingleSym and Sym in SingleSym:
            newExpr = curExpr[:-3] + Sym
            result.set(newExpr)
        else:
            newExpr = curExpr + Sym
            result.set(newExpr)

    #控制按键输入
    def PressCtrl(Sym):
        nonlocal A,B,C,D,E,F,x,y,M,UniSym,FuncSym,SingleSym,OperaSym,NumBtn,MBtn,DecOprBtn,FuncBtn,priorAns,isShift,curRadix,ans
        priorAns = False
        curExpr = result.get() 
        if Sym == 'AC':
            A = B = C = D = E = F = M = x = y = ans = 0
            result.set('')
            result2.set('')
            result3.set('')
        elif Sym == 'CE':
            result.set('')
        elif Sym == 'backspace':
            for i in range(-10,-1):
                if curExpr[i:] in UniSym:
                    result.set(curExpr[0:i])
                    return
            result.set(curExpr[0:-1])
        elif Sym == '↑':
            isShift = not isShift
            if isShift == True:
                btnShift.config(fg = 'orange')
                btnSin.config(text = 'sinh',command = lambda:PressExpr('sinh('),fg = 'orange')
                btnCos.config(text = 'cosh',command = lambda:PressExpr('cosh('),fg = 'orange')
                btnTan.config(text = 'tanh',command = lambda:PressExpr('tanh('),fg = 'orange')
                btnAsin.config(text = 'arcsinh',command = lambda:PressExpr('arcsinh('),fg = 'orange')
                btnAcos.config(text = 'arccosh',command = lambda:PressExpr('arccosh('),fg = 'orange')
                btnAtan.config(text = 'arctanh',command = lambda:PressExpr('arctanh('),fg = 'orange')
                btnDms.config(text = 'dms→',command = lambda:PressExpr('DmsTo('),fg = 'orange')
                if Angle.get() == 1:
                    btnRad.config(text = 'grad',command = lambda:PressExpr('grad('),fg = 'orange')
                elif Angle.get() == 2:
                    btnRad.config(text = 'grad',command = lambda:PressExpr('grad('),fg = 'orange')
                else:
                    btnRad.config(text = 'rad',command = lambda:PressExpr('rad('),fg = 'orange')
            else:
                btnShift.config(fg = '#4F4F4F')
                btnSin.config(text = 'sin',command = lambda:PressExpr('sin('),fg = '#4F4F4F')
                btnCos.config(text = 'cos',command = lambda:PressExpr('cos('),fg = '#4F4F4F')
                btnTan.config(text = 'tan',command = lambda:PressExpr('tan('),fg = '#4F4F4F')
                btnAsin.config(text = 'arcsin',command = lambda:PressExpr('arcsin('),fg = '#4F4F4F')
                btnAcos.config(text = 'arccos',command = lambda:PressExpr('arccos('),fg = '#4F4F4F')
                btnAtan.config(text = 'arctan',command = lambda:PressExpr('arctan('),fg = '#4F4F4F')
                btnDms.config(text = '→dms',command = lambda:PressExpr('ToDms('),fg = '#4F4F4F')
                if Angle.get() == 1:
                    btnRad.config(text = 'rad',command = lambda:PressExpr('rad('),fg = '#4F4F4F')
                elif Angle.get() == 2:
                    btnRad.config(text = 'deg',command = lambda:PressExpr('deg('),fg = '#4F4F4F')
                else:
                    btnRad.config(text = 'deg',command = lambda:PressExpr('deg('),fg = '#4F4F4F')
        elif Sym == 'sto':
            btnSto.config(command = lambda:PressSto('sto'),fg = 'orange')
            btnA.config(command = lambda:PressSto('A'),fg = 'orange')
            btnB.config(command = lambda:PressSto('B'),fg = 'orange')
            btnC.config(command = lambda:PressSto('C'),fg = 'orange')
            btnD.config(command = lambda:PressSto('D'),fg = 'orange')
            btnE.config(command = lambda:PressSto('E'),fg = 'orange')
            btnF.config(command = lambda:PressSto('F'),fg = 'orange')
            btnX.config(command = lambda:PressSto('x'),fg = 'orange')
            btnY.config(command = lambda:PressSto('y'),fg = 'orange')
        elif Sym == 'F-E':
            if PressEqual() != 0:
                PressCtrl('CE')
                return
            baseNum = ('{0:.12e}'.format(ans)).lower().replace('+','').replace('e','×10^')
            if baseNum[0] == '-':
                sign = '-'
                baseNum = baseNum[1:]
            else:
                sign = ''
            expNum = baseNum[14:]
            baseNum = baseNum[:14].rstrip('0')
            if baseNum[-1] == '.':
                baseNum = baseNum + '0'
            else:
                pass
            baseNum = baseNum + expNum[:4]
            expNum = expNum[4:]
            if expNum[0] == '-':
                baseNum = baseNum + '-'
                expNum = expNum[1:]
            else:
                pass
            expNum = expNum.lstrip('0')
            if expNum == '':
                expNum = '0'
            else:
                pass
            result.set(sign + baseNum + expNum)
            result2.set(curExpr)
        else:
            pass

    #累加存储器M的有关操作
    def PressMem(Sym):
        nonlocal A,B,C,D,E,F,x,y,M,UniSym,FuncSym,SingleSym,OperaSym,NumBtn,MBtn,DecOprBtn,FuncBtn,priorAns,isShift,curRadix,ans
        priorAns = False
        if Sym == 'MC':
            M = 0
            result3.set('')
        elif Sym == 'MS':
            if PressEqual() != 0:
                PressCtrl('CE')
                return
            result2.set(result2.get() + '→M')
            M = ans
            if M != 0:
                result3.set('M')
            else:
                result3.set('')
        elif Sym == 'M+':
            if PressEqual() != 0:
                PressCtrl('CE')
                return
            result2.set('ans M+')
            ans += M
            result.set(ans)
        elif Sym == 'M-':
            if PressEqual() != 0:
                PressCtrl('CE')
                return
            result2.set('ans M-')
            ans -= M
            result.set(ans)
        else:
            pass

    #按‘↑’后产生的寄存器A-F、x与y的存储操作
    def PressSto(Sym):
        nonlocal A,B,C,D,E,F,x,y,M,UniSym,FuncSym,SingleSym,OperaSym,NumBtn,MBtn,DecOprBtn,FuncBtn,priorAns,isShift,curRadix,ans
        btnSto.config(command = lambda:PressCtrl('sto'),fg = '#4F4F4F')
        btnA.config(command = lambda:PressExpr('A'),fg = '#4F4F4F')
        btnB.config(command = lambda:PressExpr('B'),fg = '#4F4F4F')
        btnC.config(command = lambda:PressExpr('C'),fg = '#4F4F4F')
        btnD.config(command = lambda:PressExpr('D'),fg = '#4F4F4F')
        btnE.config(command = lambda:PressExpr('E'),fg = '#4F4F4F')
        btnF.config(command = lambda:PressExpr('F'),fg = '#4F4F4F')
        btnX.config(command = lambda:PressExpr('x'),fg = '#4F4F4F')
        btnY.config(command = lambda:PressExpr('y'),fg = '#4F4F4F')
        if Sym == 'sto':
            return
        else:
            pass
        if PressEqual() != 0:
            PressCtrl('CE')
            return
        if Sym == 'A':
            A = ans
            result2.set(result2.get() + '→A')
        elif Sym == 'B':
            B = ans
            result2.set(result2.get() + '→B')
        elif Sym == 'C':
            C = ans
            result2.set(result2.get() + '→C')
        elif Sym == 'D':
            D = ans
            result2.set(result2.get() + '→D')
        elif Sym == 'E':
            E = ans
            result2.set(result2.get() + '→E')
        elif Sym == 'F':
            F = ans
            result2.set(result2.get() + '→F')
        elif Sym == 'x':
            x = ans
            result2.set(result2.get() + '→x')
        elif Sym =='y':
            y = ans
            result2.set(result2.get() + '→y')
        else:
            pass

    #计算表达式的值
    def PressEqual():
        nonlocal A,B,C,D,E,F,x,y,M,UniSym,FuncSym,SingleSym,OperaSym,NumBtn,MBtn,DecOprBtn,FuncBtn,priorAns,isShift,curRadix,ans
        try:
            DispStr = result.get()
            CompStr = DispStr
            CompStr = CompStr.replace('^','**')
            CompStr = CompStr.replace('%','*0.01')
            CompStr = CompStr.replace('mod','%')
            CompStr = CompStr.replace('π','pi')
            CompStr = CompStr.replace('×','*')
            CompStr = CompStr.replace('⊕','^')
            if not(CompStr.find('0**0')):
                raise ValueError

            FixedExpr = RadixFixExpr(CompStr)

            if curRadix != 'Dec':
                ans = int(modf(eval(FixedExpr))[1])
            elif abs(eval(FixedExpr) - int(eval(FixedExpr))) <= 1e-17:
                ans = int(eval(FixedExpr))
            else:
                ans = float('%.13f'% eval(FixedExpr))

            if curRadix == 'Bin':
                if len('{0:b}'.format(ans)) > 64:
                    raise OverflowError
                result.set('{0:b}'.format(ans))
            elif curRadix == 'Oct':
                if len('{0:o}'.format(ans)) > 32:
                    raise OverflowError
                result.set('{0:o}'.format(ans))
            elif curRadix == 'Hex':
                if len('{0:x}'.format(ans)) > 32:
                    raise OverflowError
                result.set('{0:x}'.format(ans).upper())
            elif abs(ans) >= 1e17:
                baseNum = ('{0:.12e}'.format(ans)).lower().replace('+','').replace('e','×10^')
                if baseNum[0] == '-':
                    sign = '-'
                    baseNum = baseNum[1:]
                else:
                    sign = ''
                expNum = baseNum[14:]
                baseNum = baseNum[:14].rstrip('0')
                if baseNum[-1] == '.':
                    baseNum = baseNum + '0'
                else:
                    pass
                result.set(sign + baseNum + expNum)
            elif type(ans) == int:
                result.set(ans)
            else:
                result.set('{0:.12f}'.format(ans).rstrip('0').rstrip('.'))
            result2.set(DispStr)
            priorAns = True
            return 0
        except ZeroDivisionError:
            tkinter.messagebox.showerror('除零错误',message = '除法计算时！除数不能为0！')
            return -1
        '''except ValueError:
            tkinter.messagebox.showerror('非法运算',message = '结果异常！请检查计算是否合法！')
            return -1
        except OverflowError:
            tkinter.messagebox.showerror('上界溢出',message = '结果超过了程序最大可表示范围！')
            return -1
        except:
            tkinter.messagebox.showerror('语法错误',message = '表达式有误！')
            return -1'''
    root.mainloop()

'''*****************************************************************窗体设计部分*****************************************************************'''

def LinearAlgebra():
    global root
    try:
        root.destroy()
    except:
        pass

    def about():
        tkinter.messagebox.showinfo('关于',message = '组长：阮超逸\n组员：周高超、肖文宗')
    root = Tk()  #创建一个窗口

    Menubar = tkinter.Menu(root)

    PlotList = tkinter.Menu(Menubar,tearoff = 0)
    PlotList.add_command(label = '2D绘图',command = lambda:Plot2D())
    PlotList.add_command(label = '3D绘图',command = lambda:Plot3D())

    Preference = tkinter.Menu(Menubar,tearoff = 0)
    Preference.add_command(label = '普通计算',command = lambda:main())
    Preference.add_command(label = '统计数学',command = lambda:Statistics())
    Preference.add_command(label = '微积分',command = lambda:Calculus())
    Preference.add_command(label = '线性代数',command = lambda:LinearAlgebra())
    Preference.add_cascade(label = '绘图',menu = PlotList)

    Preference.add_separator()
    Preference.add_command(label = '退出',command = lambda:root.destroy())

    Help = tkinter.Menu(Menubar,tearoff = 0)
    Help.add_command(label = '关于...',command = lambda:about())

    Menubar.add_cascade(label = '选项',menu = Preference)
    Menubar.add_cascade(label = '帮助',menu = Help)
    root['menu'] = Menubar
    
    root.title("Linear Algebra") #窗口的名字
    root.geometry("800x520") #窗口的大小
    root.resizable(False,False)
    root.iconbitmap('.\Calculator.ico')

    #窗口内容 TODO

    row = 2
    ide = {}
    list1 = [] 
    list2 = []

    def handle(str1):
        nonlocal row
        nonlocal ide
        nonlocal list1, list2
        str_list = str1.split('>')
        str1 = ''.join(str_list)
        str_list = str1.split(' ')  #取出' ' 和 '\n'
        str1 = ''.join(str_list)
        str_list = str1.split('\n')
        str1 = ''.join(str_list)
        if str1 == "clear":   #用户输入clear
            row = 2
            t.delete(1.0,'end')
            t.insert(1.0,"input there:")
            t.insert(1.61,"\n>>>")
        elif str1 == "clear_all":  #用户输入clear_all
            row = 2
            t.delete(1.0,'end')
            t.insert(1.0,"input there:")
            ide = {}
            list1 = []
            list2 = []
            var1.set(list1)
            var2.set(list2)
            t.insert(1.61,"\n>>>")
        elif '=' in str1:   #用户输入一个等式
            str_list = str1.split('=')
            print(str_list)
            try:
                word_list = findall("[a-zA-Z]+",str_list[1])  #找到所有标识符并替换
                for x in word_list:
                    if x in ide.keys():
                        index_list = [m.start() for m in finditer(x, str_list[1])]
                        for index in index_list:
                            if str_list[1][index+len(x)].isalpha():
                                pass
                            else:
                                str_list[1] = str_list[1][0:index] + ide[x][0] + str_list[1][index+len(x):]
                        #str_list[1] = str_list[1].replace(x,ide[x][0])
                list_value = []
                print(str_list[1])
                list_value.append(str_list[1])
                list_value.append(eval(str_list[1]))
                ide[str_list[0]] = list_value #如 {'a':['2',2]}
                temp = round(row-1+0.001+0.61,2)
                t.insert(temp,"\n>>>")
            except:
                mbox.showwarning(title="wrong",message="something wrong")
            for item in ide.keys():  #更新“变量 值”列表
                list1.append(item)
            for item in ide.values():
                list2.append(item[1])    
            var1.set(list1)
            var2.set(list2)
        else:   #用户输入了一个单独的标识符 或者一个匿名表达式，打印其值
            try:
                word_list = findall("[a-zA-Z]+",str1)  #找到所有标识符并替换
                for x in word_list:
                    if x in ide.keys():
                        str1 = str1.replace(x,ide[x][0])
                temp = round(row-1+0.001+0.61,2)
                t.insert(temp,"\n"+str(eval(str1)))
                if isinstance(eval(str1),(int,float)):
                    row = row + 1
                    t.insert(temp+1,"\n>>>")
                else:
                    list_size = []
                    list_size = eval(str1).shape
                    if len(list_size) == 1:
                        t.insert(temp+1,"\n>>>")
                        row = row + 1
                    else:
                        t.insert(temp+list_size[0],"\n>>>")
                        row = row + list_size[0]
            except:
                mbox.showwarning(title="wrong",message="unknown identifier")

    def callBack(event):
        if event.char == '\r':
            nonlocal row
            temp = round(row+0.001,1)
            #print(temp)
            strS1 = t.get(temp,'end')
            print(strS1)
            row = row + 1
            handle(strS1)
    
    #两个frame，用来输入和显示当前变量值，就像matlab一样
    f1 = Frame(root,height=520,width=600)
    f1.place(x=0,y=0,anchor="nw")

    f2 = Frame(root,height=520,width=200,bg="gray")
    f2.place(x=600,y=0,anchor="nw")

    #用于输入文本的text
    t = Text(f1,height=40,width=85)
    t.insert(1.0,"\n"*40)
    t.mark_set('here',1.0)
    t.insert('here',"input there:")
    t.insert(2.0,">>>")
    t.bind("<Key>",callBack)   #敲空格就开始处理
    t.place(x=0,y=0,anchor="nw")

    #显示两个label在f2上，分别是变量和值
    l1 = Label(f2,text="变量",bg="blue",width=6,height=1)
    l1.place(x=10,y=0,anchor="nw")
    l2 = Label(f2,text="值",bg="blue",width=6,height=1)
    l2.place(x=100,y=0,anchor="nw")

    #用两个listbox显示当前已经接受的变量和值
    var1 = StringVar()
    lb1 = Listbox(f2,listvariable=var1,bg="gray",width=6,height=40)
    lb1.place(x = 10,y = 20,anchor="nw")
    var2 = StringVar()
    lb2 = Listbox(f2,listvariable=var2,bg="gray",width=13,height=40)
    lb2.place(x = 100,y = 20,anchor="nw")

    #创建一个弹窗，当输入有错误时提醒用户

    root.mainloop()  #让窗口活动起来


'''*****************************************************************窗体设计部分*****************************************************************'''


def Plot2D():
    e=exp(1)
    PARSER = 'eval'  # eval or text
    initial_formula = "sin(x)"
    initial_x_range ="-10,10"
    fig, ax, plot = None, None, None
    f, x_max, x_min, WIRE,widgets=None, None, None, None, None
    def about():
        tkinter.messagebox.showinfo('关于',message = '组长：阮超逸\n组员：周高超、肖文宗')
    def get_graph_data(f, x_min, x_max):
        x_step = (x_max-x_min)/200.0
        X = np.arange(x_min, x_max + x_step, x_step)
        ylist = []
        for x in X:
            y = f(x=x)
            if y is None:
                print("y is None")
                exit(-1)
            ylist.append(y)
        Y = np.array(ylist)
        return X, Y

    def submit(text):
        nonlocal f, ax, plot, x_max, x_min,  initial_formula, WIRE
        initial_formula = text
        f = partial(text_based_function, s=text)
        print("new formula: %s" % text)
        X, Y = get_graph_data(f, x_min=x_min, x_max=x_max)
        ax.clear()
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        plot = ax.plot(X, Y)
        plt.draw()

    def set_x_range(x_range_text):
        nonlocal x_max, x_min
        b, a = x_range_text.split(",")
        x_min = float(b)
        x_max = float(a)

    def x_change(x_range_text):
        nonlocal f,ax,plot,x_max, x_min,initial_formula
        b, a = x_range_text.split(",")
        x_min = float(b)
        x_max = float(a)
        f = partial(text_based_function, s=initial_formula)
        X, Y = get_graph_data(f, x_min=x_min, x_max=x_max)
        ax.clear()
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        plot = ax.plot(X, Y)
        plt.draw()

    def draw_init(X, Y):
        nonlocal fig, ax, plot, widgets
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        axbox = plt.axes([0.1, 0, 0.2, 0.05])
        text_box = TextBox(axbox, 'Evaluate', initial=initial_formula)
        text_box.on_submit(submit)
        xbox = plt.axes([0.7, 0, 0.2, 0.05])
        x_text_box = TextBox(xbox, 'X_range', initial=initial_x_range)
        x_text_box.on_submit(x_change)
        plot = ax.plot(X, Y)
        plt.show()

    def text_based_function(s, x):
        if s.find("^"):
            s = s.replace("^","**")
        if PARSER == 'eval':
            try:
                return eval(s)
            except ZeroDivisionError:
                print("division by zero")
                return None
            except:
                return None
        else:
            print("Invalid PARSER")
            return None

    global root
    try:
        root.destroy()
    except:
        pass
    root = tkinter.Tk()

    Menubar = tkinter.Menu(root)

    PlotList = tkinter.Menu(Menubar,tearoff = 0)
    PlotList.add_command(label = '2D绘图',command = lambda:Plot2D())
    PlotList.add_command(label = '3D绘图',command = lambda:Plot3D())

    Preference = tkinter.Menu(Menubar,tearoff = 0)
    Preference.add_command(label = '普通计算',command = lambda:main())
    Preference.add_command(label = '统计数学',command = lambda:Statistics())
    Preference.add_command(label = '微积分',command = lambda:Calculus())
    Preference.add_command(label = '线性代数',command = lambda:LinearAlgebra())
    Preference.add_cascade(label = '绘图',menu = PlotList)

    Preference.add_separator()
    Preference.add_command(label = '退出',command = lambda:root.destroy())


    Help = tkinter.Menu(Menubar,tearoff = 0)
    Help.add_command(label = '关于...',command = lambda:about())

    Menubar.add_cascade(label = '选项',menu = Preference)
    Menubar.add_cascade(label = '帮助',menu = Help)
    root['menu'] = Menubar

    root.title('Plot 2D')
    root.geometry('800x520')
    root.resizable(False,False)
    root.iconbitmap('.\Calculator.ico')
    a = tkinter.Entry(root)
    a.place(y = 400,width = 810, height = 100)
    t = tkinter.Entry(root)
    t.place(x=10,y=360,height=30,width=100)
    w = tkinter.Label(root, text="x domain")
    w.place(x=10,y=330,height=30,width=100)

    def draw():
        nonlocal initial_formula ,initial_x_range,x_min,x_max,f,widgets
        initial_formula = a.get()
        initial_x_range = t.get()
        x_min = -100
        x_max = 100
        widgets = []
        set_x_range(initial_x_range)
        f = partial(text_based_function, s=initial_formula)
        draw_init(*get_graph_data(f, x_min=x_min, x_max=x_max))

    b1 = tkinter.Button(root,font = ('微软雅黑',12),fg = 'orange',bd = 0.5,text='draw', width=10,
                  height=2, command=draw)
    b1.place(x = 360,y = 300,height = 50)
    root.mainloop()


'''*****************************************************************窗体设计部分*****************************************************************'''

def Plot3D():

    e=exp(1)

    WIRE = True
    HIDE = False
    PARSER = 'eval'  # eval or text
    initial_formula = "x^2+y^2"

    initial_x_range = "-500,500"
    initial_y_range = "-500,500"

    fig, ax, plot = None, None, None
    f,x_max, x_min,y_min,y_max,widgets = None, None, None,None, None, None
    def about():
        tkinter.messagebox.showinfo('关于',message = '组长：阮超逸\n组员：周高超、肖文宗')
    def get_graph_data(f, x_min, x_max, y_min, y_max):
        x_step = (x_max-x_min)/200.0
        y_step = (y_max-y_min)/200.0
        X = np.arange(x_min, x_max + x_step, x_step)
        Y = np.arange(y_min, y_max + y_step, y_step)
        zlist = []
        xy_note = []
        X2 = []
        Y2 = []
        Z2 = []

        for y in Y:
            for x in X:
                try:
                    z = f(x=x, y=y)
                    if z is None:
                        z = 100.0

                except Exception as e:
                    print("exception: "+str(e))
                    xy_note.append((x, y))
                    z = 100.0

                zlist.append(z)
        Z = np.array(zlist)
        Z = Z.reshape(len(X), len(Y))
        X, Y = np.meshgrid(X, Y)
        return X, Y, Z


    def submit(text):
        nonlocal f, ax, plot, x_max, x_min, y_max, y_min, initial_formula, WIRE
        initial_formula = text
        f = partial(text_based_function, s=text)
        print("new formula: %s" % text)
        X, Y, Z = get_graph_data(f, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)
        ax.clear()
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')

        print("X,Y,Z")
        print(X[0])
        print(Y[0])
        print(Z[0])


        if WIRE:
            plot = ax.plot_wireframe(X, Y, Z, rcount=len(Y[0]) / 4, ccount=len(X[0]) / 4)
        else:
            plot = ax.plot_surface(X, Y, Z, rcount=len(Y[0])/4, ccount=len(X[0])/4, cmap='plasma', edgecolor='none')

        plt.draw()


    def toggle_wire(event):
        nonlocal WIRE, initial_formula
        WIRE = not WIRE
        submit(initial_formula)


    def set_x_range(x_range_text):
        nonlocal x_max, x_min
        b, a = x_range_text.split(",")
        x_min = float(b)
        x_max = float(a)


    def set_y_range(y_range_text):
        nonlocal y_max, y_min
        b, a = y_range_text.split(",")
        y_min = float(b)
        y_max = float(a)


    def x_change(x_range_text):
        nonlocal f,ax,plot,x_max, x_min,initial_formula,y_min,y_max
        b, a = x_range_text.split(",")
        x_min = float(b)
        x_max = float(a)
        f = partial(text_based_function, s=initial_formula)
        X, Y, Z  = get_graph_data(f, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)
        ax.clear()
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')

        print("X,Y,Z")
        print(X[0])
        print(Y[0])
        print(Z[0])


        if WIRE:
            plot = ax.plot_wireframe(X, Y, Z, rcount=len(Y[0]) / 4, ccount=len(X[0]) / 4)
        else:
            plot = ax.plot_surface(X, Y, Z, rcount=len(Y[0])/4, ccount=len(X[0])/4, cmap='plasma', edgecolor='none')

        plt.draw()

    def y_change(x_range_text):
        nonlocal f,ax,plot,x_max, x_min,initial_formula,y_min,y_max
        b, a = x_range_text.split(",")
        y_min = float(b)
        y_max = float(a)
        f = partial(text_based_function, s=initial_formula)
        X, Y, Z  = get_graph_data(f, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)
        ax.clear()
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')

        print("X,Y,Z")
        print(X[0])
        print(Y[0])
        print(Z[0])


        if WIRE:
            plot = ax.plot_wireframe(X, Y, Z, rcount=len(Y[0]) / 4, ccount=len(X[0]) / 4)
        else:
            plot = ax.plot_surface(X, Y, Z, rcount=len(Y[0])/4, ccount=len(X[0])/4, cmap='plasma', edgecolor='none')

        plt.draw()

    def press(event):
        nonlocal HIDE
        if event.key == 'h':
            print("h is clicked")
            for w in widgets:
                w.set_visible(HIDE)
            HIDE = not HIDE


    def draw_init(X, Y, Z):
        nonlocal fig, ax, plot, widgets
        # Plot a basic wireframe.
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        axbox = plt.axes([0.1, 0.06, 0.2, 0.05])
        text_box = TextBox(axbox, 'Evaluate', initial=initial_formula)
        text_box.on_submit(submit)

        xbox = plt.axes([0.1, 0, 0.2, 0.05])
        x_text_box = TextBox(xbox, 'X_range', initial=initial_x_range)
        x_text_box.on_submit(x_change)

        ybox = plt.axes([0.7, 0, 0.2, 0.05])
        y_text_box = TextBox(ybox, 'Y_range', initial=initial_y_range)
        y_text_box.on_submit(y_change)

        bbox = plt.axes([0, 0.9, 0.2, 0.1])
        b = Button(bbox, 'heatmap')
        b.on_clicked(toggle_wire)

        widgets = [axbox, xbox, ybox, bbox]

        fig.canvas.mpl_connect('key_press_event', press)

        if WIRE:
            plot = ax.plot_wireframe(X, Y, Z, rcount=len(Y[0]) / 4, ccount=len(X[0]) / 4)
        else:
            plot = ax.plot_surface(X, Y, Z, rcount=len(Y[0])/4, ccount=len(X[0])/4, cmap='plasma', edgecolor='none')

        plt.show()



    def text_based_function(s, x, y):
        if s.find("^"):
            s = s.replace("^","**")
        if PARSER == 'eval':
            try:
                return eval(s)
            except ZeroDivisionError:
                print("division by zero")
                return None
            except:
                return None
        else:
            print("Invalid PARSER")
            return None


    global root
    try:
        root.destroy()
    except:
        pass
    root = tkinter.Tk()
    Menubar = tkinter.Menu(root)

    PlotList = tkinter.Menu(Menubar,tearoff = 0)
    PlotList.add_command(label = '2D绘图',command = lambda:Plot2D())
    PlotList.add_command(label = '3D绘图',command = lambda:Plot3D())

    Preference = tkinter.Menu(Menubar,tearoff = 0)
    Preference.add_command(label = '普通计算',command = lambda:main())
    Preference.add_command(label = '统计数学',command = lambda:Statistics())
    Preference.add_command(label = '微积分',command = lambda:Calculus())
    Preference.add_command(label = '线性代数',command = lambda:LinearAlgebra())
    Preference.add_cascade(label = '绘图',menu = PlotList)

    Preference.add_separator()
    Preference.add_command(label = '退出',command = lambda:root.destroy())

    Help = tkinter.Menu(Menubar,tearoff = 0)
    Help.add_command(label = '关于...',command = lambda:about())

    Menubar.add_cascade(label = '选项',menu = Preference)
    Menubar.add_cascade(label = '帮助',menu = Help)
    root['menu'] = Menubar
    
    root.title('Plot 3D')
    root.geometry('800x520')
    root.resizable(False,False)
    root.iconbitmap('.\Calculator.ico')
    a = tkinter.Entry(root)
    a.place(y = 400,width = 810, height = 100)
    t = tkinter.Entry(root)
    t.place(x=10,y=360,height=30,width=100)
    w = tkinter.Label(root, text="x domain")
    w.place(x=10,y=330,height=30,width=100)

    y = tkinter.Entry(root)
    y.place(x=690,y=360,height=30,width=100)
    z = tkinter.Label(root, text="y domain")
    z.place(x=690,y=330,height=30,width=100)

    def draw():
        nonlocal initial_formula ,initial_x_range, initial_y_range,x_min,y_min,x_max,y_max,f,widgets
        initial_formula = a.get()
        initial_x_range = t.get()
        initial_y_range = y.get()
        x_min = -100
        y_min = -100
        x_max = 100
        y_max = 100
        widgets = []
        set_x_range(initial_x_range)
        set_y_range(initial_y_range)
        f = partial(text_based_function, s=initial_formula)
        draw_init(*get_graph_data(f, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max))


    b1 = tkinter.Button(root,font = ('微软雅黑',12),fg = 'orange',bd = 0.5,text='draw', width=10,
                  height=2, command=draw)
    b1.place(x = 360,y = 300,height = 50)
    root.mainloop()

'''*****************************************************************窗体设计部分*****************************************************************'''


def Statistics():
    global root
    try:
        root.destroy()
    except:
        pass
    root = tkinter.Tk()
    def about():
        tkinter.messagebox.showinfo('关于',message = '组长：阮超逸\n组员：周高超、肖文宗')

    #菜单栏部分
    Menubar = tkinter.Menu(root)

    PlotList = tkinter.Menu(Menubar,tearoff = 0)
    PlotList.add_command(label = '2D绘图',command = lambda:Plot2D())
    PlotList.add_command(label = '3D绘图',command = lambda:Plot3D())

    Preference = tkinter.Menu(Menubar,tearoff = 0)
    Preference.add_command(label = '普通计算',command = lambda:main())
    Preference.add_command(label = '统计数学',command = lambda:Statistics())
    Preference.add_command(label = '微积分',command = lambda:Calculus.main())
    Preference.add_command(label = '线性代数',command = lambda:LinearAlgebra())
    Preference.add_cascade(label = '绘图',menu = PlotList)

    Preference.add_separator()
    Preference.add_command(label = '退出',command = lambda:root.destroy())

    Help = tkinter.Menu(Menubar,tearoff = 0)
    Help.add_command(label = '关于...',command = lambda:about())

    Menubar.add_cascade(label = '选项',menu = Preference)
    Menubar.add_cascade(label = '帮助',menu = Help)
    root['menu'] = Menubar

    #窗体大小、名称与图标
    root.maxsize(320,480)
    root.minsize(320,480)
    root.title('Statistics')
    root.iconbitmap('.\Calculator.ico')
    root.resizable(False,False)

    table = ttk.Treeview(root)
    table["columns"] = ("x","y")
    table.column("#0" ,width = 50, minwidth = 50,stretch = False,anchor = 'e')
    table.column("x" ,width = 125, minwidth = 125,stretch = False,anchor = 'e')
    table.column("y" ,width = 125, minwidth = 125,stretch = False,anchor = 'e')
    table.heading("#0",text = "序号")
    table.heading("x",text = "X")  
    table.heading("y",text = "Y")  

    vbar = ttk.Scrollbar(root,orient = tkinter.VERTICAL,command = table.yview)
    table.configure(yscrollcommand = vbar.set)
    table.place(width = 320,height = 150)
    vbar.place(x = 301,y = 1,width = 19,height = 148)

    labelIndex = tkinter.Label(root,anchor = 'se',text = '行号：')
    labelXi = tkinter.Label(root,anchor = 'se',text = 'X = ')
    labelYi = tkinter.Label(root,anchor = 'se',text = 'Y = ')

    index = tkinter.StringVar()
    xi = tkinter.StringVar()
    yi = tkinter.StringVar()
    index.set('1')
    xi.set('')
    yi.set('')

    def test1(x):
        return (x)

    def test2(x):
        return testNum(x)

    testI = root.register(test1)
    testV = root.register(test2)

    entryIndex = tkinter.Entry(root,textvariable = index,validate = 'key', validatecommand=(testI,'%P'))
    entryXi = tkinter.Entry(root,textvariable = xi,validate = 'key', validatecommand=(testV,'%P'))
    entryYi = tkinter.Entry(root,textvariable = yi,validate = 'key', validatecommand=(testV,'%P'))

    labelIndex.place(x = 10, y = 165, width = 50)
    entryIndex.place(x = 60, y = 165, width = 40)
    labelXi.place(x = 110, y = 165, width = 50)
    entryXi.place(x = 160, y = 165, width = 40)
    labelYi.place(x = 210, y = 165, width = 50)
    entryYi.place(x = 260, y = 165, width = 40)

    btnIns = tkinter.Button(root,text = '插入',font = ('微软雅黑',10),fg = ('#4F4F4F'),bd = 0.5,command = lambda:TreeModify('ins'))
    btnIns.place(x = 40,y = 200,width = 40,height = 30)
    btnEdit = tkinter.Button(root,text = '编辑',font = ('微软雅黑',10),fg = ('#4F4F4F'),bd = 0.5,command = lambda:TreeModify('edt'))
    btnEdit.place(x = 110,y = 200,width = 40,height = 30)
    btnDel = tkinter.Button(root,text = '删除',font = ('微软雅黑',10),fg = ('#4F4F4F'),bd = 0.5,command = lambda:TreeModify('del'))
    btnDel.place(x = 180,y = 200,width = 40,height = 30)
    btnDes = tkinter.Button(root,text = '清空',font = ('微软雅黑',10),fg = ('#4F4F4F'),bd = 0.5,command = lambda:TreeModify('des'))
    btnDes.place(x = 250,y = 200,width = 40,height = 30)

    #当前表达式（计算结果）、上一次计算的表达式与‘M’累加器显示屏
    result = tkinter.StringVar()    #当前表达式（结果）
    result.set('')
    result2 = tkinter.StringVar()   #上一次计算的表达式
    result2.set('')

    #对应的显示屏
    label = tkinter.Label(root,font = ('微软雅黑',9),bg = '#EEE9E9',bd ='9',fg = '#828282',anchor = 'se',textvariable = result2)
    label.place(y = 250,width = 320,height = 30)
    label2 = tkinter.Label(root,font = ('微软雅黑',18),bg = '#EEE9E9',bd ='9',fg = 'black',anchor = 'se',textvariable = result)
    label2.place(y = 280,width = 320,height = 35)

    btnSX = tkinter.Button(root,text = 'Sum[X]',font = ('微软雅黑',7),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressFunc('SX'))
    btnSX.place(x = 15,y = 330,width = 40,height = 30)
    btnSX2 = tkinter.Button(root,text = 'S[X^2]',font = ('微软雅黑',7),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressFunc('SX2'))
    btnSX2.place(x = 65,y = 330,width = 40,height = 30)
    btnMEDX = tkinter.Button(root,text = 'Med[X]',font = ('微软雅黑',7),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressFunc('MEDX'))
    btnMEDX.place(x = 115,y = 330,width = 40,height = 30)
    btnEX = tkinter.Button(root,text = 'E[X]',font = ('微软雅黑',7),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressFunc('EX'))
    btnEX.place(x = 165,y = 330,width = 40,height = 30)
    btnDX = tkinter.Button(root,text = 'Var[X]',font = ('微软雅黑',7),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressFunc('DX'))
    btnDX.place(x = 215,y = 330,width = 40,height = 30)
    btnSTDX = tkinter.Button(root,text = 'Std[X]',font = ('微软雅黑',7),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressFunc('STDX'))
    btnSTDX.place(x = 265,y = 330,width = 40,height = 30)

    btnSY = tkinter.Button(root,text = 'Sum[Y]',font = ('微软雅黑',7),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressFunc('SY'))
    btnSY.place(x = 15,y = 370,width = 40,height = 30)
    btnSY2 = tkinter.Button(root,text = 'S[Y^2]',font = ('微软雅黑',7),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressFunc('SY2'))
    btnSY2.place(x = 65,y = 370,width = 40,height = 30)
    btnMEDY = tkinter.Button(root,text = 'Med[Y]',font = ('微软雅黑',7),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressFunc('MEDY'))
    btnMEDY.place(x = 115,y = 370,width = 40,height = 30)
    btnEY = tkinter.Button(root,text = 'E[Y]',font = ('微软雅黑',7),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressFunc('EY'))
    btnEY.place(x = 165,y = 370,width = 40,height = 30)
    btnDY = tkinter.Button(root,text = 'Var[Y]',font = ('微软雅黑',7),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressFunc('DY'))
    btnDY.place(x = 215,y = 370,width = 40,height = 30)
    btnSTDY = tkinter.Button(root,text = 'Std[Y]',font = ('微软雅黑',7),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressFunc('STDY'))
    btnSTDY.place(x = 265,y = 370,width = 40,height = 30)

    btnBoxX = tkinter.Button(root,text = 'Box[X]',font = ('微软雅黑',7),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressFunc('BoxX'))
    btnBoxX.place(x = 15,y = 410,width = 40,height = 30)
    btnBoxY = tkinter.Button(root,text = 'Box[Y]',font = ('微软雅黑',7),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressFunc('BoxY'))
    btnBoxY.place(x = 65,y = 410,width = 40,height = 30)
    btnHistX = tkinter.Button(root,text = 'Hist[X]',font = ('微软雅黑',7),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressFunc('HistX'))
    btnHistX.place(x = 115,y = 410,width = 40,height = 30)
    btnHistY = tkinter.Button(root,text = 'Hist[Y]',font = ('微软雅黑',7),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressFunc('HistY'))
    btnHistY.place(x = 165,y = 410,width = 40,height = 30)
    btnScatter = tkinter.Button(root,text = 'Scatter',font = ('微软雅黑',7),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressFunc('Scatter'))
    btnScatter.place(x = 215,y = 410,width = 40,height = 30)
    btnPFit = tkinter.Button(root,text = 'Ployfit',font = ('微软雅黑',7),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressFunc('PFit'))
    btnPFit.place(x = 265,y = 410,width = 40,height = 30)


    '''*****************************************************************功能实现部分*****************************************************************'''


    i = 0
    curX = 0
    curY = 0
    x = []
    y = []
    ans = 0

    def testIndex(content):
        if content == '':
            return True
        str = findall('[0-9]+',content)
        if str != [] and content == str[0] and int(str[0]) > 0 and int(str[0]) <= i + 1:
            return True
        return False

    def testNum(content):
        if content == '':
            return True
        str = findall('^[-+]?([0-9]+(\.[0-9]*)?|\.[0-9]+)$',content)
        if str != [] and content == str[0][0]:
            return True
        return False

    def onDBClick(event):
        try:
            item = table.selection()[0]
        except IndexError:
            pass
        
    table.bind("<Double-1>", onDBClick)

    def focusShift(event):
        if event.char == '\r':
            if root.focus_get() == entryIndex:
                entryXi.focus()
            elif root.focus_get() == entryXi:
                entryYi.focus()
            else:
                pass
        else:
            pass

    entryIndex.bind('<Key>',focusShift)
    entryXi.bind('<Key>',focusShift)
    entryYi.bind('<Key>',focusShift)

    def focusList(event):
        table.focus()

    btnIns.bind('<Button-1>',focusList)
    btnEdit.bind('<Button-1>',focusList)
    btnDel.bind('<Button-1>',focusList)

    def drawScatter(x, y):
        pyplot.scatter(x, y)
        pyplot.xlabel('x')
        pyplot.ylabel('y')
        pyplot.show()
        
    def drawHist(x):
        pyplot.hist(x, 100)
        pyplot.xlabel('x')
        pyplot.ylabel('Freq')
        pyplot.show()
        
    def drawBox(x):
        pyplot.boxplot([x], labels=['x'])
        pyplot.show()

    def TreeModify(Sym):
        nonlocal i
        nonlocal x
        nonlocal y
        nonlocal curX
        nonlocal curY
        try:
            if xi.get() == '':
                curX = 0
            else:
                curX = float(eval(xi.get()))
            if yi.get() == '':
                curY = 0
            else:
                curY = float(eval(yi.get()))
            tmp = int(index.get()) - 1
            if Sym == 'ins':
                if tmp < i and tmp >= 0:
                    x = x[:tmp]+[curX]+x[tmp+1:]
                    y = y[:tmp]+[curY]+y[tmp+1:]
                    i = len(x)
                    table.delete(table.get_children()[tmp])
                    table.insert('',tmp,text = str(tmp+1),values = (curX,curY))
                elif tmp == i:
                    x.append(curX)
                    y.append(curY)
                    i = len(x)
                    table.insert('',i,text = str(i),values = (curX,curY))
                else:
                    raise ValueError
            elif Sym == 'edt':
                if tmp < i + 1 and tmp >= 0:
                    x = x[:tmp]+[curX]+x[tmp+1:]
                    y = y[:tmp]+[curY]+y[tmp+1:]
                    i = len(x)
                    table.delete(table.get_children()[tmp])
                    table.insert('',tmp,text = str(tmp+1),values = (curX,curY))
                elif tmp == i + 1:
                    x.append(curX)
                    y.append(curY)
                    i = len(x)
                    table.insert('',i,text = str(i),values = (curX,curY))
                else:
                    raise ValueError
            elif Sym == 'del':
                x = x[:tmp]+x[tmp+1:]
                y = y[:tmp]+y[tmp+1:]
                i = len(x)
                for item in table.get_children():
                    table.delete(item)
                for iteration in range(len(x)):
                    table.insert('',iteration,text = str(iteration + 1),values = (x[iteration],y[iteration]))
            else:
                x = []
                y = []
                i = 0
                for item in table.get_children():
                    table.delete(item)
        except:
            i = len(x)
        index.set(str(i+1))
        xi.set('')
        yi.set('')


    def PressFunc(Sym):
        nonlocal i
        nonlocal x
        nonlocal y
        nonlocal curX
        nonlocal curY
        popup = tkinter.Toplevel()
        popup.withdraw()
        popup.iconbitmap('.\Calculator.ico')
        popup.geometry('200x150')
        popup.resizable(False,False)
        popup.title('Statistics')
        N = tkinter.StringVar()
        N.set('')
        n = 0
        labelN = tkinter.Label(popup,anchor = 'se',text = '回归最高次项次数n = ')
        labelN.place(x = 20,y = 40, width = 100)
        entryN = tkinter.Entry(popup,textvariable = N,validate = 'key', validatecommand=(testI,'%P'))
        entryN.place(x = 120,y = 40, width = 60)
        btnN = tkinter.Button(popup,text = '确定',font = ('微软雅黑',7),fg = ('#4F4F4F'),bd = 0.5,command = lambda:(getN(N.get())))
        btnN.place(x = 80,y = 80,width = 40,height = 30)
        def getN(s):
            nonlocal n
            n = int(s)
            z = numpy.polyfit(x, y, n)
            p = numpy.poly1d(z)
            res = 'y = ' + '{0:.4f}'.format(z[0]) +'x^' + str(len(z) - 1) 
            for k in range(1,len(z)-1):
                res = res + '+' + '{0:.4f}'.format(z[k]) +'x^' + str(len(z) - k - 1)
            res = res + '+' + '{0:.4f}'.format(z[-1])
            pt0 = range(floor(min(x)*100),ceil(max(x)*100))
            pt = [k / 100 for k in pt0]
            fig, ax = pyplot.subplots()
            ax.plot(pt, p(pt),'r-', label = res)
            ax.scatter(x, y)
            legend = ax.legend(loc='upper center', shadow=False, fontsize='medium')
            legend.get_frame().set_facecolor('#FFFFFF')
            pyplot.show()
        try:
            if Sym == 'SX':
                ans = 0
                if x == []:
                    result.set('NaN')
                else:
                    for k in x:
                        ans = ans + k
                    result.set(ans)
                result2.set('Sum[X]=')
            elif Sym == 'SX2':
                ans = 0
                if x == []:
                    result.set('NaN')
                else:
                    for k in x:
                        ans = ans + k * k
                    result.set(ans)
                result2.set('Sum[X^2]=')
            elif Sym == 'EX':
                ans = numpy.mean(x)
                if numpy.isnan(ans):
                    result.set('NaN')
                else:
                    result.set(ans)
                result2.set('E[X]=')
            elif Sym == 'DX':
                ans = numpy.var(x)
                if numpy.isnan(ans):
                    result.set('NaN')
                else:
                    result.set(ans)
                result2.set('Var[X]=')
            elif Sym == 'STDX':
                ans = numpy.std(x)
                if numpy.isnan(ans):
                    result.set('NaN')
                else:
                    result.set(ans)
                result2.set('StdError[X]=')
            elif Sym == 'MEDX':
                ans = numpy.median(x)
                if numpy.isnan(ans):
                    result.set('NaN')
                else:
                    result.set(ans)
                result2.set('Median[X]=')
            if Sym == 'SY':
                ans = 0
                if y == []:
                    result.set('NaN')
                else:
                    for k in y:
                        ans = ans + k
                    result.set(ans)
                result2.set('Sum[Y]=')
            elif Sym == 'SY2':
                ans = 0
                if y == []:
                    result.set('NaN')
                else:
                    for k in y:
                        ans = ans + k * k
                    result.set(ans)
                result2.set('Sum[Y^2]=')
            elif Sym == 'EY':
                ans = numpy.mean(y)
                if numpy.isnan(ans):
                    result.set('NaN')
                else:
                    result.set(ans)
                result2.set('E[Y]=')
            elif Sym == 'DY':
                ans = numpy.var(y)
                if numpy.isnan(ans):
                    result.set('NaN')
                else:
                    result.set(ans)
                result2.set('Var[Y]=')
            elif Sym == 'STDY':
                ans = numpy.std(y)
                if numpy.isnan(ans):
                    result.set('NaN')
                else:
                    result.set(ans)
                result2.set('StdError[Y]=')
            elif Sym == 'MEDY':
                ans = numpy.median(y)
                if numpy.isnan(ans):
                    result.set('NaN')
                else:
                    result.set(ans)
                result2.set('Median[Y]=')
            elif Sym == 'Scatter':
                drawScatter(x,y)
            elif Sym == 'BoxX':
                drawBox(x)
            elif Sym == 'BoxY':
                drawBox(y)
            elif Sym == 'HistX':
                drawHist(x)
            elif Sym == 'HistY': 
                drawHist(y)
            elif Sym == 'PFit':
                popup.deiconify()
            else:
                pass
            return
        except Warning:
            pass
    root.mainloop()

def Calculus():
    global root
    def about():
        tkinter.messagebox.showinfo('关于',message = '组长：阮超逸\n组员：周高超、肖文宗')


    #整体符号表：每一项都是一个整体，按BS删除时一起删除
    FuncSym = ['log10(', 'e^','ln(','log(','abs(', 'limit(','diff(','∫(','simplify(','series(',
               'sin(','cos(','tan(','arcsin(','arccos(','arctan(','1j','solve(',
               'sinh(','cosh(','tanh(','arcsinh(','arccosh(','arctanh(']

    #单字符符号表,规定mod为单字符符号
    SingleSym = ['.',',','+','-','×','*','/','^']

    #二元运算符号表
    OperaSym = SingleSym[2:]

    #数值符号表：每一项都能转化为一个数。注意e在十进制中与十六进制中不同的含义
    NumSym = ['0','1','2','3','4','5','6','7','8','9','x','y','z',
              'pi','e']

 
    x = sympy.Symbol('x')
    y = sympy.Symbol('y')
    z = sympy.Symbol('z')

    #表达式输入
    def PressExpr(Sym):
        nonlocal x,y,z,FuncSym,SingleSym,NumSym
        curExpr = result.get()
        newExpr = curExpr + Sym
        result.set(newExpr)
    

    #控制按键输入
    def PressCtrl(Sym):
        curExpr = result.get() 
        if Sym == 'AC':
            result.set('')
            result2.set('')
        elif Sym == 'CE':
            result.set('')
        elif Sym == 'backspace':
            for i in range(-10,-1):
                if curExpr[i:] in FuncSym:
                    result.set(curExpr[0:i])
                    return
            result.set(curExpr[0:-1])
        else:
            pass

    #计算表达式的值
    def PressEqual():
        nonlocal x,y,z,FuncSym,SingleSym,NumSym
        try:
            DispStr = result.get()
            CompStr = DispStr
            CompStr = CompStr.replace('^','**')
            CompStr = CompStr.replace('π','pi')
            CompStr = CompStr.replace('×','*')
            CompStr = CompStr.replace('∞','oo')
            CompStr = CompStr.replace('∫','integrate')
            CompStr = CompStr.replace('arcsin','asin')
            CompStr = CompStr.replace('arccos','acos')
            CompStr = CompStr.replace('arctan','atan')
            CompStr = CompStr.replace('arcsinh','asinh')
            CompStr = CompStr.replace('arccosh','acosh')
            CompStr = CompStr.replace('arctanh','atanh')
            CompStr = CompStr.replace('ln','log')
            if not(CompStr.find('0**0')):
                raise ValueError
            ans = str(eval(CompStr))
            ans = ans.replace('**','^')
            ans = ans.replace('pi','π')
            ans = ans.replace('*','×')
            ans = ans.replace('oo','∞')
            ans = ans.replace('integrate','∫')
            ans = ans.replace('asin','arcsin')
            ans = ans.replace('acos','arccos')
            ans = ans.replace('atan','arctan')
            ans = ans.replace('asinh','arcsinh')
            ans = ans.replace('acosh','arccosh')
            ans = ans.replace('atanh','arctanh')
            ans = ans.replace('log','ln')
            result.set(ans)
            result2.set(DispStr)
            return 0
        except ZeroDivisionError:
            tkinter.messagebox.showerror('除零错误',message = '除法计算时！除数不能为0！')
            return -1
        '''except ValueError:
            tkinter.messagebox.showerror('非法运算',message = '结果异常！请检查计算是否合法！')
            return -1
        except OverflowError:
            tkinter.messagebox.showerror('上界溢出',message = '结果超过了程序最大可表示范围！')
            return -1
        except:
            tkinter.messagebox.showerror('语法错误',message = '表达式有误！')
            return -1'''
    
    try:
        root.destroy()
    except:
        pass
    root = tkinter.Tk()

    #菜单栏部分
    Menubar = tkinter.Menu(root)

    PlotList = tkinter.Menu(Menubar,tearoff = 0)
    PlotList.add_command(label = '2D绘图',command = lambda:Plot2D())
    PlotList.add_command(label = '3D绘图',command = lambda:Plot3D())

    Preference = tkinter.Menu(Menubar,tearoff = 0)
    Preference.add_command(label = '普通计算',command = lambda:main())
    Preference.add_command(label = '统计数学',command = lambda:Statistics())
    Preference.add_command(label = '微积分',command = lambda:Calculus.main())
    Preference.add_command(label = '线性代数',command = lambda:LinearAlgebra())
    Preference.add_cascade(label = '绘图',menu = PlotList)

    Preference.add_separator()
    Preference.add_command(label = '退出',command = lambda:root.destroy())

    Edit = tkinter.Menu(Menubar,tearoff = 0)
    Edit.add_command(label = '复制',command = lambda:(root.clipboard_clear(),root.clipboard_append(result.get())))
    Edit.add_command(label = '粘贴',command = lambda:result.set(root.clipboard_get()))

    Help = tkinter.Menu(Menubar,tearoff = 0)
    Help.add_command(label = '关于...',command = lambda:about())

    Menubar.add_cascade(label = '选项',menu = Preference)
    Menubar.add_cascade(label = '编辑',menu = Edit)
    Menubar.add_cascade(label = '帮助',menu = Help)
    root['menu'] = Menubar

    root.maxsize(730,520)
    root.minsize(730,520)
    root.resizable(False,False)
    root.title('Calculus')
    root.iconbitmap('.\Calculator.ico')

    #当前表达式（计算结果）、上一次计算的表达式与‘M’累加器显示屏
    result = tkinter.StringVar()    #当前表达式（结果）
    result.set('')
    result2 = tkinter.StringVar()   #上一次计算的表达式
    result2.set('')



    #对应的显示屏
    label = tkinter.Label(root,font = ('微软雅黑',15),bg = '#EEE9E9',bd ='9',fg = '#828282',anchor = 'se',textvariable = result2)
    label.place(width = 730,height = 80)
    label2 = tkinter.Label(root,font = ('微软雅黑',30),bg = '#EEE9E9',bd ='9',fg = 'black',anchor = 'se',textvariable = result)
    label2.place(y = 78,width = 730,height = 60)

    #常用区数字按键：0-9、百分数‘%’、小数点‘.’、圆周率π、自然对数的底数e和结果寄存器ans
    btn7 = tkinter.Button(root,text = '7',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('7'))
    btn7.place(x = 450-70,y = 285,width = 60,height = 50)
    btn8 = tkinter.Button(root,text = '8',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('8'))
    btn8.place(x = 520-70,y = 285,width = 60,height = 50)
    btn9 = tkinter.Button(root,text = '9',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('9'))
    btn9.place(x = 590-70,y = 285,width = 60,height = 50)
    btn4 = tkinter.Button(root,text = '4',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('4'))
    btn4.place(x = 450-70,y = 340,width = 60,height = 50)
    btn5 = tkinter.Button(root,text = '5',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('5'))
    btn5.place(x = 520-70,y = 340,width = 60,height = 50)
    btn6 = tkinter.Button(root,text = '6',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('6'))
    btn6.place(x = 590-70,y = 340,width = 60,height = 50)
    btn1 = tkinter.Button(root,text = '1',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('1'))
    btn1.place(x = 450-70,y = 395,width = 60,height = 50)
    btn2 = tkinter.Button(root,text = '2',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('2'))
    btn2.place(x = 520-70,y = 395,width = 60,height = 50)
    btn3 = tkinter.Button(root,text = '3',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('3'))
    btn3.place(x = 590-70,y = 395,width = 60,height = 50)
    btn0 = tkinter.Button(root,text = '0',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('0'))
    btn0.place(x = 520-70,y = 450,width = 60,height = 50)
    btnComma = tkinter.Button(root,text = ',',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda :PressExpr (','))
    btnComma.place(x = 450-70,y = 450,width = 60,height = 50)
    btnDot = tkinter.Button(root,text = '.',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('.'))
    btnDot.place(x = 590-70,y = 450,width = 60,height = 50)
    btnPi = tkinter.Button(root,text = 'π',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('π'))
    btnPi.place(x = 730-70,y = 285,width = 60,height = 50)
    btne = tkinter.Button(root,text = 'e',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('e'))
    btne.place(x = 730-70,y = 340,width = 60,height = 50)
    btnAns = tkinter.Button(root,text = '∞',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressExpr('∞'))
    btnAns.place(x = 730-70,y = 395,width = 60,height = 50)

    btnv = tkinter.Button(root,text = 'x',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('x'))
    btnv.place(x = 450-70,y = 175,width = 60,height = 50)
    btnw = tkinter.Button(root,text = 'y',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('y'))
    btnw.place(x = 520-70,y = 175,width = 60,height = 50)
    btnx = tkinter.Button(root,text = 'z',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('z'))
    btnx.place(x = 590-70,y = 175,width = 60,height = 50)
    btny = tkinter.Button(root,text = '[',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('['))
    btny.place(x = 660-70,y = 175,width = 60,height = 50)
    btnz = tkinter.Button(root,text = ']',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr(']'))
    btnz.place(x = 730-70,y = 175,width = 60,height = 50)


    #常用区运算符、控制符按键：AC、CE、BS、左括号‘(’、右括号‘)’、+、-、×、/、计算（Calc）
    btnAc = tkinter.Button(root,text = 'AC',bd = 0.5,font = ('微软雅黑',12),fg = 'orange',command = lambda:PressCtrl('AC'))
    btnAc.place(x = 450-70,y = 230,width = 60,height = 50)
    btnCe = tkinter.Button(root,text = 'CE',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressCtrl('CE'))
    btnCe.place(x = 520-70,y = 230,width = 60,height = 50)
    btnBack = tkinter.Button(root,text = '←',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressCtrl('backspace'))
    btnBack.place(x = 590-70,y = 230,width = 60,height = 50)
    btnLpar = tkinter.Button(root,text = '(',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('('))
    btnLpar.place(x = 660-70,y = 230,width = 60,height = 50)
    btnRpar = tkinter.Button(root,text =')',font = ('微软雅黑',12),fg = "#4F4F4F",bd = 0.5,command = lambda:PressExpr(')'))
    btnRpar.place(x = 730-70,y = 230,width = 60,height = 50)
    btnAdd = tkinter.Button(root,text = '+',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('+'))
    btnAdd.place(x = 660-70,y = 285,width = 60,height = 50)
    btnSub = tkinter.Button(root,text = '-',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('-'))
    btnSub.place(x = 660-70,y = 340,width = 60,height = 50)
    btnMul = tkinter.Button(root,text = '×',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('×'))
    btnMul.place(x = 660-70,y = 395,width = 60,height = 50)
    btnDiv = tkinter.Button(root,text = '÷',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('/'))
    btnDiv.place(x = 660-70,y = 450,width = 60,height = 50)
    btnCalc = tkinter.Button(root,text = 'Calc',bg = 'orange',font = ('微软雅黑',12),fg = ('#4F4F4F'),bd = 0.5,command = lambda:PressEqual())
    btnCalc.place(x = 730-70,y = 450,width = 60,height = 50)

    #功能函数键右1:平方、立方、开根号、倒数、10的幂、工程对数
    btnSqr = tkinter.Button(root,text = 'x^2',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('^2'))
    btnSqr.place(x = 360-70,y = 175,width = 60,height = 50)
    btnCub = tkinter.Button(root,text = 'x^3',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('^3'))
    btnCub.place(x = 360-70,y = 230,width = 60,height = 50)
    btnSqrt = tkinter.Button(root,text = '√x',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('^0.5'))
    btnSqrt.place(x = 360-70,y = 285,width = 60,height = 50)
    btnRev = tkinter.Button(root,text = '1/x',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('^-1'))
    btnRev.place(x = 360-70,y = 340,width = 60,height = 50)
    btnPow10 = tkinter.Button(root,text = '10^x',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('10^'))
    btnPow10.place(x = 360-70,y = 395,width = 60,height = 50)
    btnLog10 = tkinter.Button(root,text = 'log10',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('log10('))
    btnLog10.place(x = 360-70,y = 450,width = 60,height = 50)

    #功能函数键右2：x^y，e的幂（注意与10的幂区分）、自然对数、一般对数、求余、绝对值
    btnExp = tkinter.Button(root,text = 'e^x',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('e^'))
    btnExp.place(x = 290-70,y = 175,width = 60,height = 50)
    btnLn = tkinter.Button(root,text = 'ln',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('ln('))
    btnLn.place(x = 290-70,y = 230,width = 60,height = 50)
    btnPow = tkinter.Button(root,text = 'x^y',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('^'))
    btnPow.place(x = 290-70,y = 285,width = 60,height = 50)
    btnLog = tkinter.Button(root,text = 'log(a,b)',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('log('))
    btnLog.place(x = 290-70,y = 340,width = 60,height = 50)
    btnMod = tkinter.Button(root,text = 'j',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('1j'))
    btnMod.place(x = 290-70,y = 395,width = 60,height = 50)
    btnAbs = tkinter.Button(root,text = 'abs',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('abs('))
    btnAbs.place(x = 290-70,y = 450,width = 60,height = 50)

    #功能函数键右3：（反）三角函数与（反）双曲函数，双曲函数按‘↑’切换
    btnSin = tkinter.Button(root,text = 'sin',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('sin('))
    btnSin.place(x = 220-70,y = 175,width = 60,height = 50)
    btnCos = tkinter.Button(root,text = 'cos',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('cos('))
    btnCos.place(x = 220-70,y = 230,width = 60,height = 50)
    btnTan = tkinter.Button(root,text = 'tan',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('tan('))
    btnTan.place(x = 220-70,y = 285,width = 60,height = 50)
    btnAsin = tkinter.Button(root,text = 'arcsin',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('arcsin('))
    btnAsin.place(x = 220-70,y = 340,width = 60,height = 50)
    btnAcos = tkinter.Button(root,text = 'arccos',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('arccos('))
    btnAcos.place(x = 220-70,y = 395,width = 60,height = 50)
    btnAtan = tkinter.Button(root,text = 'arctan',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('arctan('))
    btnAtan.place(x = 220-70,y = 450,width = 60,height = 50)

    btnSinh = tkinter.Button(root,text = 'sinh',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('sinh('))
    btnSinh.place(x = 150-70,y = 175,width = 60,height = 50)
    btnCosh = tkinter.Button(root,text = 'cosh',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('cosh('))
    btnCosh.place(x = 150-70,y = 230,width = 60,height = 50)
    btnTanh = tkinter.Button(root,text = 'tanh',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('tanh('))
    btnTanh.place(x = 150-70,y = 285,width = 60,height = 50)
    btnAsinh = tkinter.Button(root,text = 'arcsinh',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('arcsinh('))
    btnAsinh.place(x = 150-70,y = 340,width = 60,height = 50)
    btnAcosh = tkinter.Button(root,text = 'arccosh',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('arccosh('))
    btnAcosh.place(x = 150-70,y = 395,width = 60,height = 50)
    btnAtanh = tkinter.Button(root,text = 'arctanh',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('arctanh('))
    btnAtanh.place(x = 150-70,y = 450,width = 60,height = 50)


    btnLim = tkinter.Button(root,text = 'limit',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('limit('))
    btnLim.place(x = 80-70,y = 175,width = 60,height = 50)
    btnDiff = tkinter.Button(root,text = 'diff',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('diff('))
    btnDiff.place(x = 80-70,y = 230,width = 60,height = 50)
    btnInt = tkinter.Button(root,text = '∫',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('∫('))
    btnInt.place(x = 80-70,y = 285,width = 60,height = 50)
    btnSolve = tkinter.Button(root,text = 'solve',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('solve('))
    btnSolve.place(x = 80-70,y = 340,width = 60,height = 50)
    btnSeries = tkinter.Button(root,text = 'series',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('series('))
    btnSeries.place(x = 80-70,y = 395,width = 60,height = 50)   
    btnSimp = tkinter.Button(root,text = 'simplify',font = ('微软雅黑',12),fg = '#4F4F4F',bd = 0.5,command = lambda:PressExpr('simplify('))
    btnSimp.place(x = 80-70,y = 450,width = 60,height = 50)
    


    '''*****************************************************************功能实现部分*****************************************************************'''

    NumBtn =    [btn0, btn1, btn2, btn3, btn4, btn5, btn6,  btn7, btn8, btn9]

    FuncBtn =   [btnSqr,   btnCub,  btnSqrt, btnRev,  btnPow10, btnLog10,
                 btnExp,   btnLn,   btnPow,  btnLog,  btnAbs,   btnComma,
                 btnSin,   btnCos,  btnTan,  btnAsin, btnAcos,  btnAtan]
    


    

    #监视键盘的有效输入，以及菜单与快捷键的复制粘贴
    def GetKey(event):
        if event.char == '\b':
            PressCtrl('backspace')
        elif event.char == '\r':
            PressEqual()
        elif event.char.upper() in NumSym[10:13] + ['F']:
            PressExpr(event.char.upper())
        elif not(event.char in SingleSym or event.char in NumSym):
            pass
        else:
            PressExpr(event.char)

    def EditExpr(event):   
        Edit.post(event.x_root, event.y_root)

    def Copy(event):
        root.clipboard_clear()
        root.clipboard_append(result.get())

    def Paste(event):
        result.set(root.clipboard_get())

    root.bind('<Control-C>', Copy)
    root.bind('<Control-c>', Copy)
    root.bind('<Control-V>', Paste)
    root.bind('<Control-v>', Paste)
    root.bind('<Key>', GetKey)
    label2.bind('<Button-3>', EditExpr)

    root.mainloop()

if __name__ =='__main__':
    main()
