@echo off
:: Define o título da janela do terminal
title Gerenciador MeuRH

:: Verifica se o ambiente virtual (.venv) existe
if not exist ".venv" (
    echo [INFO] Ambiente virtual nao encontrado. Criando...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERRO] Python nao esta instalado ou nao esta no PATH.
        pause
        exit /b
    )
)

:: Ativa o ambiente virtual (.bat usa o activate.bat em vez do .ps1)
echo [INFO] Ativando ambiente virtual...
call .venv\Scripts\activate.bat

:: Instala as dependencias
echo [INFO] Instalando/Atualizando dependencias (isso pode demorar um pouco)...
pip install -r requirements.txt -qq

:: Executa o script principal
echo [INFO] Iniciando main.py...
echo ---------------------------------------
python main.py
echo ---------------------------------------

:: Desativa o ambiente virtual
call deactivate

:: Espera o usuário pressionar uma tecla antes de fechar a janela
echo.
echo Processo finalizado.
set /p dummy=Aperte qualquer tecla para sair...
