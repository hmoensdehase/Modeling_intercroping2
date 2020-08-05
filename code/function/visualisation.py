# -*- coding: utf-8 -*-
"""
Created on Sat May 16 15:36:30 2020

@author: Henry

Fonction de visualisation

"""

import matplotlib.pyplot as plt

def _one_plant(node) : #node is a PandasDF with column"x1","y1","z1"    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(node["x1"], node["y1"],node["z1"] ,zdir='z',s=0.05)
    ax.set_zlim(-50,50)
    plt.show()
    return ax    
    

def _plantation(espace_plante,n,spacing) : 
    #pour vérifier la plantation dans le plan
    fig = plt.figure()
    plt.title(n)
    plt.scatter(espace_plante["x1"],espace_plante["y1"])
    plt.xlim=(20,230)
    plt.ylim=(20,230)
    plt.text(0.08,-0.1,s='spacing x : '+str(spacing[0]) + '\n' +'spacing y :' +str(spacing[1]))
    return plt

def _aalPlant(espace_plante,n,spacing) :
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #Axes3D.scatter(test[:,0], test[:,1], test[:,2], zdir='z', s=20, c=None, depthshade=True)    
    ax.scatter(espace_plante["x1"], espace_plante["y1"], espace_plante["z1"] ,zdir='z',s=0.05)
    ax.set_xlim(-20,400)
    ax.set_ylim(-20,400)
    ax.set_zlim(-50,50)
    ax.text2D(0.08,-0.1,s='spacing x : '+str(round(float(spacing[0]),3)) + '\n' +'spacing y :' +str(round(float(spacing[1]),3)))
    plt.title("day : "+str(n))
    plt.xlim=(-20,400)
    plt.ylim=(-20,400)
    plt.zlim=(-50,50)
    plt.show()    
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.tight_layout()
    out=ax.get_figure()
    return out


"""
espace_plante=espace_plante[espace_plante['z1']>0]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#Axes3D.scatter(test[:,0], test[:,1], test[:,2], zdir='z', s=20, c=None, depthshade=True)    
ax.scatter(espace_plante["x1"], espace_plante["y1"], espace_plante["z1"] ,zdir='z',s=1)
ax.set_xlim(-20,400)
ax.set_ylim(-20,400)
ax.set_zlim(0,50)
ax.text2D(0.08,-0.1,s='spacing x : '+str(round(float(spacing[0]),3)) + '\n' +'spacing y :' +str(round(float(spacing[1]),3)))
plt.title("day : "+str(n))
plt.xlim=(-20,400)
plt.ylim=(-20,400)
plt.zlim=(0,50)
plt.show()    
plt.gcf().subplots_adjust(bottom=0.15)
plt.tight_layout()
out=ax.get_figure()
    
out.savefig('img/' + 'ntm',n=time,bbox_inches="tight")
"""