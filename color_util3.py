import numpy as np
import cv2

def m_name(dir):
    return dir[-21:]

def percent(image,mask,pmin,pmax):
    test=image[mask != 255]
    num=len(test)
    tsort=np.sort(test)
    low=pmin*num
    high=pmax*num
    return [tsort[low],tsort[high]]

def display(sat,mask,pmin,pmax):
    dmin,dmax=percent(sat,mask,pmin,pmax)
    print dmin,dmax
    satx=255.0*(sat-float(dmin))/float(dmax-dmin)
    satx[satx>255]=255
    satx[satx<0]=0
    return np.uint8(satx)

def m_mask(sat6x,dmin,dmax):
    mask=np.zeros(600*600,dtype=np.uint8).reshape(600,600)
    mask[sat6x < dmin]=255
    mask[sat6x > dmax]=255
    return mask

def m_mask1(sat6x,dmin,dmax):
    mask=np.zeros(7701*7511,dtype=np.uint8).reshape(7511,7701)
    mask[sat6x < dmin]=255
    mask[sat6x > dmax]=255
    return mask


def m_color_true(fname,xmin,xmax,pmin=0.05,pmax=0.95):
  print pmin,pmax
  sat6=cv2.imread(fname+'_B6.TIF',-1)
  sat6x=cv2.resize(sat6,(600,600))
  mask=m_mask(sat6x,xmin,xmax)
  sat=cv2.imread(fname+'_B4.TIF',-1)
  sat2x=cv2.resize(sat,(600,600))
  sat2y=display(sat2x,mask,pmin,pmax)
  sat=cv2.imread(fname+'_B3.TIF',-1)
  sat3x=cv2.resize(sat,(600,600))
  sat3y=display(sat3x,mask,pmin,pmax)
  sat=cv2.imread(fname+'_B2.TIF',-1)
  sat4x=cv2.resize(sat,(600,600))
  sat4y=display(sat4x,mask,pmin,pmax)
  cimg=np.zeros(3*600*600,dtype=np.uint8).reshape(600,600,3)
  cimg[:,:,0]=sat2y
  cimg[:,:,1]=sat3y
  cimg[:,:,2]=sat4y
  return cimg
  
def m_color_faulse(fname,xmin,xmax,pmin=0.05,pmax=0.95):
  print pmin,pmax
  sat6=cv2.imread(fname+'_B6.TIF',-1)
  sat6x=cv2.resize(sat6,(600,600))
  mask=m_mask(sat6x,xmin,xmax)
  sat=cv2.imread(fname+'_B3.TIF',-1)
  sat2x=cv2.resize(sat,(600,600))
  sat2y=display(sat2x,mask,pmin,pmax)
  sat=cv2.imread(fname+'_B4.TIF',-1)
  sat3x=cv2.resize(sat,(600,600))
  sat3y=display(sat3x,mask,pmin,pmax)
  sat=cv2.imread(fname+'_B5.TIF',-1)
  sat4x=cv2.resize(sat,(600,600))
  sat4y=display(sat4x,mask,pmin,pmax)
  cimg=np.zeros(3*600*600,dtype=np.uint8).reshape(600,600,3)
  cimg[:,:,0]=sat2y
  cimg[:,:,1]=sat3y
  cimg[:,:,2]=sat4y
  return cimg

def m_color_natural(fname,xmin,xmax,pmin=0.05,pmax=0.95):
  print pmin,pmax
  sat6=cv2.imread(fname+'_B6.TIF',-1)
  sat6x=cv2.resize(sat6,(600,600))
  mask=m_mask(sat6x,xmin,xmax)
  sat=cv2.imread(fname+'_B3.TIF',-1)
  sat2x=cv2.resize(sat,(600,600))
  sat2y=display(sat2x,mask,pmin,pmax)
  sat=cv2.imread(fname+'_B5.TIF',-1)
  sat3x=cv2.resize(sat,(600,600))
  sat3y=display(sat3x,mask,pmin,pmax)
  sat=cv2.imread(fname+'_B4.TIF',-1)
  sat4x=cv2.resize(sat,(600,600))
  sat4y=display(sat4x,mask,pmin,pmax)
  cimg=np.zeros(3*600*600,dtype=np.uint8).reshape(600,600,3)
  cimg[:,:,0]=sat2y
  cimg[:,:,1]=sat3y
  cimg[:,:,2]=sat4y
  return cimg


def m_color_swir(fname,xmin,xmax,pmin=0.05,pmax=0.95):
  print pmin,pmax
  sat6=cv2.imread(fname+'_B6.TIF',-1)
  sat6x=cv2.resize(sat6,(600,600))
  mask=m_mask(sat6x,xmin,xmax)
  sat=cv2.imread(fname+'_B4.TIF',-1)
  sat2x=cv2.resize(sat,(600,600))
  sat2y=display(sat2x,mask,pmin,pmax)
  sat=cv2.imread(fname+'_B6.TIF',-1)
  sat3x=cv2.resize(sat,(600,600))
  sat3y=display(sat3x,mask,pmin,pmax)
  sat=cv2.imread(fname+'_B7.TIF',-1)
  sat4x=cv2.resize(sat,(600,600))
  sat4y=display(sat4x,mask,pmin,pmax)
  cimg=np.zeros(3*600*600,dtype=np.uint8).reshape(600,600,3)
  cimg[:,:,0]=sat2y
  cimg[:,:,1]=sat3y
  cimg[:,:,2]=sat4y
  return cimg


def m_color_swir(fname,xmin,xmax,pmin=0.05,pmax=0.95):
  print pmin,pmax
  sat6=cv2.imread(fname+'_B6.TIF',-1)
  sat6x=cv2.resize(sat6,(600,600))
  mask=m_mask(sat6x,xmin,xmax)
  sat=cv2.imread(fname+'_B4.TIF',-1)
  sat2x=cv2.resize(sat,(600,600))
  sat2y=display(sat2x,mask,pmin,pmax)
  sat=cv2.imread(fname+'_B6.TIF',-1)
  sat3x=cv2.resize(sat,(600,600))
  sat3y=display(sat3x,mask,pmin,pmax)
  sat=cv2.imread(fname+'_B7.TIF',-1)
  sat4x=cv2.resize(sat,(600,600))
  sat4y=display(sat4x,mask,pmin,pmax)
  cimg=np.zeros(3*600*600,dtype=np.uint8).reshape(600,600,3)
  cimg[:,:,0]=sat2y
  cimg[:,:,1]=sat3y
  cimg[:,:,2]=sat4y
  return cimg

def m_color(fname,xmin,xmax,pmin=0.05,pmax=0.95):
  print pmin,pmax
  sat6=cv2.imread(fname+'_B6.TIF',-1)
  sat6x=cv2.resize(sat6,(600,600))
  mask=m_mask(sat6x,xmin,xmax)
  sat=cv2.imread(fname+'_B'+'self.info.slider7.GetValue()'+'.TIF',-1)
  sat2x=cv2.resize(sat,(600,600))
  sat2y=display(sat2x,mask,pmin,pmax)
  sat=cv2.imread(fname+'_B'+'self.info.slider6.GetValue()'+'.TIF',-1)
  sat3x=cv2.resize(sat,(600,600))
  sat3y=display(sat3x,mask,pmin,pmax)
  sat=cv2.imread(fname+'_B'+'self.info.slider5.GetValue()'+'.TIF',-1)
  sat4x=cv2.resize(sat,(600,600))
  sat4y=display(sat4x,mask,pmin,pmax)
  cimg=np.zeros(3*600*600,dtype=np.uint8).reshape(600,600,3)
  cimg[:,:,0]=sat2y
  cimg[:,:,1]=sat3y
  cimg[:,:,2]=sat4y
  return cimg


  
  


