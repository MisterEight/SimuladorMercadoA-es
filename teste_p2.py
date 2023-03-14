#
# Testes simples para o Projeto 2
#
# NOTA IMPORTANTE: Estes testes não são exaustivos. Na avaliação o vosso
# projeto será testado com testes adicionais, pelo que aconselhável que também
# desenvolvam os vossos próprios testes para testar situações que considerem
# importantes.
#

import p2
import io
from contextlib import redirect_stdout
import datetime

#
# cria_cliente
#
p2.estado['hoje'] = datetime.date.fromisoformat('2023-02-23')
print('TESTING cria_cliente')
cliente_id = p2.cria_cliente('987654321', 'Manuel Silva', '2000-01-01')
if cliente_id == 1 and p2.estado == {'hoje': datetime.date(2023, 2, 23), 'cliente_id': 2, 'carteira_id': 1} and p2.clientes == {1: {'nif': '987654321', 'nome': 'Manuel Silva', 'data_nasc': '2000-01-01', 'saldo': 0.0, 'carteiras_id': []}}:
	print('  OK')
else:
	print('  ERROR')

#
# encerra_cliente
#
p2.estado = {'hoje': datetime.date(2023, 2, 23), 'cliente_id': 2, 'carteira_id': 2}
p2.clientes = {1: {'nif': '987654321', 'nome': 'Manuel Silva', 'data_nasc': '2000-01-01', 'saldo': 1235.0, 'carteiras_id': [1]}}
p2.mercado = {'BCP': ('B.COM.PORTUGUES', 1.5)}
p2.carteiras = {1: {'titulares_id': 1, 'designacao': 'Carteira 1', 'data_abertura': '2023-02-23', 'titulos': [('BCP', 10)], 'operacoes': [('2023-02-23', 'ABERTURA'), ('2023-02-23', 'COMPRA', 'BCP', 10, 15.0)]}}
print('TESTING encerra_cliente')
saldo = p2.encerra_cliente(1)
if p2.clientes == {} and p2.carteiras == {1: {'titulares_id': 1, 'designacao': 'Carteira 1', 'data_abertura': '2023-02-23', 'titulos': [], 'operacoes': [('2023-02-23', 'ABERTURA'), ('2023-02-23', 'COMPRA', 'BCP', 10, 15.0), ('2023-02-23', 'VENDA', 'BCP', 10, 15.0), ('2023-02-23', 'FECHO')]}} and saldo == 1250.0:
	print('  OK')
else:
	print('  ERROR')

#
# posicao_cliente
#
p2.estado = {'hoje': datetime.date(2023, 2, 23), 'cliente_id': 2, 'carteira_id': 2}
p2.clientes = {1: {'nif': '987654321', 'nome': 'Manuel Silva', 'data_nasc': '2000-01-01', 'saldo': 1235.0, 'carteiras_id': [1]}}
p2.mercado = {'BCP': ('B.COM.PORTUGUES', 3.0)}
p2.carteiras = {1: {'titulares_id': 1, 'designacao': 'Carteira 1', 'data_abertura': '2023-02-23', 'titulos': [('BCP', 10)], 'operacoes': [('2023-02-23', 'ABERTURA'), ('2023-02-23', 'COMPRA', 'BCP', 10, 15.0)]}}
print('TESTING posicao_cliente')
posicao = p2.posicao_cliente(1)
if posicao == 1265.0:
	print('  OK')
else:
	print('  ERROR')

#
# movimenta_saldo
#
p2.estado = {'hoje': datetime.date(2023, 2, 23), 'cliente_id': 2, 'carteira_id': 1}
p2.clientes = {1: {'nif': '987654321', 'nome': 'Manuel Silva', 'data_nasc': '2000-01-01', 'saldo': 1000.0, 'carteiras_id': [1]}}
print('TESTING movimenta_saldo')
m1 = p2.movimenta_saldo(1, 1000.0)
m2 = p2.movimenta_saldo(1, -3000.0)
if m1 == 1000.0 and m2 == 2000.0 and p2.clientes[1]['saldo'] == 0.0:
	print('  OK')
else:
	print('  ERROR')

#
# abre_carteira
#

p2.estado = {'hoje': datetime.date(2023, 2, 23), 'cliente_id': 2, 'carteira_id': 1}
p2.clientes = {1: {'nif': '987654321', 'nome': 'Manuel Silva', 'data_nasc': '2000-01-01', 'saldo': 1000.0, 'carteiras_id': []}}
print('TESTING abre_carteira')
p2.abre_carteira(1, 'Nova carteira')
if p2.estado == {'hoje': datetime.date(2023, 2, 23), 'cliente_id': 2, 'carteira_id': 2} and p2.clientes == {1: {'nif': '987654321', 'nome': 'Manuel Silva', 'data_nasc': '2000-01-01', 'saldo': 1000.0, 'carteiras_id': [1]}} and p2.carteiras == {1: {'titulares_id': 1, 'designacao': 'Nova carteira', 'data_abertura': '2023-02-23', 'titulos': [], 'operacoes': [('2023-02-23', 'ABERTURA')]}}:
	print('  OK')
else:
	print('  ERROR')

#
# encerra_carteira
#
p2.estado = {'hoje': datetime.date(2023, 2, 23), 'cliente_id': 2, 'carteira_id': 2}
p2.mercado = {'BCP': ('B.COM.PORTUGUES', 1.5)}
p2.clientes = {1: {'nif': '987654321', 'nome': 'Manuel Silva', 'data_nasc': '2000-01-01', 'saldo': 985.0, 'carteiras_id': [1]}}
p2.carteiras = {1: {'titulares_id': 1, 'designacao': 'Nova carteira', 'data_abertura': '2023-02-23', 'titulos': [('BCP', 10)], 'operacoes': [('2023-02-23', 'ABERTURA'), ('2023-02-23', 'COMPRA', 'BCP', 10, 15.0)]}}
print('TESTING encerra_carteira')
p2.encerra_carteira(1)
if p2.estado == {'hoje': datetime.date(2023, 2, 23), 'cliente_id': 2, 'carteira_id': 2} and p2.clientes == {1: {'nif': '987654321', 'nome': 'Manuel Silva', 'data_nasc': '2000-01-01', 'saldo': 1000.0, 'carteiras_id': []}} and p2.carteiras == {1: {'titulares_id': 1, 'designacao': 'Nova carteira', 'data_abertura': '2023-02-23', 'titulos': [], 'operacoes': [('2023-02-23', 'ABERTURA'), ('2023-02-23', 'COMPRA', 'BCP', 10, 15.0), ('2023-02-23', 'VENDA', 'BCP', 10, 15.0), ('2023-02-23', 'FECHO')]}}:
	print('  OK')
else:
	print('  ERROR')

#
# regista_operacao
#
p2.estado = {'hoje': datetime.date(2023, 2, 23), 'cliente_id': 2, 'carteira_id': 2}
p2.mercado = {'BCP': ('B.COM.PORTUGUES', 1.5)}
p2.clientes = {1: {'nif': '987654321', 'nome': 'Manuel Silva', 'data_nasc': '2000-01-01', 'saldo': 985.0, 'carteiras_id': [1]}}
p2.carteiras = {1: {'titulares_id': 1, 'designacao': 'Nova carteira', 'data_abertura': '2023-02-23', 'titulos': [('BCP', 10)], 'operacoes': [('2023-02-23', 'ABERTURA'), ('2023-02-23', 'COMPRA', 'BCP', 10, 15.0)]}}
print('TESTING regista_operacao')
p2.regista_operacao(1, 'VENDA', 'AAAAA', 9999, 1)
if p2.estado == {'hoje': datetime.date(2023, 2, 23), 'cliente_id': 2, 'carteira_id': 2} and p2.clientes == {1: {'nif': '987654321', 'nome': 'Manuel Silva', 'data_nasc': '2000-01-01', 'saldo': 985.0, 'carteiras_id': [1]}} and p2.carteiras == {1: {'titulares_id': 1, 'designacao': 'Nova carteira', 'data_abertura': '2023-02-23', 'titulos': [('BCP', 10)], 'operacoes': [('2023-02-23', 'ABERTURA'), ('2023-02-23', 'COMPRA', 'BCP', 10, 15.0), ('2023-02-23', 'VENDA', 'AAAAA', 9999, 1)]}}:
	print('  OK')
else:
	print('  ERROR')

#
# processa_operacao
#
p2.estado = {'hoje': datetime.date(2023, 2, 23), 'cliente_id': 2, 'carteira_id': 2}
p2.mercado = {'CUR': ('AGUAS DA CURIA', 1.7), 'ALTR': ('ALTRI SGP', 4.6)}
p2.clientes = {1: {'nif': '987654321', 'nome': 'Manuel Silva', 'data_nasc': '2000-01-01', 'saldo': 1000.0, 'carteiras_id': [1]}}
p2.carteiras = {1: {'titulares_id': 1, 'designacao': 'Nova carteira', 'data_abertura': '2023-02-23', 'titulos': [], 'operacoes': [('2023-02-23', 'ABERTURA')]}}
print('TESTING processa_operacao')
p2.processa_operacao(1, 'COMPRA', 'CUR', 5)
p2.processa_operacao(1, 'COMPRA', 'ALTR', 5)
p2.processa_operacao(1, 'VENDA', 'ALTR', 10) 
if p2.estado == {'hoje': datetime.date(2023, 2, 23), 'cliente_id': 2, 'carteira_id': 2} and p2.clientes == {1: {'nif': '987654321', 'nome': 'Manuel Silva', 'data_nasc': '2000-01-01', 'saldo': 991.5, 'carteiras_id': [1]}} and p2.carteiras == {1: {'titulares_id': 1, 'designacao': 'Nova carteira', 'data_abertura': '2023-02-23', 'titulos': [('CUR', 5)], 'operacoes': [('2023-02-23', 'ABERTURA'), ('2023-02-23', 'COMPRA', 'CUR', 5, 8.5), ('2023-02-23', 'COMPRA', 'ALTR', 5, 23.0), ('2023-02-23', 'VENDA', 'ALTR', 5, 23.0)]}}:
	print('  OK')
else:
	print('  ERROR')

#
# agenda_ordem
#
p2.estado = {'hoje': datetime.date(2023, 2, 23), 'cliente_id': 2, 'carteira_id': 2}
p2.mercado = {'CUR': ('AGUAS DA CURIA', 1.7), 'ALTR': ('ALTRI SGP', 4.6)}
p2.clientes = {1: {'nif': '987654321', 'nome': 'Manuel Silva', 'data_nasc': '2000-01-01', 'saldo': 1000.0, 'carteiras_id': [1]}}
p2.carteiras = {1: {'titulares_id': 1, 'designacao': 'Nova carteira', 'data_abertura': '2023-02-23', 'titulos': [], 'operacoes': [('2023-02-23', 'ABERTURA')]}}
p2.ordens = [ ]
print('TESTING agenda_ordem')
r1 = p2.agenda_ordem(1, 'COMPRA', 'CUR', 20, 1.5, '2023-02-23')
r3 = p2.agenda_ordem(1, 'COMPRA', 'ALTR', 2, 5)
r3 = p2.agenda_ordem(1, 'COMPRA', 'ALTR', 20, 5, '2023-02-23')
r4 = p2.agenda_ordem(1, 'VENDA', 'ALTR', 10, 5, '2023-02-23')
print(p2.clientes)
print(p2.carteiras)
print(p2.ordens)
r5 = p2.agenda_ordem(1, 'COMPRA', 'ALTR', 10, 5, '2023-02-24')
if p2.clientes == {1: {'nif': '987654321', 'nome': 'Manuel Silva', 'data_nasc': '2000-01-01', 'saldo': 898.8, 'carteiras_id': [1]}} and p2.carteiras == {1: {'titulares_id': 1, 'designacao': 'Nova carteira', 'data_abertura': '2023-02-23', 'titulos': [('ALTR', 22)], 'operacoes': [('2023-02-23', 'ABERTURA'), ('2023-02-23', 'COMPRA', 'ALTR', 2, 9.2), ('2023-02-23', 'COMPRA', 'ALTR', 20, 92.0)]}} and p2.ordens == [(1, 'COMPRA', 'ALTR', 10, 5, '2023-02-24')]:
	print('  OK')
else:
	print('  ERROR')

#
# gera_resumo
#
p2.estado = {'hoje': datetime.date(2023, 2, 23), 'cliente_id': 2, 'carteira_id': 2}
p2.mercado = {'CUR': ('AGUAS DA CURIA', 1.7), 'ALTR': ('ALTRI SGP', 4.6)}
p2.clientes = {1: {'nif': '987654321', 'nome': 'Manuel Silva', 'data_nasc': '2000-01-01', 'saldo': 968.5, 'carteiras_id': [1]}}
p2.carteiras = {1: {'titulares_id': 1, 'designacao': 'Nova carteira', 'data_abertura': '2023-02-23', 'titulos': [('CUR', 5), ('ALTR', 5)], 'operacoes': [('2023-02-23', 'ABERTURA'), ('2023-02-23', 'COMPRA', 'CUR', 5, 8.5), ('2023-02-23', 'COMPRA', 'ALTR', 10, 46.0), ('2023-02-23', 'VENDA', 'ALTR', 5, 23.0)]}}
print('TESTING gera_resumo')
resumo = p2.gera_resumo(1, '2023-01-01', '2023-10-10')
if p2.clientes == {1: {'nif': '987654321', 'nome': 'Manuel Silva', 'data_nasc': '2000-01-01', 'saldo': 968.5, 'carteiras_id': [1]}} and p2.carteiras == {1: {'titulares_id': 1, 'designacao': 'Nova carteira', 'data_abertura': '2023-02-23', 'titulos': [('CUR', 5), ('ALTR', 5)], 'operacoes': [('2023-02-23', 'ABERTURA'), ('2023-02-23', 'COMPRA', 'CUR', 5, 8.5), ('2023-02-23', 'COMPRA', 'ALTR', 10, 46.0), ('2023-02-23', 'VENDA', 'ALTR', 5, 23.0)]}} and resumo == [1, 'Nova carteira', '2023-02-23', [('AGUAS DA CURIA', 'CUR', 5, 8.5), ('ALTRI SGP', 'ALTR', 5, 23.0)], [('2023-02-23', 'ABERTURA'), ('2023-02-23', 'COMPRA', 'CUR', 5, 8.5), ('2023-02-23', 'COMPRA', 'ALTR', 10, 46.0), ('2023-02-23', 'VENDA', 'ALTR', 5, 23.0)]]:
	print('  OK')
else:
	print('  ERROR')

#
# inicia_dia
#
p2.estado = {'hoje': datetime.date(2022, 2, 23), 'cliente_id': 2, 'carteira_id': 2}
p2.mercado = {'CUR': ('AGUAS DA CURIA', 1.7), 'ALTR': ('ALTRI SGP', 4.6)}
p2.clientes = {1: {'nif': '987654321', 'nome': 'Manuel Silva', 'data_nasc': '2000-01-01', 'saldo': 968.5, 'carteiras_id': [1]}}
p2.carteiras = {1: {'titulares_id': 1, 'designacao': 'Nova carteira', 'data_abertura': '2023-02-23', 'titulos': [('CUR', 5), ('ALTR', 5)], 'operacoes': [('2023-02-23', 'ABERTURA'), ('2023-02-23', 'COMPRA', 'CUR', 5, 8.5), ('2023-02-23', 'COMPRA', 'ALTR', 10, 46.0), ('2023-02-23', 'VENDA', 'ALTR', 5, 23.0)]}}
p2.ordens = [(1, 'VENDA', 'ALTR', 10, 4, '2023-02-24')]
print('TESTING inicia_dia')
p2.inicia_dia('2023-02-24')
if p2.estado == {'hoje': datetime.date(2023, 2, 24), 'cliente_id': 2, 'carteira_id': 2} and p2.clientes == {1: {'nif': '987654321', 'nome': 'Manuel Silva', 'data_nasc': '2000-01-01', 'saldo': 991.5, 'carteiras_id': [1]}} and p2.carteiras == {1: {'titulares_id': 1, 'designacao': 'Nova carteira', 'data_abertura': '2023-02-23', 'titulos': [('CUR', 5)], 'operacoes': [('2023-02-23', 'ABERTURA'), ('2023-02-23', 'COMPRA', 'CUR', 5, 8.5), ('2023-02-23', 'COMPRA', 'ALTR', 10, 46.0), ('2023-02-23', 'VENDA', 'ALTR', 5, 23.0), ('2023-02-24', 'VENDA', 'ALTR', 5, 23.0)]}} and len(p2.ordens) == 0:
	print('  OK')
else:
	print('  ERROR')

#
# carrega_mercado
#
p2.mercado = {'CUR': ('AGUAS DA CURIA', 1.7), 'ALTR': ('ALTRI SGP', 4.6)}
print('TESTING carrega_mercado')
f = open('ficheiro_exemplo_para_testar_mercado.txt', 'w')
print('AAAA AAAA AAAA AAAA \t\t\t\tESSSS\t\t\t\t\t2.71', file=f)
print('B B B B B B B B B BB\tPICCC\t\t\t\t\t3.14', file=f)
f.close()
p2.carrega_mercado('ficheiro_exemplo_para_testar_mercado.txt')
if p2.mercado == {'ESSSS': ('AAAA AAAA AAAA AAAA ', 2.71), 'PICCC': ('B B B B B B B B B BB', 3.14)}:
	print('  OK')
else:
	print('  ERROR')

#
# carrega_ordens
#
p2.estado = {'hoje': datetime.date(2023, 2, 23), 'cliente_id': 2, 'carteira_id': 2}
p2.mercado = {'CUR': ('AGUAS DA CURIA', 1.7), 'ALTR': ('ALTRI SGP', 4.6)}
p2.clientes = {1: {'nif': '987654321', 'nome': 'Manuel Silva', 'data_nasc': '2000-01-01', 'saldo': 1000.0, 'carteiras_id': [1]}}
p2.carteiras = {1: {'titulares_id': 1, 'designacao': 'Nova carteira', 'data_abertura': '2023-02-23', 'titulos': [], 'operacoes': [('2023-02-23', 'ABERTURA')]}}
p2.ordens = [ ]
print('TESTING carrega_ordens')
f = open('ficheiro_exemplo_para_testar_ordens.txt', 'w')
print('1 CUR +20 1.5 2023-02-23', file=f)
print('1 ALTR +2 5 2023-02-23', file=f)
print('1 ALTR +20 5 2023-02-23', file=f)
print('1 ALTR -10 5 2023-02-23', file=f)
print('1 ALTR +10 5 2023-02-24', file=f)
f.close()
p2.carrega_ordens('ficheiro_exemplo_para_testar_ordens.txt')
if p2.clientes == {1: {'nif': '987654321', 'nome': 'Manuel Silva', 'data_nasc': '2000-01-01', 'saldo': 898.8, 'carteiras_id': [1]}} and p2.carteiras == {1: {'titulares_id': 1, 'designacao': 'Nova carteira', 'data_abertura': '2023-02-23', 'titulos': [('ALTR', 22)], 'operacoes': [('2023-02-23', 'ABERTURA'), ('2023-02-23', 'COMPRA', 'ALTR', 2, 9.2), ('2023-02-23', 'COMPRA', 'ALTR', 20, 92.0)]}} and p2.ordens == [(1, 'COMPRA', 'ALTR', 10, 5, '2023-02-24')]:
    print('  OK')
else:
    print('  ERROR')

#
# imprime_resumo
#
resumo = [1, 'Nova carteira', '2023-02-23', [('AGUAS DA CURIA', 'CUR', 5, 8.5), ('ALTRI SGP', 'ALTR', 5, 23.0)], [('2023-02-23', 'ABERTURA'), ('2023-02-23', 'COMPRA', 'CUR', 5, 8.5), ('2023-02-23', 'COMPRA', 'ALTR', 10, 46.0), ('2023-02-23', 'VENDA', 'ALTR', 5, 23.0)]]
print('TESTING imprime_resumo')
with io.StringIO() as buf, redirect_stdout(buf):
	p2.imprime_resumo(resumo)
	output = buf.getvalue()
if output.replace('\n','') == '--------------------------------------------------CARTEIRA #000001 / Nova carteira        2023-02-23--------------------------------------------------                  ** TITULOS **--------------------------------------------------      AGUAS DA CURIA CUR           5          8.50           ALTRI SGP ALTR          5         23.00--------------------------------------------------TOTAL                                        31.50--------------------------------------------------                 ** OPERACOES **--------------------------------------------------2023-02-23 ABERTURA--------------------------------------------------2023-02-23 COMPRA    CUR           5          8.50--------------------------------------------------2023-02-23 COMPRA    ALTR         10         46.00--------------------------------------------------2023-02-23 VENDA     ALTR          5         23.00--------------------------------------------------':
    print('  OK')
else:
    print('  ERROR')
