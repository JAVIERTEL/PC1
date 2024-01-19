import logging, subprocess, re, os, shutil
from lxml import etree
from subprocess import call
from confred import CONF


log = logging.getLogger('auto_p2')
    
class MV:
  def __init__(self, nombre):
    self.nombre = nombre
   
  

  

  def crear_mv (self, imagen, interfaces_red, router):

    
  
  
    subprocess.run(['qemu-img', 'convert', '-O', 'qcow2', 'cdps-vm-base-pc1.qcow2', f'{self.nombre}.qcow2'])
    print(open('/tmp/interfaces', 'r').read())    
    subprocess.run(['sudo', 'virt-copy-in', '-a', f'{self.nombre}.qcow2', f'/tmp/interfaces', '/etc/network'])
    subprocess.run(['sudo', 'virt-copy-in', '-a', f'{self.nombre}.qcow2', f'/tmp/hostname', '/etc'])
    subprocess.run(['sudo', 'virt-edit', '-a', f'{self.nombre}.qcow2', '/etc/hosts', '-e', f's/127.0.1.1 cdps cdps/127.0.1.1 {self.nombre}/'])
    if router:
        log.debug("Es router")
        subprocess.run(['sudo', 'virt-edit', '-a', 'lb.qcow2', '/etc/sysctl.conf', '-e', 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/'])
        # subprocess.run(['sudo', 'virt-edit', '-a', 'lb.qcow2', '/tmp/rc.local', '/etc'])
        # subprocess.run(['sudo', 'virt-edit', '-a', 'lb.qcow2', '/etc/rc.local', '-e', 'service haproxy restart'])

    else:
        pass
 

       
    log.debug("crear_copiaimagen " + self.nombre)
    self.interfaces_red = interfaces_red
    log.debug("crear_mv " + self.nombre)
    shutil.copy('plantilla-vm-pc1.xml', f'{self.nombre}.xml')
    tree = etree.parse(f'{self.nombre}.xml')
    with open(f'{self.nombre}.xml', 'r') as file:
        print(file.read())

    
    nombre_mv={self.nombre}
    interfaces={interfaces_red}       
    root=tree.getroot()     
    name= root.find("name")
    name.text= self.nombre
    source= root.find("./devices/interface/source")
    source.set("bridge",self.interfaces_red)
    ubicacion = root.find("./devices/disk/source")
    ubicacion.set("file", f"/home/ignacio.divergara/Escritorio/pruebasa/{self.nombre}.qcow2")    
    nueva_interface = '''
<interface type='bridge'>
    <source bridge='LAN2'/>
    <model type='virtio'/>
</interface>
'''
    if router:
            devices = root.find('devices')
            nueva_interfaz= etree.fromstring(nueva_interface)
            devices.append(nueva_interfaz) 
            with open('lb.xml', 'wb') as archivo:
                archivo.write(etree.tostring(tree, pretty_print=True))
    else:
        tree.write(f'{self.nombre}.xml', pretty_print=True)
        pass
        
    
   
    log.debug(f"Archivo XML para {self.nombre} creado")

    with open(f'{self.nombre}.xml', 'r') as file:
        print(file.read())


       
    print("Creando maquina virtual")  

    output = subprocess.run(['sudo', 'virsh', 'list', '--all'], capture_output=True, text=True)
    if re.search(fr'\b{self.nombre}\b', output.stdout):
            log.debug(f"El dominio {self.nombre} ya está definido. Arrancándolo...")
    else:
            # Definir la configuración de la máquina virtual usando virsh
            subprocess.run(['sudo', 'virsh',  'define', nombre_fichero_salida]) 



 

          
#     #Configuramos el archivo haproxy del lb.qcow2 

#     nuevas_lineas = [
#     "frontend lb",
#     "  bind *:80",
#     "  mode http",
#     "  default_backend webservers",
#     "",
#     "backend webservers",
#     "  mode http",
#     "  balance roundrobin",
#     "  server s1 10.11.2.31:80 check",
#     "  server s2 10.11.2.32:80 check",
#     "  server s3 10.11.2.33:80 check"
# ]

#     ruta_archivo = '/etc/haproxy'

#     subprocess.run(['sudo', 'chmod', '-R', '777', ruta_archivo])

#     with open(ruta_archivo, 'a') as archivo:
#         archivo.write('\n'.join(nuevas_lineas) + '\n')


#     #Configuramos la carpeta local para que cuando se arranque se aejecuten estos dos comandos

#     subprocess.run(['sudo', 'virt-edit', '-a', 'lb.qcow2', '/etc/rc.local', '-e', 'service apache2 restart'])          
          

    
  def arrancar_mv (self):
    subprocess.run(['sudo', 'virsh', 'start', self.nombre])
    log.debug("arrancar_mv " + self.nombre)




  def abrir_consola_mv(self):
    subprocess.run(["xterm", "-e", f"sudo virsh console {self.nombre} && sleep 10"])     
    log.debug("abrir_consola_mv ")

  # def mostrar_consola_mv (self):
  #   log.debug("mostrar_mv " + self.nombre)

  def parar_mv (self):
    subprocess.run(['sudo', 'virsh', 'shutdown', self.nombre])
    log.debug("parar_mv " + self.nombre)

  def liberar_mv(self):
    
    os.remove(f"/home/ignacio.divergara/Escritorio/pruebasa/{self.nombre}.xml")
    os.remove(f"/home/ignacio.divergara/Escritorio/pruebasa/{self.nombre}.qcow2")
    subprocess.run(['sudo', 'virsh', 'destroy', self.nombre])
    

    log.debug("liberado_mv " + self.nombre)
    

