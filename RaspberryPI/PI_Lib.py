# -*- coding: utf-8 -*-
"""
Created on Sun May 28 16:48:17 2023

@author: Utku ARSLAN

Apache-2.0 license

This code is responsible from receiving data and appliying proper movement to vehicle with its sensor
"""
import socket
from threading import Lock,Thread
import time
import serial
import traceback
from datetime import datetime

###################################
stop_distance=20
motor_speed=80
motor_speed_base=1500
###################################



class M_Broadcast:
    def __init__(self,port=7070,connection=None):
        self.port=port
        self.tag='[UDP-Broadcast]'
        print(f'{self.tag} initializing.')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = socket.gethostname()
        self.sock.bind(( ip,self.port)) 
        self.start_reader()
        self.connection=connection
    def start_reader(self):
        Thread(target=self.reader_thread).start()
            
    def reader_thread(self):    
        print(f'{self.tag} listening port {self.port}')
        while True:
            data, address = self.sock.recvfrom(1024)
            print(self.tag,data)
            #self.sock.sendto('Im here!'.encode('utf-8'), address)
            if self.connection !=None:
              self.connection.sender("Im here!".encode('utf-8'),address)

class M_UDP:
    
    """
    
    
    """
    
    udp_target="utkuarslan.xyz"
    udp_port=6565
    
    udp_self_port=6060
    
    def __init__(self,aware_ping=True,aware_time=60,reader=True):
        self.tag='[UDP]'
        self.reader=reader
        self.receive_listeners=[]
        self.aware=aware_ping
        self.aware_time=aware_time
        
        print(f'{self.tag} initializing.')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #name = socket.gethostname()
        #ip=socket.gethostbyname(name)
        #dt = self.sock.bind() 
        
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
                print('[Sender]',msg,adress,port)
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
        print(f'{self.tag} thread starting.')
        Thread(target=self.aware_loop).start()
    
    def aware_loop(self):
        while True:
            with self.aware_lock:
                if not self.aware:
                    #print(f'{self.tag} interupting loop.')
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
        print(f'{self.tag}[Receive] {data}')
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
        

                
class M_Serial_2:

    def onSerialMSGReceived(self, msg, port):
        return

    def writeSerial(self, data):
        self.arduino.write(data.encode())

    def __init__(self, _port='/dev/ttyUSB0', _baudrate=9600,sleep=0.09, loop=True,debug=False,listener=None):
        self.debug=debug
        
        self.serial_port = _port
        self.serial_sleep=sleep
        self.serial_lock=Lock()
        self.loop_read=loop
        self.listener = listener
        self.init()
        if not debug:
            #self.init()
            return
        else:  
            print("[Serial_2][DEBUG MODE] Serial ports not ready...")
            
    def init(self):
        self.thread_loop = Thread(target=self.serial_starting)
        self.thread_loop.start()
        print(f"[Serial_2] initialized on port: {self.serial_port} ")

    # Tries to connect Arduino via Serial
    def serial_setup(self):
            
        try:
            self.arduino = serial.Serial(self.serial_port, 9600)
            print("[Serial_2] serial connected on:"+str(self.serial_port))
            return True
        except Exception as e:
            print(e)
            print("[Serial_2] serial failed to connect on:"+str(self.serial_port))
            return False

    # Serial starting
    def serial_starting(self):
        
        #Bağlantı kurulana kadar 5 sn boyunca dener
        while self.serial_setup() is False:
            time.sleep(5)
        
        if self.loop_read:
            self.serial_loop()


    def serial_loop(self):
        print('[SerialRead_2] read loop started...')
        while True:
            data = self.arduino.readline()
            print('[SerialRead_2]',data)
            #data="41.2587:22.789;174#"
            self.listener(data, self.serial_port)
            #time.sleep(self.serial_sleep)

    def writeSerial(self, data):
        #print(data[0])
        if self.debug:
            return
        with self.serial_lock:
            self.arduino.write(data[0]) #TODO

class M_Sensors_2():

    def __init__(self,main_control=None, _listenPort='/dev/ttyACM0',debug=False):
        self.controller = main_control
        self.debug=debug
        self.sensor_lock = Lock()
        #M_Serial.__init__(self, _listenPort,sleep=0.04,debug=debug)
        self.serial = M_Serial_2(_port=_listenPort,sleep=0.04,debug=debug,listener=self.onSerialMSGReceived)
        print("[Sensors 2] initializing...")
        self.ultrasonic_front = 0
        self.ultrasonic_left = 0
        self.ultrasonic_right = 0
  
    #28:213;12/\r\n
    def onSerialMSGReceived(self, msg, port):
        temp = ""
        
        #print(msg)
        try:
            msg=msg.decode()
        except:
            print("[Serial_2][ERR] UTF-8")
        for c in msg:
            if c == ':':
                with self.sensor_lock:
                    self.ultrasonic_front = int(temp)
                    temp=""
                    #print("LO:"+str(self.gps_lon))
            elif c == ';':
                with self.sensor_lock:
                    self.ultrasonic_left = int(temp)
                    temp = ""
                    #print("LA:"+str(self.gps_lat))
            elif c == '/':
                if len(temp) == 0 :
                    return
                with self.sensor_lock:
                    self.ultrasonic_right = int(temp)
                    temp = ""
                    #print("R:"+str(self.rotation))
            else:
                temp += str(c)
                            
        if self.controller.get_last_msg() == 'forward':
            if self.getFront() <= 20:
                self.controller.motor.sendMsgMotor("1500:1500;")
        elif self.controller.get_last_msg() == 'right':
            if self.getRight() <= 20:
                self.controller.motor.sendMsgMotor("1500:1500;")    
        elif self.controller.get_last_msg() == 'left':
            if self.getLeft() <= 20:
                self.controller.motor.sendMsgMotor("1500:1500;")  
        
   
        
    def getFront(self):
        with self.sensor_lock:
            return self.ultrasonic_front
    def getLeft(self):
        with self.sensor_lock:
            return self.ultrasonic_left
    def getRight(self):
        with self.sensor_lock:
            return self.ultrasonic_right
    def getDataStr(self):
        with self.sensor_lock:
            return str(self.ultrasonic_front) + ":" + str(self.ultrasonic_left) + ";" + str(self.ultrasonic_right)+"/"

class M_Motors():

    def __init__(self,_listenPort='/dev/ttyUSB0',debug=False):
        print("[Motors] initializing...")
        
        self.serial_lock=Lock()
        self.debug=debug
        
        if not debug:
            self.arduino = serial.Serial(_listenPort, 9600)
            print("[Motors] Arduino created...")
            self.writeSerial("1500:1500;".encode())
            self.left = 1500
            self.right = 1500

    def writeSerial(self, data):
        if self.debug:
            print(f'[M_Motor] received data {str(data)}')
            return
        #print(data[0])
        with self.serial_lock:
            self.arduino.write(data) #TODO
            #print("[Seial-Debug] writing data"+str(data))

    def checkRange(self, value, max=1900, min=1100):
        return max if value > max else (min if min > value else value)

    def setMotorsM(self, left, right):  # range 1900-1100
        self.left = self.checkRange(left)
        self.right = self.checkRange(right)
        self.updateMotors()

    # -400 backward / 0 stop / 400 Forward
    def setMotors(self, left=0, right=0):
        self.left = self.checkRange(1500 + left)
        self.right = self.checkRange(1500 + right)
        self.updateMotors()

    def updateMotors(self):
        self.writeSerial((str(self.left) + ":" + str(self.right) + ";").encode())

    def sendMsgMotor(self, ss):
        self.writeSerial(ss) # TODO
        
        """
    def writeSerial(self, data):
        #print(data[0])
        with self.serial_lock:
            self.arduino.write(data) #TODO
            #print("[Seial-Debug] writing data"+str(data))
            """

    def checkRange(self, value, max=1900, min=1100):
        return max if value > max else (min if min > value else value)

    def setMotorsM(self, left, right):  # range 1900-1100
        self.left = self.checkRange(left)
        self.right = self.checkRange(right)
        self.updateMotors()

    # -400 backward / 0 stop / 400 Forward
    def setMotors(self, left=0, right=0):
        self.left = self.checkRange(1500 + left)
        self.right = self.checkRange(1500 + right)
        self.updateMotors()

    def updateMotors(self):
        self.writeSerial((str(self.left) + ":" + str(self.right) + ";").encode())

    def sendMsgMotor(self, ss):
        self.writeSerial(ss.encode('UTF-8')) # TODO 
        
class MainController:
        
    """
    Expected commands:
        Headset Commands:
            forward-left(turning around)-right(turning around)-stop
        Server Commands:
            1500:1500;  ->For motors value, 1100:Backward, 1500:Stop 1900:Forward
            s           ->To sends the sensor data back
            c           ->Block the headset
            h           ->Enable the headset
            p           ->Close pinging
    
    """
    def __init__(self):
        DEBUG=True
        self.last_msg_lock=Lock()
        self.last_msg=None
        self.motor=M_Motors(_listenPort='/dev/ttyUSB1',debug=False)
        self.sensors=M_Sensors_2(main_control=self,_listenPort='/dev/ttyUSB0',debug=True)
        #self.broadcast=M_Broadcast()
        self.tag='[H-Controller]'
        
        #Server Configuration
        self.connection=M_UDP()
        self.connection.add_listener(self.on_server)
        self.connection_lock=Lock()
        
        self.headset_control=True
        
    def get_last_msg(self):
        with self.last_msg_lock:
            return self.last_msg
            
    def set_last_msg(self):
        with self.last_msg_lock:
            self.last_msg="1500:1500;"
        
    def on_server(self,data,adress):
        print(f'{self.tag} server "{data}" - {datetime.now().strftime("%H:%M:%S")} - {self.headset_control}') 
        self.last_msg=data
        if data.endswith(';'):
            if "1500:1500;" != data:
                self.headset_control=False
            self.motor.sendMsgMotor(data)
        elif len(data)==1:
            if data=='h':
                self.headset_control=True 
                self.connection.sender("headset",adress=adress[0],port=adress[1])
                print(f'{self.tag} headset controller Enabled')
            elif data=='c':
                self.headset_control=False
                self.connection.sender("blocked",adress=adress[0],port=adress[1])
                print(f'{self.tag} headset controller Blocked')
            elif data=='s':
                self.connection.sender(self.sensors.getDataStr(),adress=adress[0],port=adress[1])
            elif data=='p':
                print(f'{self.tag} aware pinging turned off')
                self.connection.stop_aware()
                
        elif self.headset_control:
            print(f'{self.tag} Headset_Control')
            if 'forward' == data:
                if self.sensors.getFront() > stop_distance: 
                    #self.change_motors(200,200)
                    self.motor.sendMsgMotor(f"{motor_speed_base+motor_speed}:{motor_speed_base+motor_speed};")
                else:
                    self.motor.sendMsgMotor(f"{motor_speed_base}:{motor_speed_base};")
            elif 'left' == data:
                if self.sensors.getLeft() > stop_distance: 
                    #self.change_motors(-200,200)
                    self.motor.sendMsgMotor(f"{motor_speed_base-motor_speed}:{motor_speed_base+motor_speed};") 
                else:
                    self.motor.sendMsgMotor(f"{motor_speed_base}:{motor_speed_base};")
            elif 'right' == data:
                if self.sensors.getRight() > stop_distance: 
                    #self.change_motors(200,-200)
                    self.motor.sendMsgMotor(f"{motor_speed_base+motor_speed}:{motor_speed_base-motor_speed};")
                else:
                    self.motor.sendMsgMotor(f"{motor_speed_base}:{motor_speed_base};")
            elif 'stop' == data:
                #self.change_motors(0,0)
                self.motor.sendMsgMotor(f"{motor_speed_base}:{motor_speed_base};")
        
    def change_motors(self,left,right):
        print(f'{self.tag} {left},{right}')
        return
        

        
if __name__ == '__main__':
    
    
    M=MainController() 
    
    #sensors=M_Sensors_2(_listenPort='/dev/ttyUSB0',debug=False)
    

    
    #sensors=M_Sensors_2(_listenPort='/dev/ttyUSB0',debug=False)
    
    """
    def test1():
        def on_receive(data,adress):
            print(f'[On_Receiver] {data}')
        u=M_UDP(aware_time=0.2)
        u.add_listener(on_receive)
        time.sleep(2)
        u.shutdown()
    """
    
    
    
        """
    def test1():
        def on_receive(data,adress):
            print(f'[On_Receiver] {data}')
        u=M_UDP(aware_time=0.2)
        u.add_listener(on_receive)
        time.sleep(2)
        u.shutdown()
    """
          
"""
    #front:left;right/
    def onSerialMSGReceived(self, msg, port):
        temp = ""
        
        try:
            msg=msg.decode("utf-8")
        except:
            print("[Sensor_2][ERR] UTF-8")
        for c in msg:
            if c == ':':
                with self.sensor_lock:
                    self.ultrasonic_front = float(temp)
                    temp=""
            elif c == ';':
                with self.sensor_lock:
                    self.ultrasonic_left = float(temp)
                    temp = ""
            
            elif c == '/':
                if len(temp) == 0:
                    return
                with self.sensor_lock:
                    self.ultrasonic_right = float(temp if temp != '' else self.ultrasonic_right)
                    temp = ""
            else:
                temp += str(c)
                
        self.motor

    def getFront(self):
        with self.sensor_lock:
            return self.ultrasonic_front
    def getLeft(self):
        with self.sensor_lock:
            return self.ultrasonic_left
    def getRight(self):
        with self.sensor_lock:
            return self.ultrasonic_right
    def getDataStr(self):
        with self.sensor_lock:
            return str(self.ultrasonic_front) + ":" + str(self.ultrasonic_left) + ";" + str(self.ultrasonic_right)+"/"
            
                            
        if self.controller.last_msg == 'forward':
            if self.getFront() <= 20:
                self.controller.motors.sendMsgMotor("1500:1500;")
        elif self.controller.last_msg == 'right':
            if self.getRight() <= 20:
                self.controller.motors.sendMsgMotor("1500:1500;")    
        elif self.controller.last_msg == 'left':
            if self.getLeft() <= 20:
                self.controller.motors.sendMsgMotor("1500:1500;")  
                
class M_Sensors(M_Serial):

    def __init__(self, _listenPort='/dev/ttyACM0',debug=False):
        self.debug=debug
        self.sensor_lock = Lock()
        M_Serial.__init__(self, _listenPort,sleep=0.04,debug=debug)
        print("[Sensors] initializing...")
        self.ultrasonic_front = 0
        self.ultrasonic_left = 0
        self.ultrasonic_right = 0
        

    #front:left;right/
    def onSerialMSGReceived(self, msg, port):
        temp = ""
        
        print(msg)
        try:
            msg=msg.decode()
        except:
            print("[Serial][ERR] UTF-8")
        for c in msg:
            if c == ':':
                with self.sensor_lock:
                    self.ultrasonic_front = float(temp)
                    temp=""
            elif c == ';':
                with self.sensor_lock:
                    self.ultrasonic_left = float(temp)
                    temp = ""
            
            elif c == '/':
                if len(temp) == 0:
                    return
                with self.sensor_lock:
                    self.ultrasonic_right = float(temp if temp != '' else self.ultrasonic_right)
                    temp = ""
            else:
                temp += str(c)

    def getFront(self):
        with self.sensor_lock:
            return self.ultrasonic_front
    def getLeft(self):
        with self.sensor_lock:
            return self.ultrasonic_left
    def getRight(self):
        with self.sensor_lock:
            return self.ultrasonic_right
    def getDataStr(self):
        with self.sensor_lock:
            return str(self.ultrasonic_front) + ":" + str(self.ultrasonic_left) + ";" + str(self.ultrasonic_right)+"/"
    
    
    #28:213;12/\r\n
    def onSerialMSGReceived(self, msg, port):
        temp = ""
        
        #print(msg)
        try:
            msg=msg.decode()
        except:
            print("[Serial][ERR] UTF-8")
        for c in msg:
            if c == ':':
                with self.sensor_lock:
                    self.ultrasonic_front = int(temp)
                    temp=""
                    #print("LO:"+str(self.gps_lon))
            elif c == ';':
                with self.sensor_lock:
                    self.ultrasonic_left = int(temp)
                    temp = ""
                    #print("LA:"+str(self.gps_lat))
            elif c == '/':
                if len(temp) == 0 :
                    return
                with self.sensor_lock:
                    self.ultrasonic_right = int(temp)
                    temp = ""
                    #print("R:"+str(self.rotation))
            else:
                temp += str(c)

    def getFront(self):
        with self.sensor_lock:
            return self.ultrasonic_front
    def getLeft(self):
        with self.sensor_lock:
            return self.ultrasonic_left
    def getRight(self):
        with self.sensor_lock:
            return self.ultrasonic_right
    def getDataStr(self):
        with self.sensor_lock:
            return str(self.ultrasonic_front) + ":" + str(self.ultrasonic_left) + ";" + str(self.ultrasonic_right)+"/"
            
   
                    
class M_Serial:

    def onSerialMSGReceived(self, msg, port):
        return

    def writeSerial(self, data):
        self.arduino.write(data.encode())

    def __init__(self, _port='/dev/ttyUSB0', _baudrate=9600,sleep=0.1, loop=True,debug=False):
        self.debug=debug
        
        self.serial_port = _port
        self.serial_sleep=sleep
        self.serial_lock=Lock()
        self.loop_read=loop
        if not debug:
            self.init()
            #super(M_Serial).__init__()
        else:  
            print("[Serial][DEBUG MODE] Serial ports not ready...")
            
    def init(self):
        self.thread_loop = Thread(target=self.serial_starting)
        self.thread_loop.start()
        print(f"[Serial] initialized on port: {self.serial_port} ")

    # Tries to connect Arduino via Serial
    def serial_setup(self):
            
        try:
            self.arduino = serial.Serial(self.serial_port, 9600)
            print("[Serial] serial connected on:"+str(self.serial_port))
            return True
        except Exception as e:
            print(e)
            print("[Serial] serial failed to connect on:"+str(self.serial_port))
            return False

    # Serial starting
    def serial_starting(self):
        
        #Bağlantı kurulana kadar 5 sn boyunca dener
        while self.serial_setup() is False:
            time.sleep(5)
        
        if self.loop_read:
            self.serial_loop()


    def serial_loop(self):
        print('[SerialRead] read loop started...')
        while True:
            data = self.arduino.readline()
            print('[SerialRead]',data)
            #data="41.2587:22.789;174#"
            self.onSerialMSGReceived(data, self.serial_port)
            #time.sleep(self.serial_sleep)

    def writeSerial(self, data):
        #print(data[0])
        if self.debug:
            return
        with self.serial_lock:
            self.arduino.write(data[0]) #TODO
 
"""