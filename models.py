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

    def get_attr_printable_list(self):
        return [self.id,
        self.timestamp.strftime('%d/%m/%Y %H:%M:%S'),
        self.tempCarc,
        self.velEsteira,
        self.cargaPV,
        self.tensaoRS,
        self.statusPID,
        self.frequencia,
        self.correnteMedia,
        self.potAtivaTotal,
        self.fpTotal,
        self.freqRotacao,
        self.indicaPartida,
        self.torque,
        self.tipoMotor
        ]