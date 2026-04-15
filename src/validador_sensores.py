from sensor_aoa import SensorAOA
from mcas import MCAS

class ValidadorDeSensores:
    """
    Camada de verificação: O filtro que compara os dados de ambos os sensores
    antes de autorizar processamentos críticos. (Fail-Safe)
    """
    def __init__(self, sensor1: SensorAOA, sensor2: SensorAOA, mcas: MCAS):
        self.sensor1 = sensor1
        self.sensor2 = sensor2
        self.mcas = mcas
        self.tolerancia = 5.0 # Divergência máxima tolerada em graus (mockado)

    def validar_e_processar(self):
        leitura1 = self.sensor1.ler_angulo()
        leitura2 = self.sensor2.ler_angulo()
        
        diferenca = abs(leitura1 - leitura2)
        print(f"[Validador] Sensor 1 (AOA): {leitura1:.2f}° | Sensor 2 (AOA): {leitura2:.2f}° | Diferença: {diferenca:.2f}°")
        
        if diferenca > self.tolerancia:
            # Requisito RNF01 e RNF03: Evitar Single Point of Failure e Acionar Fail-Safe
            self.mcas.desativar_sistema("Divergência Crítica entre os dois sensores de Ângulo.")
        else:
            # Requisito RF01: Validação cruzada bem-sucedida, seguir com leitura media.
            angulo_consolidado = (leitura1 + leitura2) / 2
            print(f"[Validador] Leituras validadas cruzadamente (Consolidado: {angulo_consolidado:.2f}°)")
            self.mcas.processar_correcao(angulo_consolidado)
