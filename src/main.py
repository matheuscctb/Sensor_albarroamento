import pandas as pd
import time
from src.embarcacao import Embarcacao
from src.sistema import SistemaAntiAbalroamento

def rodar_simulacao(arquivo_csv):
    """
    Orquestra a simulação de um cenário a partir de um arquivo CSV.
    """
    print(f"Iniciando simulação do cenário: {arquivo_csv}")
    
    # 1. Carrega os dados do cenário
    df = pd.read_csv(arquivo_csv)
    
    # 2. Instancia o algoritmo de desvio
    algoritmo = SistemaAntiAbalroamento(cpa_limite_metros=500, tcpa_limite_segundos=300)
    
    # 3. Itera sobre cada momento (timestamp) da simulação
    for t in sorted(df['timestamp'].unique()):
        print(f"\n--- Tempo: {t}s ---")
        
        dados_no_tempo_t = df[df['timestamp'] == t]
        
        # Cria o objeto para a embarcação própria
        dados_propria = dados_no_tempo_t[dados_no_tempo_t['id_embarcacao'] == 'propria'].iloc[0]
        propria = Embarcacao(
            dados_propria['id_embarcacao'], dados_propria['latitude'], 
            dados_propria['longitude'], dados_propria['velocidade_nos'], 
            dados_propria['curso_graus']
        )
        print(f"  > Própria: {propria}")

        # Itera sobre todas as outras embarcações (alvos)
        dados_alvos = dados_no_tempo_t[dados_no_tempo_t['id_embarcacao'] != 'propria']
        for _, dados_alvo in dados_alvos.iterrows():
            alvo = Embarcacao(
                dados_alvo['id_embarcacao'], dados_alvo['latitude'], 
                dados_alvo['longitude'], dados_alvo['velocidade_nos'], 
                dados_alvo['curso_graus']
            )
            print(f"  > Alvo: {alvo}")

            # 4. Executa o algoritmo
            cpa, tcpa, recomendacao = algoritmo.analisar_risco_e_recomendar(propria, alvo)

            # 5. Exibe os resultados
            print(f"    - CPA: {cpa:.2f} m | TCPA: {tcpa:.2f} s")
            print(f"    - Status: {recomendacao}")

        time.sleep(0.1) # Pequena pausa para facilitar a leitura da simulação

if __name__ == "__main__":
    # O arquivo gerado no passo anterior
    caminho_cenario = 'dados_simulados/cenario_rumos_opostos.csv'
    rodar_simulacao(caminho_cenario)