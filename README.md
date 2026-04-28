# Horas_meuRH

### PROBLEMA
No serviço em que estou não existe um calculo rápido de quantas horas tenho do "banco de horas", 
o meuRH da TOTSV até mostra o saldo, porém o gestor demora para validar os pontos que não foram batidos:
seja por falha na conexão, falha do pripio sistema, ou falha do usuário que se esqueceu de bater o ponto.

### Objetivo
Logo com base nesse problema, o programa irá acessar o meuRH e fazer webscrapping de todos pontos batidos naquele mês e dos pontos de atenção (que foram os inseridos manualmente) e retornar quantas horas tem-se no banco de horas caso todos os pontos de atenção for validados.
---
### Como utilizar o sistema

1. Faça o git clone do repositorio
2. No .env-example:
   1. Altere o nome do arquivo para .env
   2. Abra o arquivo e preencha o USER_NAME com seu nome
   3. Abra o arquivo e preencha o USER_PASSWORD com sua senha
   4. __Não obrigatorio__: se deseja que o codigo execute mais rapido coloque algum tempo menor no T_WAIT (sujeito a bugar por falhar o carregamento por não esperar o suficiente)
3. Execute o .bat (caso dê erro execute novamente, pode ter sido algum acesso ao browser que falhou momentaneamente) __FALHARÁ SE O .ENV ESTIVER VAZIO__
4. Analise a saida no terminal e feche ele



