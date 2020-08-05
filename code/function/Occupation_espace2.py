# -*- coding: utf-8 -*-
"""
Created on Mon May 11 12:00:42 2020

@author: Henry




La plante sera dans ce travail caractérisé comme étant un ensemble de point dans l'espace que nous appellerons noeud (node)
Celles-ci seront le plus souvent une matrice 3D caractérisant l'état finale. 

"""
import os
working_directory="D:/download/Memoire_code/function"
os.chdir(working_directory)

import numpy as np
import pandas as pd
import os 

#visualisage
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from visualisation import *
import visualisation

import imageio # pour animation

#rotation
from scipy.spatial.transform import Rotation as R

working_space='D:\download\Memoire_code'
os.chdir(working_space)

T= "chicon_entire.xml.txt"
S=T#"taproot_andLat.xml.txt"
T1=T#"salade_tapETLAt_V1.xml.txt"


def choose_schema() :
     schema=[T,T1,T,S,S,S,T1,T,T1]
     
     rotation=[]
     for i in range (0,9):
         rotation.append(np.random.randint(1,360))
     return schema,rotation



def get_plant_info(name="chicon_entire.xml.txt"):    #sert à connaitres les dimensions des PLantuNit
    plant1 = pd.read_csv(name, sep=" ")
    plant1=plant1.drop(['R','G','B'],axis=1)
    #get coordinate of node
    node=plant1[["x1","y1","z1"]]


    #get the dimension of the plant list of [maxX2,minX1],[maxy,miny] etc..
    dim=[[max(node["x1"]),min(node["x1"])],
              [max(node["y1"]),min(node["y1"])],
                   [max(node["z1"]),min(node["z1"])]]
    plantdim=[dim[0][0]-dim[0][1],dim[1][0]-dim[1][1],dim[2][0]-dim[2][1]]
    
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






def get_coordinate(planttxt,age=1000):
    
    plant1 = pd.read_csv(planttxt, sep=" ")
    plant=plant1.drop(['R','G','B'],axis=1)
    #get coordinate of node
    node_coor=plant1[["x1","y1","z1","age"]]
    
    #on va multiplier par round(10) et récuperer les valeur distinct
    #node_coor=round(node_coor*10)  #permet de simplifier les données mais pas encore sur d'etre utile
    #puis on elève les point deux fois pas sur de l'utilité
    node_coor=node_coor.drop_duplicates()
    
    #sous-selection en fonction de l'age
    node_coor=node_coor[node_coor["age"]<age]
    #verification node_coor[node_coor["age"]<=700]
    
    #on translate l'espace dimensionel de manière à avoir de valeurs positives (pas sur de la nécéssité)
    #test=node_coor.to_numpy().astype(int)
    #translation=[ min(test[:,0]), min(test[:,1]), min(test[:,2])]
    #test=test-translation
       
    return node_coor




def translate_plant_into_space_position ( space_coor,centerx,centery,schema,age,rotation): #si j'ai tout les coordonées de mes points. IL me suffit d'appliquer une addition vectoriel pour effectuer une transaltion.
    
    #for 9 plant
    for i in range(0,9):
        #print(i,centerx[i],centery[i])
        
        
        planttxt=schema[i]
        #getplantcord
        plant_coor=get_coordinate(planttxt,age) 
        #rotate the plant
        
        plant_coor[["x1", "y1","z1"]]=rotate_plant(plant_coor,rotation[i])
            
        #remettre en DF
        plant_coor= pd.DataFrame(data=plant_coor, columns=["x1", "y1","z1","age"])
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
    




#Vérifier la superposition des points. 
def _superposition(espace_plante):
    # On compte le nombre de point qui existent plusieurs fois
    count=espace_plante.groupby(espace_plante[['age', 'x1', 'y1', 'z1']].columns.tolist()).size().reset_index().\
        rename(columns={0:'records'}) 
    #on regarde si l'age fait problème ==> En effet deux points peuvent coexister mais differer de leur age.
    #count=espace_plante.groupby(espace_plante[[ 'x1', 'y1', 'z1']].columns.tolist()).size().reset_index().\
    #    rename(columns={0:'records'}) 
    
    test=espace_plante.pivot_table(index=['age', 'x1', 'y1', 'z1'], aggfunc='size')
    
    lonely_point=count[count["records"]==1] # les points qui ne sont pas superposé
    super_point=count[count["records"]!=1]  # les points qui ont au moins une superpostions
    unique=lonely_point.shape[0]
    superposition=sum(super_point["records"])-super_point["records"].shape[0] # egal NB points ou coexisent - nm distinct point
    if (superposition == 0):
        ratio = 0
    else :
        ratio = unique/superposition  
    
    return ratio,superposition

    #%"
    #o verifie le nombre max de superpositions.
    super_point["records"].drop_duplicates()
    #verifier les ligne avec doublons ode[node["x1"]==-75][node["y1"]==-113]
    espace_plante[espace_plante["x1"]==-75][espace_plante["y1"]==-113]










def simplification_espace(espace_plante,facteur=10):
    espace_plante[["x1", "y1","z1"]]= round(espace_plante[["x1", "y1","z1"]]*facteur)/facteur
    return espace_plante



#test 1 evolution de la superposition en fonction de Ex, Ey 
    


def analyse_E(plotage=True,param=True):
    #ON choisit le schéma de plantation
    schema=choose_schema()
    #On récupere la valeur de la boxplant
    Px,Py,z=get_plant_info()
    #On définit nos paramètres
    Ex=np.linspace(-Px,Px*1.5,num=10)  
    #Ex=30
    Ey = np.linspace(-Py,Py*1.5,num=10)
    #Ey=30
    E=[Ex,Ey]
    d=0.0

    
    
    
    
#parameètre d'analyse
    output=[]
    cnt=0    
    images3D=[]
    imagesP=[]
    for ex,ey in np.nditer([Ex,Ey]) :        ##on test à travers 10 valeur de Ex Ey 
        print(ex,ey)
        cnt+=1
        #On crée un espace de coorodnnée
        spacesize,centerx,centery,space_coor = create_space(Px,Py,ex,ey,z,d)
        #On remplit l'espace avec les plantes
        espace_plante=translate_plant_into_space_position ( space_coor,centerx,centery,schema,age,rotation)
        #simplification de l'espace
        espace_plante=simplification_espace(espace_plante,facteur=10)
        #analyse
        ratio,superposition=_superposition(espace_plante)
        #creation du dic de résult
        testi={"Ex" : ex.sum(), "Ey" : ey.sum(), "superpos" : superposition, "ratio" : ratio}
        #résultats
        output.append(testi)
        
        if (plotage ==True) :
            #Plantation visualisation
            imgname='P'+str(cnt)+'test_with_EX_' + str(int(ex))        
            plti=visualisation._plantation(espace_plante)
            plti.savefig('img/' + imgname)         
            imagesP.append(imageio.imread('img/' + str(imgname + '.png')))
        
            #3D visualisation
            imgname='3D'+str(cnt)+'test_with_EX_' + str(int(ex))        
            plti=visualisation._aalPlant(espace_plante)
            plti.savefig('img/' + imgname)
            images3D.append(imageio.imread('img/' +str(imgname + '.png')))
        
            #On calcule la superposition
    
            imageio.mimsave('movie3D.gif', images3D,duration=0.3)
            imageio.mimsave('movieP.gif', imagesP,duration=0.3)

    return output


    
    
    croissance=np.linspace(1,700,5)
    def _croissance(croissance):
        imagescroissance=[]
        for i in croissance :
            espace_plante=b_run(age=i)[0]
            #3D visualisation
            imgname='croissance'+ str(cnt)        
            plti=visualisation._aalPlant(espace_plante)
            plti.savefig('img/' + imgname)
            imagescroissance.append(imageio.imread('img/' +str(imgname + '.png')))
        
            #On calcule la superposition
    
        imageio.mimsave('img/croissance.gif', images3D,duration=0.3)
        
output=analyse_E()

def plantation (age,plotage=True): #anciennement b_run
    #ON choisit le schéma de plantation
    schema,rotation=choose_schema()
    #On récupere la valeur de la boxplant
    Px,Py,z=get_plant_info()
    #On définit nos paramètres
    Ex=30
    Ey = 30
    d=0.1
    #On crée un espace de coorodnnée
    spacesize,centerx,centery,space_coor = create_space(Px,Py,Ex,Ey,z,d)
    #On remplit l'espace avec les plantes
    espace_plante=translate_plant_into_space_position ( space_coor,centerx,centery,schema,age,rotation)
    # ON plot pour vérifier que ça a fonctionné 
    if (plotage ==True) :  
        plti=visualisation._aalPlant(espace_plante,n=1)
        plti=visualisation._plantation(espace_plante,n=1)        
    return espace_plante,centerx,centery,plt


#ON choisit le schéma de plantation
schema,rotation=choose_schema()

facteur_simplification=100
#On définit nos paramètres
Ex=np.linspace(-Px,Px,num=10) # * facteur_simplification
#Ex=30
Ey = np.linspace(-Py,Py,num=10) # * facteur_simplification
#Ey=30
age= np.linspace(0,150,3)

age=np.array([0,15,30,50,100])
d=0.0

param={"Ex":Ex,"Ey":Ey,"d":d,"age":age,"facteur_simplification":facteur_simplification}

def analyse(param,plotage=True):    
    #On récupere la valeur de la boxplant
    Px,Py,z=get_plant_info() 
    #parameètre d'analyse
    output=[]
    cnt=0    
    images3D=[]
    imagesP=[]
    for ex,ey in np.nditer([param["Ex"],param["Ey"]]) :  ##on test à travers 10 valeur de Ex Ey 
        for age in param["age"]    :     ##on regarde aux différents stades d'evolutions
            print('ex :',ex,'ey:' ,ey ,'age :', age)
            cnt+=1
            #On crée un espace de coorodnnée
            spacesize,centerx,centery,space_coor = create_space(Px,Py,ex,ey,z,param["d"])
            #On remplit l'espace avec les plantes
            espace_plante=translate_plant_into_space_position ( space_coor,centerx,centery,schema,age,rotation)
            #simplification de l'espace
            espace_plante=simplification_espace(espace_plante,param["facteur_simplification"])
            #analyse
            ratio,superposition=_superposition(espace_plante)
            #creation du dic de résult
            testi={"Ex" : ex.sum(), "Ey" : ey.sum(),"age" : age , "superpos" : superposition, "ratio" : ratio}
            #résultats
            output.append(testi)
            if (plotage ==True) :
                #Plantation visualisation
                imgname='P'+str(cnt)+'test_with_EX_' + str(int(ex))        
                plti=visualisation._plantation(espace_plante,n=cnt)
                plti.savefig('img/' + imgname,n=cnt)         
                imagesP.append(imageio.imread('img/' + str(imgname + '.png')))
                
                #3D visualisation
                imgname='3D'+str(cnt)+'test_with_EX_' + str(int(ex))        
                plti=visualisation._aalPlant(espace_plante,n=cnt)
                plti.savefig('img/' + imgname,n=cnt)
                images3D.append(imageio.imread('img/' +str(imgname + '.png')))
        
                #On calcule la superposition
    
                imageio.mimsave('Analyse_movie3D.gif', images3D,duration=0.3)
                imageio.mimsave('Analyse_movieP.gif', imagesP,duration=0.3)
    output=a=pd.DataFrame.from_dict(output, orient='columns')

    return output








#tentative animation
images = []
filenames=['1test_with_EX_-183.png','2test_with_EX_-142.png','3test_with_EX_-102.png','4test_with_EX_-61.png','5test_with_EX_-20.png','6test_with_EX_20.png','7test_with_EX_61.png','8test_with_EX_102.png','9test_with_EX_142.png','10test_with_EX_183.png']
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('movie.gif', images,duration=0.3)








"D:\download\Memoire_code\result\ "  + str(cnt)+'test_with_EX_' + str(int(ex))



#plot one plant and rotate
nodeturn=get_coordinate(planttxt)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(nodeturn["x1"], nodeturn["y1"],nodeturn["z1"] ,zdir='z')
plt.show()  

nodeturn=rotate_plant(nodeturn,165)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(nodeturn[:,0], nodeturn[:,1],nodeturn[:,2] ,zdir='z')
plt.show() 

























