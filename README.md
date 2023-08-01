# API de Logística para uma Cooperativa Social
***

Está é uma API utilizada como um serviço web que traça as rotas para entrega de 
cestas de alimentos organicos em SP, para melhorar a experiencia do entregador 
e também o tempo e dinheiro gasto para efetuar todas as entregas fiz uma modelagem 
variante do Caixeiro Viajante (Travel Salesman Problemn) para fazer a mensagem e 
criar o link do google maps para ser utilizado.

# Como Rodar?

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

# Futuras Melhorias

 - Fazer uma comunicação com a API da Meta para enviar as rotas direto para o whatsapp do entregador
 
 - Deixar o código mais limpo e tipar melhor, depois vou

 - Adicionar uma etapa de divisão de rotas automática, porem a cada dia, cada entregador pode ou não ter uma restrição de quais bairros ele pode entregar, numero de entrega ou volume.