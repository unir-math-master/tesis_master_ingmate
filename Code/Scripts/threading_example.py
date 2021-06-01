from threading import Thread

class MyThread(Thread):                    # MyThread hereda el subproceso de la clase principal

    def __init__(self, name):              # Aquí la subclase MyThread hereda el nombre del método de construcción de la clase padre Thread, _init_ (name = None) inicializa el nombre del hilo
        Thread.__init__(self, name=name)   # name = name nombre del método del constructor de la superclase = nombre del método del constructor de la subclase

    def run(self):                         #Método  run () Este método se ejecuta cuando el hilo adquiere recursos de CPU
        print("Hello, my name is %s" % self.getName())  #% De salida formateada

    def main(self):                        # Use el método principal para iniciar un nuevo hilo y salir normalmente en la terminal
        MyThread("xiaoming").start()


if __name__ == '__main__':
    process = MyThread("xiaoming")
    process.start()                        #El método start () hace que el nuevo proceso entre en el estado listo, solo se permite ejecutar una vez, de lo contrario se generará una excepción
    process.main()
    process.getName()