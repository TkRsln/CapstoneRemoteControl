
"""
Created on Thu Jun  1 12:16:27 2023

@author: Utku ARSLAN

Apache-2.0 license

This code is responsible from transmitting the data between RaspberyPI and User/Controller
"""

import socket
from threading import Lock,Thread
import time
import traceback
from datetime import datetime



class M_UDP:
    
    """
    def on_receive(data,adress):
    
    """
    udp_target="utkuarslan.xyz"
    
    def __init__(self,aware_ping=False,aware_time=60,reader=True,port=6565,tag='[UDP]'):
        self.tag=tag
        self.reader=reader
        self.receive_listeners=[]
        self.aware=aware_ping
        self.aware_time=aware_time
        self.port=port
        
        print(f'{self.tag} initializing.')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = socket.gethostname()
        self.sock.bind(( "utkuarslan.xyz",self.port)) 
        self.lock = Lock()
        self.aware_lock=Lock()
        self.thread_start_loop()
        if reader:
            self.reader_lock=Lock()
            self.thread_start_reader()
        
        #self.sender('Raspi Available!')
    
    #////////////////////[Sender]
    #msg sender, takes argument as a str
    def sender(self,msg,adress= 'utkuarslan.xyz', port=6565):
        msg=msg.encode('utf-8')
        with self.lock:
            try:
                self.sock.sendto(msg, (adress, port))
            except Exception:
                print(f'{self.tag}[ERR] couldnt send the data to target')
                print(traceback.format_exc())

    #////////////////////[Aware-Functions]
    def stop_aware(self):
        with self.aware_lock:
            self.aware=False
            
    def start_aware(self):
        if not self.aware:
            self.aware=True
            self.thread_start_loop()
            
    def thread_start_loop(self):
        return
        print(f'{self.tag} thread starting.')
        Thread(target=self.aware_loop).start()
    
    def aware_loop(self):
        while True:
            with self.aware_lock:
                if not self.aware:
                    break
            self.sender('Raspi Available!')
            time.sleep(self.aware_time)
            
    #////////////////////[Reader]
    def thread_start_reader(self):
        Thread(target=self.reader_loop).start()

    def reader_loop(self):
        while True:
            with self.reader_lock:
                if not self.reader:
                    break
            data, address = self.sock.recvfrom(1024)
            print(data)
            data=data.decode("utf-8")
            self.l_send(data, address)
            
        
    def l_send(self,data,address):
        #print(f'{self.tag}[Receive] {data}')
        for f in self.receive_listeners:
            try:
                f(data,address)
            except Exception:
                print(f'{self.tag}[OnListener] error accured on running listener function')
                print(traceback.format_exc())
        
    #////////////////////[Reader]
    def add_listener(self,listener_function):
        self.receive_listeners.append(listener_function)
        
    def remove_listener(self,listener_f):
        self.receive_listeners.remove(listener_f)
        
    #/////////////////////[Shutdown]
    def shutdown(self):
        self.reader=False
        self.stop_aware()
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except:
            pass
        print(f'{self.tag}[Shutdown] Socket closed')
        
        
class MainServer:
    
    def __init__(self):
        self.con_pi=M_UDP(port=6565,tag='[UDP-Pi]')
        self.con_user=M_UDP(port=6464,tag='[UDP-User]')
        self.con_pi.add_listener(self.on_pi_message)
        self.con_user.add_listener(self.on_user_message)
        self.user_adress=None
        self.pi_adress=None
        self.pi_last="-1"
        
    def on_pi_message(self,data,address):
        print('[OnPi] ',data)
        self.pi_last=datetime.now()
        self.pi_adress = address#Raspi Available!
        if data=='Raspi Available!':
          self.con_pi.sender('Hey!',address[0],address[1])
          print('OnPi--',address[0],address[1])
          return
        if self.user_adress!=None:
            self.con_user.sender(data,self.user_adress[0],self.user_adress[1])
    
    
    def on_user_message(self,data,address):
        print('[OnUser] ',data)
        self.user_adress = address
        if data=='last':
          self.con_user.sender(str(self.pi_last)+str(self.pi_adress),address[0],address[1])
          return
        if self.pi_adress!=None:
            self.con_pi.sender(data,self.pi_adress[0],self.pi_adress[1])
            print("Sent to: ",data,self.pi_adress[0],self.pi_adress[1],"data:",data)
            
MainServer()