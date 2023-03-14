import datetime
# define as variáveis de estado
estado = {
    'hoje': datetime.date.today(),
    'cliente_id': 1,
    'carteira_id': 1
}
# define as estruturas de dados para as outras entidades
mercado = {
    'EDPR': ('EDP RENOVAVEIS', 19.99),
    'GALP': ('GALP ENERGIA-NOM', 12.315),
    'JMT': ('J.MARTINS,SGPS', 19.29),
    'EGL': ('MOTA ENGIL', 2.04)
}
clientes = {}
carteiras = {}
ordens = []
operacoes = []


def verifica_operacao(operacao):
    #Caso a operação enviada esteja incorreta.
    if operacao != "COMPRA" and operacao != "VENDA":
        raise ValueError("Modo de operação não reconhecido")

def verificar_titulo(nome_titulo):
    # Verifica se o titulo existe
    if nome_titulo not in mercado:
        raise ValueError("Este titulo não existe!")

def verificar_carteira(carteira_id):
    #Verifica se a cateira existe.
    if carteira_id not in carteiras:
        raise ValueError("Carteira não encontrada.")

def cria_cliente(nif, nome, data_nasc):
    """
    Cria um novo cliente com as informações fornecidas e devolve o seu identificador.

    Argumentos:
    - nif: número de identificação fiscal do cliente (string)
    - nome: nome do cliente (string)
    - data_nasc: data de nascimento do cliente (string no formato "AAAA-MM-DD")

    Retorna:
    - o identificador do cliente criado (número inteiro)
    """
    global clientes
    id_cliente = estado["cliente_id"]

    # cria um novo dicionário com as informações do cliente e o adiciona ao dicionário de clientes
    clientes[id_cliente] = {
        "nif": nif,
        "nome": nome,
        "data_nasc": data_nasc,
        "saldo": 0.0,
        "carteiras_id": []
    }

    # atualiza o identificador do próximo cliente
    estado["cliente_id"] += 1

    # retorna o identificador do cliente criado
    return id_cliente

def encerra_cliente(cliente_id):
    """
    Encerra todas as carteiras de títulos das quais o cliente com o identificador cliente_id é o único titular e apaga toda
    a informação relativa a esse cliente. Retorna o saldo do cliente após a encerramento de todas as suas carteiras.
    
    Argumentos:
    - cliente_id: identificador do cliente a encerrar (número inteiro)
    
    Retorno:
    - Valor a entregar ao cliente (número real), correspondente ao saldo atual da conta após o encerramento de todas as
    carteiras das quais o cliente é o único titular. Caso o cliente com o identificador cliente_id partilhar a titularidade
    de alguma carteira com outros clientes, a função deverá gerar uma exceção do tipo ValueError, com a mensagem “cliente
    tem carteiras partilhadas”. Caso não exista um cliente com o identificador cliente_id, a função não deverá fazer nada e
    deverá devolver o valor 0.
    """
    # Verifica se o cliente existe
    if cliente_id not in clientes:
        return 0
    
    # Verifica se o cliente tem carteiras partilhadas
    carteiras_cliente = clientes[cliente_id]["carteiras_id"]
    for carteira_id in carteiras_cliente:
        carteira = carteiras[carteira_id]
        if isinstance(carteira["titulares_id"], tuple):
            raise ValueError("cliente tem carteiras partilhadas")
    
    # Encerra as carteiras e calcula o valor a ser devolvido ao cliente
    valor_a_devolver = 0 + clientes[cliente_id]['saldo']
    if clientes[cliente_id]["carteiras_id"] != None:
        for carteira_id in carteiras_cliente:
            valor_da_carteira = encerra_carteira(carteira_id)
            valor_a_devolver += valor_da_carteira
        
    
    # Apaga toda a informação relativa ao cliente
    del clientes[cliente_id]
    
    return valor_a_devolver

def posicao_cliente(cliente_id):
    """
    Retorna a posição do cliente com o identificador cliente_id,
    que é igual à soma do saldo do cliente com o valor atual
    de todas as ações das carteiras das quais o cliente é titular.

    Args:
        cliente_id (int): identificador do cliente.

    Returns:
        float: posição do cliente.

    """

    #verifica se o cliente existe.
    if cliente_id not in clientes:
        return 0.0
    #O saldo do cliente.
    posicao = clientes[cliente_id]['saldo']
    #Calculo de quanto as ações do cliente valem junto com a posicão.
    for carteira_id, carteira_items in carteiras.items():
        if cliente_id == carteira_items["titulares_id"]:
            for titulo in (carteira_items["titulos"]):
                preço_de_acoes = titulo[1]*mercado[titulo[0]][1]
                posicao += preço_de_acoes
        elif cliente_id in carteira_items["titulares_id"]:
            for titulo in (carteira_items["titulos"]):
                preço_de_acoes = titulo[1]*mercado[titulo[0]][1] / len(carteira_items["titulares_id"])
                posicao += preço_de_acoes
            

    return posicao


def movimenta_saldo(cliente_id, valor):
    """
    Movimenta o saldo do cliente com o identificador cliente_id.

    Argumentos:
    - cliente_id: identificador do cliente (número inteiro)
    - valor: valor a movimentar (número real)

    Retorna:
    - valor movimentado, que deverá ser sempre um valor não negativo

    Esta função permite movimentar o saldo do cliente. Caso o valor seja negativo, ela irá reduzir o saldo do cliente nesse valor e caso seja positivo irá aumentar o saldo do cliente nesse valor. Caso valor seja negativo e o saldo do cliente seja inferior a |valor|, então o saldo do cliente será colocado a 0.0 e o valor devolvido pela função será esse saldo (antes de ser colocado a zero). O saldo de um cliente nunca pode ser inferior a 0.0.
    """
    # verifica se o valor é um número real
    if not isinstance(valor, float) and not isinstance(valor, int):
        raise TypeError("O valor deve ser um número real.")

    # verifica se o cliente existe
    if cliente_id not in clientes:
        return 0.0

    #Saldo do cliente.
    saldo_atual = clientes[cliente_id]['saldo']
    novo_saldo = saldo_atual + float(valor)

    # caso o novo saldo seja negativo, zera o saldo e devolve o valor anterior
    if novo_saldo < 0:
        valor_movimentado = saldo_atual
        novo_saldo = 0.0
    # caso contrário, atualiza o saldo com o valor fornecido
    else:
        valor_movimentado = float(valor)

    clientes[cliente_id]['saldo'] = float('%.3f'%(novo_saldo))

    return valor_movimentado

def abre_carteira(titulares_id, designacao):
    """
    Cria uma nova carteira com o(s) titular(es) e a designação especificados e retorna o seu identificador.

    Argumentos:
    - titulares_id: identificador do cliente titular da carteira (número inteiro) ou, alternativamente,
    tuplo contendo os identificadores de todos os clientes que são titulares da carteira (tuplo de números inteiros);
    o tuplo só será utilizado quando a carteira tiver mais do que um titular;
    - designacao: designação da carteira, que não é mais do que uma descrição textual da carteira
    (string com, no máximo, 20 caracteres).

    Retorna:
    - o identificador da carteira criada (número inteiro).
    """
    global carteiras
    global estado
    global operacoes

    # Cria um novo dicionário com as informações da carteira
    carteira = {
        "titulares_id": titulares_id,
        "designacao": designacao,
        "data_abertura": str(estado["hoje"]),
        "titulos": [],
        "operacoes": [],
        
    }

    # Adiciona a nova carteira ao dicionário de carteiras
    carteira_id = estado["carteira_id"]
    carteiras[carteira_id] = carteira

    # Atualiza o identificador da próxima carteira
    estado["carteira_id"] += 1

    # Adiciona o identificador desta carteira ao campo carteiras_id de todos os seus titulares
    if isinstance(titulares_id, tuple):
        for cliente_id in titulares_id:
            clientes[cliente_id]["carteiras_id"].append(carteira_id)
    else:
        clientes[titulares_id]["carteiras_id"].append(carteira_id)

    # Adiciona a operação de abertura à lista de operações
    regista_operacao(carteira_id,"ABERTURA")

    return carteira_id

def encerra_carteira(carteira_id):
    """
    Encerra a carteira com o identificador carteira_id. Vende todos os títulos da carteira, transfere os valores obtidos com
    a venda, de forma proporcional, para os saldos dos seus titulares e apaga o identificador da carteira no campo
    carteiras_id de todos os seus titulares. Adiciona à lista operacoes a operação “FECHO”. Se não existir uma carteira com o
    identificador carteira_id, gera uma exceção do tipo ValueError, com a mensagem “carteira inexistente”.

    Argumentos:
    - carteira_id: identificador da carteira a encerrar (número inteiro)

    Retorna:
    - o valor a ser devolvido aos titulares da carteira (número real).
    """
    global carteiras
    global operacoes
    valor_a_devolver = 0

    # Verifica se a carteira existe
    verificar_carteira(carteira_id)
    carteira = carteiras[carteira_id]
    titulares_id = carteira["titulares_id"]
    
    #Se for apenas um titular.
    if isinstance(titulares_id, int):
        titulares_id = (titulares_id,)
    
    # Vende todas as ações da carteira e calcula o valor a ser transferido para cada titular
    for acao, quantidade in carteira["titulos"]:
        preco_venda = mercado[acao][1]
        valor_venda = quantidade * preco_venda
        valor_a_devolver += valor_venda
        for titular_id in titulares_id:
            participacao_titular = 1/len(titulares_id) if isinstance(titulares_id, tuple) and len(titulares_id) > 1 else 1
            processa_operacao(carteira_id,"VENDA", acao, quantidade)
        
    # Apaga a carteira do campo carteiras_id de todos os seus titulares
    for titular_id in titulares_id:
        clientes[titular_id]["carteiras_id"].remove(carteira_id)

    # Adiciona a operação de fecho à lista de operações
    regista_operacao(carteira_id, "FECHO", nome_titulo=None, quantidade=None, valor=None)

    return valor_a_devolver



def regista_operacao(carteira_id, descricao="", nome_titulo=None, quantidade=None, valor=None):
    """
    Registra uma operação na carteira com o id especificado.

    Argumentos:
    - carteira_id: identificador da carteira (número inteiro).
    - descricao: descrição da operação (string com, no máximo, 8 caracteres).
    - nome_titulo: nome do título transacionado (string com, no máximo, 5 caracteres).
    - quantidade: número de unidades do título transacionadas (número inteiro).
    - valor: valor total da operação (número real).

    Esta função adiciona uma operação à lista 'operacoes' da carteira com identificador 'carteira_id'.
    Os três últimos argumentos são opcionais, não sendo passados no caso das operações “ABERTURA” e “FECHO”.
    A data da operação é sempre a data atual dada por estado[“hoje”], mas guardada como uma string no formato “AAAA-MM-DD”.

    Note que a operação é modelada por um tuplo contendo a informação anteriormente descrita. 
    O campo operacoes de cada carteira de títulos deverá ser manipulado exclusivamente através desta função.

    Lança um ValueError caso a carteira com id 'carteira_id' não exista.

    Retorna None.
    """
    # Obtem a data atual no formato "AAAA-MM-DD".
    data_atual = estado["hoje"].strftime("%Y-%m-%d")

    # Cria a operação a ser adicionada à carteira.
    if nome_titulo != None and quantidade != None and valor != None:
        operacao = (data_atual, descricao, nome_titulo, quantidade, float(valor))
    else:
        operacao = (data_atual, descricao)

    # Verifica se a carteira com o id especificado existe.
    if carteira_id not in carteiras:
        raise ValueError("Carteira não encontrada.")

    # Adiciona a operação à lista 'operacoes' da carteira.
    if "operacoes" not in carteiras[carteira_id]:
        carteiras[carteira_id]["operacoes"] = []
    
    carteiras[carteira_id]["operacoes"].append(operacao)
       
def processa_operacao(carteira_id,operacao, nome_titulo, quantidade):
    """
    Funcao processa_operacao: Adiciona ou Retira ações de uma carteira.

    Args:
        carteira_id (int): Identificador da carteira.
        operacao (str): opereção a realizar.
        nome_titulo (str): Nome do título a ser adicionado.
        quantidade (int): Número de unidades do título a serem adicionadas.
    
    Raises:
        ValueError: Se a carteira não existir.
    """

    #Variável para guardar o valor total do processo.
    custo_total = 0

    titulares = carteiras[carteira_id]['titulares_id']
    carteira_acoes = carteiras[carteira_id]["titulos"]
    #Caso a operação enviada esteja incorreta.
    if operacao != "COMPRA" and operacao != "VENDA":
        raise ValueError("Modo de operação não reconhecido")

    # Verifica se o titulo existe
    if nome_titulo not in mercado:
        raise ValueError("Este titulo não existe!")
    # Verifica se a carteira existe
    if carteira_id not in carteiras:
        raise ValueError("Carteira não encontrada.")
    
    # Adiciona o título à carteira
    if operacao == "COMPRA":
        #Caso a carteira tenha apenas um titular.
        if isinstance(titulares, int):
            custo_total = mercado[nome_titulo][1] * quantidade
            if clientes[titulares]["saldo"] < custo_total:
                raise ValueError(f"Cliente {titulares} não tem fundos suficientes.")
            movimenta_saldo(titulares, -custo_total)
            regista_operacao(carteira_id, operacao, nome_titulo, quantidade, '%.1f'%(custo_total))
            #Se a carteira ainda não tiver ações.
            if len(carteira_acoes) <= 0:
                carteira_acoes.append((nome_titulo, quantidade))
            #Se a carteira tiver ações e for a mesma.
            else:
                posicão_titulo = 0
                for titulo in carteira_acoes:
                    if nome_titulo == titulo[0]:
                        quantidade_acao = titulo[1]
                        quantidade_acao += quantidade
                        carteira_acoes[posicão_titulo] = (nome_titulo,quantidade_acao)
                        posicão_titulo += 0
            #Se a carteira tiver ações.
            if len(carteira_acoes) > 0:
                for titulo in carteira_acoes:
                    if nome_titulo not in titulo[0]:
                        carteira_acoes.append((nome_titulo, quantidade))
                        
                        
            

        #Caso a carteira tenha mais de um titular.
        if isinstance(titulares, tuple):
            custo_total = (mercado[nome_titulo][1] * quantidade) / len(titulares)
            for titulares_id in carteiras[carteira_id]["titulares_id"]:
                if clientes[titulares_id]["saldo"] < custo_total:
                    raise ValueError(f"Cliente {titulares_id} não tem fundos suficientes.")
                movimenta_saldo(titulares_id, -custo_total)
                regista_operacao(carteira_id, operacao, nome_titulo, quantidade, '%.1f'%(custo_total))
                #Se a carteira ainda não tiver ações.
                if len(carteira_acoes) <= 0:
                    carteira_acoes.append((nome_titulo, quantidade))
                #Se a carteira tiver ações e for a mesma.
                else:
                    posicão_titulo = 0
                    for titulo in carteira_acoes:
                        if nome_titulo == titulo[0]:
                            quantidade_acao = titulo[1]
                            quantidade_acao += quantidade
                            carteira_acoes[posicão_titulo] = (nome_titulo,quantidade_acao)
                            posicão_titulo += 0
                #Se a carteira tiver ações.
                if len(carteira_acoes) > 0:
                    for titulo in carteira_acoes:
                        if nome_titulo not in titulo[0]:
                            carteira_acoes.append((nome_titulo, quantidade))



    # Retira o título à carteira.
    if operacao == "VENDA":
            for titulo in carteira_acoes:
                if nome_titulo in titulo[0]:    
                    titulo[1] - quantidade
                    #Caso a carteira tenha apenas um titular
                    if isinstance(carteiras[carteira_id]["titulares_id"], int):
                        if titulo[1] < quantidade:
                            quantidade = titulo[1]
                        preco_total = mercado[nome_titulo][1] * quantidade
                        #Caso a quantidade seja maior que o número de ações.
                        movimenta_saldo(titulares, +preco_total)
                        regista_operacao(carteira_id, operacao, nome_titulo, quantidade, '%.1f'%(preco_total))

                    #Caso a carteira tenha mais de um titular.
                    if isinstance(titulares, tuple):
                        #Caso a quantidade seja maior que o número de ações.
                        if carteira_acoes[nome_titulo] < quantidade:
                            quantidade = carteira_acoes[nome_titulo]
                        preco_total = (mercado[nome_titulo][1] * quantidade) / len(titulares)
                        for titulares_id in titulares:
                            movimenta_saldo(titulares_id, +preco_total)
                        regista_operacao(carteira_id, operacao, nome_titulo, quantidade, '%.1f'%(custo_total))
                    carteiras[carteira_id]['titulos'].remove((titulo[0], titulo[1]))
                    break
            

            


def agenda_ordem(carteira_id,operacao,nome_titulo,quantidade,preco_limite,data_str=estado['hoje']):
    """
    Funcao agenda_ordem: Esta função oermite agendar ordens na data atual ou numa data futura.

    Args:
        carteira_id (int): Identificador da carteira.
        operacao (str): opereção a realizar.
        nome_titulo (str): Nome do título a ser adicionado.
        quantidade (int): Número de unidades do título a serem adicionadas.
        preco_limite(int): preço limite.
        data_str(str): data em que a operação deverá ser realizada
    
    Retorna: 
    True caso a ordem será realizada ou False se não é possível realizar a ordem.
    """
    #verifica se é uma operação valida.
    verifica_operacao(operacao)
    #verifica se é um titulo valido
    verificar_titulo(nome_titulo)
    #verifica se é uma carteira valida
    verificar_carteira(carteira_id)
    #transformação da data_str para date para comparação
    #verificação para vê se a data é presente, futuro ou passado.
    if str(data_str) == str(estado["hoje"]):
        data = "presente"
    elif str(data_str) > str(estado["hoje"]):
        data = "futuro"
    else:
        return False
    
    #Caso o preço limite for maior ou igual ao preço do mercado, a operação for compra e a data é hoje.
    if preco_limite > mercado[nome_titulo][1] and operacao == "COMPRA" and data == "presente":
        #Tratação de raise ValueError.
        try:
            processa_operacao(carteira_id,operacao,nome_titulo,quantidade)
        except:
            return False
        return True
    #Caso o preço limite for maior ou igual ao preço do mercado, a operação for compra e a data é futura.
    elif preco_limite >= mercado[nome_titulo][1] and operacao == "COMPRA" and data == "futuro":
        #adicionamos os dados em ordens.
        ordens.append((carteira_id,operacao,nome_titulo,quantidade,preco_limite,data_str))
        return True
    #Caso o preço limite for inferior ou igual ao preço do mercado, a operação for venda e a data é presente.
    elif preco_limite < mercado[nome_titulo][1] and operacao == "VENDA" and data == "presente":
        #Tratação de raise ValueError
        try:
            processa_operacao(carteira_id,operacao,nome_titulo,quantidade)
        except:
            return False
        return True
    
    #Caso o preço limite for inferior ou igual ao preço do mercado, a operação for venda e a data é futura.
    elif mercado[nome_titulo][1] >= preco_limite and operacao == "VENDA" and data == "futuro":
        ordens.append((carteira_id,operacao,nome_titulo,quantidade,preco_limite,data_str))
        return True

def gera_resumo(carteira_id, data_inicio_str= '', data_fim_str=''):
        """
    Funcao gera_resumo: Esta função gera um resumo da carteira.

    Args:
        carteira_id (int): Identificador da carteira.
        data_inicio_str (str): data de inicio.
        data_fim_str (str): data de fim.
    
    Retorna: 
    Uma lista de contendo a informação de um resumo da carteira
    """ 
        #lista para guardar operações
        lista_operacao = []

        for operacao in carteiras[carteira_id]["operacoes"]:
            #se for a operação de abertura ou de fechar
            if len(operacao) == 2:
                operacao = (operacao[0],operacao[1])
                lista_operacao.append(operacao)
            #Caso tenhamos as duas datas.
            elif data_inicio_str != "" and data_fim_str != "":
                if data_fim_str > operacao[0]:
                    operacao = (operacao[0],operacao[1],operacao[2],operacao[3],operacao[4])
                    lista_operacao.append(operacao)
            #Caso tenhamos apenas a data de fim.
            elif data_inicio_str == "" and data_fim_str not in "":
                if data_fim_str > operacao[0]:
                    operacao = (operacao[0],operacao[1],operacao[2],operacao[3],operacao[4])
                    lista_operacao.append(operacao)
            #Caso tenhamos apenas a data de inicio.
            elif data_fim_str == '' and data_inicio_str not in "":
                print("Oi")
                operacao_data = datetime.datetime.strptime(operacao[0], '%Y-%m-%d').date()
                if operacao[0] > data_inicio_str and operacao_data <= estado['hoje']:
                    operacao = (operacao[0],operacao[1],operacao[2],operacao[3],operacao[4])
                    lista_operacao.append(operacao)
            #Caso não tenhamos nenhuma das datas   
            elif data_fim_str =="" and data_inicio_str == "":
                operacao = (operacao[0],operacao[1],operacao[2],operacao[3],operacao[4])
                lista_operacao.append(operacao)

        #lista de titulos
        lista_titulos = []
        for titulo, quantidade in carteiras[carteira_id]["titulos"]:
            titulo = (mercado[titulo][0], titulo, quantidade, float('%.1f'%(mercado[titulo][1]*quantidade)))
            lista_titulos.append(titulo)

        return[carteira_id,carteiras[carteira_id]["designacao"],str(estado['hoje']),lista_titulos, lista_operacao]

import datetime

def imprime_resumo(resumo):
    """Funcao imprime_resumo: Esta função imprime um resumo.

    Args:
        resumo (lista): lista de resumo das carteiras gerado pela função gera resumo.
    
    Retorna: 
    Uma impressão do resumo.
    """ 
    #dados para o resumo
    carteira_id = str(resumo[0]).zfill(6)
    carteira_nome = resumo[1]
    data_atual = str(estado["hoje"])
    titulos = resumo[3]
    operacoes = resumo[4]

    #total de titulos.
    total = sum([t[2] * t[3] for t in titulos])

    #informações da carteira e a data atual
    print(f"{'-'*50}\nCARTEIRA #{carteira_id} / {carteira_nome.ljust(21)} {data_atual}\n{'-'*50}\n{' '*18}** TITULOS **")


    #Mostra a lista de titulos
    for titulo in titulos:
        empresa = titulo[0].ljust(20)
        ativo = titulo[1].ljust(5)
        quantidade = str(titulo[2]).rjust(9)
        valor = f'{titulo[3]:.2f}'.rjust(16)
        print(f"{empresa}{ativo}{quantidade}{valor}")

    #Motra o total e todas as operações
    print(f"{'-'*50}\nTOTAL{' '*32}{total:.2f}\n{'-'*50}\n{' '*17}** OPERACOES **\n{'-'*50}")

    for operacao in operacoes:
        data = operacao[0]
        acao = operacao[1]

        if len(operacao) == 2:
            print(f"{data} {acao.ljust(8)}\n{'-'*50}")
        else:
            ativo = operacao[2].ljust(5)
            quantidade = str(operacao[3]).rjust(9)  
            valor = f'{operacao[4]:.2f}'.rjust(14)

            print(f"{data} {acao.ljust(8)}{ativo}{quantidade}{valor}\n{'-'*50}")


def carrega_mercado(nome_ficheiro):
    """
    Funcao gera_resumo: Esta função carrega um mercado de um ficheiro.

    Args:
        nome_ficheiro (str): nome do ficheiro a processar(str).
    Retorna: 
    O mercado do ficheiro.
    """ 
    #Torna o mercado global
    global mercado
    try:
        with open(nome_ficheiro, 'r+') as f:
            #Renicia o mercado
            mercado = {}
            #Abre linha por linha
            for line in f:
                #Limpa as linhas
                dados = line.strip().split('\t')
                #Tira os espaços restantes
                dados_sem_espacos = list(filter(lambda x: x != '', dados))
                mercado[dados_sem_espacos[1]] = (dados_sem_espacos[0], float(dados_sem_espacos[2]))
        return mercado
    except:
        raise ValueError("erro a abrir o ficheiro")
    
 
    
def carrega_ordens(nome_ficheiro):
    """
    Funcao gera_resumo: Esta função carrega um ficheiro de ordens.

    Args:
        nome_ficheiro (str): nome do ficheiro a processar(str).
    Retorna: 
    Carrega um mercado de um ficheiro de ordens.
    """ 
    try:
        with open(fr"{nome_ficheiro}" ,'r+',encoding="utf8") as f:
            for line in f:
                dados = line.strip().split()
                carteira = int(dados[0])
                titulo = dados[1]
                unidades = int(dados[2])
                preco_limite = float(dados[3])
                data = dados[4]
                if unidades < 0:
                    operacao = "VENDA"
                elif unidades == 0:
                    print("Não pode se comprar ou vender 0 unidades!")
                    break
                else:
                    operacao = "COMPRA"
                agenda_ordem(carteira,operacao,titulo,unidades,preco_limite,data)
    except:
        raise ValueError("erro a abrir o ficheiro")

def inicia_dia(data_str=''):
    """
    Funcao gera_resumo: Esta função inicia um novo dia.

    Args:
        data_str (str): nova data atual(str).
    Retorna: 
    Carrega um mercado de um ficheiro de ordens.
    """ 
    # atualiza a data atual.
    if data_str:
        estado['hoje'] = datetime.date.fromisoformat(data_str)
        print(estado["hoje"])
    else:
        estado['hoje'] += datetime.timedelta(days=1)    
    # processas as ordens do dia
    index = 0
    while index < len(ordens):
        ordem = ordens[index]
        if ordem[5] == str(estado['hoje']):
            try:
                processa_operacao(ordem[0],ordem[1], ordem[2], ordem[3])
            except Exception as e:
                print(f'Erro na ordem {ordem[1]} de {ordem[2]}: {str(e)}')
            finally:
                ordens.pop(index)
        else:
            index += 1



