from bge import logic


class Proyeccion:
    def __init__(self):
        self.cont = logic.getCurrentController()
        self.own=self.cont.owner
        self.escena=logic.getCurrentScene()
        #Capturar los objetos
        self.objeto = self.escena.objects['Objeto']
        self.camara=self.escena.objects['Camera']
        #coordenada estática del objeto
        self.coordsObjeto=self.objeto.position
   def prueba(self):
       return ("hola")
        
        
    def start(self):
        print (self.camara.orientation.to_euler())
        print ("Coordenadas del objeto: ",self.coordsObjeto)
 

if __name__=="__main__":
    Proyeccion().start()




