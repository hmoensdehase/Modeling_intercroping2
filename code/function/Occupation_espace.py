# -*- coding: utf-8 -*-
"""
Created on Mon May 11 12:00:42 2020

@author: Henry
"""

import numpy as np
import pandas as pd


#read a txt file
name="chicon_entire.xml.txt"
plant1 = pd.read_csv(name, sep=" ")
plant1=plant1.drop(['R','G','B'],axis=1)
#get coordinate of node
node=plant1[["x1","y1","z1"]]

#create a space for analysis
space=np.ndarray()




#test

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(plant1.loc[plant1['branchID'] == 1])


# #<---Click this triangle to load python libraries/ download CPlantBox from GitHub/ Make a plant and visualize it
#############loading other python library or packages. Only need to run once at the start.##########
import os
import sys
! pip3 install vtk
import vtk
from vtk.util import numpy_support as VN

############# Download CPlantBox from GitHub #######################################################
! git clone https://github.com/Plant-Root-Soil-Interactions-Modelling/CPlantBox # downloading the source code
os.chdir("/content/CPlantBox/tutorial/jupyter") # Change to the python directory only for colab (working directory)
!rm modelparameter
!ln -s /content/CPlantBox/modelparameter/ modelparameter
# Loading specific python scripts for CPlantBox and CRootBox
from CPlantBox_PiafMunch import *
plotly.__version__