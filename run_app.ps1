#Cria um ambiente virtual caso não exista
if (-not (Test-Path ".\.venv")) {
    Write-Host "Ambiente virtual não encontrado. Criando..." -ForegroundColor Cyan
    python -m venv .venv
}

#Ativa o ambiente virtual
.\.venv\Scripts\activate.ps1
#Instala as dependencias do requirements.txt
pip install -r .\requirements.txt -qq

#Executa o programa main.py
python .\main.py

#Desativa o ambiente virtual
deactivate
#Espera um input do usuario
Read-Host "Aperte um botão para sair..."