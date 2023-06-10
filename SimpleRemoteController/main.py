# Import the Required libraries
from tkinter import *
import socket

# Create an instance of tkinter frame or window
win= Tk()
print('1')
# Set the size of the window
win.geometry("700x350")

#####

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('2')
ip = socket.gethostname()
sock.bind(( ip,6464))
sock.sendto('last'.encode('utf-8'), ('utkuarslan.xyz', 6464))
print('3')
data, address = sock.recvfrom(1024)
last_msg=data.decode('utf-8')
print('4')
print('[RECV] ',data.decode('UTF-8'))
#####

# Define a function to display the message
left_motor = 1500
right_motor = 100
max_speed = 100
base_motor = 1500

last_key_press='a'
def key_press(e):
   global last_msg,left_motor,right_motor
   label.config(text=f"{last_msg} {e.char}")
   c=e.char
   last_key_press=c
   if c == 'w':
      left_motor=base_motor+max_speed
      right_motor = base_motor+max_speed
      sock.sendto((f'{left_motor}:{right_motor};').encode('utf-8'), ('utkuarslan.xyz', 6464))
   elif  c == 'a':
      left_motor=base_motor+max_speed*(-1)
      right_motor = base_motor+max_speed
      sock.sendto((f'{left_motor}:{right_motor};').encode('utf-8'), ('utkuarslan.xyz', 6464))
   elif  c == 'd':
      left_motor=base_motor+max_speed
      right_motor = base_motor+max_speed*(-1)
      sock.sendto((f'{left_motor}:{right_motor};').encode('utf-8'), ('utkuarslan.xyz', 6464))
   elif  c == 's':
      left_motor=base_motor+max_speed*(-1)
      right_motor = base_motor+max_speed*(-1)
      sock.sendto((f'{left_motor}:{right_motor};').encode('utf-8'), ('utkuarslan.xyz', 6464))
   elif  c == 'q':
      left_motor=base_motor
      right_motor = base_motor+max_speed
      sock.sendto((f'{left_motor}:{right_motor};').encode('utf-8'), ('utkuarslan.xyz', 6464))
   elif  c == 'e':
      left_motor = base_motor+max_speed
      right_motor = base_motor
      sock.sendto((f'{left_motor}:{right_motor};').encode('utf-8'), ('utkuarslan.xyz', 6464))
   elif  c == 'l':
      sock.sendto('last'.encode('utf-8'), ('utkuarslan.xyz', 6464))
      data, address = sock.recvfrom(1024)
      last_msg=data.decode('utf-8')
      label.config(text=f"{last_msg} {e.char}")
   elif  c == 'h':
      sock.sendto('h'.encode('utf-8'), ('utkuarslan.xyz', 6464))
      #data, address = sock.recvfrom(1024)
      #last_msg=data.decode('utf-8')
      #label.config(text=f"{last_msg} {e.char}")
   elif  c == 'c':
      sock.sendto('c'.encode('utf-8'), ('utkuarslan.xyz', 6464))
      #data, address = sock.recvfrom(1024)
      #last_msg=data.decode('utf-8')
      #label.config(text=f"{last_msg} {e.char}")
   elif  c == 'm':
      sock.sendto('s'.encode('utf-8'), ('utkuarslan.xyz', 6464))
      data, address = sock.recvfrom(1024)
      last_msg=data.decode('utf-8')
      label.config(text=f"{last_msg} {e.char}")
   elif  c == 'f':
      sock.sendto('forward'.encode('utf-8'), ('utkuarslan.xyz', 6464))
   elif  c == 'r':
      sock.sendto('right'.encode('utf-8'), ('utkuarslan.xyz', 6464))
   elif  c == 'v':
      sock.sendto('left'.encode('utf-8'), ('utkuarslan.xyz', 6464))
   elif  c == 'p':
      sock.sendto('1500:1500;'.encode('utf-8'), ('utkuarslan.xyz', 6464))




def key_released(e):
   label.config(text=f"{last_msg}")
   left_motor = base_motor
   right_motor = base_motor
   if(last_key_press=='v' or last_key_press=='f' or last_key_press=='r'):
         return
   sock.sendto((f'{left_motor}:{right_motor};').encode('utf-8'), ('utkuarslan.xyz', 6464))





label= Label(win, text= last_msg, font= ('Helvetica 17 bold'))
label.pack(pady= 50)

w = Canvas(win, width=300, height=300)
#rectangle = w.create_rectangle(0, 0, 20, 140, fill='orange')
#w.create_rectangle(0, 0, 100, 100, fill="blue", outline = 'blue')
#w.create_rectangle(50, 50, 100, 100, fill="red", outline = 'blue')
w.pack()

#canvas.itemconfig(rectangle, fill='green')


# Bind the Mouse button event
win.bind('<KeyPress>',key_press)
win.bind('<KeyRelease>',key_released )
win.mainloop()