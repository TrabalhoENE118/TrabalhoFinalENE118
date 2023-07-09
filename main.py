from kivy.app import App
from mainwidget import MainWidget
from kivy.lang.builder import Builder

class MainApp(App):
    """
    Widdget principal da aplicação
    """
    def build(self):
        """
        Método que gera o aplicativo com o widget principal
        """
        self._widget=MainWidget(scan_time=1000,server_ip='192.168.0.11',server_port=502,
        modbus_addrs={
            'tempCarc':{
                'addr':706, 
                'legenda': 'Temperatura da carcaça(ºC)',
                'tipo':'FP',
                'div':10.0
            },
            'velEsteira':{
                'addr':724, 
                'legenda': 'Velocidade da esteira(m/min)',
                'tipo':'FP',
                'div':1.0
            },
            'cargaPV':{
                'addr':710,
                'legenda': 'Carga sobre a esteira(Kgf/m²)',
                'tipo':'FP',
                'div':1.0

            },
            'tensaoRS':{
                'addr':847,
                'legenda': 'Tensão entre R e S(V)',   
                'tipo':'4X',
                'div':10.0
            },
            'statusPID':{
                'addr':722,
                'legenda': 'Status do PID',
                'tipo':'4X',
                'div':1.0
            },
            'frequencia':{
                'addr':830,
                'legenda': 'Frequência da rede(Hz)',
                'tipo':'4X',
                'div':100.0
            }   ,
            'correnteMedia':{
                'addr':845,
                'legenda': 'Corrente média(A)',
                'tipo':'4X',
                'div':100.0
            },
            'potAtivaTotal':{
                'addr':855,
                'legenda': 'Potência ativa total(W)',
                'tipo':'4X',
                'div':1.0

            },
            'fpTotal':{
                'addr':871,
                'legenda': 'Fator de potência total',
                'tipo':'4X',
                'div':1000.0
            },
            'freqRotacao':{
                'addr':884,
                'legenda': 'Frequência de rotação(Hz)',
                'tipo':'FP',
                'div':1.0
            },
            'indicaPartida':{
                'addr':1216, 
                'legenda': 'Indica partida(0=desligado, 1=ligado)',      
                'tipo':'4X',
                'div':1.0
            },
            'torque':{
                'addr':1420,
                'legenda': 'Torque(N.m)',
                'tipo':'FP',
                'div':100.0
            },
            'tipoMotor':{
                'addr':708,
                'legenda': 'Tipo de motor',
                'tipo':'4X',
                'div':1.0
            }
            
        },
        atuadores={
            'partidaInversor':{
                'addr':1312,
                #Partida do inversor(0=desligado, 1=ligado, 2=reset)
                'tipo':'4X',
                'div':1.0
            },
            'partidaSoftStart':{
                'addr':1316,
                #Partida do soft start(0=desligado, 1=ligado, 2=reset)
                'tipo':'4X',
                'div':1.0
            },
            'partidaDireta':{
                'addr':1319,
                #Partida direta(0=desligado, 1=ligado, 2=reset)
                'tipo':'4X',
                'div':1.0
            },
            'velInversor':{
                'addr':1313,
                #Velocidade do inversor
                'tipo':'4X',
                'div':10.0
            },
            'selPID':{
                'addr':1332,
                #Seleção do PID(0=automático, 1=manual)
                'tipo':'4X',
                'div':1.0
            },
            'selTipoPartida':{
                'addr':1324,
                #Seleção do tipo de partida(3=direta, 1=soft start, 2=inversor)
                'tipo':'4X',
                'div':1.0
            },
            'defineSetPoint':{
                'addr':1302,
                #Define o set point do PID
                'tipo':'FP',
                'div':1.0
            },
            'defineMV':{
                'addr':1310,
                #Define o MV% do PID
                'tipo':'FP',
                'div':1.0
            },
            'defineP':{
                'addr':1304,
                #Define o P do PID
                'tipo':'FP',
                'div':1.0
            },
            'defineI':{
                'addr':1306,
                #Define o I do PID
                'tipo':'FP',
                'div':1.0
            },
            'defineD':{
                'addr':1308,
                #Define o D do PID
                'tipo':'FP',
                'div':1.0
            },
            'defineaccInversor':{
                'addr':1314,
                #Define a aceleração do inversor(10s a 60s)
                'tipo':'4X',
                'div':10.0
            },
            'definedccInversor':{
                'addr':1315,
                #Define a desaceleração do inversor(10s a 60s)
                'tipo':'4X',
                'div':10.0
            },
            'defineaccSoftStart':{
                'addr':1317,
                #Define a aceleração do soft start(10s a 60s)
                'tipo':'4X',
                'div':1.0
            },
            'definedccSoftStart':{
                'addr':1318,
                #Define a desaceleração do soft start(10s a 60s)
                'tipo':'4X',
                'div':1.0
            }

        }
        )
        return self._widget
    def on_stop(self):
        """
        Método chamado quando o programa é fechado
        """
        self._widget.stopRefresh()
        
    
if __name__ == "__main__":
    
    Builder.load_string(open("mainwidget.kv",encoding="utf-8").read(),rulesonly=True)
    Builder.load_string(open("popups.kv",encoding="utf-8").read(),rulesonly=True)
    MainApp().run()

#Dúvidas


# Só escrever quando houver mudança de valor
# Preset de valores iniciais
#consegui fazer

# Dados em tempo real
# Banco de dados
# Arrumei o soft start
