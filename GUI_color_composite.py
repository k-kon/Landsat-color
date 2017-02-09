#!/usr/bin/env python
# coding:utf-8
# cd /Users/konkazu/Desktop/GUI_color
# pythonw ./GUI_color_composite.py
import wx
import numpy as np
import cv2
import sys
import array
from struct import *
import os
import convert_util as ut1
import color_util3 as ut
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure

def sdisp(ref,min,max):
  refx=cv2.resize(ref,(600,600))
  temp=255*(refx-min)/(max-min)
  temp[temp < 0]=0.0
  temp[temp > 255]=255.0
  timg=np.zeros((600,600,3),dtype=np.uint8)
  timg[:,:,0]=temp.astype(np.uint8)
  timg[:,:,1]=temp.astype(np.uint8)
  timg[:,:,2]=temp.astype(np.uint8)
  return timg


temp=os.listdir('.')

element=[x for x in temp if os.path.isdir(x) and x.find('LC8')==0]
print(element)
nlen = len(element)

fname=element[0]+'/'+element[0]
Xmin = 8000
Xmax = 16000
Pmin = float(5)
Pmax = float(95)
img=ut.m_color_true(fname,Xmin,Xmax,Pmin/100,Pmax/100)

class ImagePanel(wx.Panel):
    def __init__(self, parent, size, ID = wx.ID_ANY):
        wx.Panel.__init__(self, parent, ID, size = size)
        self.size = size
        bmp = wx.EmptyBitmap(self.size[0], self.size[1])
        self.stbmp = wx.StaticBitmap(self, bitmap = bmp)
        
        
    def redraw(self, img):
        #matplotlib figure
        self.figure = Figure( figsize=(7.5,7.5),frameon=False )
        self.figure.set_facecolor( (0.7,0.7,1.) )
        self.figure.subplots_adjust(left=0.00, bottom=0.00, right=1.00, top=1.0)
        #canvas
        self.canvas = FigureCanvasWxAgg( self, -1, self.figure )
        self.subplot = self.figure.add_subplot( 111 )
        self.subplot.imshow(img)
        cid = self.canvas.mpl_connect('button_press_event', self.onclick)

    def redraw3(self, img):
        #matplotlib figure
        self.figure = Figure(figsize=(5.0,5.0), tight_layout=False )
        self.figure.set_facecolor( (0.7,0.7,1.) )
        #canvas
        self.canvas = FigureCanvasWxAgg( self, -1, self.figure )
        self.subplot = self.figure.add_subplot( 111 )
        #self.subplot.hist(img,bins=50)
        #self.subplot.hist(img)
        self.subplot.plot(img)


    def onclick(self,event):
        print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
            event.button, event.x, event.y, event.xdata, event.ydata)
        num = frame.info.listbox.GetSelection()
        self.fname = element[num]+'/'+element[num]+'_'
        self.sat=ut1.original(self.fname)
        self.land6=cv2.imread(element[num]+'/'+element[num]+'_B6.TIF',-1)
        self.land6x=cv2.resize(self.land6,(600,600))
        self.Mask=ut.m_mask(self.land6x,frame.info.slider.GetValue(),frame.info.slider2.GetValue())
        self.land=cv2.imread(element[num]+'/'+element[num]+'_B'+str(frame.info.slider5.GetValue())+'.TIF',-1)
        self.land2x=cv2.resize(self.land,(600,600))
        dmin4,dmax4=ut.percent(self.land2x,self.Mask,float(frame.info.slider3.GetValue())/100,float(frame.info.slider4.GetValue())/100)
        self.land2y=ut.display(self.land2x,self.Mask,float(frame.info.slider3.GetValue())/100,float(frame.info.slider4.GetValue())/100)
        self.land=cv2.imread(element[num]+'/'+element[num]+'_B'+str(frame.info.slider6.GetValue())+'.TIF',-1)
        self.land3x=cv2.resize(self.land,(600,600))
        dmin3,dmax3=ut.percent(self.land3x,self.Mask,float(frame.info.slider3.GetValue())/100,float(frame.info.slider4.GetValue())/100)
        self.land3y=ut.display(self.land3x,self.Mask,float(frame.info.slider3.GetValue())/100,float(frame.info.slider4.GetValue())/100)
        self.land=cv2.imread(element[num]+'/'+element[num]+'_B'+str(frame.info.slider7.GetValue())+'.TIF',-1)
        self.land4x=cv2.resize(self.land,(600,600))        
        dmin2,dmax2=ut.percent(self.land4x,self.Mask,float(frame.info.slider3.GetValue())/100,float(frame.info.slider4.GetValue())/100)
        self.land4y=ut.display(self.land4x,self.Mask,float(frame.info.slider3.GetValue())/100,float(frame.info.slider4.GetValue())/100)
        img=np.zeros(3*600*600,dtype=np.uint8).reshape(600,600,3)
        img[:,:,0]=self.land2y
        img[:,:,1]=self.land3y
        img[:,:,2]=self.land4y
        frame.ip.redraw(img)
        self.subplot.plot([event.xdata,event.xdata+600*600/self.sat.imax],[event.ydata,event.ydata],'r--',lw=4)
        self.subplot.plot([event.xdata+600*600/self.sat.imax,event.xdata+600*600/self.sat.imax],[event.ydata,event.ydata+600*600/self.sat.jmax],'r--',lw=4)
        self.subplot.plot([event.xdata,event.xdata],[event.ydata,event.ydata+600*600/self.sat.jmax],'r--',lw=4)
        self.subplot.plot([event.xdata,event.xdata+600*600/self.sat.imax],[event.ydata+600*600/self.sat.jmax,event.ydata+600*600/self.sat.jmax],'r--',lw=4)
        self.subplot.plot([event.xdata],[event.ydata],marker="o", markersize=10, markeredgecolor="y", markeredgewidth=2)
        self.subplot.imshow(img)
        self.canvas.draw()
        self.y=self.sat.imax*self.sat.jmax*2
        self.g=open(element[num]+'/'+element[num]+'_B6.TIF','rb')
        self.g.seek(8)
        self.x=self.g.read(self.y)
        self.g.close()

        l_start=int(event.ydata*self.sat.jmax/600) 
        c_start=int(event.xdata*self.sat.imax/600)
        print c_start
        print l_start
        c_max=self.sat.imax
        l_max=self.sat.jmax
        self.ex=[]


        self.g=open(element[num]+'/'+element[num]+'_B6.TIF','rb')

        for i in range(600):
            ii=8+2*c_max*(i+l_start)+2*c_start
            self.g.seek(ii)
            self.x=self.g.read(1200)
            self.ex.append(array.array('h',self.x))

        self.g.close()
        self.xx=np.array(self.ex)
        #print self.xx
        self.maskA=np.zeros(600*600,dtype=np.uint8).reshape(600,600)
        self.maskA[self.xx < frame.info.slider.GetValue()]=255
        self.maskA[self.xx > frame.info.slider2.GetValue()]=255
        self.g=open(element[num]+'/'+element[num]+'_B'+str(frame.info.slider7.GetValue())+'.TIF','rb')
        self.g.seek(8)
        self.x=self.g.read(self.y)
        self.g.close()  
        self.ex=[]
        self.g=open(element[num]+'/'+element[num]+'_B'+str(frame.info.slider7.GetValue())+'.TIF','rb')
        for i in range(600):
            ii=8+2*c_max*(i+l_start)+2*c_start
            self.g.seek(ii)
            self.x=self.g.read(1200)
            self.ex.append(array.array('h',self.x))  
        self.g.close()
        self.land=np.array(self.ex)  
        self.land2x=255.0*(self.land-float(dmin2))/float(dmax2-dmin2)
        self.land2x[self.land2x>255]=255
        self.land2x[self.land2x<0]=0
        self.land2y=np.uint8(self.land2x)
        self.g=open(element[num]+'/'+element[num]+'_B'+str(frame.info.slider6.GetValue())+'.TIF','rb')
        self.g.seek(8)
        self.x=self.g.read(self.y)
        self.g.close()  
        self.ex=[]
        self.g=open(element[num]+'/'+element[num]+'_B'+str(frame.info.slider6.GetValue())+'.TIF','rb')
        for i in range(600):
            ii=8+2*c_max*(i+l_start)+2*c_start
            self.g.seek(ii)
            self.x=self.g.read(1200)
            self.ex.append(array.array('h',self.x))  
        self.g.close()
        self.land=np.array(self.ex)  
        self.land3x=255.0*(self.land-float(dmin3))/float(dmax3-dmin3)
        self.land3x[self.land3x>255]=255
        self.land3x[self.land3x<0]=0
        self.land3y=np.uint8(self.land3x)

        self.g=open(element[num]+'/'+element[num]+'_B'+str(frame.info.slider5.GetValue())+'.TIF','rb')
        self.g.seek(8)
        self.x=self.g.read(self.y)
        self.g.close()  
        self.ex=[]
        self.g=open(element[num]+'/'+element[num]+'_B'+str(frame.info.slider5.GetValue())+'.TIF','rb')
        for i in range(600):
            ii=8+2*c_max*(i+l_start)+2*c_start
            self.g.seek(ii)
            self.x=self.g.read(1200)
            self.ex.append(array.array('h',self.x))  
        self.g.close()
        self.land=np.array(self.ex)  
        self.land4x=255.0*(self.land-float(dmin4))/float(dmax4-dmin4)
        self.land4x[self.land4x>255]=255
        self.land4x[self.land4x<0]=0
        self.land4y=np.uint8(self.land4x)
        
        img1=np.zeros(3*600*600,dtype=np.uint8).reshape(600,600,3)
        img1[:,:,0]=self.land4y
        img1[:,:,1]=self.land3y
        img1[:,:,2]=self.land2y
        plt.figure(figsize=(6,6))
        plt.tick_params(labelbottom='off')
        plt.tick_params(labelleft='off')
        plt.subplots_adjust(left=0,right=1.0,top=1.0,bottom=0,wspace=0,hspace=0)
        plt.imshow(img1)
        plt.show()
        
        frame.ip.redraw(img)


    def onclick1(self,event):
        print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
            event.button, event.x, event.y, event.xdata, event.ydata)

        


class InfoPanel(wx.Panel):
    def __init__(self, parent, size, ID = wx.ID_ANY):
        wx.Panel.__init__(self, parent, ID, size = size)
        self.size = size
        self.text = wx.StaticText(self, wx.ID_ANY, u"[フォルダの選択]")
        self.text2 = wx.StaticText(self, wx.ID_ANY, u"xmin")
        #self.listbox = wx.ListBox(self, wx.ID_ANY, choices=element, style=wx.LB_SINGLE, size=(200,170))
        self.text3 = wx.StaticText(self, wx.ID_ANY, u"xmax")
        self.text4 = wx.StaticText(self, wx.ID_ANY, u"pmin(%)")
        self.text5 = wx.StaticText(self, wx.ID_ANY, u"pmax(%)")
        self.text6 = wx.StaticText(self, wx.ID_ANY, u"[バンドの選択]")
        self.text7 = wx.StaticText(self, wx.ID_ANY, u"RED")
        self.text8 = wx.StaticText(self, wx.ID_ANY, u"GREEN")
        self.text9 = wx.StaticText(self, wx.ID_ANY, u"BLUE")
        self.slider = wx.Slider(self,wx.ID_ANY,style=wx.SL_LABELS)
        self.slider.SetMin(6000)
        self.slider.SetMax(9000)
        self.slider2 = wx.Slider(self,wx.ID_ANY,style=wx.SL_LABELS)
        self.slider2.SetMin(12000)
        self.slider2.SetMax(18000)
        self.slider3 = wx.Slider(self,wx.ID_ANY,style=wx.SL_LABELS)
        self.slider3.SetMin(float(0))
        self.slider3.SetMax(float(10))
        self.slider4 = wx.Slider(self,wx.ID_ANY,style=wx.SL_LABELS)
        self.slider4.SetMin(float(90))
        self.slider4.SetMax(float(100))
        self.slider5 = wx.Slider(self,wx.ID_ANY,style=wx.SL_LABELS)
        self.slider5.SetMin(float(1))
        self.slider5.SetMax(float(11))
        self.slider6 = wx.Slider(self,wx.ID_ANY,style=wx.SL_LABELS)
        self.slider6.SetMin(float(1))
        self.slider6.SetMax(float(11))
        self.slider7 = wx.Slider(self,wx.ID_ANY,style=wx.SL_LABELS)
        self.slider7.SetMin(float(1))
        self.slider7.SetMax(float(11))
        self.listbox = wx.ListBox(self, wx.ID_ANY, choices=element, style=wx.LB_SINGLE, size=(200,170))
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.text)
        layout.Add(self.listbox)
        layout.Add(self.text6)
        layout.Add(self.text7)
        layout.Add(self.slider5)
        layout.Add(self.text8)
        layout.Add(self.slider6)
        layout.Add(self.text9)
        layout.Add(self.slider7)
        layout.Add(self.text2)
        layout.Add(self.slider)
        layout.Add(self.text3)
        layout.Add(self.slider2)
        layout.Add(self.text4,flag=wx.EXPAND | wx.TOP,  border=3)
        layout.Add(self.slider3)
        layout.Add(self.text5)
        layout.Add(self.slider4)
        self.SetSizer(layout)
                

class ButtonPanel(wx.Panel):
    def __init__(self, parent, size, ID = wx.ID_ANY):
        wx.Panel.__init__(self, parent, ID, size = size)
        self.size = size
        self.buttonA = wx.Button(self, wx.ID_ANY, 'COLOR', pos=(200,0))
        self.buttonA.Bind(wx.EVT_BUTTON, parent.buttonPressed_TRUE1)
        self.buttonB = wx.Button(self, wx.ID_ANY, 'MASK', pos=(0,0))
        self.buttonB.Bind(wx.EVT_BUTTON, parent.buttonPressed_MASK)
        self.buttonC = wx.Button(self, wx.ID_ANY, 'HIST', pos=(100,0))
        self.buttonC.Bind(wx.EVT_BUTTON, parent.buttonPressed_HIST)
        self.buttonD = wx.Button(self,wx.ID_ANY,'RESET',pos=(300,0))
        self.buttonD.Bind(wx.EVT_BUTTON,parent.buttonPressed_RESET)
        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(self.buttonB,flag=wx.SHAPED)
        layout.Add(self.buttonC,flag=wx.SHAPED)
        layout.Add(self.buttonA,flag=wx.SHAPED)
        layout.Add(self.buttonD,flag=wx.SHAPED)
        self.SetSizer(layout)
  
class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title, size=(805,680), pos=(100,50))
        self.ip = ImagePanel(self, size = (img.shape[1], img.shape[0]))
        self.bpanel = ButtonPanel(self,(600,30))
        self.button2 = wx.Button(self, wx.ID_ANY, 'SAVE')
        self.button2.Bind(wx.EVT_BUTTON, self.buttonPressed_SAVE)
        self.info = InfoPanel(self,(100,200))
        sizer = wx.FlexGridSizer(2,2)
        sizer.Add(self.ip,flag=wx.GROW)
        sizer.Add(self.info, flag=wx.GROW)
        sizer.Add(self.bpanel, flag = wx.ALIGN_CENTER)
        sizer.Add(self.button2, flag = wx.ALIGN_CENTER)
        sizer.AddGrowableRow(0)
        sizer.AddGrowableCol(1)
        self.SetSizer(sizer)
    

   
    def buttonPressed_SAVE(self,event):
        num = self.info.listbox.GetSelection()
        self.land6=cv2.imread(element[num]+'/'+element[num]+'_B6.TIF',-1)
        self.land6x=cv2.resize(self.land6,(600,600))
        self.Mask=ut.m_mask(self.land6x,self.info.slider.GetValue(),self.info.slider2.GetValue())
        self.land=cv2.imread(element[num]+'/'+element[num]+'_B'+str(self.info.slider7.GetValue())+'.TIF',-1)
        self.land2x=cv2.resize(self.land,(600,600))
        self.land2y=ut.display(self.land2x,self.Mask,float(self.info.slider3.GetValue())/100,float(self.info.slider4.GetValue())/100)
        self.land=cv2.imread(element[num]+'/'+element[num]+'_B'+str(self.info.slider6.GetValue())+'.TIF',-1)
        self.land3x=cv2.resize(self.land,(600,600))
        self.land3y=ut.display(self.land3x,self.Mask,float(self.info.slider3.GetValue())/100,float(self.info.slider4.GetValue())/100)
        self.land=cv2.imread(element[num]+'/'+element[num]+'_B'+str(self.info.slider5.GetValue())+'.TIF',-1)
        self.land4x=cv2.resize(self.land,(600,600))
        self.land4y=ut.display(self.land4x,self.Mask,float(self.info.slider3.GetValue())/100,float(self.info.slider4.GetValue())/100)
        img=np.zeros(3*600*600,dtype=np.uint8).reshape(600,600,3)
        img[:,:,0]=self.land2y
        img[:,:,1]=self.land3y
        img[:,:,2]=self.land4y
        cv2.imwrite('./'+element[num]+'.tif',img) 
        print 'SAVE_COMPLETE'


    def buttonPressed_TRUE1(self,event):
        num = self.info.listbox.GetSelection()
        self.land6=cv2.imread(element[num]+'/'+element[num]+'_B6.TIF',-1)
        self.land6x=cv2.resize(self.land6,(600,600))
        self.Mask=ut.m_mask(self.land6x,self.info.slider.GetValue(),self.info.slider2.GetValue())
        self.land=cv2.imread(element[num]+'/'+element[num]+'_B'+str(self.info.slider5.GetValue())+'.TIF',-1)
        self.land2x=cv2.resize(self.land,(600,600))
        self.land2y=ut.display(self.land2x,self.Mask,float(self.info.slider3.GetValue())/100,float(self.info.slider4.GetValue())/100)
        self.land=cv2.imread(element[num]+'/'+element[num]+'_B'+str(self.info.slider6.GetValue())+'.TIF',-1)
        self.land3x=cv2.resize(self.land,(600,600))
        self.land3y=ut.display(self.land3x,self.Mask,float(self.info.slider3.GetValue())/100,float(self.info.slider4.GetValue())/100)
        self.land=cv2.imread(element[num]+'/'+element[num]+'_B'+str(self.info.slider7.GetValue())+'.TIF',-1)
        self.land4x=cv2.resize(self.land,(600,600))
        self.land4y=ut.display(self.land4x,self.Mask,float(self.info.slider3.GetValue())/100,float(self.info.slider4.GetValue())/100)
        img=np.zeros(3*600*600,dtype=np.uint8).reshape(600,600,3)
        img[:,:,0]=self.land2y
        img[:,:,1]=self.land3y
        img[:,:,2]=self.land4y
        self.ip.redraw(img)

     
    def buttonPressed_MASK(self,event3):
        num = self.info.listbox.GetSelection()
        self.sat=cv2.imread(element[num]+'/'+element[num]+'_B6.TIF',-1)
        self.satx=cv2.resize(self.sat,(600,600))
        self.mask=ut.m_mask(self.satx,self.info.slider.GetValue(),self.info.slider2.GetValue())
        print self.mask
        self.mask=sdisp(self.mask,0.0,0.06)
        self.ip.redraw(self.mask)
 
    def buttonPressed_HIST(self, event = None):
        num = self.info.listbox.GetSelection()
        self.sat=cv2.imread(element[num]+'/'+element[num]+'_B6.TIF',-1)
        self.satx=cv2.resize(self.sat,(600,600))
        self.mask=ut.m_mask(self.satx,self.info.slider.GetValue(),self.info.slider2.GetValue())
        self.sat2=cv2.imread(fname+'_B'+str(self.info.slider7.GetValue())+'.TIF',-1)
        self.sat2x=cv2.resize(self.sat2,(600,600))
        self.test=self.sat2x[self.mask != 255]
        self.num1=len(self.test)
        self.tsort=np.sort(self.test)
        plt.hist(self.tsort,histtype="stepfilled", label = "before",range=(5000,20000),bins = 1000,alpha = 0.5,color = 'blue')
        self.low=float(self.info.slider3.GetValue())/100*self.num1
        self.high=float(self.info.slider4.GetValue())/100*self.num1
        plt.hist(self.tsort[int(self.low):int(self.high)],histtype="stepfilled", label = "after",range=(5000,20000),bins = 1000,alpha = 0.5,color='red')
        plt.xlabel("Degital Number(DN)")
        plt.ylabel("Frequency")
        plt.legend()
        plt.show()

    def buttonPressed_RESET(self,event = None):
        num = self.info.listbox.GetSelection()
        fname=element[num]+'/'+element[num]        
        img=ut.m_color_true(fname,Xmin,Xmax,Pmin/100,Pmax/100)
        frame.info.slider.SetValue(Xmin)
        frame.info.slider2.SetValue(Xmax)
        frame.info.slider3.SetValue(Pmin)
        frame.info.slider4.SetValue(Pmax)
        frame.info.slider5.SetValue(4)
        frame.info.slider6.SetValue(3)
        frame.info.slider7.SetValue(2)
        self.ip.redraw(img)
        


    def buttonPressedD(self,event = None):
        num = self.info.listbox.GetSelection()
        self.sat=cv2.imread(element[num]+'/'+element[num]+'_B6.TIF',-1)
        self.satx=cv2.resize(self.sat,(600,600))
        self.mask=ut.m_mask(self.satx,self.info.slider.GetValue(),self.info.slider2.GetValue())
        self.sat2=cv2.imread(fname+'_B'+str(self.info.slider7.GetValue())+'.TIF',-1)
        self.sat2x=cv2.resize(self.sat2,(600,600))
        self.test=self.sat2x[self.mask != 255]
        self.before=sdisp(self.test,0.0,0.06)
        self.ip.redraw3(self.before)
        
        



             
        



if __name__ == '__main__':

    app = wx.App(False)
    frame = MyFrame(None, wx.ID_ANY, sys.argv[0])
    frame.info.listbox.SetSelection(0)
    frame.info.slider.SetValue(Xmin)
    frame.info.slider2.SetValue(Xmax)
    frame.info.slider3.SetValue(Pmin)
    frame.info.slider4.SetValue(Pmax)
    frame.info.slider5.SetValue(4)
    frame.info.slider6.SetValue(3)
    frame.info.slider7.SetValue(2)
    frame.ip.redraw(img)
    frame.Show()
    app.MainLoop()
