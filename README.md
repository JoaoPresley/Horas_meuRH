# 🕒 Horas_meuRH

O **Horas_meuRH** é um automatizador de extração e análise de banco de horas para o portal TOTVS MeuRH. Ele utiliza Selenium para navegar no sistema, extrai os dados via Web Scraping e utiliza lógica de processamento de dados para calcular seu saldo real, ignorando a latência de aprovação dos gestores.

## Demonstração do Projeto
[[video:demonstacao_funcionamento.mp4]]

## 🛠️ O que o código faz?
* **Automação de Login:** Acessa o portal de RH de forma segura usando suas credenciais.
* **Web Scraping Inteligente:** Extrai os dados brutos da tabela de "Espelho de Ponto" usando BeautifulSoup4.
* **Cálculo de Saldo Projetado:** * Identifica automaticamente feriados e fins de semana.
    * Calcula o saldo diário subtraindo a meta de 08:00 (em dias úteis) do total de batidas.
    * Soma o saldo acumulado do mês com o saldo anterior.
* **Exportação de Dados:** Gera um arquivo `.csv` detalhado para que você possa conferir os cálculos no Excel.

---

## 📁 Estrutura do Projeto
* `main.py`: Orquestrador do processo.
* `src/`: Contém a lógica de automação do Selenium e processamento de dados.
* `config/`: Gerencia as variáveis de ambiente e configurações de URL.
* `data/`: Pasta onde os resultados processados são salvos.
* `start.bat`: Script inteligente de inicialização (detecta Python, Anaconda e configura o VENV automaticamente).

---

## 🚀 Como utilizar

### 1. Preparação
Clone o repositório e configure seu arquivo de credenciais:
1.  Renomeie `.env-example` para `.env`.
2.  Preencha as variáveis:
    * `USER_NAME`: Seu login do sistema.
    * `USER_PASSWORD`: Sua senha.
    * `T_WAIT`: Tempo de espera (padrão 10s). Aumente se sua internet estiver lenta.

### 2. Execução
Basta executar o arquivo **`start.bat`**. 
O script irá:
1. Detectar se você tem Python ou Anaconda instalado.
2. Criar um ambiente virtual (`.venv`) se ele não existir.
3. Instalar as dependências necessárias automaticamente.
4. Rodar a análise e mostrar o resultado no terminal.

### 3. Resultados
Ao final, o programa exibirá no console:
* **Saldo Anterior** (extraído do sistema).
* **Saldo do Mês** (calculado pelo script).
* **Saldo Total** (Soma projetada).

Um log detalhado será salvo em: `./data/horas_processadas.csv`

---

## 🧰 Requisitos Técnicos
As principais bibliotecas utilizadas são:
* `selenium`: Navegação e interação com o portal.
* `beautifulsoup4`: Parsing do HTML extraído.
* `pandas`: Processamento matemático das horas e exportação para CSV.
* `python-dotenv`: Segurança das suas credenciais.

---

### ⚠️ Notas de Segurança
> **Atenção:** Seus dados sensíveis (usuário e senha) ficam armazenados apenas localmente no seu arquivo `.env`. Nunca compartilhe ou faça commit desse arquivo no GitHub.
