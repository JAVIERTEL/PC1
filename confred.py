import os

class CONF: 
    def __init__(self, nombre):
        self.nombre = nombre
        self.ips = {
            's1': '10.11.2.31',
            's2': '10.11.2.32',
            's3': '10.11.2.33',
            'c1': '10.11.1.2',
            'lb': '10.11.1.1'
            # Agrega más IPs según sea necesario para otros nombres
        }
        self.ip = self.ips.get(self.nombre)
        
        
        self.lans = {
        's1': '10.11.2.1',
        's2': '10.11.2.1',
        's3': '10.11.2.1',
        'c1': '10.11.1.1',
        'lb': '10.11.1.1'        
        }
        
        
        self.lan = self.lans.get(self.nombre)

    def archivos_conf(self,router):
       
        hostname_content = f"{self.nombre}\n"
        print(f"Router recibido para {self.nombre}: {router}")
        if  not router:
            interface_content = f"""
auto lo
iface lo inet loopback
auto eth0
iface eth0 inet static
address {self.ip}
netmask 255.255.255.0
gateway {self.lan}
"""
            

        else:
            print("Es lb por lo tanto es router")
            interface_content = f"""
auto lo
iface lo inet loopback
auto eth0
iface eth0 inet static
address {self.ip}
netmask 255.255.255.0
gateway {self.lan}
auto eth1
iface eth1 inet static
address 10.11.2.1
netmask 255.255.255.0
gateway 10.11.2.1
"""

#         haproxy_content = f"""
# frontend lb
# bind *:80
# mode http
# default_backend webservers

# backend webservers
# mode http
# balance roundrobin
# server s1 10.11.2.31:80 check
# server s2 10.11.2.32:80 check
# server s3 10.11.2.33:80 check
# """
   
#         with open(f"/tmp/rc.local", "w") as local_file:
#             local_file.write(haproxy_content)
 


        
        with open(f"/tmp/hostname", "w") as hostname_file:
            hostname_file.write(hostname_content)

        with open(f"/tmp/interfaces", "w") as interface_file:
            interface_file.write(interface_content)
            print(interface_content)
        
        print("Archivos de configuración creados en /tmp.")
        

        