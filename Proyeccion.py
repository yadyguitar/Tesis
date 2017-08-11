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
    x,y=[objeto[0]-(persona[0]*-1),objeto[1]-persona[1]]
    try:
        zRad = abs(math.atan(y/x))
    except:
        return 0
    #print (x,y)
    #print (zRad)
    #Segun el cuadrante, angulos con respecto a y
    if (x>=0 and y>=0): #I
        return zRad + math.radians(270)
    elif (x<0 and y>0): #II
        return math.radians(90) - zRad
    elif (x<0 and y<0): #III
        return zRad + math.radians(90)
    else:#IV
        return (math.radians(90) - zRad) + math.radians(180)
    

def rotaventana(persona):
    global camara
    puntoCentral=(-32.0,24.0)
    #own.applyRotation([0.0,0.0,0.01],True)
    x,y=[puntoCentral[0] - (persona[0]*-1), puntoCentral[1] -persona[1]]
    try:
        zLocal= abs(math.atan(y/x))
    except: 
        return 0
    print (math.degrees(zLocal))
    ##angulos!!!, aún no los pasos a radianes
    if (x>=0 and y>=0): #I
        zLocal+=math.radians(180)
        zLocal*=-1
    elif (x<0 and y>0): #II
        zLocal=((math.radians(90)-zLocal)+math.radians(270))*-1
    elif (x<0 and y<0): #III
        zLocal*=-1
    else:#IV
        zLocal=((math.radians(90)-zLocal)+math.radians(90))*-1
    
    camara.applyRotation([0.0,0.0,zLocal],True)
    
def equivalenciaAltura(altura):
    altura*=10
    if altura>153:
        altura=153
    posZ=(153-altura)*(1/2)
    return posZ

def getInclinacion(posx,posy, altura):
    global camara
    puntoCentral=(-32.0,24.0,0.0) #plano xz 
    ###Primero, pasar los dos vectores a las coords
    vectCentral=(0.0,0.0,altura)
    persona=((posx*-1)-puntoCentral[0],posy-puntoCentral[1],altura-puntoCentral[2])

    producto_escalar=vectCentral[2]*persona[2]
    moduloPersona= math.sqrt(persona[0]**2+persona[1]**2+persona[2]**2)
    moduloCentro = vectCentral[2] 
    cosAlfa=producto_escalar/(moduloPersona*moduloCentro)
    xRad=math.acos(cosAlfa)
    return xRad

def main():
    global cont
    global camara
    global escena
    #objetos de la escena
    pointOfView=(-35.0,24.0,0.0)
    
    posicion=getPosicion()
    #print(camara.orientation.to_euler())
    altura=equivalenciaAltura(posicion[2]) #le paso el 3er elemento de persona-> la altura dada por kinect
    if (posicion[0]!=camara["posx"]/10) or (posicion[1]!=camara["posy"]/10):
        #print(posicion)
        #print("posicion de las propiedades: " + str(camara["posx"]) + "," + str(camara["posy"]))
        camara["posx"]=int(posicion[0]*10)
        camara["posy"]=int(posicion[1]*10)
        try:
            orientacion=camara.localOrientation.to_euler()
            anguloZ=getAnguloZ(posicion,[pointOfView[0],pointOfView[1]]) 
            orientacion[0]=getInclinacion(posicion[0],posicion[1],altura)
            orientacion[1]=0
            orientacion[2]=anguloZ
            camara.localOrientation = orientacion.to_matrix()
            rotaventana(posicion)
        except:
            print ("error en dar la posicion")

    camara.position.x=posicion[0]*-1
    camara.position.y=posicion[1]
    camara.position.z=altura
    
       
    

if __name__=='__main__':
    main()
