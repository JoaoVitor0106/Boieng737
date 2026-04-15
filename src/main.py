import time
from sensor_aoa import SensorAOA
from mcas import MCAS
from validador_sensores import ValidadorDeSensores

def simular_cenario(nome_cenario: str, leituras_s1: list, leituras_s2: list):
    print(f"\n{'-'*60}")
    print(f" SIMULANDO CENÁRIO: {nome_cenario}")
    print(f"{'-'*60}")
    
    # Instanciando Componentes da Arquitetura
    sensor1 = SensorAOA(id_sensor=1)
    sensor2 = SensorAOA(id_sensor=2)
    
    mcas = MCAS()
    mcas.resetar() # Reinicia estado para o cenário simulado
    
    validador = ValidadorDeSensores(sensor1, sensor2, mcas)
    
    # Loop de Leituras Simuladas
    for instante, (v1, v2) in enumerate(zip(leituras_s1, leituras_s2)):
        print(f"\n>>> Tempo T+{instante} segundos")
        sensor1.simular_leitura(base_angulo=v1, ruido=0.1)
        sensor2.simular_leitura(base_angulo=v2, ruido=0.1)
        
        validador.validar_e_processar()
        
        # Pausa leve para acompanhar simulação pelo terminal
        time.sleep(0.5)

if __name__ == "__main__":
    print("="*60)
    print("  SIMULADOR DO NOVO SISTEMA ARQUITETURAL - BOEING 737 MCAS")
    print("="*60)
    
    # Cenário 1: Voo Equilibrado
    # Ângulo normal, sensores emitindo informações similares.
    simular_cenario(
        nome_cenario="1. VOO NORMAL E EQUILIBRADO", 
        leituras_s1=[4.0, 4.2, 4.5, 4.1],
        leituras_s2=[4.1, 4.0, 4.4, 4.2]
    )
                    
    # Cenário 2: Risco Iminente
    # O ângulo do avião começa a subir muito (Stall). Ambos os sensores leem a subida.
    simular_cenario(
        nome_cenario="2. ÂNGULO CRÍTICO (STALL REAL DETECTADO)",
        leituras_s1=[8.0, 11.5, 13.5, 15.0],
        leituras_s2=[7.8, 11.8, 13.2, 14.8]
    )
                    
    # Cenário 3: O Ponto Único de Falha evitado
    # Sensor 1 estragou e relata subida absurda. Sensor 2 afirma voo normal.
    # O Sistema Validador deve notar a falha e desarmar o MCAS.
    simular_cenario(
        nome_cenario="3. FALHA NO SENSOR 1 (PREVENÇÃO DE ACIDENTE / FAIL-SAFE)",
        leituras_s1=[4.0, 5.0, 16.0, 19.0], # Falha abruta no sensor 1 a partir do T+2
        leituras_s2=[4.1, 4.9, 5.2, 5.0]  # Sensor 2 relata voo normal
    )
    
    print("\n")
    print("="*60)
    print("  FIM DA SIMULAÇÃO")
    print("="*60)
