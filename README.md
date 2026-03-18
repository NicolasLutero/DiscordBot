# ☕ NPC Bartender Bot (Discord)

Sistema de narrativa interativa para Discord baseado em **máquina de estados + eventos (symbols)**.  
O jogador interage com uma NPC (Liu) em uma cafeteria, escolhendo ações via comandos.

---

## 📌 Visão Geral

O projeto implementa um motor genérico que permite:

- Interações narrativas dinâmicas
- Estados contextuais por jogador
- Ações disponíveis baseadas no contexto atual
- Modularização por domínio (café, doces, conversa, etc.)

Arquitetura base:
```
Discord → Symbol → Machine → State → Handler → Response
````

---

## 🧠 Conceitos Principais

### Machine
Orquestra o sistema:
- Mantém estados
- Decide quais ações são válidas
- Executa handlers

---

### State
Define **quando algo pode acontecer**:

```python
def is_active(self, machine, sender) -> bool
````

* Pode haver múltiplos estados ativos simultaneamente

---

### Symbol

Representa uma **ação do jogador**:

Exemplos:

* Pedir café
* Conversar
* Olhar o menu

---

### Handler

Função executada quando:

* Um símbolo é recebido
* E o estado está ativo

Responsável por:

* Alterar estado
* Gerar resposta narrativa

---

### Sender (Player)

Representa o jogador:

* Estado individual por usuário
* Persistido em memória

---

## ⚙️ Estrutura do Projeto

```
.
├── bot.py
├── requirements.txt
├── token.json
│
├── NPC_RPG_BOT/
│   ├── machine.py
│   ├── base_state.py
│   ├── base_symbol.py
│   └── sender.py
│
├── NPC_Bartender/
│   ├── outin_machine.py
│   ├── coffee_machine.py
│   ├── dessert_machine.py
│   ├── coffeetalk_machine.py
│   └── smalltalk_machine.py
```

---

## ▶️ Como Executar

### 1. Criar ambiente virtual

```bash
python -m venv venv
```

### 2. Ativar ambiente

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

---

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 4. Configurar token

Crie um arquivo `token.json`:

```json
{
  "token": "SEU_TOKEN_AQUI"
}
```

---

### 5. Rodar o bot

```bash
python bot.py
```

---

## 🎮 Como Jogar

### Ver ações disponíveis

```
/simbolos
```

---

### Exemplos de ações

#### Entrada

```
/getin
```

#### Café

```
/askcoffee
/askespressocoffee
/askcappuccinocoffee
```

#### Doces

```
/askdessert
/askcroissantdessert
```

#### Interação

```
/justlooking
/makeorder
/seemenu
```

#### Conversa

```
/casualtalk
/askwork
```

---

## 🔁 Fluxo de Interação

1. Jogador entra na cafeteria
2. Estado inicial: neutro (`Nothing`)
3. Escolhe uma intenção:

   * Café
   * Doce
   * Conversa
   * Explorar
4. Sistema muda o estado
5. Novas ações são liberadas

---

## 🧩 Modularidade

Cada arquivo representa um domínio:

* `outin_machine` → entrada
* `coffee_machine` → café
* `dessert_machine` → doces
* `coffeetalk_machine` → ambiente
* `smalltalk_machine` → conversa

Todos são combinados em uma única máquina.

---

## ⚠️ Limitações Atuais

* Este exemplo tem estado global único, mas a base permite estados ativos multiplos.
* Sem persistência (reset ao reiniciar)
* Comandos registrados manualmente
* UI baseada apenas em texto

---

## 🚀 Possíveis Evoluções

* Persistência (SQLite / JSON)
* Interface com botões (Discord UI)
* Registro automático de commands
* Usar Sistema de múltiplos estados simultâneos
* Expansão para RPG completo

---
