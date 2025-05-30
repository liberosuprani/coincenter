Projeto desenvolvido para a cadeira de Aplicações Distribuídas, no 4º semestre da faculdade.
Consiste em uma aplicação que simula um sistema de compra e venda de ativos (criptomoedas), permitindo a um utilizador "manager" criar e remover ativos, ver transações dos outros clientes, entre outros.
Um utilizador normal pode depositar e retirar um valor, comprar e vender ativos, entre outros.

Foi utilizado flask no programa servidor para criação de um servidor REST HTTP, Zookeeper para notificação aos clientes quando um manager cria um novo ativo e sqlite3 para persistência dos dados. 
