from db import Base
from sqlalchemy import Column, Integer, DateTime, Float

class DadosEsteira(Base):
    """
    Modelo dos dados
    """
    __tablename__ = 'dadosesteira'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    tempCarc = Column(Float)
    velEsteira = Column(Float)
    cargaPV = Column(Float)
    tensaoRS = Column(Integer)
    statusPID = Column(Integer)
    frequencia=Column(Integer)
    correnteMedia = Column(Integer)
    potAtivaTotal = Column(Integer)
    fpTotal = Column(Integer)
    freqRotacao = Column(Float)
    indicaPartida = Column(Integer)
    torque = Column(Float)
    tipoMotor = Column(Integer)

    def get_resultsdic(self):
        return {'id':self.id,
        'timestamp':self.timestamp.strftime('%d/%m/%Y %H:%M:%S'),
        'tempCarc':self.tempCarc,
        'velEsteira':self.velEsteira,
        'cargaPV':self.cargaPV,
        'tensaoRS':self.tensaoRS,
        'statusPID':self.statusPID,
        'frequencia':self.frequencia,
        'correnteMedia':self.correnteMedia,
        'potAtivaTotal':self.potAtivaTotal,
        'fpTotal':self.fpTotal,
        'freqRotacao':self.freqRotacao,
        'indicaPartida':self.indicaPartida,
        'torque':self.torque,
        'tipoMotor':self.tipoMotor
        }