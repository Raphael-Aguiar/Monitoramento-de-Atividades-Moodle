
'''
Programa para monitorar a conclusão de atividades, no Moodle, pelos alunos de um determinado professor de PSP

(Este arquivo é uma versão em Python do notebook do mesmo nome).

A ùnica diferença é que, neste código, é preciso colar os nomes dos arquivos nas linhas 42 e 43.

Observação Importante:
Esse código se encontra adaptado no Google Colab para uso por colegas da
disciplina de PSP no seguinte link: https://colab.research.google.com/drive/13iGkc5mI0Wclp204VNuiEspKCr191be-?usp=sharing

Instruções:

Antes de usar o programa, você deve baixar dois arquivos do Moodle no formato CSV.

a) Arquivo com o nome de seus alunos: Para baixar esse arquivo, acesse a turma no Moodle (não a metaturma, mas a sua própria turma!), clique em “participantes” e, na parte inferior da página, marque a opção “marcar todos os X participantes” e, em seguida, “baixar tabela - Valores separados por vírgulas” (CSV);

b) Arquivo geral com todas as atividades concluídas por todos os alunos da metaturma: Para baixar esse arquivo, clique na engrenagem no canto superior direito datela principal da metaturma e, em seguida, clique em "Mais". Na aba "Relatórios", clique em "Conclusão de Atividades". Escolha a opção "Download em formato CSV UTF-8".

Para usar esse programa, você deve:

1. Estar logado(a) com sua conta de Gmail, caso não esteja.
2. Apertar as teclas Control e F9 para executá-lo (CTRL + F9)
3. O programa vai te pedir (logo abaixo da primeira parte do código) para
selecionar o primeiro arquivo que você baixou (com o nome das turmas). Esse arquivo deve ter um nome parecido com "courseid_3858_participants.csv". Selecione-o e aperte enter.
4. Em seguida, ele pedirá para selecionar o segundo arquivo, que deve ter um
nome parecido com "progress.20212_meta_turma_mps005-a1-a2-b1-b2-c1-c2-d1-d2.csv". Selecione-o e aperte enter.

O programa irá gerar uma tabela, na parte inferior da página, com o nome
de todos os seus alunos na seguinte ordem: do aluno que concluiu mais atividades para o que concluiu menos.

A primeira coluna contém o número de total de atividades não concluídas. Por isso, esse número será mais baixo para o primeiro aluno.

Importante: Essa tabela permite apenas uma comparação relativa entre os próprios alunos, e não uma comparação absoluta, pois nem todos os itens marcados como atividades são realmente atividades.

'''

import pandas as pd

# Lendo os arquivos e criando os dataframes
alunos = pd.read_csv('courseid_3858_participants.csv')
log = pd.read_csv('progress.20221_meta_turma_mps005-ta1-ta2-tb1-tb2-tc1-tc2-td1-td2.csv')

# Organizando o dataframe dos alunos
alunos["Nome_Completo"] = alunos["Nome"] + " " + alunos["Sobrenome"]
alunos = alunos.sort_values("Nome_Completo")

# Organizando o dataframe de conclusão de atividades
log = log.rename({'Unnamed: 0':'Nome'}, axis = 1)
log = log.drop(['Endereço de email'], axis = 1)
coluna_count = 3
while coluna_count <= 183:
    indice = 'Unnamed: ' + str(coluna_count)
    from contextlib import suppress
    with suppress(Exception):
        log = log.drop([indice], axis = 1)
    coluna_count += 2

# Separando a lista dos alunos do(a) professor(a)
meus_alunos = alunos["Nome_Completo"].tolist()
for aluno in range(len(log)):
    if log.at[aluno,'Nome'] not in meus_alunos:
        log.drop(aluno, axis = 0, inplace = True)

# Construindo a tabela comparativa final
log.set_index('Nome', inplace=True)
log = log.sort_values("Nome")
log['Sem Conclusão'] = log[log == 'Não concluído'].count(axis=1)
log = log.sort_values(by = 'Sem Conclusão', ascending=True)

# Criando a primeira coluna da tabela com a totalização das atividades não concluídas
first_column = log.pop('Sem Conclusão')
log.insert(0, 'Sem Conclusão', first_column)

# Colorindo as atividades não concluídas
def color_negative_red(val):
    # Takes a scalar and returns a string with the css property `'color:
    # red'` for negative strings, black otherwise.
    color = 'red' if val == 'Não concluído' else 'white'
    return 'color: %s' % color

log.style.applymap(color_negative_red)