# Sistema MCAS (Boeing 737 MAX) - Proposta de Arquitetura de Software

Este repositório contém uma **implementação simulada** da proposta de solução arquitetural (N-Tier) para corrigir as falhas presentes no software do sistema MCAS do Boeing 737 MAX 8.

Este projeto faz parte do trabalho da disciplina de **Arquitetura de Software**.

## 📌 Escopo do Repositório

O repositório está focado na validação do conceito e contém:
- **Código-fonte em Python** estruturado segundo as boas práticas de Design Patterns;
- **Dados mockados e inputs simulados**, focados em demonstrar a inteligência do sistema baseada na arquitetura proposta.

## 🏗️ Arquitetura Proposta

A simulação adota a abordagem **N-Tier**, organizando responsabilidades em camadas distintas e utilizando padrões de projeto cruciais.

### Componentes e Responsabilidades:

1. **Camada Física (Sensores AOA):** `sensor_aoa.py`
   - O avião original possuía apenas um sensor avaliado pelo sistema por vez. Na nova proposta, foram implementados **DOIS sensores físicos de Ângulo de Ataque** para fornecer redundância de entrada e resolver o Ponto Único de Falha (*Single Point of Failure*).
   
2. **Camada de Validação (Fail-Safe):** `validador_sensores.py`
   - Um novo módulo que faz a checagem dupla das informações antes de autorizar a atuação autônoma da aeronave. 
   - Ao receber leituras fora da tolerância entre os dois sensores, a diferença obriga o sistema a entrar em estado de Fail-Safe (Desativação + Alerta aos pilotos).

3. **Camada de Aplicação (MCAS Central):** `mcas.py`
   - Padronizado com **Singleton** para existir apenas uma instância de controle (evitando concorrência nos atuadores).
   - Somente atrilado a correções se os dados forem criticamente verificados na etapa anterior. Há um limite numérico estrito sobre quanto ele pode ajustar o nariz sem intervenção humana.

4. **Camada de Apresentação (Interface com Piloto):** `sistema_alerta.py`
   - Usa o padrão **Observer** para notificar automaticamente a tripulação no momento em que alguma inconsistência é detectada, o que garante a consciência situacional que faltou nos trágicos acidentes.

## 🚀 Como Executar a Simulação

### Requisitos
- Você precisará ter o **Python 3.x** instalado.

### Passos

1. Faça um `git clone` deste repositório na sua máquina (ou baixe via ZIP).
2. Pelo terminal ou prompt de comando (`cmd`/`powershell`/`bash`), navegue até o diretório raiz do projeto.
3. Para executar o simulador com cenários pré-definidos, execute:

```bash
python src/main.py
```

### O que acontece na simulação?

Ao rodar o `main.py`, o script irá demonstrar **3 cenários consecutivos** diretamente no console:
- **Cenário 1:** O avião voa sob condições normais de estabilidade. Os sensores atestam a regularidade. Nenhuma correção agressiva do MCAS.
- **Cenário 2 (Real Stand):** Uma turbulência repentina ou ação faz ambos os sensores detectarem uma inclinação perigosa (Stall). O Validador atesta veracidade, e o MCAS aciona o reajuste do estabilizador vertical.
- **Cenário 3 (Simulação do Incidente e Correção Algorítmica):** Um dos sensores apresenta mau funcionamento (lendo > 18 graus sem sentido). Graças às novas camadas implementadas, o **Validador de Sensores** constata a falha na leitura cruzada (*Cross-Check*), aciona o componente de alerta aos pilotos e desabilita o sistema para prevenir a queda dramática do avião.
