
#valida se o campo esta preenchido
def funcaoAlert(variavel):
    while(variavel == ""):
      print("\033[0;31mEste é um campo obrigatório!\033[m")
      variavel = input("Por favor preencha-o corretamente: ")
      return variavel

#Cadastra o cliente
def funcaoCadastra():

#abre o arquivo em modo append e corrige caracteres especiais no texto em pt-br
  banco = open("database.txt", "a", encoding="utf-8")

  insereCliente = input("Insira o nome do titular: ")
  funcaoAlert(insereCliente)

  insereCpf = input("Insira o cpf do titular: ")
  
  #valida a quantidade de digitos digitados no cpf
  validaCpf = len(insereCpf)
  while (validaCpf < 11) or (validaCpf > 11):
    funcaoAlert(insereCpf)
    print("\033[0;31mCampo incorreto!\033[m")
    insereCpf = input("Por favor digite o CPF corretamente: ")
    validaCpf = len(insereCpf)
  
  numeroPessoas = input("Insira o número de pessoas: ")
  funcaoAlert(numeroPessoas)

  tipoQuarto = input("Insira o tipo do quarto S (Standard), D (Deluxe) ou P (Premium): ")

  #aceita letras maiusculas e minusculas
  while((tipoQuarto != "S") and (tipoQuarto != "s") and (tipoQuarto != "D") and (tipoQuarto != "d") and (tipoQuarto != "P") and (tipoQuarto != "p")):
    funcaoAlert(tipoQuarto)
    print("\033[0;31mCampo incorreto!\033[m")
    tipoQuarto = input("Os tipos de quartos são S, D ou P, por favor insira um destes: ")

  numeroDias = input("Insira o numero de dias da reserva: ")

#converte de str para int para fazer o calculo
  nPessoas = int(numeroPessoas)
  nDias = int(numeroDias)

  #calcula o valor total da diaria

  if tipoQuarto == "S" or "s":
    valorQuarto = 100

  elif tipoQuarto == "D" or "d":
    valorQuarto = 200

  elif tipoQuarto == "P" or "p":
    valorQuarto = 300

  #calcula o valor total da diaria

  valor = nPessoas * nDias * valorQuarto

  status = ["R","A""C","F"]

  #insere o cadastro no banco

  banco.writelines("{},{},{},{},{},{},{},".format(insereCliente,insereCpf,numeroPessoas,tipoQuarto,numeroDias,valor,status[0]) + "\n")
  
  banco.close()
  
  print("Cadastro concluído com sucessso!")

#busca os arquivos
def funcaoBusca():
    arquivo = open("database.txt", "r")
    listaClientes = arquivo.readlines()
    arquivo.close

    novaLista = []
    for i in listaClientes:
        insereCliente,insereCpf,nPessoas,tipoQuarto,valor,nDias,status,valida = i.split(",")
        clientes = {"nome" : insereCliente, "cpf" : insereCpf, "nPessoas" : nPessoas, "tipoQuarto" : tipoQuarto, "nDias" : nDias, "valor" : valor, "status" : status}
        novaLista.append(clientes)
    return novaLista

#Reescreve a lista com os dados alterados no banco
def funcaoAltera(novaLista):
    arquivo = open("database.txt", "w")
    for i in novaLista:
        arquivo.write(f"{i['nome']},{i['cpf']},{i['nPessoas']},{i['tipoQuarto']},{i['nDias']},{i['valor']},{i['status']},\n")
    arquivo.close

#Entrada de cliente
def funcaoCheckIn():
    cpf = input("Procurar por cpf: ")
    
    novaLista = funcaoBusca()
    reserva = 0
    for i in novaLista:
        if(cpf == i['cpf']):
            #formata o texto com a variavel i e acrescenta os numeros dos clientes na lista
            reserva+=1
            print(f"Reserva n°:{reserva} - {i['nome']},{i['cpf']},{i['nPessoas']},{i['tipoQuarto']},{i['nDias']},{i['valor']},{i['status']},\n")
    selecionaReserva = int(input("Selecione a reserva que deseja alterar: "))
    reserva = 0
    for i in novaLista:
        if(cpf == i['cpf']):
            #para cada cliente adiciona um a contagem
            reserva += 1
            if(reserva == selecionaReserva):
                i['status'] = "A"
    funcaoAltera(novaLista)
    
    print("Check in realizado com sucesso!!!")

#Saída de cliente
def funcaoCheckOut():
    cpf = input("Procurar por cpf: ")
    
    novaLista = funcaoBusca()
    selecionaReserva = 0
    reserva = 0
    for i in novaLista:
        if(cpf == i['cpf']):
            reserva += 1
            print(f"Reserva n°:{reserva}> - {i['nome']},{i['cpf']},{i['nPessoas']},{i['tipoQuarto']},{i['nDias']},{i['valor']},{i['status']},\n")
    selecionaReserva = int(input("Selecione a reserva que deseja alterar: "))
    reserva = 0
    for i in novaLista:
        if(cpf == i['cpf']):
            #para cada cliente adiciona um a contagem
            reserva += 1
            if(reserva == selecionaReserva):
                i['status'] = "F"
    funcaoAltera(novaLista)
    
    print("Check out realizado com sucesso!!!")

#altera os dados da reserva
def funcaoAlterarReserva():
    cpf = input("Procurar por cpf: ")
    
    novaLista = funcaoBusca()
    reserva = 0
    for dados in novaLista:
        if(cpf == dados['cpf']):
            reserva+=1
            print(f"Reserva n°:{reserva} - {dados['nome']},{dados['cpf']},{dados['nPessoas']},{dados['tipoQuarto']},{dados['nDias']},{dados['valor']},{dados['status']},\n")
    selecionaReserva = int(input("Selecione a reserva que deseja alterar: "))
    reserva = 0
    for dados in novaLista:
        if(cpf == dados['cpf']):
            #para cada cliente adiciona um a contagem
            reserva += 1
            if(reserva == selecionaReserva):
                    dados['nPessoas'] = int(input("Numero de pessoas: "))
                    dados['nDias'] = int(input("Numero de dias: "))
                    dados['tipoQuarto'] = input("Tipo de quarto S (Standard), D (Deluxe) ou P (Premium): ").upper()
                    dados['status'] = input("Status do quarto: ").upper()
                    if(dados['tipoQuarto'] == "S"): dados['valor'] = (100*dados['nPessoas'])*dados['nDias']
                    elif(dados['tipoQuarto'] == "D"): dados['valor'] = (100*dados['nPessoas'])*dados['nDias']
                    elif(dados['tipoQuarto'] == "P"): dados['valor'] = (100*dados['nPessoas'])*dados['nDias']
    funcaoAltera(novaLista)
    
    print("Alteração realizada com sucesso!!")

#relatorios
def funcaoRelatorio():
    
    novaLista = funcaoBusca()
    opcaoRelatorio = int(input("1 - Relatório de todas as reservas com status R\n2 - Relatório de todas as reservas com status C\n3 - Relatório de todas as reservas com status A\n4 - Relatório de todas as reservas com status F\n5 - Relatório total recebido\n6 – Relatório de Reserva por pessoa\n> "))
    if opcaoRelatorio == 1:
        reserva = 0
        for i in novaLista:
            if("R" == i['status']):
                reserva += 1
                print(f"Reserva n°:{reserva} - {i['nome']},{i['cpf']},{i['nPessoas']},{i['tipoQuarto']},{i['nDias']},{i['valor']},{i['status']},\n")
    elif opcaoRelatorio == 2: 
        reserva = 0
        for dados in novaLista:
            if("C" == dados['status']):
                reserva += 1
                print(f"Reserva n°:{reserva} - {dados['nome']},{dados['cpf']},{dados['nPessoas']},{dados['tipoQuarto']},{dados['nDias']},{dados['valor']},{dados['status']},\n")
    elif opcaoRelatorio == 3: 
        
        reserva = 0
        for dados in novaLista:
            if("A" == dados['status']):
                reserva+=1
                print(f"Reserva n°:{reserva} - {dados['nome']},{dados['cpf']},{dados['nPessoas']},{dados['tipoQuarto']},{dados['nDias']},{dados['valor']},{dados['status']},\n")
    elif opcaoRelatorio == 4: 
        
        reserva = 0
        for dados in novaLista:
            if("F" == dados['status']):
                reserva+=1
                print(f"Reserva n°:{reserva} - {dados['nome']},{dados['cpf']},{dados['nPessoas']},{dados['tipoQuarto']},{dados['nDias']},{dados['valor']},{dados['status']},\n")
    elif opcaoRelatorio == 5: 
        
        totalRecebido = 0
        for dados in novaLista:
            totalRecebido += int(dados["nDias"])
        print(f"Total Recebido = {totalRecebido}")
    elif opcaoRelatorio == 6: 
        cpf = input("Procurar por cpf: ")
        
        reserva = 0
        for dados in novaLista:
            if(cpf == dados['cpf']):
                reserva+=1
                print(f"Reserva n°:{reserva} - {dados['nome']},{dados['cpf']},{dados['nPessoas']},{dados['tipoQuarto']},{dados['nDias']},{dados['valor']},{dados['status']},\n")

#menu    
while True:

  print("          *** Menu ***\n"
    "[ 1 ] Cadastrar uma reserva\n"
    "[ 2 ] Entrada do cliente (check in)\n"
    "[ 3 ] Saída do cliente (check out)\n"
    "[ 4 ] Alterar reserva\n"
    "[ 5 ] Relatórios\n"
    "[ 6 ] Sair do programa\n"
  )

  opcao = int(input("Escolha uma das opções acima: "))

  if opcao == 1:
    funcaoCadastra()
  
  elif opcao == 2: 
    funcaoCheckIn()

  elif opcao == 3:
    funcaoCheckOut()  

  elif opcao == 4:
    funcaoAlterarReserva()

  elif opcao == 5:
    funcaoRelatorio()

  elif opcao == 6:
        break