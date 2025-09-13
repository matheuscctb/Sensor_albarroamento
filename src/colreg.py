import math

class COLREG72:
    """
    Encapsula a lógica para determinar a regra aplicável do COLREG-72
    em uma situação de encontro entre duas embarcações à vista uma da outra.
    """
    def determinar_situacao_e_acao(self, propria, alvo, marcacao_relativa_deg):
        """
        Analisa a situação e retorna uma string com a recomendação.
        As regras são verificadas em ordem de precedência: Ultrapassagem (13),
        depois Rumos Opostos (14) e, por fim, Rumos Cruzados (15).
        """
        # =======================================================================
        # REGRA 13: ULTRAPASSAGEM (Overtaking)
        # Esta regra tem precedência sobre todas as outras (14, 15).
        # Uma embarcação está ultrapassando se ela se aproxima de outra vinda
        # de uma direção de mais de 22.5 graus para ré do través desta última.
        # Na prática, se o alvo está no nosso setor de popa (traseiro).
        # O setor de popa é definido entre 112.5° e 247.5° (360 - 112.5).
        # =======================================================================
        if 112.5 < marcacao_relativa_deg < 247.5:
            # Neste caso, NÓS estamos sendo ultrapassados pelo alvo.
            # A Regra 17 diz que devemos manter nosso rumo e velocidade.
            return (f"[INFO] Situação: Sendo Ultrapassado (Regra 13). "
                    f"Você tem preferência. Mantenha rumo e velocidade (Regra 17).")
        
        # NOTA: A situação inversa (nós ultrapassando o alvo) é mais complexa de
        # determinar apenas com estes dados, mas a lógica fundamental é que
        # a embarcação que ultrapassa é sempre a que manobra.

        # =======================================================================
        # REGRA 14: SITUAÇÃO DE RUMOS OPOSTOS (Head-on)
        # Quando duas embarcações se aproximam em rumos diretamente opostos
        # ou quase opostos, de maneira que envolva risco de colisão.
        # =======================================================================
        diferenca_curso_deg = abs(propria.curso_graus - alvo.curso_graus)
        # Verificamos se a diferença de cursos está próxima de 180 graus.
        if 170 < diferenca_curso_deg < 190: # Usando uma janela mais restrita
            return (f"[ALERTA MÁXIMO] Risco: Rumos Opostos (Regra 14). "
                    f"Ambas as embarcações devem guinar para ESTIBORDO (DIREITA).")

        # =======================================================================
        # REGRA 15: SITUAÇÃO DE RUMOS CRUZADOS (Crossing)
        # Quando duas embarcações se cruzam em rumos que não sejam nem
        # opostos nem de ultrapassagem.
        # =======================================================================
        # CASO 1: O alvo está a nosso ESTIBORDO (lado direito).
        # O setor de estibordo vai da proa (0°) até o través (90-112.5°).
        if 5 < marcacao_relativa_deg <= 112.5:
            # Nós somos a embarcação "give-way" (que cede passagem).
            # A Regra 16 (Ação da embarcação que manobra) exige ação clara e antecipada.
            return (f"[ALERTA] Risco: Rumos Cruzados (Regra 15). "
                    f"Alvo por estibordo. Você deve ceder passagem. "
                    f"Ação evasiva substancial para ESTIBORDO é recomendada (Regra 16).")
        
        # CASO 2: O alvo está a nosso BOMBORDO (lado esquerdo).
        # O setor de bombordo vai da proa (360°) até o través esquerdo (247.5°).
        if 247.5 <= marcacao_relativa_deg < 355:
            # Nós somos a embarcação "stand-on" (que tem preferência).
            # Aplicamos a Regra 17.
            return (f"[INFO] Situação: Rumos Cruzados (Regra 15). "
                    f"Alvo por bombordo. Você tem preferência. "
                    f"Mantenha rumo e velocidade e monitore a manobra do alvo (Regra 17).")

        # =======================================================================
        # Nenhuma regra específica de encontro se aplica, mas o risco de CPA/TCPA
        # foi identificado pelo sistema. Isso pode ocorrer em situações complexas.
        # A Regra 8 (Ação para Evitar Colisão) se aplica de forma geral.
        # =======================================================================
        return (f"[ALERTA] Risco de colisão detectado! "
                f"Nenhuma regra de encontro clara se aplica. "
                f"Avalie e manobre com extrema cautela (Regra 8).")

if __name__ == "__main__":
    "teste a ser feito"