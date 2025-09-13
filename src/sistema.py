import numpy as np

class SistemaAntiAbalroamento:
    """
    Contém a lógica para calcular riscos de abalroamento e sugerir manobras.
    """
    def __init__(self, cpa_limite_metros=500, tcpa_limite_segundos=300):
        """
        Inicializa o sistema com os limiares de segurança.
        """
        self.CPA_LIMITE_METROS = cpa_limite_metros
        self.TCPA_LIMITE_SEGUNDOS = tcpa_limite_segundos

    def calcular_cpa_tcpa(self, embarcacao_propria, embarcacao_alvo):
        """
        Calcula o CPA e o TCPA entre duas embarcações.
        """
        # Posição relativa em metros (aproximação para pequenas distâncias)
        # Eixo X (Leste), Eixo Y (Norte)
        delta_lon = embarcacao_alvo.longitude - embarcacao_propria.longitude
        delta_lat = embarcacao_alvo.latitude - embarcacao_propria.latitude
        
        # Converte graus de longitude para metros
        fator_lon = np.cos(np.radians(embarcacao_propria.latitude))
        pos_relativa_metros = np.array([
            delta_lon * 111320 * fator_lon,
            delta_lat * 111132
        ])

        # Velocidade relativa
        vel_propria_vetor = embarcacao_propria.obter_vetor_velocidade()
        vel_alvo_vetor = embarcacao_alvo.obter_vetor_velocidade()
        vel_relativa = vel_alvo_vetor - vel_propria_vetor

        # Cálculo do TCPA
        norma_vel_rel_sq = np.dot(vel_relativa, vel_relativa)
        if norma_vel_rel_sq == 0: # Embarcações com a mesma velocidade e curso
            return np.linalg.norm(pos_relativa_metros), float('inf')

        tcpa = -np.dot(pos_relativa_metros, vel_relativa) / norma_vel_rel_sq

        # Cálculo do CPA
        posicao_cpa = pos_relativa_metros + vel_relativa * tcpa
        distancia_cpa = np.linalg.norm(posicao_cpa)

        return distancia_cpa, tcpa

    def analisar_risco_e_recomendar(self, propria, alvo):
        """
        Analisa o risco de colisão e recomenda uma manobra baseada no COLREG-72.
        """
        distancia_cpa, tcpa = self.calcular_cpa_tcpa(propria, alvo)

        # Consideramos risco apenas se a aproximação ocorrer no futuro
        if tcpa < 0:
            return distancia_cpa, tcpa, "Passagem segura. Alvo se afastando."

        # Verifica se os valores de CPA e TCPA estão abaixo dos limiares
        if distancia_cpa < self.CPA_LIMITE_METROS and tcpa < self.TCPA_LIMITE_SEGUNDOS:
            # Lógica de recomendação baseada nas regras do COLREG-72 [cite: 47]
            diferenca_curso_deg = abs(propria.curso_graus - alvo.curso_graus)

            # Regra 14: Situação de Rumos Opostos
            if 165 < abs(diferenca_curso_deg) < 195:
                return distancia_cpa, tcpa, "[ALERTA] Risco de colisão! Situação de rumos opostos. GUINAR PARA ESTIBORDO."
            
            # Adicionar outras regras aqui (ex: rumos cruzados, ultrapassagem)
            
            # Alerta genérico se nenhuma regra específica for atendida
            return distancia_cpa, tcpa, "[ALERTA] Risco de colisão! Avalie a situação e manobre."

        return distancia_cpa, tcpa, "Navegação segura. Monitorando."