import random

class SensorAOA:
    """
    Representa o sensor físico de Ângulo de Ataque (AoA).
    """
    def __init__(self, id_sensor: int):
        self.id_sensor = id_sensor
        self.angulo_atual = 0.0

    def ler_angulo(self) -> float:
        """Retorna a leitura atual do sensor em graus."""
        return self.angulo_atual

    def simular_leitura(self, base_angulo: float, ruido: float = 0.5):
        """Metódo auxiliar para simular uma leitura com pequeno ruído (dados mockados)"""
        self.angulo_atual = base_angulo + random.uniform(-ruido, ruido)
