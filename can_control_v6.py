"""
Created on Wed Jan 22 14:38:34 2020

@author: logan
50:2.62
"""  
import tkinter as tk
from time import sleep
import pyfirmata2
import time

def Reset():
    
    board = pyfirmata2.Arduino('/dev/ttyACM100') # change this line if broken. Change the  to 1 or 1 to 0.
    it = pyfirmata2.util.Iterator(board)
    it.start()
    sleep(10)

    global Charge_A_Pin
    Charge_A_Pin = board.get_pin('a:0:i')

    global HV_Pin_Read
    HV_Pin_Read = board.get_pin('a:1:i')
    
    global HV_Pin_Write
    HV_Pin_Write = board.get_pin('d:5:p')

    global Charge_Relay
    Charge_Relay = board.get_pin('d:2:o')

    global Discharge_Relay
    Discharge_Relay = board.get_pin('d:3:o')
    
    global HV
    HV = board.get_pin('d:4:o')
    
Reset()

#defines what the buttons do
def CA_ON(): #defines what happens when Charge A On Button is pressed
    try:
        Discharge_ON["state"]="disable"
        Discharge_OFF["state"]="disable"
        Charge_Relay.write(1)
        print("Charge ON!")
        CA_label["text"]="ON"
        CA_label["bg"]="red"
    except OSError:
        Reset()
        sleep(5)
        CA_ON()
def CA_OFF():  #defines what happens when Charge A Off Button is pressed
    try:
        Charge_Relay.write(0)
        Discharge_ON["state"]="normal"
        Discharge_OFF["state"]="normal"
        print("Charge Off!")
        CA_label["text"]="OFF"
        CA_label["bg"]="grey"
    except OSError:
        Reset()
        sleep(5)
        CA_OFF()


def D_ON(): #defines what happens when Discharge On Button is pressed
    try:
        Charge_A_ON["state"]="disable"
        Charge_A_OFF["state"]="disable"
        Discharge_Relay.write(1)
        print("Discharge ON!")
        D_label["text"]="ON"
        D_label["bg"]="red"
    except OSError:
        Reset()
        sleep(5)
        D_ON()

def D_OFF():  #defines what happens when Discharge Off Button is pressed
    try:
        Discharge_Relay.write(0)
        Charge_A_ON["state"]="normal"
        Charge_A_OFF["state"]="normal"
        print("Discharge Off!")
        D_label["text"]="OFF"
        D_label["bg"]="grey"
    except OSError:
        Reset()
        sleep(5)
        D_OFF()

 
def HV_ON(): #defines what happens when Charge A On Button is pressed
    try:
        HV.write(1)
        print("High Voltage Supply ON!")
        HV_label["text"]="ON"
        HV_label["bg"]="red"
    except OSError:
        Reset()
        sleep(5)
        HV_ON()
def HV_OFF():  #defines what happens when Charge A Off Button is pressed
    try:
        HV.write(0)
        print("High Voltage Supply Off!")
        HV_label["text"]="OFF"
        HV_label["bg"]="grey"
    except OSError:
        Reset()
        sleep(5)
        HV_OFF()

    
def CA_V():
        global Charge_A_Voltage
        Charge_A_Value = Charge_A_Pin.read()
        Charge_A_Voltage= Charge_A_Value*5
        Charge_A_Voltage=round(Charge_A_Voltage,3)
        voltage_A= tk.Label(root, text=(str(Charge_A_Voltage)+" V"),relief="solid", width=8,font=16)
        voltage_A.grid(row=7,column=1)
        root.after(1000,CA_V)
        

def HV_V():
        global HV_Voltage
        HV_Value = HV_Pin_Read.read()
        HV_Voltage= round((HV_Value*50),3)
        voltage_HV= tk.Label(root, text=(str(HV_Voltage)+" kV"),relief="solid", width=8,font=16)
        voltage_HV.grid(row=7,column=0)
        root.after(1000,HV_V)
        
def HV_Set():
    V_Set=HV_IN.get()

    if V_Set>500:
        V_Set=500
    if V_Set<0:
        V_Set=0
    V_Set=V_Set/500
    print(V_Set)
    HV_Pin_Write.write(V_Set)
        
        
    
#tkinter intalizations
root=tk.Tk()
root.grid()
root.title("Can control")

#creates buttons
Charge_A_ON= tk.Button(root,text="Charge ON", fg="red", command= CA_ON) # Creates Charge A On Button
Charge_A_ON.grid(row=0,column=1,padx=30,pady=10) #Places Charge A Button

Charge_A_OFF= tk.Button(root,text="Charge OFF", command= CA_OFF) # Creates Charge A Off Button
Charge_A_OFF.grid(row=2,column=1,padx=30,pady=10) #Places Charge A Button



Discharge_ON= tk.Button(root,text="Discharge ON", fg="red", command= D_ON) # Creates Discharge On Button
Discharge_ON.grid(row=0,column=3,padx=30,pady=10)#Places Discharge Button

Discharge_OFF= tk.Button(root,text="Discharge OFF", command= D_OFF) # Creates Discharge Off Button
Discharge_OFF.grid(row=2,column=3,padx=30,pady=10) #Places Discharge Button

HV_ON= tk.Button(root,text="HV ON", fg="red", command= HV_ON) # Creates Charge A On Button
HV_ON.grid(row=0,column=0,padx=30,pady=10) #Places Charge A Button

HV_OFF= tk.Button(root,text="HV OFF", command= HV_OFF) # Creates Charge A Off Button
HV_OFF.grid(row=2,column=0,padx=30,pady=10) #Places Charge A Button

HV_IN=tk.IntVar()
HV_Input=tk.Entry(root, width=15, textvariable=HV_IN)
HV_Input.grid(row=7,column=3,padx=30,pady=10)

HV_Set= tk.Button(root,text="Set kV", command= HV_Set) # Creates Charge A Off Button
HV_Set.grid(row=7,column=4,pady=10) #Places Charge A Button

Reset= tk.Button(root,text="Reset", command= Reset) # Creates Charge A Off Button
Reset.grid(row=4,column=5,padx=30,pady=10) #Places Charge A Button




#creates on off indicators
CA_label= tk.Label(root, text="OFF",relief="solid",bg="grey", width=8,font=16)
CA_label.grid(row=1,column=1)


HV_label= tk.Label(root, text="OFF",relief="solid", bg="grey",width=8,font=16)
HV_label.grid(row=1,column=0)

D_label= tk.Label(root, text="OFF",relief="solid", bg="grey",width=8,font=16)
D_label.grid(row=1,column=3)

# #runs program

#voltage
HV_V()
voltage_HV= tk.Label(root, text=(str(HV_Voltage)+" kV"),relief="solid", width=8,font=16)
voltage_HV.grid(row=7,column=0)

voltage_HV_Label= tk.Label(root, text=("HV Supply"),relief="solid", width=10,font=16)
voltage_HV_Label.grid(row=6,column=0,pady=30)


CA_V()
voltage_A= tk.Label(root, text=(str(Charge_A_Voltage)+" V"),relief="solid", width=8,font=16)
voltage_A.grid(row=7,column=1)

voltage_A_Label= tk.Label(root, text=("Charge"),relief="solid", width=10,font=16)
voltage_A_Label.grid(row=6,column=1,pady=30)

root.mainloop()
 
