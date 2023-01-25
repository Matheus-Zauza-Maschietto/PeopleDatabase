import PySimpleGUIQt as sg
import sqlite3 as sql
import datetime
import os
import imghdr
from PIL import Image
from base64 import b64encode, b64decode


class projetoFuncionarios:
    def __init__(self):
        #sg.Theme('Reddit')
        # Abrindo banco de dados
        self.criandoBDDsqlite()

        # Criando pasta para manter as fotos dos funcionarios
        if not os.path.exists('CacheFuncionarios'):
            os.makedirs('CacheFuncionarios')

        # Recebendo os nomes e sobre nomes dos funcionarios
        listaPessoas = self.mostrandolistaPessoa()

        # Deixando em ordem alfabetica a lista de pessoas
        listaPessoas.sort()

        # Titulo do texto
        titulo = [[sg.T('SELECIONAR PERFIL', justification='center', font=['calibri', 30])]]

        # List compreension dos botões para perfies
        linhaBotoes = [
            [sg.B(f'{listaPessoas[y][0]}', size=(70, 1.5), font=['y', 20]) for x in range(1)] for y
            in
            range(len(listaPessoas))]

        # Transformando em uma lista com possibilidade de descer e subir
        colunaScroll = [[sg.Column(linhaBotoes, size=(800, 400), scrollable=True)]]

        # Botões de opções
        botoes = [[sg.B('Sair', font=['Helvetica', 20], size=(7, 1.7)),
                   sg.B('Criar Perfil', font=['Helvetica', 20], size=(16, 1.7))]]

        # Somando as lista para usar como layout
        layout_inicial = titulo + colunaScroll + botoes

        # Iniciando janela principal
        janela_inicial = sg.Window('Tela Inicial', layout=layout_inicial, size=(800, 500))
        while True:
            self.key, value = janela_inicial.read()

            # If para fechar a janela
            if self.key == sg.Window.Close or self.key == 'Sair':
                break

            # If para criar um perfil
            if self.key == 'Criar Perfil':
                janela_inicial.Hide()
                self.telaAdicionar()
                janela_inicial.UnHide()

            if self.key != 'Criar Perfil' and self.key != sg.Window.Close and self.key != 'Sair':
                janela_inicial.Hide()
                self.telaAmostragem(self.key)
                janela_inicial.UnHide()

    def telaAdicionar(self):
        # Tela para adicionar novos perfis

        dataatual = datetime.datetime.now().year
        # salvando o ano atual

        # Titulo
        layoutAdicionar = [[sg.T('Tela de Adicionar', justification='center', font=['calibri', 30])],
                           # Campo do nome
                           [sg.T('Nome', font=['calibri', 20], size=(7, 1.5)),
                            sg.I(font=['calibri', 20], size=(81, 1.2))],
                           # Campo do sobrenome
                           [sg.T('Sobrenome ', font=['calibri', 20], size=(13, 1.5)),
                            sg.I(font=['calibri', 20], size=(75, 1.2))],
                           # campo da data de nascimento e sexo
                           [sg.T('Data de Nascimento', font=['calibri', 20], size=(23, 1.5)),
                            sg.Combo([x for x in range(1, 32)], font=['calibri', 20], size=(6, 1), readonly=True),
                            sg.T('/', font=['calibri', 20], size=(2, 1.5)),
                            sg.Combo([x for x in range(1, 13)], font=['calibri', 20], size=(6, 1), readonly=True),
                            sg.T('/', font=['calibri', 20], size=(2, 1.5)),
                            sg.Combo([x for x in range(dataatual, 1900, -1)], font=['calibri', 20], size=(9, 1), readonly=True),
                            sg.T('  Sexo', font=['calibri', 20], size=(7, 1.5)),
                            sg.Combo(['Masculino', 'Feminino', 'Outro'], font=['calibri', 20], size=(14, 1))],
                           # Campo do email
                           [sg.T(' E-Mail', font=['calibri', 20], size=(8, 1.5)),
                            sg.I(font=['calibri', 20], size=(80, 1.1))],
                           # Campo numero de telefone
                           [sg.T('N° Telefone', font=['calibri', 20], size=(13, 1.5)),
                            sg.I(font=['calibri', 20], size=(30, 1.1))],
                           # Campo da cidade e bairro
                           [sg.T('Cidade', font=['calibri', 20], size=(8, 1.5)),
                            sg.I(font=['calibri', 20], size=(35, 1.1)),
                            sg.T('Bairro', font=['calibri', 20], size=(8, 1.5)),
                            sg.I(font=['calibri', 20], size=(36, 1.1))],
                           # Campo do endereço e complemento
                           [sg.T('Endereço', font=['calibri', 20], size=(10, 1.5)),
                            sg.I(font=['calibri', 20], size=(78, 1.1))],
                           [sg.T('Complemento', font=['calibri', 20], size=(16, 1.5)),
                            sg.I(font=['calibri', 20], size=(72, 1.1))],
                           [sg.T('Adicionar imagem aqui', font=['calibri', 20], enable_events=True, key='imagem')],
                           # Botões de voltar e sair
                           [sg.B('Voltar', font=['calibri', 20], size=(8, 1.7)),
                            sg.B('Salvar', font=['calibri', 20], size=(8, 1.7))]]

        # Variavel referente a janela
        janelaAdicionar = sg.Window('Tela de Adicionar', layoutAdicionar)

        # Contador para impedir que a pessoa saia sem colocar uma imagem
        contador = 0
        while True:
            # Lendo valores e keys
            key, value = janelaAdicionar.read()

            if key == sg.Window.Close or key == 'Voltar' or self.key == 'Sair' or self.key == sg.Window.Close:
                # If para fechar janela e voltar a tela inicial
                janelaAdicionar.close()
                break

            elif key == 'imagem':
                # If para verificar se o arquivo existe e se é uma imagem e transformar-la em binario
                imagemCaminho = sg.popup_get_file('Escolha a Imagem de perfil', no_window=True)
                # if para resolver problema caso a janela seja fechada sem digitar um caminho
                if os.path.exists(imagemCaminho):
                    verification = self.verificacao(imagemCaminho)
                    if verification:
                        self.imagemBDD = self.mudandoTamanhoImagem(imagemCaminho)
                        contador += 1
                    else:
                        sg.PopupOK('ERRO o arquivo selecionado não possui uma extensão aceita')

            if key == 'Salvar':
                if contador >= 1:
                    temCerteza = sg.popup_yes_no('Tem Certeza que deseja salvar')
                    if temCerteza == 'Yes':
                        # Fechando a janela e passando os valores
                        datadeNascimento, idade = self.transformandoSTR(value[2], value[3], value[4])
                        self.adicionandoDados(value, datadeNascimento, idade, self.imagemBDD)
                        janelaAdicionar.close()
                        break

                elif contador < 1:
                    sg.popup_ok('Adicione uma imagem para salvar')

    # -----------------------------------------------------------------------------
    # DEFs relacionados a janela usada para adicionar novos perfies

    def verificacao(self, path):
        if os.path.isfile(path):
            extensao = self.identificandoExtensao(path)
            if extensao != False:
                return True
            else:
                return False

    def adicionandoDados(self, valores, DataNscimento, Idade, imagemCodificada):
        # Adicionando os valore captados pela tela adicionar
        # Junção das strings para formar o nome completo
        nome = f'{valores[0]} {valores[1]}'
        self.mouse.execute('INSERT INTO funcionarios VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                           (nome, DataNscimento, Idade, valores[5], valores[6], valores[7],
                            valores[8], valores[9], valores[10], valores[11], imagemCodificada))
        self.BDD.commit()

    def transformandoSTR(self, dia, mes, ano):
        # Transformando em STR a data de nascimento e a idade
        mes_Atual = datetime.datetime.now().month
        dia_Atual = datetime.datetime.now().day
        ano_Atual = datetime.datetime.now().year
        if mes_Atual == mes:
            if dia_Atual >= dia:
                idade = ano_Atual - ano
            elif dia_Atual < dia:
                idade = (ano_Atual - ano) - 1
        elif mes_Atual < mes:
            idade = (ano_Atual - ano) - 1
        else:
            idade = ano_Atual - ano
        dataNascimento = f'{dia}/{mes}/{ano}'
        dataNascimento = str(dataNascimento)
        idade = str(idade)
        return dataNascimento, idade

    def identificandoExtensao(self, pathArquivo):
        # Identifica a extensão da imagem e salva em uma variavel que será retornada
        listaExtensoes = ['jpeg', 'png', 'jpg', 'JPG', 'JPEG', 'PNG']
        if imghdr.what(pathArquivo) in listaExtensoes:
            for c in range(0, len(listaExtensoes)):
                if imghdr.what(pathArquivo) == listaExtensoes[c]:
                    extensao = listaExtensoes[c]
                    return extensao
        else:
            # Usado para verificiar antes de entrar em outras funções
            return False

    def mudandoTamanhoImagem(self, arquivo):
        # Mudando de tamanho a imagem
        imagem = Image.open(arquivo)
        imagem_resize = imagem.resize((300, 260))
        # Função necessaria para identificar
        extensão = self.identificandoExtensao(arquivo)
        # Retirando extensões para que não haja erro de nomes iguais
        if extensão in 'jpg''png''JPG''PNG':
            arquivo = arquivo[:-4]
        elif extensão in 'JPEG''jpeg':
            arquivo = arquivo[:-5]
        # Dando um nome especial para o arquivo para não haver problema de arquivos iguais
        pathResized = arquivo + '212412456776809.png'
        imagem_resize.save(pathResized)
        # Função necessaria para transformar a imagem em binario
        imagemBinaria = self.transformandoImagem(pathResized)
        # Excluindo arquivo criado para não deixar vestigios
        os.remove(pathResized)
        return imagemBinaria

    def transformandoImagem(self, caminhoImagem):
        # transformando uma imagem normal em uma imagem binaria
        with open(caminhoImagem, 'rb') as file:
            imagemBinaria = b64encode(file.read())
        return imagemBinaria

    # -----------------------------------------------------------------------------
    # DEFs relacionados a tela de perfil de cada usuario

    def telaAmostragem(self, funcionario):
        # DEF para selecionar imagem do funcionario
        dadosFuncionario = self.recebendoDados(funcionario)

        # DEF para decodificar e enviar foto para pasta de Cache
        # Retirando valor de dentro da tupla e da lista
        self.abrindoFoto(dadosFuncionario[0][10], funcionario)

        layoutAmostragem = [[sg.Image(rf'CacheFuncionarios\{funcionario}'),
                             sg.Frame(layout=[[sg.T('Nome:', font=['calibri', 20], size=(8, 1)),
                                               sg.T(f'{dadosFuncionario[0][0]}', font=['calibri', 20])],
                                              [sg.T('Data de Nascimento:', font=['calibri', 20], size=(23, 1)),
                                               sg.T(f'{dadosFuncionario[0][1]}', font=['calibri', 20])],
                                              [sg.T('Idade:', font=['calibri', 20], size=(7, 1)),
                                               sg.T(f'{dadosFuncionario[0][2]} Anos', font=['calibri', 20],
                                                    size=(11, 1)),
                                               sg.T('Sexo:', font=['calibr', 19], size=(7, 1)),
                                               sg.T(f'{dadosFuncionario[0][3]}', font=['calibri', 20])],
                                              [sg.T('E-mail:', font=['calibri', 20]),
                                               sg.T(f'{dadosFuncionario[0][4]}', font=['calibri', 20])],
                                              [sg.T('Telefone:', font=['calibri', 20], size=(10, 1)),
                                               sg.T(f'{dadosFuncionario[0][5]}', font=['calibri', 20])],
                                              [sg.T('Cidade:', font=['calibri', 20], size=(8, 1)),
                                               sg.T(f'{dadosFuncionario[0][6]}', font=['calibri', 20]),
                                               sg.T('Bairro:', font=['calibri', 20], size=(8, 1)),
                                               sg.T(f'{dadosFuncionario[0][7]}', font=['calibri', 20])],
                                              [sg.T('Endereço:', font=['calibri', 20], size=(11, 1)),
                                               sg.T(f'{dadosFuncionario[0][8]}', font=['calibri', 20])],
                                              [sg.T('Complemento:', font=['calibri', 20], size=(17, 1)),
                                               sg.T(f'{dadosFuncionario[0][9]}', font=['calibri', 20])]], title=None)],
                            [sg.B('Voltar', font=['calibri', 20], size=(10, 1.7)),
                             sg.B('Editar Perfil', font=['calibri', 20], size=(14, 1.7)),
                             sg.B('Excluir Perfil', font=['calibri', 20], size=(17, 1.7))]]

        janelaAmostragem = sg.Window(f'Perfil de {funcionario}', layoutAmostragem)
        while True:
            key, value = janelaAmostragem.read()
            if key == sg.Window.Close or key == 'Voltar':
                janelaAmostragem.close()
                break

            if key == 'Editar Perfil':
                janelaAmostragem.Hide()
                self.telaEdita(funcionario)
                janelaAmostragem.UnHide()

            if key == 'Excluir Perfil':
                confirma = sg.PopupYesNo(f'Tem certeza que deseja excluir o perfil {funcionario} ?')
                if confirma == 'Yes':
                    # Excluindo perfil do banco de dados e da pasta cache
                    self.excluindoPerfil(funcionario)
                    sg.PopupOK('Reinicie o programa para efetivar a mudança')

    def excluindoPerfil(self, funcionario):
        # Deletando um perfil
        quarry = f'DELETE FROM funcionarios WHERE nomesobrenome = "{funcionario}"'
        self.mouse.execute(quarry)
        self.BDD.commit()
        os.remove(rf'CacheFuncionarios\{funcionario}.png')

    def recebendoDados(self, funcionario):
        # Selecionando a imagem respectiva ao nome
        self.mouse.execute(f'SELECT * FROM funcionarios WHERE nomesobrenome = "{funcionario}"')
        return self.mouse.fetchall()

    def abrindoFoto(self, fotoEncodada, funcionario):
        # Decodificando a imagem encodificada com base64 e colocando-á na pasta de cache
        decodeit = open(rf'CacheFuncionarios\{funcionario}.png', 'wb')
        decodeit.write(b64decode(fotoEncodada))
        decodeit.close()

    # -----------------------------------------------------------------------------
    # DEFs relacionados a tela de atualização de perfil

    def telaEdita(self, funcionario):
        # Layout da tela de edição de perfil
        layout = [[sg.Frame(layout=[[sg.T('                     ', size=(20, 2))],
                                    [sg.T('Foto', justification='center', font=['calibri', 30], enable_events=True,
                                          key='Foto')],
                                    [sg.T('                     ', size=(20, 2))]], title=None),
                   sg.Frame(
                       layout=[[sg.T('Nome', font=['calibri', 28], size=(10, 1.5), enable_events=True, key='Nome')],
                               [sg.T('Data de Nascimento', font=['calibri', 28], size=(32, 1.5),
                                     enable_events=True, key='Data de Nascimento')],
                               [sg.T('Sexo', font=['calibri', 28], size=(14, 1.5), enable_events=True, key='Sexo')],
                               [sg.T('E-Mail', font=['calibri', 28], size=(20, 1.5), enable_events=True, key='E-Mail'),
                                sg.T('Numero de Telefone', font=['calibri', 28], enable_events=True,
                                     key='Numero de Telefone')],
                               [sg.T('Cidade', font=['calibri', 28], size=(20, 1.5), enable_events=True, key='Cidade'),
                                sg.T('Bairro', font=['calibri', 28], enable_events=True, key='Bairro')],
                               [sg.T('Endereço', font=['calibri', 28], size=(20, 1.5), enable_events=True,
                                     key='Endereço'),
                                sg.T('Complemento', font=['calibri', 28], size=(26, 1.5), enable_events=True,
                                     key='Complemento')]], title=None)],
                  [sg.B('Voltar', font=['calibri', 20], size=(10, 1.7))]]

        listaNormais = ['Nome', 'E-Mail', 'Numero de Telefone', 'Cidade', 'Bairro', 'Endereço', 'Complemento']
        listaSQLite = ['nomesobrenome', 'email', 'numeroTelefone', 'cidade', 'bairro', 'endereco', 'complemento']

        # Abrindo janela de edição
        janelaEdicao = sg.Window(f'Editando Perfil de {funcionario}', layout)
        while True:
            key, value = janelaEdicao.read()

            if key == sg.Window.Close or key == 'Voltar':
                # Identificando se o usuario gostaria de voltar
                janelaEdicao.Close()
                break

            if key in listaNormais:
                # Identificando se a key esta em um dos campos que não exigem alteração na estrutura
                for campo in range(len(listaNormais)):
                    if key == listaNormais[campo]:
                        while True:
                            alteracaoNormal = sg.PopupGetText(f'Digite um novo {listaNormais[campo]}',
                                                              title=f'Alterando {listaNormais[campo]}',
                                                              font=['calibri', 20], keep_on_top=True)
                            if alteracaoNormal is None:
                                # Quebra a estrutura de repetição caso a ação seja cancelada
                                break

                            elif alteracaoNormal.strip() == '':
                                # Previne que não seja executado com um valor vazio
                                sg.Popup('Valor invalido, tente digitar algo para proseguir',
                                         title='Valor Invalido Digitado')

                            else:
                                # Confirma se o usuario realmente deseja alterar o campo selecionado
                                confirmacao = sg.PopupYesNo(
                                    f'Tem certeza que deseja alterar o {listaNormais[campo]} do perfil {funcionario} para: {alteracaoNormal}?',
                                    font=['calibri', 16])
                                if confirmacao == 'Yes':
                                    # Def para alterar no banco de dados os dados
                                    self.alterandoCampo(funcionario, listaSQLite[campo], alteracaoNormal)
                                    break

            if key == 'Sexo' or key == 'Data de Nascimento':
                # Janela destinada a mudança do campo sexo e data de nascimento
                if key == 'Sexo':
                    # Layout que a janela receberá caso o campo a ser editado for sexo
                    layout = [[sg.T('Selecione um novo sexo', font=['calibri', 20])],
                              [sg.Combo(['Masculino', 'Feminino', 'Outro'], font=['calibri', 20], size=(14, 1))],
                              [sg.B('Voltar', font=['calibri', 20]), sg.B('Confirmar', font=['calibri', 20])]]
                    campoSQL = 'sexo'

                else:
                    # Layout que a janela receberá caso o campo a ser editado for data de nascimento
                    anoAtual = datetime.datetime.now().year
                    # variavel que recebe o ano atual
                    layout = [[sg.T('Selecione uma nova data de nascimento', font=['calibri', 20])],
                              [sg.Combo([x for x in range(1, 32)], font=['calibri', 20], size=(6, 1)),
                               sg.T('/', font=['calibri', 20], size=(2, 1.5)),
                               sg.Combo([x for x in range(1, 13)], font=['calibri', 20], size=(6, 1)),
                               sg.T('/', font=['calibri', 20], size=(2, 1.5)),
                               sg.Combo([x for x in range(anoAtual, 1900, -1)], font=['calibri', 20], size=(9, 1))],
                              [sg.B('Voltar', font=['calibri', 20]), sg.B('Confirmar', font=['calibri', 20])]]
                    campoSQL = 'dataNascimento'

                janelaAlteracao = sg.Window(f'Alterando {key}', layout, keep_on_top=True)
                while True:
                    # Lendo valores e keys
                    key, value = janelaAlteracao.read()
                    if key == 'Voltar' or key == sg.Window.Close:
                        janelaAlteracao.close()
                        break
                    if key == 'Confirmar':
                        confirmacao = sg.PopupYesNo(
                            f'Tem Certeza que deseja mudar campo o {key} do perfil {funcionario}', font=['calibri', 16],
                            keep_on_top=True)
                        if confirmacao == 'Yes':
                            if campoSQL == 'dataNascimento':
                                # Selecioando os itens da variavel para a data de nascimento
                                dataCerta, idade = self.transformandoSTR(value[0], value[1], value[2])
                                self.alterandoCampo(funcionario, campoSQL, dataCerta)
                                self.alterandoIdade(idade, funcionario)
                                janelaAlteracao.close()
                                break
                            else:
                                # Selecionando o primeiro item da variavel para o sexo
                                self.alterandoCampo(funcionario, campoSQL, value[0])
                                janelaAlteracao.close()
                                break

            if key == 'Foto':
                layout = [[sg.T(f'Alterando a imagem de perfil do perfil {funcionario}', font=['calibri', 20])],
                          [sg.T('Para adicionar uma nova imagem', font=['calibri', 20]),
                           sg.T('Clique aqui', font=['calibri', 24], enable_events=True, key='adicionar imagem')],
                          [sg.B('Voltar', font=['calibri', 20], size=(11, 1)),
                           sg.B('Confirmar', font=['calibri', 20], size=(14, 1))]]
                # variavel destinada a descobrir se foi selecionada uma foto para que seja possivel confirmar o processo
                confirmacaoRecebimentoImagem = False

                janelaAlteracaoImagem = sg.Window(f'Alterando a imagem', layout, keep_on_top=True)
                while True:
                    # Lendo as keys e valores de janelaAlteracaoImagem
                    key, value = janelaAlteracaoImagem.read()

                    if key == 'Voltar' or key == sg.Window.Close:
                        # Caso deseje fechar a janela
                        janelaAlteracaoImagem.close()
                        break

                    if key == 'adicionar imagem':
                        # Popup para selecionar o arquivo
                        fotoPath = sg.PopupGetFile('Escolha a imagem', no_window=True,
                                                   title='Escolha a imagem substituta')

                        if os.path.exists(fotoPath):
                            # Verifica se existe esse path
                            verifica = self.verificacao(fotoPath)

                            if verifica:
                                # Confirma que foi adicionado uma imagem
                                # recebe em uma variavel a imagem codificada em base64
                                confirmacaoRecebimentoImagem = True
                                self.imagemBinario = self.mudandoTamanhoImagem(fotoPath)

                            else:
                                # Trata o erro de extensão errada
                                sg.PopupOK('ERRO, O formato do arquivo não é aceito')
                        else:
                            # Trata o erro de path errado
                            sg.PopupOK('ERRO, Não foi possivel encontrar o arquivo')

                    if key == 'Confirmar':
                        # Confirma se a imagem foi recebida
                        if confirmacaoRecebimentoImagem:
                            confirma = sg.popup_yes_no('Deseja Confirmar a mudança ?', keep_on_top=True)
                            # Confirma se o usuario deseja confirma o processo
                            if confirma == 'Yes':
                                self.alterandoCampo(funcionario, 'imagem', self.imagemBinario)
                                janelaAlteracaoImagem.close()
                                break
                        else:
                            sg.PopupOK('Voce não adicionou nenhuma imagem, Adicione uma para proseguir')

    def alterandoCampo(self, funcionario, campoSQLite, alteracao):
        # Função usada para adicionar todas informações no SQLite
        quarry = f"UPDATE funcionarios SET {campoSQLite} = ? WHERE nomesobrenome = ?"
        self.mouse.execute(quarry, (alteracao, funcionario))
        self.BDD.commit()

    def alterandoIdade(self, idadeCerta, funcionario):
        quarry = f"UPDATE funcionarios SET idade = ? WHERE nomesobrenome = ?"
        self.mouse.execute(quarry, (idadeCerta, funcionario))
        self.BDD.commit()

    # -----------------------------------------------------------------------------
    # DEFs usados na tela inicial

    def criandoBDDsqlite(self):
        # Inicia banco de dados e cria uma mesa caso ela não exista
        self.BDD = sql.connect('banco_de_dados.db')
        self.mouse = self.BDD.cursor()
        self.mouse.execute('CREATE TABLE IF NOT EXISTS funcionarios(nomesobrenome TEXT,'
                           'dataNascimento TEXT, idade CHARACTER, sexo TEXT, email TEXT, numeroTelefone TEXT,'
                           ' cidade TEXT, bairro TEXT, endereco TEXT,'
                           ' complemento TEXT, imagem BLOB)')

    def mostrandolistaPessoa(self):
        # Devolve ao inicio uma lista com os nomes e sobrenomes dos funcionarios para escolha
        self.mouse.execute('SELECT nomesobrenome FROM funcionarios')
        return self.mouse.fetchall()


inicar = projetoFuncionarios()
