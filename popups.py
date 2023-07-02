from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian

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
    def __init__(self,scan_time,**kwargs):
        """
        Construtor da classe ScanPopup
        """
        super().__init__(**kwargs)
        self.ids.txt_st.text = str(scan_time)

class PidPopup(Popup):
    """
    Popup para a configuração do PID
    """
    
    def __init__(self,**kwargs):
        """
        Construtor da classe PidPopup
        """
        super().__init__(**kwargs)
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
        medida['values']['defineSetpoint']=int(self.ids.defineSetpoint.text)
        medida['values']['defineMv']=int(self.ids.defineMV.text)
        medida['values']['defineP']=int(self.ids.defineP.text)
        medida['values']['defineI']=int(self.ids.defineI.text)
        medida['values']['defineD']=int(self.ids.defineD.text)
        
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
    

    def __init__(self,**kwargs):
        """
        Construtor da classe ComandoPopup
        """
        super().__init__(**kwargs)
    def update(self,medida):
        self.ids.definevelInversor.text = str(self.ids.sliderInversor.value)
        aceleracao=int(self.ids.defineaccInversor.text)
        desaceleracao=int(self.ids.definedccInversor.text)
        velInversor=int(self.ids.definevelInversor.text)
        print(f'Velocidade do inversor:{velInversor}')
        if self._partida is not None and self._operacao is not None:
            if self._partida== 'Direta':
                medida['values']['partidaDireta']=self._operacao
            elif self._partida == 'Soft-start':
                medida['values']['partidaSoftStart']=self._operacao
                medida['values']['defineaccSoftStart']=aceleracao
                medida['values']['definedccSoftStart']=desaceleracao
            elif self._partida == 'Inversor':
                medida['values']['partidaInversor']=self._operacao
                medida['values']['defineaccInversor']=aceleracao
                medida['values']['definedccInversor']=desaceleracao
                medida['values']['definevelInversor']=velInversor

    def setPartida(self,partida):
        self._partida=partida
    def setOperacao(self,operacao):
        self._operacao=operacao


class DataGraphPopup(Popup):
    pass
