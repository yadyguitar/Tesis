from bge import logic
import numpy as np
import math

#variables globales
ruta='/home/yadyguitar/workspace/Tesis/'
cont = logic.getCurrentController()
camara=cont.owner
escena=logic.getCurrentScene()


def getPosicion():
    global ruta
    try:
        file=open(ruta+'infoPersona.txt','r')
        posicion=np.loadtxt(ruta+'infoPersona.txt')
        file.close
        return posicion/10
    except:
        print ("estan modificando el archivo")

def getAnguloZ(persona,objeto):
    x,y=[objeto[0]-persona[0],objeto[1]-persona[1]]
    zRad = abs(math.atan(y/x))
    print (x,y)
    print (zRad)
    #Segun el cuadrante, angulos con respecto a y
    if (x>=0 and y>=0): #I
        return zRad + math.radians(270)
    elif (x<0 and y>0): #II
        return math.radians(90) - zRad
    elif (x<0 and y<0): #III
        return zRad + math.radians(90)
    else:#IV
        return (math.radians(90) - zRad) + math.radians(180)
    

def main():
    global cont
    global camara
    global escena
    #objetos de la escena
    objeto=escena.objects['Objeto']
    posicion=getPosicion()
    
    try:
        orientacion=camara.localOrientation.to_euler()
        anguloZ=getAnguloZ(posicion,[objeto.position.x,objeto.position.y])
        orientacion[2]=anguloZ
        camara.localOrientation = orientacion.to_matrix()
    except:
        print ("error en dar la posicion")
        
    camara.position.x=posicion[0]
    camara.position.y=posicion[1]
       
    

if __name__=='__main__':
    main()
