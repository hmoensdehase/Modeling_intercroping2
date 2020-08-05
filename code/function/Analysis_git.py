# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 17:31:19 2020

@author: Henri

#cette section contient le code ayant servis à analyser 
l'interaction racinaire dans nore culture associé entre des tomates et des laitues 

"""

#package
import os
working_directory="D:/download/Memoire_code/function"
os.chdir(working_directory)

from visualisation import *
import visualisation

from space_construction import *
import space_construction






#working_place
working_directory="D:/download/Memoire_code"
os.chdir(working_directory)



 

#Declaration des fonctions



def choose_schema(schema=[T,T1,T,S,S,S,T1,T,T1]) :
          
     rotation=[]
     for i in range (0,9):
         rotation.append(np.random.randint(1,360))
     return schema,rotation

def choose_spacing(Px,Py,d,nx=10,ny=10) :
     
    Ex=np.linspace(-Px,-Px/2,num=nx) # * facteur_simplification
    #Ex=np.insert(Ex,len(Ex),15)
    Ex=Ex[::-1]   #to get 0 first
    
    Ey = np.linspace(-Py,-Py/2,num=ny) # * facteur_simplification
   # Ey=np.insert(Ey,len(Ey),15)
    Ey=Ey[::-1]
    d=d
    return Ex,Ey,d


#VCette fonction calcule la superposition(super_point_different) et le taux de superposition (percentage)
def _superposition(espace_plante,time):
    #ce serait mieux si on analysait seulement la superposition racinaire donc avec z<0
    espace_plante=espace_plante[espace_plante['z1']<0]
    espace_plante=espace_plante[espace_plante['time']<time]
    
    # On compte le nombre de point qui existent plusieurs fois pour l'ensemble des plantes
    count=espace_plante.groupby(espace_plante[[ 'x1', 'y1', 'z1']].columns.tolist()).size().reset_index().\
        rename(columns={0:'records'}) 
        
    #test=espace_plante.pivot_table(index=['time', 'x1', 'y1', 'z1'], aggfunc='size')
    #la superposition c'est le nombre de point différent total moins le nombre de points ayant au moins deux superpositions
    lonely_point=count[count["records"]==1] # les points qui ne sont pas superposé
    super_point=count[count["records"]!=1]  # les points qui ont au moins une superpostions
    unique=lonely_point.shape[0]
    sup=super_point.shape[0]
    superposition=sum(super_point["records"])-super_point["records"].shape[0] # egal NB points ou coexisent - nm distinct point
    #if (superposition == 0):
        #ratio =0
    #else :
     #   ratio = unique/superposition  
    #if (sup == 0):
     #   ratio2 =0
    #else :
     #   ratio2=unique/sup    
        
    #on va faire la meme mais en différenciant par plante
    #counting occurence for each    'time', 'x1', 'y1', 'z1','ID'
    ratio=0
    ratio2=0
    countbyplant=espace_plante.groupby(espace_plante[[ 'x1', 'y1', 'z1','ID']].columns.tolist()).size().reset_index().\
        rename(columns={0:'records'}) 
    #on regarde si l'time fait problème ==> En effet deux poin ts peuvent coexister mais differer de leur time.
    
    
    #counting occurence for each coordinate ==> nombre de lieux où deux racines de plantes différentes se croisent
    
    
    duplicate=countbyplant.groupby(countbyplant[[ 'x1', 'y1', 'z1']].columns.tolist()).size().reset_index().\
        rename(columns={0:'records'}) 
 
    super_point_different=duplicate[duplicate["records"]!=1] .shape[0]
    #roots density number of dot by cell
    
    if (count.shape[0] == 0):
        rho=np.nan
        percentage=np.nan
    else :
        rho=sum(count["records"])/count.shape[0] 
        # % cell occupied by another plant
        percentage= super_point_different/count.shape[0]
    
    return ratio,rho,percentage,ratio2,superposition,super_point_different


def simplification_espace(espace_plante,facteur=10):
    espace_plante[["x1", "y1","z1"]]= round(espace_plante[["x1", "y1","z1"]]*facteur)/facteur
    return espace_plante





#cette fonction réalise l'analyse en regardant la superposition pour différentes périodes de temps
    # et pour différente valeur d'esapcement. 
#En affichant le plotage=True vous indiquez que vous souhaitez créer un gif de la simulation. Cela rallonge le temps d'exécution du programme. 
def analyse2(param,plotage=True):    #analyse au travers de plusieurs Ex pour chqaue Ey pour chqaue periode considérée
    #On récupere la valeur de la boxplant
    Px,Py,z=get_plant_info(schema) 
    #parameètre d'analyse
    output=[]
    cnt=0    
    imtimes3D=[]
    imtimesP=[]
    counter=len(param["Ex"])*len(param["Ey"])*len(param["time"])
    for ex in param["Ex"] :  ##on test à travers 10 valeur de Ex Ey 
        for ey in param["Ey"] :
            
            
            #On crée un espace de coorodnnée
            spacesize,centerx,centery,space_coor = create_space(Px,Py,ex,ey,z,param["d"])
            #On remplit l'espace avec les plantes
            espace_plante=translate_plant_into_space_position ( space_coor,centerx,centery,schema,rotation,time=60)
            #simplification de l'espace
            espace_plante=simplification_espace(espace_plante,param["facteur_simplification"])
            #analyse
            for time in param["time"]    :     ##on regarde aux différents stades d'evolutions
                cnt+=1
                ratio,rho,percentage,ratio2,superposition,super_point_different=[0,0,0,0,0,0]#_superposition(espace_plante,time)
                print(ratio,rho,percentage,ratio2,superposition,super_point_different)
                #creation du dic de résult
                testi={"Ex" : round(ex,4), "Ey" : round(ey,4),"time" : time , "superpos" : superposition, "ratio" : ratio,"super_point_different" :super_point_different,"ratio2":ratio2,"percentage":percentage,"rho":rho}
                    #résultats
                output.append(testi)
                print('ex :',ex,'ey:' ,ey ,'time :', time,' ', round(cnt/counter*100,2), "%")
                if (plotage ==True) :
                    #Plantation visualisation
                    #imgname='P'+str(cnt)+'test_with_EX_' + str(int(ex))        
                    #plti=visualisation._plantation(espace_plante,n=time,spacing=[ex,ey])
                    #plti.savefig('img/' + imgname,n=time,bbox_inches="tight")         
                    #imtimesP.append(imageio.imread('img/' + str(imgname + '.png')))
                
                        #3D visualisation
                    imgname='3D'+str(cnt)+'test_with_EX_' + str(int(ex))        
                    plti=visualisation._aalPlant(espace_plante,n=time,spacing=[ex,ey])
                    plti.savefig('img/' + imgname,n=time,bbox_inches="tight")
                    imtimes3D.append(imageio.imread('img/' +str(imgname + '.png')))
        
     
                    imageio.mimsave('Analyse_Finale_movie3D.gif', imtimes3D,duration=0.3)
                    #imageio.mimsave('Analyse_movieP.gif', imtimesP,duration=0.3)
    output=a=pd.DataFrame.from_dict(output, orient='columns')
    output.to_csv('final_result/superposition.csv')
    np.savetxt('final_result/superposition.txt',output.values)
    return output





"""
Nous réalisons l'analyse principale sur Ex(5values),Ey(5values),(f5values)
"""

S='finale_salade_60d.txt'
T='finale_tomato_root_60d_2.txt'
[S,T,S,T,S,T,S,T,S]

S3='finale_salade_60d_2.txt'
S4='finale_salade_60d_3.txt'
S5='finale_salade_60d_4.txt'
S6='finale_salade_60d_5.txt'
T1='finale_Tomato_aerial_60d.txt'
T2=T1
T3=T1
T3='final_tomato_root_60d.txt'

#ON choisit le schéma de plantation
schema,rotation=choose_schema([S,T,S,T,S,T,S,T,S])     

facteur_simplification=1
#On définit nos paramètrestion
Px,Py,z=get_plant_info(schema)
Ex,Ey,d=choose_spacing(Px,Py,d=0,nx=5,ny=5)
time= np.linspace(0,30,3)
time=np.array([1,3,5,10,15,20,25,30,35,40,45,50,55, 60])
d=0.0
param={"Ex":Ex,"Ey":Ey,"d":d,"time":time,"facteur_simplification":facteur_simplification}





#analyse occupation espace  au travers de 3 facteurs de simplification
#d'une evolution de Ex pour chaque Ey 
facteur=[0.3,0.5,1,5,10] #3cm,1cm,0.5cm,1mm
outputt=[]
cnt=0
for fact in facteur:
    print(param)
    param["facteur_simplification"]=fact
    output=analyse2(param,plotage=True)   
    output.to_csv('final_result/superposition_Schtest_F'+str(fact)+'.csv')  
    cnt=cnt+1
    


#analyse de l'effet de la période de plantation

#cette fonction permet de prendre un fichier de coordonnée de CplantBox et de rajouter du temps à l'age des plantes et d'enregistrer le nouveau fichier dans un autre doc csv.
# Ceci permet de décaler la croissance dans le temps.
#cette fonction n'a pas besoin d'etre lancé pour la simulation car les fichiers des plantes décalé dans le temps sont déja disponible. 
def add_time(planttxt):
    seeding_period=[0,7,15,21]
    for sp in seeding_period :
        node_coor=get_coordinate(planttxt)
        node_coor['time']=node_coor['time'] + sp
        node_coor.to_csv('/data'+planttxt+'sp'+sp)

outputt=[]
#ensuite on va juste modifier le schéma en mettant des plantes plus agées. 
#on va faire en alterner   
#le meme jour

T1='final_tomato_root_60d_3_sp0.txt'
T2='final_tomato_root_60d_3_sp0.txt'
T3='final_tomato_root_60d_3_sp0.txt'
S1='finale_salade_60d_4_sp0.txt'
S2='finale_salade_60d_3_sp0.txt'
S3='finale_salade_60d_2_sp0.txt'
S4='finale_salade_60d_sp0.txt'
S5='finale_salade_60d_5_sp0.txt'
schema,rotation=choose_schema([S1,T1,S2,T2,S3,T3,S4,T1,S5])  
outputt.append(analyse3(param,plotage=False))

#tomate 7 j avant
T1='final_tomato_root_60d_3_sp0.txt'
T2='final_tomato_root_60d_3_sp0.txt'
T3='final_tomato_root_60d_3_sp0.txt'
S1='finale_salade_60d_4_sp7.txt'
S2='finale_salade_60d_3_sp7.txt'
S3='finale_salade_60d_2_sp7.txt'
S4='finale_salade_60d_sp7.txt'
S5='finale_salade_60d_5_sp7.txt'
schema,rotation=choose_schema([S1,T1,S2,T2,S3,T3,S4,T1,S5])  
outputt.append(analyse3(param,plotage=False))
#tomate 14 j avant
T1='final_tomato_root_60d_3_sp0.txt'
T2='final_tomato_root_60d_3_sp0.txt'
T3='final_tomato_root_60d_3_sp0.txt'
S1='finale_salade_60d_4_sp15.txt'
S2='finale_salade_60d_3_sp15.txt'
S3='finale_salade_60d_2_sp15.txt'
S4='finale_salade_60d_sp15.txt'
S5='finale_salade_60d_5_sp15.txt'
schema,rotation=choose_schema([S1,T1,S2,T2,S3,T3,S4,T1,S5])  
outputt.append(analyse3(param,plotage=False))
#tomate 21 j avant
T1='final_tomato_root_60d_3_sp0.txt'
T2='final_tomato_root_60d_3_sp0.txt'
T3='final_tomato_root_60d_3_sp0.txt'
S1='finale_salade_60d_4_sp21.txt'
S2='finale_salade_60d_3_sp21.txt'
S3='finale_salade_60d_2_sp21.txt'
S4='finale_salade_60d_sp21.txt'
S5='finale_salade_60d_5_sp21.txt'
schema,rotation=choose_schema([S1,T1,S2,T2,S3,T3,S4,T1,S5])  
outputt.append(analyse3(param,plotage=False))
#tomate 7 j apres
T1='final_tomato_root_60d_3_sp7.txt'
T2='final_tomato_root_60d_3_sp7.txt'
T3='final_tomato_root_60d_3_sp7.txt'
S1='finale_salade_60d_4_sp7.txt'
S2='finale_salade_60d_3_sp7.txt'
S3='finale_salade_60d_2_sp7.txt'
S4='finale_salade_60d_sp7.txt'
S5='finale_salade_60d_5_sp7.txt'
schema,rotation=choose_schema([S1,T1,S2,T2,S3,T3,S4,T1,S5])  
outputt.append(analyse3(param,plotage=False))
#tomate 14 j apres
T1='final_tomato_root_60d_3_sp15.txt'
T2='final_tomato_root_60d_3_sp15.txt'
T3='final_tomato_root_60d_3_sp15.txt'
S1='finale_salade_60d_4_sp0.txt'
S2='finale_salade_60d_3_sp0.txt'
S3='finale_salade_60d_2_sp0.txt'
S4='finale_salade_60d_sp0.txt'
S5='finale_salade_60d_5_sp0.txt'
schema,rotation=choose_schema([S1,T1,S2,T2,S3,T3,S4,T1,S5])  
outputt.append(analyse3(param,plotage=False))
#tomate 21 j apres
T1='final_tomato_root_60d_3_sp21.txt'
T2='final_tomato_root_60d_3_sp21.txt'
T3='final_tomato_root_60d_3_sp21.txt'
S1='finale_salade_60d_4_sp0.txt'
S2='finale_salade_60d_3_sp0.txt'
S3='finale_salade_60d_2_sp0.txt'
S4='finale_salade_60d_sp0.txt'
S5='finale_salade_60d_5_sp0.txt'
schema,rotation=choose_schema([S1,T1,S2,T2,S3,T3,S4,T1,S5])  
outputt.append(analyse3(param,plotage=False))

name=[0,-7,-15,-21,7,15,21]
cnti=0
for out in outputt:
    out['sp']=name[cnti]
    out.to_csv('final_result/superposition_Sp'+str(name[cnti])+'.csv') 
    cnti+=1
   


#cette analyse ne s'attarde pas sur l'espacement.    
def analyse3(param,plotage=True):    #analyse au travers de plusieurs Ex pour chqaue Ey pour chqaue periode
    #On récupere la valeur de la boxplant
    Px,Py,z=get_plant_info(schema) 
    #parameètre d'analyse
    output=[]
    cnt=0    
    imtimes3D=[]
    imtimesP=[]
    #On crée un espace de coorodnnée
    spacesize,centerx,centery,space_coor = create_space(Px,Py,ex,ey,z,param["d"])
    #On remplit l'espace avec les plantes
    espace_plante=translate_plant_into_space_position ( space_coor,centerx,centery,schema,rotation,time=100)
    #simplification de l'espace
    espace_plante=simplification_espace(espace_plante,param["facteur_simplification"])
    #analyse
    for time in param["time"]    :     ##on regarde aux différents stades d'evolutions
        cnt+=1
        ratio,rho,percentage,ratio2,superposition,super_point_different=_superposition(espace_plante,time)
        print(ratio,rho,percentage,ratio2,superposition,super_point_different)
        #creation du dic de résult
        testi={"Ex" : round(ex,4), "Ey" : round(ey,4),"time" : time , "superpos" : superposition, "ratio" : ratio,"super_point_different" :super_point_different,"ratio2":ratio2,"percentage":percentage,"rho":rho}
        #résultats
        output.append(testi)
        print('ex :',ex,'ey:' ,ey ,'time :', time,' ')
        if (plotage ==True) :
           #Plantation visualisation
           #imgname='P'+str(cnt)+'test_with_EX_' + str(int(ex))        
           #plti=_plantation(espace_plante,n=time,spacing=[ex,ey])
           #plti.savefig('img/' + imgname,n=time,bbox_inches="tight")         
           #imtimesP.append(imageio.imread('img/' + str(imgname + '.png')))
                
           #3D visualisation
           imgname='3D'+str(cnt)+'test_with_EX_' + str(int(ex))        
           plti=_aalPlant(espace_plante,n=time,spacing=[ex,ey])
           plti.savefig('img/plot' + imgname,n=time,bbox_inches="tight")
           imtimes3D.append(imageio.imread('img/' +str(imgname + '.png')))
        
     
           imageio.mimsave('Analyse_Finale_movie3Dlast.gif', imtimes3D,duration=0.3)
                        #imageio.mimsave('Analyse_movieP.gif', imtimesP,duration=0.3)
    output=a=pd.DataFrame.from_dict(output, orient='columns')
    output.to_csv('final_result/superposition.csv')
    np.savetxt('final_result/superposition.txt',output.values)
    return output

