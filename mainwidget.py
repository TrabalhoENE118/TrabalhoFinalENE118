from kivy.uix.boxlayout import BoxLayout
from popups import ModbusPopup,ScanPopup,PidPopup,MedicoesPopup
from pyModbusTCP.client import ModbusClient
from kivy.core.window import Window
from threading import Thread
from time import sleep
from datetime import datetime
import random
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian


class MainWidget(BoxLayout):
    """
    Widdget principal da aplicação
    """
    _tags={}
    _updateThread = None
    _updateWidgets= True
    def __init__(self,**kwargs):
        """
        Construtor do widget principal
        """
        super().__init__()
        self._scan_time=kwargs.get('scan_time')
        self._server_ip=kwargs.get('server_ip')
        self._server_port=kwargs.get('server_port')
        self._modbusClient=ModbusClient(host=self._server_ip,port=self._server_port)
        self._modbusPopup=ModbusPopup(server_ip=self._server_ip,server_port=self._server_port)
        self._scanPopup=ScanPopup(scan_time=self._scan_time)
        
        self._meas={}
        self._meas['timestamp']= None
        self._meas['values']={}
        for key,value in kwargs.get('modbus_addrs').items():
            plot_color=(random.random(),random.random(),random.random(),1)
            self._tags[key]={'addr':value['addr'],'color':plot_color,'tipo':value['tipo'],'div':value['div']}
        
        for key,value in kwargs.get('atuadores').items():
            self._tags[key]={'addr':value['addr'],'tipo':value['tipo'],'div':value['div']}


        self._pidPopup=PidPopup()
        self._medicoesPopup=MedicoesPopup()
        
    def startDataRead(self,ip,port):
        """
        Método utilizado para a configuração do IP e porta 
        Inicializar uma thread para a leiura dos dados e atualização da interface gráfica
        """
    
        self._server_ip=ip
        self._server_port=port
        self._modbusClient.host=self._server_ip
        self._modbusClient.port=self._server_port
        try:
            Window.set_system_cursor('wait')
            self._modbusClient.open()
            Window.set_system_cursor('arrow')
            if self._modbusClient.is_open:
                self._updateThread = Thread(target=self.updater)
                self._updateThread.start()
                self.ids.img_con.source= 'imgs/conectado.png'
                self._modbusPopup.dismiss()
             
            else:
                self._modbusPopup.setInfo('Erro na conexão com o servidor')
        except Exception as e:
            print("Erro:",e.args)
    
    def updater(self):
        """
        Método que invoca as rotinas de leitura de dados, atualização da interface e inserção dos dados no Banco de dados
        """
        try:
            while self._updateWidgets:
                self.readData()
                self.updateGUI()
                #Atualiza o banco de dados
                sleep(self._scan_time/1000)
        except Exception as e:
            self._modbusClient.close()
            print("Erro:",e.args)

                
    def readData(self):
        """
        Método para a leitura dos dados por meio do protocolo MODBUS
        """
        self._meas['timestamp']=datetime.now() 
        print("------------------------")
        for key,value in self._tags.items():
            if value['tipo']=='4X': #Holding Register 16bits
                self._meas['values'][key]=(self._modbusClient.read_holding_registers(value['addr'],1)[0])/value['div']
                print(f'{key}={self._meas["values"][key]}')
            elif value['tipo']=='FP': #Floating Point
                self._meas['values'][key]=(self.lerFloat(value['addr']))/value['div']
                print(f'{key}={self._meas["values"][key]}')
    def updateGUI(self):
        '''
        Método para a atualização da interface gráfica
        '''
        self.ids['tempCarc'].text=str(self._meas['values']['tempCarc'])+' ºC'
        self.ids['velEsteira'].text=str(round(self._meas['values']['velEsteira'],2))+' m/min'
        self.ids['cargaPV'].text=str(self._meas['values']['cargaPV'])+' kgf/cm²'
        self.ids['freqRotacao'].text=str(self._meas['values']['freqRotacao'])+' RPM'
        partida=self._meas['values']['indicaPartida']
        if partida==3:
            self.ids['indicaPartida'].text='Direta'
        elif partida==1:
            self.ids['indicaPartida'].text='Soft-Start'
        elif partida==2:
            self.ids['indicaPartida'].text='Inversor'
        self.ids['torque'].text=str(self._meas['values']['torque'])+' N.m'
        tipoMotor=self._meas['values']['tipoMotor']
        if tipoMotor==1:
            self.ids['tipoMotor'].source='imgs/verde.png'
        elif tipoMotor==2:
            self.ids['tipoMotor'].source='imgs/azul.png'
        self._pidPopup.update(self._meas)
        self._medicoesPopup.update(self._meas)

    def lerFloat(self,addr):
        """
        Método para a leitura de um "float" na tabela MODBUS
        """
        result = self._modbusClient.read_holding_registers(addr,2)
        decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.Big, wordorder=Endian.Little)
        decoded = decoder.decode_32bit_float()
        return decoded
            
        