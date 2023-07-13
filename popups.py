from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian
from kivy_garden.graph import LinePlot
class ModbusPopup(Popup):
    """
    Popup para a configuração do protocolo MODBUS
    """
    _info_lb=None
    def __init__(self,server_ip,server_port,**kwargs):
        """
        Construtor da classe ModbusPopup
        """
        super().__init__(**kwargs)
        self.ids.txt_ip.text = str(server_ip)
        self.ids.txt_port.text = str(server_port)
    def setInfo(self,message):
        self._info_lb=Label(text=message)
        self.ids.layout.add_widget(self._info_lb)
    def clearInfo(self):
        if self._info_lb is not None:
            self.ids.layout.remove_widget(self._info_lb)
    
class ScanPopup(Popup):
    """
    Popup para a configuração do tempo de varredura
    """
    def __init__(self,scantime,**kwargs):
        """
        Construtor da classe ScanPopup
        """
        super().__init__(**kwargs)
        self.ids.txt_st.text = str(scantime)

class PidPopup(Popup):
    """
    Popup para a configuração do PID
    """
    _SP=None
    _MV=None
    _P=None
    _I=None
    _D=None
    def __init__(self,**kwargs):
        """
        Construtor da classe PidPopup
        """
        super().__init__(**kwargs)
        self._MV=0.0
        self._SP=0.0
        self._P=8.0
        self._I=5.0
        self._D=2.0
    def update(self,medida):
        """
        Método utilizado para atualizar os valores do PID
        """
        self.ids.cargaPV.text = str(medida['values']['cargaPV'])
        statusPID=medida['values']['statusPID']
        if statusPID == 0:
            self.ids.statusPID.text = 'Automático'
        elif statusPID == 1:
            self.ids.statusPID.text = 'Manual'
        #Atuadores
        AutomaticoPid=self.ids.AutomaticoOn.active
        if AutomaticoPid:
            medida['values']['selPID']=0
        else:
            medida['values']['selPID']=1
        medida['values']['defineMV']=self._MV
        medida['values']['defineSetPoint']=self._SP
        medida['values']['defineP']=self._P
        medida['values']['defineI']=self._I
        medida['values']['defineD']=self._D
    def setSetPoint(self):
        self._SP= float(self.ids.defineSetPoint.text) 
    def setMV(self):
        self._MV= float(self.ids.defineMV.text)
    def setP(self):
        self._P= float(self.ids.defineP.text)
    def setI(self):
        self._I= float(self.ids.defineI.text)
    def setD(self):
        self._D= float(self.ids.defineD.text)

class MedicoesPopup(Popup):
    """
    Popup para a configuração das medições
    """
    def __init__(self,**kwargs):
        """
        Construtor da classe MedicoesPopup
        """
        super().__init__(**kwargs)
    def update(self,medida):
        """
        Método utilizado para atualizar os valores das medições
        """
        self.ids.correnteMedia.text = str(medida['values']['correnteMedia'])
        self.ids.potAtivaTotal.text = str(medida['values']['potAtivaTotal'])
        self.ids.frequencia.text = str(medida['values']['frequencia'])
        self.ids.fpTotal.text = str(medida['values']['fpTotal'])
        self.ids.tensaoRS.text = str(medida['values']['tensaoRS'])    
class ComandoPopup(Popup):
    """
    Popup para a configuração dos comandos do motor
    """
    _partida=None
    _operacao=None
    _velInversor=None
    _aceleracao=None
    _desaceleracao=None
    def __init__(self,**kwargs):
        """
        Construtor da classe ComandoPopup
        """
        super().__init__(**kwargs)
        self._partida= 'Inversor' #Partida padrão como inversor
        self._operacao= 0 #Operação padrão como parado
        self._velInversor=float(self.ids.velInversor.text)
        self._aceleracao=float(self.ids.defineaccInversor.text)
        self._desaceleracao=float(self.ids.definedccInversor.text)
    def update(self,medida):
        medida['values']['partidaDireta']=None

        medida['values']['partidaSoftStart']=None
        medida['values']['defineaccSoftStart']=None
        medida['values']['definedccSoftStart']=None

        medida['values']['partidaInversor']=None
        medida['values']['defineaccInversor']=None
        medida['values']['definedccInversor']= None
        medida['values']['velInversor']=None

        if self._partida is not None:
            if self._partida== 'Direta':
                medida['values']['partidaDireta']=self._operacao
                medida['values']['selTipoPartida']=3
    

            elif self._partida == 'Soft-Start':
                medida['values']['partidaSoftStart']=self._operacao
                medida['values']['defineaccSoftStart']=self._aceleracao
                medida['values']['definedccSoftStart']=self._desaceleracao
                medida['values']['selTipoPartida']=1

            elif self._partida == 'Inversor':
                medida['values']['partidaInversor']=self._operacao
                medida['values']['defineaccInversor']=self._aceleracao
                medida['values']['definedccInversor']=self._desaceleracao
                medida['values']['velInversor']=self._velInversor
                medida['values']['selTipoPartida']=2



    def setPartida(self,partida):
        self._partida=partida
    def setOperacao(self,operacao):
        self._operacao=operacao
    def setAcc(self):
        self._aceleracao=float(self.ids.defineaccInversor.text)
    def setDcc(self):
        self._desaceleracao=float(self.ids.definedccInversor.text)
    def setVelInversor(self):
        self._velInversor=int(self.ids.velInversor.text)
    def setVelInversorSlider(self,vel):
        self._velInversor=vel
        
class DataGraphPopup(Popup):
    def __init__(self,xmax,plot_color,**kwargs):
        super().__init__(**kwargs)
        self.plot = LinePlot(line_width=1.5)
        self.ids.graph.add_plot(self.plot)
        self.ids.graph.xmax = xmax
class LabeledCheckBoxDataGraph(BoxLayout):
    pass
class SelectDataGraphPopup(Popup):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

class HistGraphPopup(Popup):
    def __init__(self,**kwargs):
        super().__init__()
        for key,value in kwargs.get('tags').items():
            cb = LabeledCheckBoxHistGraph()
            cb.ids.label.text = key
            cb.id= key
            self.ids.sensores.add_widget(cb)
class LabeledCheckBoxHistGraph(BoxLayout):
      pass