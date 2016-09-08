#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 17:11:38 2016

@author: konkazu
"""

#cd /Users/konkazu/Desktop/LS8
# color_composite3.py LC81080322015193LGN00


import sys
import os
import cv2
import color_util as ut
import proj_util as pr
"""
os.chdir('..')
reload(ut)
"""
param=sys.argv
fscene=param[1]
os.chdir(fscene)
dir=os.getcwd()
fname=ut.m_name(dir)
cimg=ut.m_color(fname,8000,16000,pmin=0.01,pmax=0.97)
cv2.imshow('color',cimg)
print  'now image "color" is xmin 8000 xmax 16000'
loop_flag = True
while loop_flag:
          xmin,xmax = raw_input('Please write xmin and xmax or if you want to save, please write xmin "0"  ').split()
          x = [xmin,xmax]
          if xmin == '0':
              while True:
                YorN = raw_input('save the image y/n?  ')
                if YorN == 'y':
                   pr.write_tif('../'+fname+'.tif',cimg2,1)
                   loop_flag = False
                   break
                elif YorN == 'n':
                   loop_flag = False
                   break
                else:
                    print 'Please enter y/n'
                    
          else:
            xmin = int(x[0])
            xmax = int(x[1])
            cimg2=ut.m_color(fname,xmin,xmax,pmin=0.01,pmax=0.97)
            cv2.destroyWindow('color2')
            cv2.imshow('color2',cimg2)





