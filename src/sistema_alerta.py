class SistemaAlerta:
    """
    Padrão Observer: Ouve e exibe os alertas gerados pelo sistema para o piloto.
    """
    def __init__(self):
        self.alertas = []

    def notificar(self, mensagem: str):
        """Recebe a notificação (método update do Observer)"""
        alerta = f"[ALERTA DE SISTEMA] {mensagem}"
        self.alertas.append(alerta)
        print(f"\033[91m{alerta}\033[0m")  # Imprime em vermelho para destacar
