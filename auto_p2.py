#!/usr/bin/env python3

from lib_mv import MV
from confred import CONF
import logging, sys, json, os, subprocess, json, multiprocessing


log = logging.getLogger('auto_p2')


class Configuracion:
    def __init__(self, num_servidores, debug):
        self.num_servidores = num_servidores
        self.debug = debug

# Creacion y configuracion del logger
def init_log():
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('auto_p2')
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.propagate = False


def pause():
    programPause = input("Press <ENTER> to continue")


def abrir_consola(self):
    maquina.abrir_consola_mv()
    print(f"Consola abierta de {maquina.nombre}")
    


def leer_configuracion():
    try:
        with open('auto-p2.json', 'r') as archivo_config:
            configuracion = json.load(archivo_config)
            num_servidores = configuracion.get('num_serv')  
            debug = configuracion.get('debug', False) 
        return Configuracion(num_servidores, debug), debug

    except FileNotFoundError:
        print("Error: El archivo de configuración 'auto-p2.json' no se encontró.")
        return None
    except json.JSONDecodeError:
        print("Error: El archivo de configuración 'auto-p2.json' no tiene un formato JSON válido.")
        return None


#Funcion para comprobar que el numero de servidores del archivo json no es mayot que 5
def comprobar_numero_servidores(configuracion):
    if configuracion is not None: 
        num_servidores = configuracion.num_servidores
        if isinstance(num_servidores, int) and 1 <= num_servidores <= 5:
            return num_servidores
        else:
            print("Error: El número de servidores especificado en 'auto-p2.json' debe ser un entero entre 1 y 5.")
        
        
    return None





    


# Main
#Inicializa los objetos
configuracion, debug = leer_configuracion()
num_servidores = comprobar_numero_servidores(configuracion)
if num_servidores is not None:
    print(f"Se arrancarán {num_servidores} servidores web.")
else:
    print(f"Corrija los errores {num_servidores} en el archivo de configuración antes de continuar.")

if configuracion.debug:
    print("Modo debug activado")
else:
    print("modo debug desactivado")


if debug:
    log.debug('Se inicializan los objetos')
else:
    pass
init_log()
s1 = MV('s1')
s2 = MV('s2')
s3 = MV('s3')
c1 = MV('c1')
lb = MV('lb')
if debug:
    log.debug('Se crea un array con los 5 componentes de la red')
else:
    pass
maquinas_virt = [s1, s2, s3, c1, lb]

existing_interfaces = subprocess.run("brctl show", shell=True, capture_output=True, text=True)



#Para definir y luego crear las maquinas virtuales
if(sys.argv[1] == "crear"):
    if debug:
        log.debug('Se ejecuta el comando crear')
    else:
        pass
    

    #Configuramos el host

    if debug:
        log.debug('Se configura el host')
    else:
        pass
    subprocess.run(['sudo', 'ifconfig', 'LAN1', '10.11.1.3/24'])
    subprocess.run(['sudo', 'ip', 'route', 'add', '10.11.0.0/16', 'via', '10.11.1.1'])

    if debug:
        log.debug('Comprueba que las lanes no existen y de ser así las crea')
    else:
        pass

    if "LAN1" not in existing_interfaces.stdout:
        subprocess.run("sudo brctl addbr LAN1", shell=True, check=True)
        subprocess.run("sudo ifconfig LAN1 up", shell=True, check=True)
    else:
        print("LAN1 ya existe. No se crea.")

    if "LAN2" not in existing_interfaces.stdout:
        subprocess.run("sudo brctl addbr LAN2", shell=True, check=True)
        subprocess.run("sudo ifconfig LAN2 up", shell=True, check=True)
    else:
        print("LAN2 ya existe. No se crea.")
    if len(sys.argv) >= 3:
        if(sys.argv[2] == "s1"):
            conf_maquina = CONF(s1)
            conf_maquina.archivos_conf(False)
            s1.crear_mv('cdps-vm-base-pc1.qcow2', 'LAN2', False)
        elif(sys.argv[2] == "s2"):
            conf_maquina = CONF(s2)
            conf_maquina.archivos_conf(False)
            s2.crear_mv('cdps-vm-base-pc1.qcow2', 'LAN2', False)
        elif(sys.argv[2] == "s3"):
            conf_maquina = CONF(s3)
            conf_maquina.archivos_conf(False)
            s3.crear_mv('cdps-vm-base-pc1.qcow2', 'LAN2', False)
        elif(sys.argv[2] == "c1"):
            conf_maquina = CONF(c1)
            conf_maquina.archivos_conf(False)
            c1.crear_mv('cdps-vm-base-pc1.qcow2', 'LAN1', False)
        elif(sys.argv[2] == "lb"):
            conf_maquina = CONF(lb)
            conf_maquina.archivos_conf(True)
            lb.crear_mv('cdps-vm-base-pc1.qcow2', 'LAN1', True)
    else:
        for maquina in maquinas_virt: 
                if debug:
                    log.debug('Crea los archivos de configuración de cada máquina y los guarda en un fichero temporal')
                else:
                    pass
                conf_maquina = CONF(maquina.nombre)
                if debug:
                    log.debug('Llama a la funcón crear_mv en la que se crean las imágenes como copias de "cdps-vm-base-pc1.qcow2, los ficheros xml y sudo virsh define')
                else:
                    pass
                if maquina.nombre == "lb":
                    conf_maquina.archivos_conf(True)
                    
                    maquina.crear_mv('cdps-vm-base-pc1.qcow2', 'LAN1', True)

                elif maquina.nombre == "c1":
                    conf_maquina.archivos_conf(False)
                    maquina.crear_mv('cdps-vm-base-pc1.qcow2', 'LAN1', False)
               
                else:
                    conf_maquina.archivos_conf(False)
                    maquina.crear_mv('cdps-vm-base-pc1.qcow2', 'LAN2', False)
    pass

#Arrancar las maquinas (sudo virsh start)
if(sys.argv[1] == "arrancar"):
    if len(sys.argv) >= 3:
        if(sys.argv[2] == "s1"):
            s1.arrancar_mv()
        if(sys.argv[2] == "s2"):
            s2.arrancar_mv()
        if(sys.argv[2] == "s3"):
            s3.arrancar_mv()
        if(sys.argv[2] == "c1"):
            c1.arrancar_mv()
        if(sys.argv[2] == "lb"):
            lb.arrancar_mv()
    else:
        for maquina in maquinas_virt:
                maquina.arrancar_mv()
    pass

    if debug:
        log.debug('Llama a la funcón arrancar_mv en la que se ejecuta sudo virsh start')
    else:
        pass
    


#Detener las maquinas virtuales (sudo virsh shutdown)
if(sys.argv[1] == "parar"):
    if len(sys.argv) >= 3:
        if(sys.argv[2] == "s1"):
            s1.parar_mv()
        if(sys.argv[2] == "s2"):
            s2.parar_mv()
        if(sys.argv[2] == "s3"):
            s3.parar_mv()
        if(sys.argv[2] == "c1"):
            c1.parar_mv()
        if(sys.argv[2] == "lb"):
            lb.parar_mv()
    else:
        for maquina in maquinas_virt:
                maquina.parar_mv()
    pass
    if debug:
        log.debug('Llama a la funcón parar_mv en la que se ejecuta sudo virsh shutdown')
    else:
        pass
    

#Eliminar las maquinas virtuales (sudo virsh destroy)
if(sys.argv[1] == "liberar"):

    if len(sys.argv) >= 3:
        if(sys.argv[2] == "s1"):
            s1.liberar_mv()
        if(sys.argv[2] == "s2"):
            s2.liberar_mv()
        if(sys.argv[2] == "s3"):
            s3.liberar_mv()
        if(sys.argv[2] == "c1"):
            c1.liberar_mv()
        if(sys.argv[2] == "lb"):
            lb.liberar_mv()
    else:
        for maquina in maquinas_virt:
                maquina.liberar_mv()
    pass
    if debug:
        log.debug('Llama a la funcón liberar_mv en la que se ejecuta sudo virsh destroy y borra los ficheros xml y las imágenes')
    else:
        pass
    
if(sys.argv[1] == "monitor"):
    for maquina in maquinas_virt:
        output = subprocess.run(['sudo', 'virsh' , 'domstate', maquina.nombre], capture_output = True, text = True)
        print(f"Estado de {maquina.nombre}: {output.stdout.strip()}")
pass 

# if(sys.argv[1] == "consola"):
#     for maquina in maquinas_virt:
#         maquina.abrir_consola_mv()
#         print(f"Consola abierta de {maquina.nombre}")
# pass 

if sys.argv[1] == "arrancar":
    processes = []
    for maquina in maquinas_virt:
        process = multiprocessing.Process(target=abrir_consola, args=(maquina,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print("Todas las consolas se han abierto")
