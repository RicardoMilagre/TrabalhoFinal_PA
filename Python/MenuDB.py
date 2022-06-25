
from tkinter import *
import Reconhecimento
from PDF.PDF import LoadPDF
import pymssql
from HTML.HTML import printit
import sys

# DEFINIÇÃO DE FUNÇÕES
def fetch():   # SOFTWARE DE RECONHECIMENTO FACIAL
    Reconhecimento.ReconhecimentoFacial()

def MenuDataBase():  # MENU DA DATABASE

    def confirmar(): # DEPENDENDO DO QUE O USER SELECIONAR EM BOTAO DE ESCOLHA, APRESENTA A DB.
        if variavel.get() == "Produtos":
            ListaProdutos()
            ChangeLog_Generic("Produtos")
        elif variavel.get() == "Marcas":
            ListaMarcas()
            ChangeLog_Generic("Marcas")
        elif variavel.get() == "Fornecedores":
            ListaFornecedores()
            ChangeLog_Generic("Fornecedores")
        elif variavel.get() == "Tipo de Produtos":
            ListaTipoProdutos()
            ChangeLog_Generic("Tipo de Produtos")

    def AdicionarBD(): # SABE QUAL A DB ABERTA NA FUNÇÃO ANTERIOR E FAZ APPEND À ABERTA
        if variavel.get() == "Produtos":
            AdicionarProdutos()
        elif variavel.get() == "Marcas":
            AdicionarMarcas()
        elif variavel.get() == "Fornecedores":
            AdicionarFornecedores()
        elif variavel.get() == "Tipo de Produtos":
            AdicionarTipoProdutos()

    def AdicionarBD_UPD(): # SABE QUAL A DB ABERTA NA FUNÇÃO ANTERIOR E FAZ O UPDATE À ABERTA
        if variavel.get() == "Produtos":
            UpdateProdutos()
        elif variavel.get() == "Marcas":
            UpdateMarcas()
        elif variavel.get() == "Fornecedores":
            UpdateFornecedores()
        elif variavel.get( ) == "Tipo de Produtos":
            UpdateTipoProdutos()

    def DeleteBD_UPD(): # SABE QUAL A DB ABERTA NA FUNÇÃO ANTERIOR E FAZ O DELETE À ABERTA
        if variavel.get() == "Produtos":
            DeleteProdutos()
        elif variavel.get() == "Marcas":
            DeleteMarcas()
        elif variavel.get() == "Fornecedores":
            DeleteFornecedores()
        elif variavel.get() == "Tipo de Produtos":
            DeleteTipoProdutos()


    def ChangeLog_Generic(x): # CHANGELOG GENERICO QUE INDICA QUAL A DB ABERTA AO USER, BEM COMO OPÇÕES DISPONIVEIS
        tabela = x
        tabelaPrint = Label(ChangeLogTEXT, text=(
                    "Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS - A apresentar resultados da tabela " + tabela +
                    "\n\nSERVIÇOS DISPONIVEIS:\n1 - ADICIONAR: Insira um valor/item novo na BD (Não insira o id)\n2 - DELETE: Insira o valor do ID para este ser apagado"
                    "\n3 - MODIFY: Insira o valor do ID do produto seguido dos campos presentes a alterar"),
                            anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
        tabelaPrint.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)

    def ChangeLog_Generic_NOVALUES(x):  # CASO O USER PRETENDA APPEND/DELETE/UPDATE SEM VALORES DA INDICAÇÃO DE ERRO
        tabela = x
        tabelaPrint = Label(ChangeLogTEXT, text=(
                    "Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS - A apresentar resultados da tabela " + tabela +
                    "\n\nDADOS NÃO INSERIDOS\n\nPor favor insira os dados e selecione uma opção"),
                            anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
        tabelaPrint.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)

    ################################################################################################################
    ####                                      DEFINIÇÃO DE SQL FORNECEDORES                                     ####
    ################################################################################################################

    def ListaFornecedores():    # APRESENTA LISTA DE FORNECEDORES
        mydb = pymssql.connect('srvsql-ipt.ddns.net', '81750', '81750', "PA_81750_81810_81817_81818")
        cursor = mydb.cursor(as_dict=True) #CONNECT à DB
        querys = ['SELECT idFornecedor, nomeFornecedor,contacto,email FROM Fornecedores'] #QUERY
        cab = []        # RETIRA OS ELEMENTOS DO DICIONARIO UM A UM. CRIA 2 VARIAVEIS QUE GUARDAM OS NOMES NAS TABELAS
        tab = []        # E OS PRODUTOS
        cursor.execute(querys[0])
        for x in cursor:    #SEPARA OS KEYS DOS ARGUMENTOS.
            for key, value in x.items():
                cab.append(key)
                tab.append(str(value))
        cab = list(dict.fromkeys(cab))  # CODIGO PARA APAGAR REPETIDOS, DE FORMA A TERMOS APENAS UM LABEL DE KEYS.
        r1 = len(tab)                   #GUARDA TAMANHO DA TAB
        n = [n for n in range(0, r1, 4)] #  N É UMA LISTA QUE PRECORRE OS ELEMENTOS DE TAB, E QUE DE 4 EM 4 OS SEPARA
        f1 = list()                      # NESTE CASO FORAM 4, MAS O CÓDIGO É DINAMICO E É UTILIZADO NAS OUTRAS LISTAS.
        for item in n:                   # APENAS É NECESSÁRIO MUDAR O PASSO.
            v = tab[item:item + 4]       # V VAI TER  A UNIÃO DE ITEMS 4 A 4. (DINAMICO NOVAMENTE, USADO EM TODOS OS RESTANTES)
            f1.append(v)                 #F1 VAI TER COMO RESULTADO APENAS OS VALUES ORIGINAIS.
        ViewerTEXTscroll = Scrollbar(ViewerTEXT)    # CRIAÇÃO DE SCROLLBAR QUE VARIA DE ACORDO COM TAMANHO DA LISTA
        ViewerTEXTscroll.pack(side=RIGHT,fill=Y)
        listbox = Listbox(ViewerTEXT, yscrollcommand=ViewerTEXTscroll.set)
        listbox.insert(END,str(cab))
        for a in f1:                    # INSERE CADA ELEMENTO NA LISTBOX.
            listbox.insert(END,a)
        listbox.place(x=5,y=5,width=760, height=775)    #COLOCAÇÃO DA LISTBOX
        listbox.config(width=500,justify=LEFT,)
        ViewerTEXTscroll.config(command=listbox.yview)

    def AdicionarFornecedores():    # ADICIONA FORNECEDORES
        mydb = pymssql.connect('srvsql-ipt.ddns.net', '81817', '81817', "PA_81750_81810_81817_81818")
        cursor = mydb.cursor(as_dict=True)
        sql = "INSERT INTO fornecedores(nomeFornecedor,contacto,email) VALUES (%s,%d,%s)" #QUERY
        if (ENTRADA2.get()==""):    # SE ENTRADA FOR VAZIA, REDIRECIONA PARA CHANGELOG ERRO. USADO EM TODAS AS FUNÇÕES APPEND,DELETE,MODIFY
            ChangeLog_Generic_NOVALUES("Fornecedores")
            breakpoint
        else:
            val = []
            for x in (ENTRADA2.get()).split(","): # CADA VEZ QUE DETECTA UMA ',' RECONHECE COMO SENDO UM NOVO PARAMETRO.
                val.append(x)                     # CADA VEZ QUE TEM ESSE PARAMETRO FAZ APPEND.
            val2 = (str(val[0]), int(val[1]), str(val[2]))
            try:
                if len(val) > 3:       # EXCEPÇÕES USADAS USADOS EM TODOS AS FUNÇÕES DE UPDATE/APPEND/DELETE. SERVEM PARA COMUNICAR AO USER NO CHANGLOG
                    imprimir = Label(ChangeLogTEXT, # ERROS OBTIDOS. CASO SEJA REALIZADO COM SUCESSO TAMBÉM É COMUNICADO AO USER.
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nFALHA A ADICIONAR À BASE DE DADOS",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
                elif len(val) == 3:
                    cursor.execute(sql, val2) #EXECUTA EM SQL
                    mydb.commit() #NECESSARIO COMMIT PARA REALIZAR ALTERAÇÃO. SEM ISSO NÃO GRAVA MUDANÇAS.
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nADICIONADO À BASE DE DADOS COM SUCESSO",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
            except:
                imprimir = Label(ChangeLogTEXT,
                                 text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nUNEXPECTED ERROR 12286. VERY UNEXPECTED...",
                                 anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)

    def UpdateFornecedores(): # UPDATE FORNECEDORES
        mydb = pymssql.connect('srvsql-ipt.ddns.net', '81750', '81750', "PA_81750_81810_81817_81818")
        cursor = mydb.cursor(as_dict=True)
        sql = "UPDATE fornecedores SET nomeFornecedor=%s,contacto=%d,email=%s WHERE idFornecedor = %d"
        if (ENTRADA2.get()==""):
            ChangeLog_Generic_NOVALUES("Fornecedores")
            breakpoint
        else:
            val = []
            for x in (ENTRADA2.get()).split(","):
                val.append(x)
            val2 = (str(val[1]), int(val[2]), str(val[3]), int(val[0]))
            try:
                if len(val)>4:
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nFALHA A ADICIONAR À BASE DE DADOS",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
                elif len(val) == 4:
                    cursor.execute(sql, val2)
                    mydb.commit()
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nALTERADA NA BASE DE DADOS COM SUCESSO",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
            except:
                imprimir = Label(ChangeLogTEXT,
                                 text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nUNEXPECTED ERROR 12286. VERY UNEXPECTED...",
                                 anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)

    def DeleteFornecedores():
        mydb = pymssql.connect('srvsql-ipt.ddns.net', '81750', '81750', "PA_81750_81810_81817_81818")
        cursor = mydb.cursor(as_dict=True)
        sql = "DELETE FROM fornecedores WHERE idFornecedor = %d"
        if (ENTRADA2.get()==""):    # SE ENTRADA FOR VAZIA, REDIRECIONA PARA CHANGELOG ERRO
            ChangeLog_Generic_NOVALUES("Fornecedores")
            breakpoint
        else:
            val = ENTRADA2.get()
            try:
                if val == "":
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nFALHA A ADICIONAR À BASE DE DADOS",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
                else:
                    cursor.execute(sql, val)
                    mydb.commit()
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nALTERADA NA BASE DE DADOS COM SUCESSO",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
            except:
                imprimir = Label(ChangeLogTEXT,
                                 text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nUNEXPECTED ERROR 12286. VERY UNEXPECTED...",
                                 anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)

    ################################################################################################################
    ####                                 DEFINIÇÃO DE PRODUTOS/TIPO PRODUTOS                                    ####
    ################################################################################################################
    def ListaProdutos():
        mydb = pymssql.connect('srvsql-ipt.ddns.net', '81817', '81817', "PA_81750_81810_81817_81818")
        cursor = mydb.cursor(as_dict=True)
        querys = ['SELECT idProduto, nomeProduto, stockComprado, stockVendido,idMarca,idTipoProduto,idFornecedor FROM produtos']
        cab = []
        tab = []  #JÁ EXPLICADO
        cursor.execute(querys[0])
        for x in cursor:
            for key, value in x.items():
                cab.append(key)
                tab.append(str(value))
        cab = list(dict.fromkeys(cab))
        r1 = len(tab)
        n = [n for n in range(0, r1, 7)]
        f1 = list()
        for item in n:
            v = tab[item:item + 7]
            f1.append(v)
        ViewerTEXTscroll = Scrollbar(ViewerTEXT)
        ViewerTEXTscroll.pack(side=RIGHT,fill=Y)
        listbox = Listbox(ViewerTEXT, yscrollcommand=ViewerTEXTscroll.set)
        listbox.insert(END,str(cab))
        for a in f1:
            listbox.insert(END,a)
        listbox.place(x=5,y=5,width=760, height=775)
        listbox.config(width=500,justify=LEFT,)
        ViewerTEXTscroll.config(command=listbox.yview)

    def ListaTipoProdutos():
        mydb = pymssql.connect('srvsql-ipt.ddns.net', '81817', '81817', "PA_81750_81810_81817_81818")
        cursor = mydb.cursor(as_dict=True)
        querys = ['SELECT idTipoProduto,tipoProduto FROM tipoProdutos']
        cab = []
        tab = []
        cursor.execute(querys[0])
        for x in cursor:
            for key, value in x.items():
                cab.append(key)
                tab.append(str(value))
        cab = list(dict.fromkeys(cab))
        r1 = len(tab)
        n = [n for n in range(0, r1, 2)]
        f1 = list()
        for item in n:
            v = tab[item:item + 2]
            f1.append(v)
        ViewerTEXTscroll = Scrollbar(ViewerTEXT)
        ViewerTEXTscroll.pack(side=RIGHT,fill=Y)
        listbox = Listbox(ViewerTEXT, yscrollcommand=ViewerTEXTscroll.set)
        listbox.insert(END,str(cab))
        for a in f1:
            listbox.insert(END,a)
        listbox.place(x=5,y=5,width=760, height=775)
        listbox.config(width=500,justify=LEFT,)
        ViewerTEXTscroll.config(command=listbox.yview)

    def AdicionarProdutos():
        mydb = pymssql.connect('srvsql-ipt.ddns.net', '81750', '81750', "PA_81750_81810_81817_81818")
        cursor = mydb.cursor(as_dict=True)
        sql = "INSERT INTO produtos(nomeProduto,stockComprado,stockVendido,idMarca,idTipoProduto,idFornecedor) VALUES(%s,%d,%d,%d,%d,%d)"
        val = []
        if (ENTRADA2.get()==""):    # SE ENTRADA FOR VAZIA, REDIRECIONA PARA CHANGELOG ERRO
            ChangeLog_Generic_NOVALUES("Produtos")
            breakpoint
        else:
            for x in (ENTRADA2.get()).split(","):
                val.append(x)
            val2 = (str(val[0]), int(val[1]), int(val[2]), int(val[3]), int(val[4]), int(val[5]))
            try:
                if len(val) > 6:
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nFALHA A ADICIONAR À BASE DE DADOS",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
                elif len(val) == 6:
                    cursor.execute(sql, val2)
                    mydb.commit()
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nADICIONADO À BASSE DE DADOS COM SUCESSO",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
            except:
                imprimir = Label(ChangeLogTEXT,
                                 text="Logged in ao server srvsql-ipt.ddns.net\nSERVIÇOS CONECTADOS\nUNEXPECTED ERROR 12286. VERY UNEXPECTED...",
                                 anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)

    def AdicionarTipoProdutos():
        mydb = pymssql.connect('srvsql-ipt.ddns.net', '81750', '81750', "PA_81750_81810_81817_81818")
        cursor = mydb.cursor(as_dict=True)
        sql = "INSERT INTO tipoProdutos(tipoProduto) VALUES (%s)"
        if (ENTRADA2.get()==""):
            ChangeLog_Generic_NOVALUES("Tipo de Produtos")
            breakpoint
        else:
            val2 = str(ENTRADA2.get())
            try:
                if val2 == "":
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nFALHA A ADICIONAR À BASE DE DADOS",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
                elif val2 != "":
                    cursor.execute(sql, val2)
                    mydb.commit()
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nADICIONADO À BASSE DE DADOS COM SUCESSO",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
            except:
                imprimir = Label(ChangeLogTEXT,
                                 text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nUNEXPECTED ERROR 12286. VERY UNEXPECTED...",
                                 anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)

    def UpdateProdutos():
        mydb = pymssql.connect('srvsql-ipt.ddns.net', '81750', '81750', "PA_81750_81810_81817_81818")
        cursor = mydb.cursor(as_dict=True)
        sql = "UPDATE produtos SET nomeProduto=%s,stockComprado=%d,stockVendido=%d,idMarca=%d,idTipoProduto=%d,idFornecedor=%d WHERE idProduto = %d"
        val = []
        if (ENTRADA2.get()==""):
            ChangeLog_Generic_NOVALUES("Produtos")
            breakpoint
        else:
            for x in (ENTRADA2.get()).split(","):
                val.append(x)
            val2 = (str(val[1]), int(val[2]), int(val[3]), int(val[4]), int(val[5]), int(val[6]), int(val[0]))
            try:
                if len(val)>7:
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nFALHA A ADICIONAR À BASE DE DADOS",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
                elif len(val) == 7:
                    cursor.execute(sql, val2)
                    mydb.commit()
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nALTERADA NA BASE DE DADOS COM SUCESSO",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
            except:
                imprimir = Label(ChangeLogTEXT,
                                 text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nUNEXPECTED ERROR 12286. VERY UNEXPECTED...",
                                 anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)

    def UpdateTipoProdutos():
        mydb = pymssql.connect('srvsql-ipt.ddns.net', '81750', '81750', "PA_81750_81810_81817_81818")
        cursor = mydb.cursor(as_dict=True)
        sql = "UPDATE tipoProdutos SET tipoProduto=%s WHERE idTipoProduto = %d"
        val = []
        if (ENTRADA2.get()==""):
            ChangeLog_Generic_NOVALUES("Tipo de Produtos")
            breakpoint
        else:
            for x in (ENTRADA2.get()).split(","):
                val.append(x)
            val2 = (str(val[1]), int(val[0]))
            try:
                if len(val)>2:
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nFALHA A ADICIONAR À BASE DE DADOS",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
                elif len(val) == 2:
                    cursor.execute(sql, val2)
                    mydb.commit()
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nALTERADA NA BASE DE DADOS COM SUCESSO",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
            except:
                imprimir = Label(ChangeLogTEXT,
                                 text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nUNEXPECTED ERROR 12286. VERY UNEXPECTED...",
                                 anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)

    def DeleteProdutos():
        mydb = pymssql.connect('srvsql-ipt.ddns.net', '81750', '81750', "PA_81750_81810_81817_81818")
        cursor = mydb.cursor(as_dict=True)
        sql = "DELETE FROM produtos WHERE idProduto = %d"
        if (ENTRADA2.get()==""):
            ChangeLog_Generic_NOVALUES("Produtos")
            breakpoint
        else:
            val = ENTRADA2.get()
            try:
                if val == "":
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nFALHA A ADICIONAR À BASE DE DADOS",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
                else:
                    cursor.execute(sql, val)
                    mydb.commit()
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nALTERADA NA BASE DE DADOS COM SUCESSO",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
            except:
                imprimir = Label(ChangeLogTEXT,
                                 text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nUNEXPECTED ERROR 12286. VERY UNEXPECTED...",
                                 anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)

    def DeleteTipoProdutos():
        mydb = pymssql.connect('srvsql-ipt.ddns.net', '81750', '81750', "PA_81750_81810_81817_81818")
        cursor = mydb.cursor(as_dict=True)
        sql = "DELETE FROM tipoProdutos WHERE idTipoProduto = %d"
        if (ENTRADA2.get()==""):
            ChangeLog_Generic_NOVALUES("Tipo de Produtos")
            breakpoint
        else:
            val = ENTRADA2.get()
            try:
                if val == "":
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nFALHA A ADICIONAR À BASE DE DADOS",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
                else:
                    cursor.execute(sql, val)
                    mydb.commit()
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nALTERADA NA BASE DE DADOS COM SUCESSO",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
            except:
                imprimir = Label(ChangeLogTEXT,
                                 text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\numa tab",
                                 anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)

    ################################################################################################################
    ####                                      DEFINIÇÃO DE MARCAS                                               ####
    ################################################################################################################

    def ListaMarcas():
        mydb = pymssql.connect('srvsql-ipt.ddns.net', '81817', '81817', "PA_81750_81810_81817_81818")
        cursor = mydb.cursor(as_dict=True)
        querys = ['SELECT idMarca,nomeMarca FROM Marcas']
        cab = []
        tab = []
        cursor.execute(querys[0])
        for x in cursor:
            for key, value in x.items():
                cab.append(key)
                tab.append(str(value))
        cab = list(dict.fromkeys(cab))
        r1 = len(tab)
        n = [n for n in range(0, r1, 2)]
        f1 = list()
        for item in n:
            v = tab[item:item + 2]
            f1.append(v)
        ViewerTEXTscroll = Scrollbar(ViewerTEXT)
        ViewerTEXTscroll.pack(side=RIGHT,fill=Y)
        listbox = Listbox(ViewerTEXT, yscrollcommand=ViewerTEXTscroll.set)
        listbox.insert(END,str(cab))
        for a in f1:
            listbox.insert(END,a)
        listbox.place(x=5,y=5,width=760, height=775)
        listbox.config(width=500,justify=LEFT,)
        ViewerTEXTscroll.config(command=listbox.yview)

    def AdicionarMarcas():
        mydb = pymssql.connect('srvsql-ipt.ddns.net', '81750', '81750', "PA_81750_81810_81817_81818")
        cursor = mydb.cursor(as_dict=True)
        sql = "INSERT INTO marcas(nomeMarca) VALUES (%s)"
        if (ENTRADA2.get()==""):    # SE ENTRADA FOR VAZIA, REDIRECIONA PARA CHANGELOG ERRO
            ChangeLog_Generic_NOVALUES("Marcas")
            breakpoint
        else:
            val2 = str(ENTRADA2.get())
            try:
                if val2 == "":
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nFALHA A ADICIONAR À BASE DE DADOS",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
                elif val2 != "":
                    cursor.execute(sql, val2)
                    mydb.commit()
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nADICIONADO À BASSE DE DADOS COM SUCESSO",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
            except:
                imprimir = Label(ChangeLogTEXT,
                                 text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nUNEXPECTED ERROR 12286. VERY UNEXPECTED...",
                                 anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)

    def UpdateMarcas():
        mydb = pymssql.connect('srvsql-ipt.ddns.net', '81750', '81750', "PA_81750_81810_81817_81818")
        cursor = mydb.cursor(as_dict=True)
        sql = "UPDATE marcas SET nomeMarca=%s WHERE idMarca = %d"
        val = []
        if (ENTRADA2.get()==""):    # SE ENTRADA FOR VAZIA, REDIRECIONA PARA CHANGELOG ERRO
            ChangeLog_Generic_NOVALUES("Marcas")
            breakpoint
        else:
            for x in (ENTRADA2.get()).split(","):
                val.append(x)
            val2 = (str(val[1]), int(val[0]))
            try:
                if len(val)>2:
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nFALHA A ADICIONAR À BASE DE DADOS",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
                elif len(val) == 2:
                    cursor.execute(sql, val2)
                    mydb.commit()
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nALTERADA NA BASE DE DADOS COM SUCESSO",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
            except:
                imprimir = Label(ChangeLogTEXT,
                                 text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nUNEXPECTED ERROR 12286. VERY UNEXPECTED...",
                                 anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)

    def DeleteMarcas():
        mydb = pymssql.connect('srvsql-ipt.ddns.net', '81750', '81750', "PA_81750_81810_81817_81818")
        cursor = mydb.cursor(as_dict=True)
        sql = "DELETE FROM marcas WHERE idMarca = %d"
        if (ENTRADA2.get()==""):    # SE ENTRADA FOR VAZIA, REDIRECIONA PARA CHANGELOG ERRO
            ChangeLog_Generic_NOVALUES("Marcas")
            breakpoint
        else:
            val =ENTRADA2.get()
            try:
                if val=="":
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nFALHA A ADICIONAR À BASE DE DADOS",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
                else:
                    cursor.execute(sql, val)
                    mydb.commit()
                    imprimir = Label(ChangeLogTEXT,
                                     text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nALTERADA NA BASE DE DADOS COM SUCESSO",
                                     anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                    imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)
            except:
                imprimir = Label(ChangeLogTEXT,
                                 text="Logged in ao server srvsql-ipt.ddns.net\n\nSERVIÇOS CONECTADOS\n\nUNEXPECTED ERROR 12286. VERY UNEXPECTED...",
                                 anchor="nw", font=("Calibri bold", 12), background="#ffffff", justify=LEFT)
                imprimir.place(anchor="center", relx=0.5, rely=0.5, width=900, height=225)


    ################################################################################################################
    ####                                   DEFINIÇÃO DE JANELA DA FUNÇÃO TESTES2()                              ####
    ################################################################################################################

    def about(): # MENU GUI - DEFINIÇÃO ABOUT######################################################################
        nova_janela = Toplevel(janela) # ABRE A JANELA ABOUT EM TOP LEVEL
        nova_janela.title('About')
        nova_janela.geometry('300x300') # TAMANHO DA JANELA
        x=Label(nova_janela,font=("Calibri",18),anchor="center",text="Trabalho realizado por\n\n Ricardo Milagre\n Pedro Manuel\n Luiz Santos\n Filipe Ferreira")
        x.place(width=275,height=275,rely=0.5,relx=0.5,anchor="center") # PARAMETROS DA JANELA, LOCALIZAÇÃO, TAMANHO ETC

    janela = Tk()
    janela.title("Logged in srvsql-ipt.ddns.net") #TITULO DA JANELA
    janela.iconbitmap("Outros/favicon.ico") # ICON COLOCADO NA JANELA DA BD.
    janela.geometry('1920x1080')
    janela.state('zoomed') #FULLSCREEN
    menubar = Menu(janela, background='#ffffff')
    # FILE###########################################################################################################
    file = Menu(menubar, tearoff=0, foreground='black')
    file.add_separator() #SEPARA O LOG IN DO EXIT
    file.add_command(label="Exit", command=janela.quit)
    menubar.add_cascade(label="File", menu=file)
    janela.config(menu=menubar)
    # ABOUT#########################################################################################################
    sobre = Menu(menubar, tearoff=0, foreground='black')
    sobre.add_separator() #SEPARA O LOG IN DO EXIT
    sobre.add_command(label="Realizado Por", command=about)
    menubar.add_cascade(label="About", menu=sobre)
    janela.config(menu=menubar)

    ################################################################################################################
    ####                               LABELS E OBJECTOS CRIADOS NA JANELA                                      ####
    ################################################################################################################

    # INFO LABEL####################################################################################################
    info = Label(janela, text="Conectado À Base de Dados de Componentes de Computadores", foreground="#FFFFFF",
                 font=("Calibri, bold", 16),
                 background="#212F3C")
    info.place(anchor='n', x=960, y=0, width=janela.winfo_screenwidth(), height=50)


    # VIEWER LABEL##################################################################################################
    Viewer = Label(janela, text="Viewer",foreground="#FFFFFF", font=("Calibri bold", 20), anchor='n',
                   background="#212F3C",justify="center")
    Viewer.place(x=60, y=95, width=800, height=850)
    # VIEWERTEXT
    ViewerTEXT = Label(Viewer, foreground="#FFFFFF", font=("Calibri bold", 12), anchor='n',
                       justify=LEFT)
    ViewerTEXT.place(anchor="center", rely=0.525, relx=0.5, width=780, height=790)

    # OPÇÕES LABEL###################################################################################################
    Opções = Label(janela, text="Menu Opções",foreground="#FFFFFF", font=("Calibri bold", 20), anchor='n',
                   background="#212F3C",justify="center")
    Opções.place(x=875, y=430, width=975, height=515)

    # CHANGELOG#####################################################################################################
    ChangeLog = Label(janela, text="ChangeLog", foreground="#FFFFFF", font=("Calibri bold", 12), anchor='n',
                      background="#212F3C")
    ChangeLog.place(x=875, y=95, width=975, height=325)
    # CHANGELOGTEXT
    ChangeLogTEXT = Label(ChangeLog, font=("Calibri bold", 12), anchor='n', background="#FFFFFF")
    ChangeLogTEXT.place(anchor="center", rely=0.55, relx=0.5, width=955, height=250)


    ################################################################################################################
    ################################################################################################################


    # ESCOLHA DE DB################################################################################################
    Escolha = Label(Opções, text="Escolha Base de Dados", foreground="#FFFFFF",
                    font=("Calibri bold", 17), anchor='n',
                    background="#17202A")
    Escolha.place(x=5, y=75, width=475, height=200)


    opções = ["Escolha a DB", "Marcas", "Produtos", "Fornecedores", "Tipo de Produtos"]
    variavel = StringVar(janela)
    variavel.set(opções[0])

    # ESCOLHA DB - MENU ESCOLHA
    DropEscolha = OptionMenu(Escolha, variavel, *opções)
    DropEscolha.config(background="#8A8A8C",foreground="#ffffff")
    DropEscolha.place(anchor='center', width=425, height=70, relx=0.5, rely=0.435,
                      bordermode="outside")  # side=LEFT,anchor='center')
    DropEscolha.config(font=("Calibri bold", 12))
    # ESCOLHA DB - BOTÃO CONFIRMAÇÃO
    Confirmar = Button(Escolha, text="Confirmar", command=confirmar, fg="#ffffff", font=("Calibri bold", 12),background="#8A8A8C")
    Confirmar.place(anchor='center', width=425, height=70, relx=0.5, rely=0.8, bordermode="outside")


    # PROGRAMAÇÃO AVANÇADA LABEL####################################################################################
    PA = Label(Opções, text="IPT - CTESP INFORMÁTICA\n\nProgramação Avançada", foreground="#FFFFFF",
                        font=("Calibri bold", 17), anchor='n',
                    background="#17202A")
    PA.place(x=485, y=75, width=480, height=200)


    # PAINEL INFORMAÇÕES LABEL#######################################################################################
    ENTRADA3 = Label(Opções, foreground="#FFFFFF", text="Painel Informações",
                       font=("Calibri bold", 13), border=1, borderwidth=1, justify="center",anchor="n",
                       background="#17202A")
    ENTRADA3.place(width=960, height=105, x=5, y=285)
    ENTRADA4 = Label(ENTRADA3, relief='sunken', foreground="#000000",text="Primeiro selecionar a Base de Dados pretendida do menu 'Escolha BD'.\n"
                                                                          "Após confirmação de conexão no changelog Inserir valores. "
                                                                          "Após inserir valores, selecionar opção pretendida\n\n"
                                                                          "ATENÇÃO: Respeite sempre os argumentos da Base de dados aberta. Separe os elementos por ','",

                       border=1, borderwidth=1, justify="left",font=("Calibri", 10),
                       background="#ffffff",anchor="nw")
    ENTRADA4.place(width=945, height=70, relx=0.5,rely=0.6,anchor="center")


    # ENTRADA LABEL##################################################################################################
    #ENTRADA
    ENTRADA = Label(Opções, foreground="#FFFFFF", text="Entrada De Dados",
                       font=("Calibri bold", 17), border=1, borderwidth=1, justify="center",anchor="n",
                       background="#17202A")
    ENTRADA.place(width=685, height=105, x=5, y=400)
    ENTRADA2= Entry(ENTRADA, relief='sunken', foreground="#000000",
                       font=("Calibri ", 12), border=1, borderwidth=1, justify="left",
                       background="#ffffff")
    ENTRADA2.place(width=670, height=50, relx=0.5,rely=0.70,anchor="center")


    # BOTÕES#########################################################################################################
    #BOTÃO DELETE
    APAGAR_BOTAO = Button(Opções, text="Delete", foreground="#FFFFFF",
                 font=("Calibri bold", 12), anchor='center',
                 background="#8A8A8C",command=DeleteBD_UPD)
    APAGAR_BOTAO.place(y=400, x=835, width=130, height=50)
    #BOTÃO TEST BUILD
    TEST_BUTTON = Button(Opções, text="Test Build\nNº 12286", foreground="#FFFFFF",
                 font=("Calibri bold", 12), anchor='center',
                 background="#8A8A8C",)
    TEST_BUTTON.place(width=130, height=50, x=835, y=455)
    #BOTAO UPDATE
    ATUALIZAR_BOTAO = Button(Opções, text="Update", foreground="#FFFFFF",
                 font=("Calibri bold", 12), anchor='center',
                 background="#8A8A8C",command=AdicionarBD_UPD)
    ATUALIZAR_BOTAO.place(width=130, height=50, x=700, y=400)
    #NOTÃO ADD
    ADICIONAR_BOTAO = Button(Opções, text="Add", foreground="#FFFFFF",
                 font=("Calibri bold", 12), anchor='center',
                 background="#8A8A8C",command=AdicionarBD)
    ADICIONAR_BOTAO.place(width=130, height=50, x=700, y=455)
    #BOTAO PDF
    PDF = Button(PA,text="Mostrar Items em Rutura\nPDF", foreground="#FFFFFF",
                    font=("Calibri bold", 12), anchor='center',
                    background="#8A8A8C",command=LoadPDF)
    PDF.place(width=230, height=50, x=5, y=143)
    #BOTÃO HTML
    HTML = Button(PA, foreground="#FFFFFF", text="Converter BD\nEm HTML",
                    font=("Calibri bold", 12), anchor='center',
                    background="#8A8A8C",command=printit)
    HTML.place(width=230, height=50, x=243, y=143)
    janela.mainloop()


