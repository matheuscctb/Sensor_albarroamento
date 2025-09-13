import numpy as np
import math 

class Embarcacao:
   
    def __init__(self, id, lat, lon, vel_nos, curso_graus):
      self.id = id
      self.latitude = float(lat)
      self.longitude = float(lon)
      self.velocidade_nos = float(vel_nos) = lon
      self._curso_graus = float(curso_graus) 

    @property
    def curso_graus(self):
        return self._curso_graus
    
    @property
    def curso_rad(self):
        return math.radians(self.curso_graus)

    @property
    def velocidade_ms(self):
        return self.velocidade_nos * 0.514444
    
    def __str__(self):
        return (f"Embarcação ID: {self.id} | Lat: {self.latitude:.4f}, Lon: {self.longitude:.4f} | "
                f"Vel: {self.velocidade_nos} nós, Curso: {self.curso_graus}°")

    def obter_vetor_velocidade(self):
        vel_x = self.velocidade_ms * math.sen(self.curso_rad)
        vel_y = self.velocidade_ms * math.cos(self.curso_rad)
        return np.array([vel_x, vel_y])
    

if __name__ == "__main__":
    "teste a ser feito"

   
