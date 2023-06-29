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
        self._widget=MainWidget(scantime=1000,server_ip='localhost',server_port=502,
        modbus_addrs={
            'tempCarc':{
                'addr':706, 
                #Temperatura da carcaça
                'tipo':'FP',
                'div':10.0
            },
            'velEsteira':{
                'addr':724, 
                #Velocidade da esteira
                'tipo':'FP',
                'div':1.0
            },
            'cargaPV':{
                'addr':710,
                #Valor lido da carga na esteira(PV) 
                'tipo':'FP',
                'div':1.0

            },
            'tensaoRS':{
                'addr':847,
                #Valor de ddp entre R e S   
                'tipo':'4X',
                'div':10.0
            },
            'statusPID':{
                'addr':722,
                #Status do PID     
                'tipo':'4X',
                'div':1.0
            },
            'frequencia':{
                'addr':830,
                #Frequência da rede
                'tipo':'4X',
                'div':100.0
            }   ,
            'correnteMedia':{
                'addr':845,
                #Corrente média     
                'tipo':'4X',
                'div':100.0
            },
            'potAtivaTotal':{
                'addr':855,
                #Potência ativa total
                'tipo':'4X',
                'div':1.0

            },
            'fpTotal':{
                'addr':871,
                #Fator de potência total
                'tipo':'4X',
                'div':1000.0
            },
            'freqRotacao':{
                'addr':884,
                #Frequência de rotação
                'tipo':'FP',
                'div':1.0
            },
            'indicaPartida':{
                'addr':1216, 
                #Indica a partida selecionada(Direta=0, Soft Start=1, Inversor=2)         
                'tipo':'4X',
                'div':1.0
            },
            'torque':{
                'addr':1420,
                #Torque
                'tipo':'FP',
                'div':100.0
            }
            
        },
        atuadores={

        }
        )
        return self._widget
    
if __name__ == "__main__":
    
    Builder.load_string(open("mainwidget.kv",encoding="utf-8").read(),rulesonly=True)
    Builder.load_string(open("popups.kv",encoding="utf-8").read(),rulesonly=True)
    MainApp().run()

#ERROS ENCONTRADOS
#2) Carga sobre a esteira PV não muda nem no supervisório da bancada