from kivy.uix.boxlayout import BoxLayout
from popups import ModbusPopup,ScanPopup,PidPopup,MedicoesPopup,ComandoPopup,DataGraphPopup,SelectDataGraphPopup, HistGraphPopup
from pyModbusTCP.client import ModbusClient
from kivy.core.window import Window
from threading import Thread
from time import sleep
from datetime import datetime
import random
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian
from timeseriesgraph import TimeSeriesGraph
from threading import Lock
from tabulate import tabulate
from db import Base,Session,engine
from models import DadosEsteira
from kivy_garden.graph import LinePlot
class MainWidget(BoxLayout):
    """
    Widdget principal da aplicação
    """
    _tags={'modbusaddrs':{},'atuadores':{}}
    _updateThread = None
    _updateWidgets= True
    _anterior={'inicio':1}
    _max_points=20
    _dados={}
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
        self._scanPopup=ScanPopup(self._scan_time)
        
        self._session=Session()
        Base.metadata.create_all(engine)
        self._lock=Lock()

        self._meas={}
        self._meas['timestamp']= None
        self._meas['values']={}
        for key,value in kwargs.get('modbus_addrs').items():
            plot_color=(random.random(),random.random(),random.random(),1)
            self._tags['modbusaddrs'][key]={'addr':value['addr'],'color':plot_color,'legenda':value['legenda'],'tipo':value['tipo'],'div':value['div'],'escalamax':value['escalamax']}
        
        for key,value in kwargs.get('atuadores').items():
            self._tags['atuadores'][key]={'addr':value['addr'],'tipo':value['tipo'],'div':value['div']}


        self._pidPopup=PidPopup()
        self._medicoesPopup=MedicoesPopup()
        self._comandoPopup=ComandoPopup()
        self._selection='potAtivaTotal'
        self._selectData= SelectDataGraphPopup()

        for key,value in self._tags['modbusaddrs'].items():
            if self._selection == key:
                self._graph=DataGraphPopup(self._max_points,self._tags['modbusaddrs'][key]['color'])
        
        self._hgraph= HistGraphPopup(tags=self._tags['modbusaddrs'])

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
                self._dataBankThread = Thread(target=self.updateDataBank)
                self._updateThread.start()
                self._dataBankThread.start()
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
                self.updateDataBank()
                #Atualiza o banco de dados
                sleep(self._scan_time/1000)
        except Exception as e:
            self._modbusClient.close()
            print("Erro:",e.args)

    def updateDataBank(self):
        """
        Método para a inserção dos dados no Banco de dados
        """
        try:
            self._dados['timestamp']=self._meas['timestamp']
            for key in self._tags['modbusaddrs']:
                self._dados[key]=self._meas['values'][key]
            dado=DadosEsteira(**self._dados)
            self._lock.acquire()
            self._session.add(dado)
            self._session.commit()
            self._lock.release()
        except Exception as e:
            print("Erro na atualização do banco:",e.args)
    def getDataDB(self):
        """
        Método que coleta as informações da interface pelo usuário
        e requisita a busca no Banco de dados
        """
        try:
            init_t=self._hgraph.ids.txt_init_time.text
            final_t=self._hgraph.ids.txt_final_time.text
            init_t=datetime.strptime(init_t,'%d/%m/%Y %H:%M:%S')
            final_t=datetime.strptime(final_t,'%d/%m/%Y %H:%M:%S')
                
            if init_t is None or final_t is None:
                return
            self._lock.acquire()
            results=self._session.query(DadosEsteira).filter(DadosEsteira.timestamp.between(init_t,final_t)).all()
            self._lock.release()
            results = [reg.get_resultsdic() for reg in results]
            sensorAtivo=[]
            for sensor in self._hgraph.ids.sensores.children:
                if sensor.ids.checkbox.active:
                    sensorAtivo.append(sensor.ids.label.text)
            if results is None or len(results)==0:
                return
            self._hgraph.ids.graph.clearPlots()
            tempo=[]
            for i in results:
                for key,value in i.items():
                    if key=='timestamp':
                        tempo.append(value)
                        continue
                    elif key=='id':
                        continue
                    for s in sensorAtivo:
                        if key==s:
                            p= LinePlot(line_width=1)
                            p.points = [(x, results[x][key]) for x in range(0,len(results))]
                            self._hgraph.ids.graph.add_plot(p)
                            self._hgraph.ids.graph.ymax=self._tags['modbusaddrs'][s]['escalamax']
                            self._hgraph.ids.graph.y_ticks_major=self._tags['modbusaddrs'][s]['escalamax']/5
                            self._hgraph.ids.graph.ylabel= self._tags['modbusaddrs'][s]['legenda']
            self._hgraph.ids.graph.xmax=len(results)
            self._hgraph.ids.update_x_labels(tempo)
            

        except Exception as e:
            print("Erro na busca no banco:",e.args)

    def readData(self):
        """
        Método para a leitura dos dados por meio do protocolo MODBUS
        """
        self._meas['timestamp']=datetime.now() 
        
        print("------------------------")
        for key,value in self._tags['modbusaddrs'].items():
            if value['tipo']=='4X': #Holding Register 16bits
                self._meas['values'][key]=(self._modbusClient.read_holding_registers(value['addr'],1)[0])/value['div']      
        
            elif value['tipo']=='FP': #Floating Point
                self._meas['values'][key]=(self.lerFloat(value['addr']))/value['div']

    def writeData(self,addr,tipo,div,value):
        """
        Método para a escrita de dados por meio do protocolo MODBUS
        """
        
        if tipo=='4X':
            self._modbusClient.write_single_register(addr,int(value*div))
        elif tipo=='FP':
            self.escreveFloat(addr,value*div)
    def updateGUI(self):
        '''
        Método para a atualização da interface gráfica
        '''
        self.ids['tempCarc'].text=str(self._meas['values']['tempCarc'])+' ºC'
        self.ids['velEsteira'].text=str(round(self._meas['values']['velEsteira'],2))+' m/min'
        self.ids['cargaPV'].text=str(round(self._meas['values']['cargaPV'],2))+' kgf/cm²'
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
            self.ids['btnComando'].background_color=(0,1,0,1)
        elif tipoMotor==2:
            self.ids['btnComando'].background_color=(0,0,1,1)
        self._pidPopup.update(self._meas)
        self._medicoesPopup.update(self._meas)
        self._comandoPopup.update(self._meas)

        self.updateAtuadores()
        self.updateGraph() 
        
    def updateAtuadores(self):
        '''
        Método para a atualização dos atuadores
        '''
        #Atuadores no formato(addr,tipo,div,value)
        print("------------------------")
        print("Atuadores:")
        if self._anterior['inicio']==1:
            print("Configuração inicial")
            for key,value in self._tags['atuadores'].items():
                print(f'{key}={self._meas["values"][key]}')
                if self._meas['values'][key]!=None: #Configuração inicial
                    self.writeData(value['addr'],value['tipo'],value['div'],self._meas['values'][key])
                self._anterior[key]=self._meas['values'][key]
                self._anterior['inicio']=0
        else:
            for key,value in self._tags['atuadores'].items():
                print(f'{key}={self._meas["values"][key]} {self._anterior[key]}')
                if self._meas['values'][key]!=None and self._meas['values'][key]!=self._anterior[key]:
                    print(f'{key}={self._meas["values"][key]}')
                    self.writeData(value['addr'],value['tipo'],value['div'],self._meas['values'][key])
                    self._anterior[key]=self._meas['values'][key]
    def updateGraph(self):
        '''
        Método para a atualização do gráfico
        '''
        self._graph.ids.graph.updateGraph((self._meas['timestamp'],self._meas['values'][self._selection]),0)
        self._graph.ids.graph.ylabel= self._tags['modbusaddrs'][self._selection]['legenda']
        self._graph.ids.graph.ymax=self._tags['modbusaddrs'][self._selection]['escalamax']
        self._graph.ids.graph.y_ticks_major=self._tags['modbusaddrs'][self._selection]['escalamax']/5
    def stopRefresh(self): 
        """
        Método para a parada da atualização da interface gráfica
        """
        self._updateWidgets=False

    def lerFloat(self,addr):
        """
        Método para a leitura de um "float" na tabela MODBUS
        """
        result = self._modbusClient.read_holding_registers(addr,2)
        decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.Big, wordorder=Endian.Little)
        decoded = decoder.decode_32bit_float()
        return decoded
    def escreveFloat(self,addr,float):
        """
        Método para a escrita de um "float" na tabela MODBUS
        """
        builder = BinaryPayloadBuilder()
        builder.add_32bit_float(float)
        payload = builder.to_registers()
        return self._modbusClient.write_multiple_registers(addr,payload)
            
        