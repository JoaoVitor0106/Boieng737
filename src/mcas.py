from sistema_alerta import SistemaAlerta

class MCAS:
    """
    Padrão Singleton: Garante que exista apenas uma instância do controle do estabilizador.
    Controla o estabilizador para ajustar o nariz do avião caso o ângulo de ataque seja crítico.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MCAS, cls).__new__(cls)
            cls._instance.ativo = True
            cls._instance.limite_ajuste = 2.5 # Limite máximo de atuação mecânica
            cls._instance.ajuste_atual = 0.0
            cls._instance.sistema_alerta = SistemaAlerta()
        return cls._instance

    def processar_correcao(self, angulo_validado: float):
        """Atua no estabilizador caso o ângulo seja perigoso e as leituras sejam válidas"""
        if not self.ativo:
            return

        limite_perigo = 12.0 # Ângulo considerado perigoso (Stall iminente)
        
        if angulo_validado > limite_perigo:
            # Necessário forçar inclinação do nariz para baixo
            ajuste_necessario = (angulo_validado - limite_perigo) * 0.5
            ajuste_aplicado = min(ajuste_necessario, self.limite_ajuste)
            self.ajuste_atual -= ajuste_aplicado
            
            print(f"[MCAS] Atuando no estabilizador. Corrigindo o nariz do avião em {self.ajuste_atual:.2f} graus.")
        else:
            print("[MCAS] Ângulo de ataque aceitável. Nenhuma atuação necessária.")

    def desativar_sistema(self, motivo: str):
        """Desativa o sistema em caso de ativação do Fail-Safe"""
        if self.ativo:
            self.ativo = False
            self.sistema_alerta.notificar(f"MCAS DESATIVADO. Motivo: {motivo}. Assuma o controle manual.")

    def resetar(self):
        """Método auxiliar para resetar o singleton no meio das simulações"""
        self.ativo = True
        self.ajuste_atual = 0.0
