import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import ipaddress
from pyModbusTCP.client import ModbusClient
import time
import os
import threading
class Menubar():
        def __init__(self,parent):
            
            font_menu = ('ubuntu',10)
            self.menu_bar= tk.Menu(root,font = font_menu)
            parent.root.config(menu=self.menu_bar)
            self.menu_file = tk.Menu(self.menu_bar,font = font_menu,tearoff=0)
            self.menu_info = tk.Menu(self.menu_bar,font = font_menu,tearoff=0)
            self.menu_bar.add_cascade(label = 'File',menu = self.menu_file)
            self.menu_bar.add_cascade(label = '?',menu = self.menu_info)
            self.menu_file.add_command(label = 'Connetti',command = lambda:self.frame_connect.connetti(parent,self))
            self.menu_file.add_command(label = 'Disconnetti',command = lambda:self.frame_connect.disconnetti(parent,self))
            self.menu_file.add_separator()
            self.menu_file.add_command(label = 'Esci',command = parent.root.destroy)
            self.menu_file.entryconfig(0,state = 'active')
            self.menu_file.entryconfig(1,state = 'disabled')
            self.menu_info.add_command(label = '?',command =Info)
            self.frame_connect = Frame_Connect(self)       
            
class Info():
    def __init__(self):
        self.frame_info = tk.Toplevel()    
        self.frame_info.geometry('234x480+500+200')
        self.frame_info.resizable(False,False)
        self.frame_info.iconbitmap('./info.ico')
        self.frame_info.title('Info')
        self.frameCnt = 58
        self.frames = [tk.PhotoImage(file = 'gif.gif',format = 'gif -index %i' %(i)) for i in range(self.frameCnt)]
        self.label = tk.Label(self.frame_info)
        self.label.pack()
        self.frame_info.after(0, self.update, 0)
        
    def update(self,ind):
        frame = self.frames[ind]
        ind += 1
        if ind == self.frameCnt:
             ind = 0
        self.label.configure(image=frame)
        self.frame_info.after(50, self.update, ind)

            
    
        
class Frame_Connect():
    def __init__(self,parent_menubar): 
        pass
    def connetti(self,parent,parent_menubar):
        self.frame_connect = tk.Toplevel()
        self.frame_connect.geometry('400x250+500+400')
        self.frame_connect.resizable(False,False)
        self.frame_connect.iconbitmap('./connection.ico')
        self.frame_connect.title('Parametri_Di_Connessione')
        self.frame_connect.configure(background='light yellow')
        self.frame_connect.columnconfigure(1,weight=1)
        label_Title = tk.Label(self.frame_connect, text='Parametri di Connessione :',
                                foreground = 'black',font = ('candara',20,'bold italic'),background=('light yellow'))
        label_IP = tk.Label(self.frame_connect, text='IP:',
                                    foreground = 'black',font = ('candara',15,'bold italic'),background=('light yellow'))
        self.ip = tk.StringVar()
        entry_IP = tk.Entry(self.frame_connect,font = ('calibri',13,'bold'),width=14,justify = 'center',
                            textvariable=self.ip,highlightbackground="black",highlightthickness=1)
        entry_IP.insert(0,'127.0.0.1')
        entry_IP.focus_set()
        label_Port = tk.Label(self.frame_connect, text='Port:',
                                foreground = 'black',font = ('candara',15,'bold italic'),background=('light yellow'))
        self.port = tk.StringVar()
        entry_Port = tk.Entry(self.frame_connect,font = ('calibri',13,'bold'),width=5,justify = 'center',
                              textvariable=self.port,highlightbackground="black",highlightthickness=1) 
        entry_Port.insert(0,'502')
        button_connect = tk.Button(self.frame_connect,text = 'Connect',font = ('Calibri Bold',13,'italic'),
                                       foreground='black',background='green',width=10,activebackground ='red',
                                       relief = 'groove',command = lambda:self.Pulsante_Connect(parent,parent_menubar))
        
        self.status_connection = tk.StringVar()
        self.status_connection.set('NON CONNESSO!!')
        self.label_status_connection = tk.Label(self.frame_connect, textvariable=self.status_connection,
                                foreground = 'red',font = ('Candara',15),background=('light yellow'))
        
        label_Title.grid(row=0,column=1,pady=10)
        label_IP.grid(row=1,column=0,sticky=tk.W,pady = 5,padx =100,columnspan=2)
        entry_IP.grid(row=1,column=1,pady=5)
        label_Port.grid(row=2,column=0,sticky=tk.W,pady = 5,padx =80,columnspan=2)
        entry_Port.grid(row=2,column=1,pady=5)
        button_connect.grid(row=3,column=1,pady=10)
        self.label_status_connection.grid(row=4,column=1,pady=3)
             
    def Pulsante_Connect(self,parent,parent_menubar):
        self.ip_tpc,self.port_tcp = self.verifica_ip()
        self.client = ModbusClient(host = self.ip_tpc, port = self.port_tcp, auto_open = False,auto_close = False,timeout = 10)
        try:
            self.client.open()
            if self.client.is_open == True:
                parent.label_state_connection.configure(foreground = 'green')
                parent.status.set('CONNESSO!!')
                self.label_status_connection.configure(foreground = 'green')
                self.status_connection.set('CONNESSO!!')
                self.frame_connect.destroy()
                parent_menubar.menu_file.entryconfig(0,state = 'disabled')
                parent_menubar.menu_file.entryconfig(1,state = 'active')
                parent.frame_setting_register.IP.set(f'{self.ip_tpc}:{self.port_tcp}')
                parent.frame_setting_register.button_update.configure(state='normal',background='green')
                for item in parent.table.get_children():
                    parent.table.delete(item)
            else:
                parent.label_state_connection.configure(foreground = 'red')
                parent.status.set('NON CONNESSO!!')
                msg_impossibile_connettersi = tk.messagebox.showerror(title='Impossibile Connettersi!', 
                                               message=f'''QUESTO NON DOVEVA SUCCEDERE!\nVerifica indirizzo ip e porta\n[IP:{self.ip_tpc} PORT:{self.port_tcp}]''')      
                self.frame_connect.lift()                                        
        except Exception as e:
            print(f'{e}')
    
    def verifica_ip(self):
        try:
            ipaddress.ip_address(self.ip.get())
        except ValueError:
            mess_ip = tk.messagebox.showerror(title='Errore Indirizzo IP', 
                                               message=f'Questo non è un indirizzo valido[{self.ip.get()}]\n#########COGLIONE#########')
            ip_ok = False
            if mess_ip == 'ok':
                self.frame_connect.lift()        
        else:
            ip_ok = True
            
        try:
            int(self.port.get())
        except ValueError:
            mess_port = tk.messagebox.showerror(title='Porta Non Valida', 
                                                message=f'Questa non è una porta valida[{self.port.get()}]\n#########COGLIONE#########')
            port_ok = False
            if mess_port == 'ok':
                self.frame_connect.lift() 
        else:
            port_ok = True      
            
        if ip_ok and port_ok:   
            return self.ip.get(),int(self.port.get())
           
    def disconnetti(self,parent,parent_menubar):
        if self.client.is_open == True:
            self.client.close()
            parent.label_state_connection.configure(foreground = 'red')
            parent.status.set('NON CONNESSO!!')
            parent_menubar.menu_file.entryconfig(0,state = 'active')
            parent_menubar.menu_file.entryconfig(1,state = 'disabled')
            parent.frame_setting_register.IP.set(f'--')
            parent.frame_setting_register.button_update.configure(state='disabled',background='green')
            parent.frame_setting_register.button_write.configure(state='disabled',background='green')
class Frame_Setting_Register():
    def __init__(self,parent):
        self.font = ('Calibri',11,'bold italic')
        self.frame_conn_parms = tk.Frame(parent.root,background='light blue',highlightbackground="black",highlightthickness=2)          
        self.frame_conn_parms.grid_propagate(False)
        self.frame_conn_parms.config(width=270)
        self.frame_conn_parms.columnconfigure(3,weight=1) 
        self.frame_conn_parms.rowconfigure(20,weight=1) 
        label_ip = tk.Label(self.frame_conn_parms, text='Parametri:',
                                    foreground = 'black',font = ('Candara',27,'bold italic underline'),background=('light blue'))   
        self.frame_conn_parms.pack(fill=tk.BOTH,side = tk.RIGHT) 
        self.IP = tk.StringVar()
        self.IP.set('--')
        label_IP = tk.Label(self.frame_conn_parms, textvariable=self.IP,
                                    foreground = 'black',font = ('Calibri',17,'bold italic'),background=('light blue'))
        label_register = tk.Label(self.frame_conn_parms, text='Funzione:',
                                    foreground = 'black',font = self.font,background=('light blue'),justify='right')
        self.register = tk.StringVar() 
        self.register.set('03 Holding Register (4x)')
        self.register_combobox = ttk.Combobox(self.frame_conn_parms,textvariable=self.register)
        self.register_combobox['value'] = ['01 Coil Status (0x)','02 Input Status (1x)','03 Holding Register (4x)','04 Input Register (3x)']
        self.register_combobox['state'] = 'readonly'
        self.register_combobox.configure(font=('Calibri',10,'italic'))
       
        label_address = tk.Label(self.frame_conn_parms, text='Indirizzo:',
                                    foreground = 'black',font = self.font,background=('light blue'),justify='right')
        self.indirizzo = tk.StringVar()
        self.indirizzo.set(0) 
        self.entry_address = tk.Entry(self.frame_conn_parms,font =self.font,width=10,highlightbackground="black",highlightthickness=1,
                                      textvariable=self.indirizzo,justify='center')
        label_NReg = tk.Label(self.frame_conn_parms, text='N.Registri:',
                                    foreground = 'black',font = self.font,background=('light blue'),justify='right')
        self.num_indirizzi = tk.StringVar()
        self.num_indirizzi.set(10)
        self.entry_NReg = tk.Entry(self.frame_conn_parms,font =self.font,width=10,highlightbackground="black",highlightthickness=1,
                                    textvariable=self.num_indirizzi,justify='center')
        self.button_update = tk.Button(self.frame_conn_parms,text = 'UPDATE',font = ('Calibri Bold',13,'italic'),
                                       foreground='black',background='green',width=10,activebackground ='red', padx=10,
                                       relief = 'groove',
                                       command = lambda:threading.Thread(target=parent.Update_table).start())
        self.button_update.configure(state='disabled',background='light green')
        
        self.button_stop = tk.Button(self.frame_conn_parms,text = 'STOP',font = ('Calibri Bold',13,'italic'),
                                       foreground='black',background='red',width=10,activebackground ='red', padx=10,
                                       relief = 'groove',
                                       command = lambda:parent.stop_read())
        self.button_stop.configure(state='disabled',background='#FFB6C1')
        
        label_Scrivi  = tk.Label(self.frame_conn_parms, text='Scrivi Valore', 
                                    foreground = 'black',font = ('Candara',20,'bold italic underline'),background=('light blue'),justify='right')
        
        label_Indirizzo  = tk.Label(self.frame_conn_parms, text='Indirizzo:', 
                                    foreground = 'black',font = self.font,background=('light blue'),justify='right')

        self.w_register = tk.IntVar()
        self.entry_register = tk.Entry(self.frame_conn_parms,font =self.font,width=10,highlightbackground="black",highlightthickness=1,
                                        textvariable=self.w_register,justify='center')
            
        label_Valore  = tk.Label(self.frame_conn_parms, text='Valore:', 
                                        foreground = 'black',font = self.font,background=('light blue'),justify='right')
            
        self.w_valore = tk.IntVar()
        self.entry_valore = tk.Entry(self.frame_conn_parms,font =self.font,width=10,highlightbackground="black",highlightthickness=1,
                                            textvariable=self.w_valore,justify='center')
                
        self.lable_contatore = tk.Label(self.frame_conn_parms, text = 'N.Letture ---> [0]',
                                            foreground = 'black',font = ('calibri',10),background=('light blue'),justify='right')

        self.button_write = tk.Button(self.frame_conn_parms,text = 'WRITE',font = ('Calibri Bold',13,'italic'),
                                            foreground='black',background='green',width=10,activebackground ='red', padx=10,
                                            relief = 'groove',command = lambda:parent.write_register_selection(self.w_register.get(),
                                                                                                        self.w_valore.get()))
        self.button_write.configure(state='disabled',background='light green')

                
        
                        
        label_ip.grid(row=0,column=0,sticky=tk.NSEW,columnspan=4)
        label_IP.grid(row=1,column=0,sticky=tk.NSEW,columnspan=4)
        label_register.grid(row=2,column=0,columnspan=2,sticky=tk.NE,pady=0)
        self.register_combobox.grid(row=2,column=2,columnspan=4,sticky=tk.NW,padx=14,pady=2)
        label_address.grid(row=3,column=0,columnspan=2,pady=10,sticky=tk.NE)
        self.entry_address.grid(row=3,column=2,columnspan=3,sticky=tk.NW,padx=15,pady=12)
        label_NReg.grid(row=4,column=0,columnspan=2,pady=2,sticky=tk.NE)   
        self.entry_NReg.grid(row=4,column=2,columnspan=3,sticky=tk.NW,padx=15,pady=4)
        self.button_update.grid(row=6,column=0,columnspan=4,sticky=tk.NW,pady=8,padx=8)
        self.button_stop.grid(row=6,column=1,columnspan=4,sticky=tk.NE,pady=8,padx=8)
        
        label_Scrivi.grid(row=7,column=0,columnspan=4,sticky=tk.NSEW,pady=0)
        label_Indirizzo.grid(row=8,column=0,columnspan=2,sticky=tk.E,pady=0)
        self.entry_register.grid(row=8,column=2,columnspan=3,sticky=tk.NW,padx=15,pady=8)
        label_Valore.grid(row=9,column=0,columnspan=2,sticky=tk.E,pady=0)
        self.entry_valore.grid(row=9,column=2,columnspan=3,sticky=tk.NW,padx=15,pady=8)
        self.button_write.grid(row=11,column=0,columnspan=4,sticky=tk.N,pady=8)
        
        self.lable_contatore.grid(row=20,column=0,columnspan=2,pady=2,sticky=tk.S) 
        
          
class MainWindow:
    def __init__(self,root):
        root.title("Py_ModBus_Client")
        root.geometry('1200x700')
        root.configure(background='light grey')
        self.root = root
        root.iconbitmap('./main_ico.ico')
        self.status = tk.StringVar()
        self.status.set('NON CONNESSO!!')
        self.label_state_connection = tk.Label(root, textvariable=self.status,
                                               foreground = 'red',font = ('Calibri',17,'bold'),background=('light grey'))
        self.label_state_connection.pack(side=tk.TOP)
        self.frametabella = tk.Frame(root,background='light green',highlightbackground="black",highlightthickness=2)
        
        self.frame_setting_register = Frame_Setting_Register(self)   
        self.frametabella.pack(fill=tk.BOTH,expand=True)
        
        colonne = (0,1,2,3)
        self.table = ttk.Treeview(self.frametabella, columns=colonne,show = 'headings')
        
        self.table.column(0,width=90,anchor=tk.N)
        self.table.column(1,anchor=tk.N)
        self.table.column(2,anchor=tk.N)
        self.table.column(3,anchor=tk.N)
        
        self.table.heading(0,text='Numero_Registro')
        self.table.heading(1,text='Valore_Int')
        self.table.heading(2,text='Valore_Hex')
        self.table.heading(3,text='Valore_Binario')
        
        style = ttk.Style() 
        style.theme_use('default')
        style.configure("Treeview", background="light yellow",fieldbackground="light green", foreground="black",font = ('Roboto',13,'bold'))
        style.configure('Treeview.Heading', background="light grey",font = ('Calibri',13,'bold italic'))
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        
        self.menubar = Menubar(self)
        
        scroolbar = ttk.Scrollbar(self.frametabella,orient='vertical',command=self.table.yview)
        self.table.configure(yscrollcommand=scroolbar.set)
        scroolbar.pack(fill=tk.Y,side = tk.RIGHT)
        self.table.pack(fill='both',expand=True, )
        self.stop_ora = False
        self.only_one = False
    def Update_table(self):
        self.num_registri = self.frame_setting_register.num_indirizzi.get()
        self.f = 0
        self.only_one = False
        while True:                 
            try: 
                self.frame_setting_register.button_stop.configure(state='normal',background='red')
                self.frame_setting_register.button_update.configure(state='disabled',background='light green')             
                if self.menubar.frame_connect.client.is_open == False:
                    self.menubar.frame_connect.client.open()
                else: 
                    err_msg = self.Leggi_registri(self.num_registri)
                if self.status.get() == 'NON CONNESSO!!':
                    for _ in self.table.get_children():
                        self.table.delete(_)
                        self.only_one = False
                    break      
                if err_msg == 'ok':
                    self.frame_setting_register.button_stop.configure(state='disabled',background='#FFB6C1')
                    self.frame_setting_register.button_update.configure(state='normal',background='green')
                    self.only_one = False  
                    break
                if  self.stop_ora == True:
                    self.frame_setting_register.button_stop.configure(state='disabled',background='#FFB6C1')
                    self.frame_setting_register.button_update.configure(state='normal',background='green')
                    self.stop_ora = False
                    break  
            except Exception as a:
                tk.messagebox.showerror(title='Errore di Connessione', 
                                                        message=f'Questo non deve succedere [{a}]\nErrore di connessione')
                self.only_one = False
                break
            
    def Leggi_registri(self, num_registri):
            self.client = self.menubar.frame_connect.client
            self.reg_iniziale_app = self.frame_setting_register.indirizzo.get()
            self.reg_finale_app = num_registri                                                   
            self.reg_iniziale = int(self.reg_iniziale_app)
            self.reg_finale = int(self.reg_finale_app)
            self.num_registri = self.reg_finale - self.reg_iniziale
            
            #Leggi 01 Coil Status (0x)
            try:                 
                if self.frame_setting_register.register.get() == '01 Coil Status (0x)':  
                    self.frame_setting_register.button_write.configure(state='normal',background='green')
                    self.data = self.client.read_coils(self.reg_iniziale,self.num_registri)
                    if self.only_one == False:       
                        for _ in self.table.get_children():
                            self.table.delete(_)    
                        for reg in range(self.reg_iniziale, self.reg_finale):
                            self.table.insert('','end',values = reg)
                        self.only_one = True   
                    e=-1   
                    for i in self.table.get_children():
                            e=e+1
                            data = str(self.data[e])
                            self.table.set(i,1,'----')
                            self.table.set(i,2,'----')
                            self.table.set(i,3,data)  
                                
                    self.f=self.f+1    
                    self.frame_setting_register.lable_contatore.configure(text = f'N.Letture ---> [{self.f}]')
                time.sleep(2)
            except Exception as r:
                    err_msg = tk.messagebox.showerror(title='Errore_Lettura_Registri', 
                                                        message=f'Questo non deve succedere [{r}]\nRiguarda i parametri per la lettura dei registri')
                    return err_msg
                
            #Leggi 02 Input Status (1x)'
            try:
                if self.frame_setting_register.register.get() == '02 Input Status (1x)':
                    self.frame_setting_register.button_write.configure(state='disabled',background='light green')
                    self.data = self.client.read_discrete_inputs(self.reg_iniziale,self.num_registri)
                    if self.only_one == False:       
                        for _ in self.table.get_children():
                            self.table.delete(_)    
                        for reg in range(self.reg_iniziale, self.reg_finale):
                            self.table.insert('','end',values = reg)
                        self.only_one = True  
                    e=-1    
                    for i in self.table.get_children():
                            e=e+1
                            data = str(self.data[e])
                            self.table.set(i,1,'----')
                            self.table.set(i,2,'----')
                            self.table.set(i,3,data)    
                    self.f=self.f+1    
                    self.frame_setting_register.lable_contatore.configure(text = f'N.Letture ---> [{self.f}]')
                    time.sleep(2)           
            except Exception as r:
                err_msg = tk.messagebox.showerror(title='Errore_Lettura_Registri', 
                                                        message=f'Questo non deve succedere [{r}]\nRiguarda i parametri per la lettura dei registri')
                return err_msg
            
            #Leggi 03 Holding Register (4x)'
            try:
                if self.frame_setting_register.register.get() == '03 Holding Register (4x)':
                    self.frame_setting_register.button_write.configure(state='normal',background='green')
                    self.data = self.client.read_holding_registers(self.reg_iniziale,self.num_registri)
                    if self.only_one == False:       
                        for _ in self.table.get_children():
                            self.table.delete(_)    
                        for reg in range(self.reg_iniziale, self.reg_finale):
                            self.table.insert('','end',values = reg)
                        self.only_one = True  
                    e=-1    
                    
                    for i in self.table.get_children():
                            e=e+1
                            data_hex_list = str((hex(self.data[e]))).upper() 
                            data_hex_list = data_hex_list.replace('X','x')
                            data_binary_list = str(bin(self.data[e]))
                            self.table.set(i,1,str(self.data[e]))
                            self.table.set(i,2,data_hex_list)
                            self.table.set(i,3,data_binary_list[2:])    
                    self.f=self.f+1    
                    self.frame_setting_register.lable_contatore.configure(text = f'N.Letture ---> [{self.f}]')
                    time.sleep(2)           
            except Exception as r:
                err_msg = tk.messagebox.showerror(title='Errore_Lettura_Registri', 
                                                        message=f'Questo non deve succedere [{r}]\nRiguarda i parametri per la lettura dei registri')
                return err_msg
            
            #Leggi 04 Input Register (3x)'
            try:
                if self.frame_setting_register.register.get() == '04 Input Register (3x)':
                    self.frame_setting_register.button_write.configure(state='disabled',background='light green')
                    self.data = self.client.read_input_registers(self.reg_iniziale,self.num_registri)
                    if self.only_one == False:       
                        for _ in self.table.get_children():
                            self.table.delete(_)    
                        for reg in range(self.reg_iniziale, self.reg_finale):
                            self.table.insert('','end',values = reg)
                        self.only_one = True  
                    e=-1    
                    for i in self.table.get_children():
                            e=e+1
                            data_hex_list = str((hex(self.data[e]))).upper() 
                            data_hex_list = data_hex_list.replace('X','x')
                            data_binary_list = str(bin(self.data[e]))
                            self.table.set(i,1,str(self.data[e]))
                            self.table.set(i,2,data_hex_list)
                            self.table.set(i,3,data_binary_list[2:])    
                    self.f=self.f+1    
                    self.frame_setting_register.lable_contatore.configure(text = f'N.Letture ---> [{self.f}]')
                    time.sleep(2)           
            except Exception as r:
                err_msg = tk.messagebox.showerror(title='Errore_Lettura_Registri', 
                                                        message=f'Questo non deve succedere [{r}]\nRiguarda i parametri per la lettura dei registri')
                return err_msg      
                  
    def stop_read(self):
        self.stop_ora = True
        self.only_one = False
        return self.stop_ora       
        
    def write_register_selection(self,indirizzo, valore):
            if self.frame_setting_register.register.get() == '01 Coil Status (0x)':
               self.write_coil(indirizzo, valore) 
            elif self.frame_setting_register.register.get() == '02 Input Status (1x)':    
                pass
            elif self.frame_setting_register.register.get() == '03 Holding Register (4x)':
                self.write_register(indirizzo, valore)
            elif self.frame_setting_register.register.get() == '04 Input Register (3x)':
                pass               
                
                
    def write_coil(self, indirizzo, valore):
        if self.frame_setting_register.register.get() == '01 Coil Status (0x)':
            try:        
                self.menubar.frame_connect.client.write_single_coil(indirizzo,bool(valore))
            except Exception as e :
                tk.messagebox.showerror(title='Errore_Scrittura_Registri', 
                                                            message=f"Questo non deve succedere [{e}]\nImpossibile scrivere il valore nel registro")
                
    def write_register(self, indirizzo, valore):
            try:        
                self.menubar.frame_connect.client.write_single_register(indirizzo,valore)
            except Exception as e :
                tk.messagebox.showerror(title='Errore_Scrittura_Registri', 
                                                            message=f"Questo non deve succedere [{e}]\nImpossibile scrivere il valore nel registro")
            
            
                 
        
        
            
    
    
    
if __name__ == '__main__':
    root = tk.Tk()
    mainwindow = MainWindow(root)
    root.mainloop()