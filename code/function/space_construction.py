# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 14:15:09 2020

@author: Henry


Space creation 

Contain all function to create a space 
"""


import os
working_directory="D:/download/Memoire_code/function"
os.chdir(working_directory)

import numpy as np
import pandas as pd
import os 

#visualistime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from visualisation import *
import visualisation

import imageio # pour animation

#rotation
from scipy.spatial.transform import Rotation as R

working_space='D:/download/Memoire_code'
os.chdir(working_space)


def get_plant_info(schema):    #Revnoie les dimensiosn maximal des box de la plantation
    xmax=0
    ymax=0
    zmax=0
    for i in schema :
        
        plant1 = pd.read_csv(str('data/'+i), sep=" ")
        plant1=plant1.drop(['R','G','B'],axis=1)
        #get coordinate of node
        node=plant1[["x1","y1","z1"]]


        #get the dimension of the plant list of [maxX2,minX1],[maxy,miny] etc..
        dim=[[max(node["x1"]),min(node["x1"])],
                  [max(node["y1"]),min(node["y1"])],
                       [max(node["z1"]),min(node["z1"])]]
        plantdim=[dim[0][0]-dim[0][1],dim[1][0]-dim[1][1],dim[2][0]-dim[2][1]]
        
        if xmax < plantdim[0]:
            xmax=plantdim[0]
        if ymax < plantdim[1]:
            ymax=plantdim[1]
        if zmax < plantdim[2]:
            zmax=plantdim[2]
        plantdim=[xmax,ymax,zmax]
        
    #plantdim = [i * facteur_simplification for i in plantdim] c la couille de l'espace
    return  plantdim #[element * 10 for element in plantdim] # 


def create_space(Px,Py,Ex,Ey,z,d) :      #creer un df de coordoonées de l'espace et ses dimensions ainsi que les coordoonées des centres des 9 plants dans cette espace.
       
    #bon tout le truc du dessus me soule un peu donc on va recommencer la définition de l'espace 
    spacesize=[3*Px + 2*Ex + d, 3*Py + 2*Ey , z ]    
    centerx =np.array([Px/2, spacesize[0]/2,spacesize[0]-Px/2,  #for ligne1
                       
                       Px/2 + d, spacesize[0]/2 + d, spacesize[0]-Px/2 + d , #for decalate line

                      Px/2, spacesize[0]/2,spacesize[0]-Px/2])
    
    centery =np.array([spacesize[1]-Py/2, spacesize[1]-Py/2,spacesize[1]-Py/2,  #for ligne1
                       
                       spacesize[1]/2,spacesize[1]/2,spacesize[1]/2, #for decalate line

                   Py/2 ,Py/2, Py/2    ])
    space_coor = pd.DataFrame(np.array([[0,0,0]]),
                   columns=['x1', 'y1', 'z1'])    
    
    return spacesize,centerx,centery,space_coor


def get_coordinate(planttxt,ID,time=1000):
    
    plant1 = pd.read_csv(str('data/'+planttxt), sep=" ")
    plant=plant1.drop(['R','G','B'],axis=1)
    #get coordinate of node
    node_coor=plant1[["x1","y1","z1","time"]]
    node_coor["ID"]=ID
    #on va multiplier par round(10) et récuperer les valeur distinct
    #node_coor=round(node_coor*10)  #permet de simplifier les données mais pas encore sur d'etre utile
    #puis on elève les point deux fois pas sur de l'utilité
    node_coor=node_coor.drop_duplicates()
    
    #sous-selection en fonction de l'time
    node_coor=node_coor[node_coor["time"]<time]
    #verification node_coor[node_coor["time"]<=700]
    
    #on translate l'espace dimensionel de manière à avoir de valeurs positives (pas sur de la nécéssité)
    #test=node_coor.to_numpy().astype(int)
    #translation=[ min(test[:,0]), min(test[:,1]), min(test[:,2])]
    #test=test-translation
       
    return node_coor


def translate_plant_into_space_position ( space_coor,centerx,centery,schema,rotation,time=60): #si j'ai tout les coordonées de mes points. IL me suffit d'appliquer une addition vectoriel pour effectuer une transaltion.
    
    #for 9 plant
    for i in range(0,len(schema)):
        #print(i,centerx[i],centery[i])

        
        planttxt=schema[i]
        #getplantcord
        plant_coor=get_coordinate(planttxt,time=time,ID=i+1) 
        #rotate the plant
        
        plant_coor[["x1", "y1","z1"]]=rotate_plant(plant_coor,rotation[i])
            
        #remettre en DF
        plant_coor= pd.DataFrame(data=plant_coor, columns=["x1", "y1","z1","time","ID"])
        #position plant as his center
        plant_coor["x1"]=plant_coor["x1"] +  centerx[i]
        plant_coor["y1"]=plant_coor["y1"] +  centery[i]
        space_coor=space_coor.append(plant_coor)
        #print(planttxt)
    return space_coor


def rotate_plant(node,angle):    
    rotation_degrees = angle
    rotation_radians = np.radians(rotation_degrees)
    rotation_axis = np.array([0, 0, 1])    
    rotation_vector = rotation_radians * rotation_axis
    r = R.from_rotvec(rotation_vector)
    nodeturn=r.apply(node[["x1","y1","z1"]])
    return nodeturn


def simplification_espace(espace_plante,facteur=10):
    espace_plante[["x1", "y1","z1"]]= round(espace_plante[["x1", "y1","z1"]]*facteur)/facteur
    return espace_plante
