
import webbrowser
import pymssql
import threading
import keyboard

def criarHtml(): #faz a Ligação a base de dados fazendo uma querry que busca os dados
    mydb = pymssql.connect('srvsql-ipt.ddns.net', '81817', '81817', "PA_81750_81810_81817_81818")
    cursor = mydb.cursor(as_dict=True)

    # Faz um query a base de dados onde procuramos os nomes dos produtos, o stock comprado, o stock vendido, o nome da marca, e o nome do fornecedor
    querys = ('SELECT nomeProduto,stockComprado,stockVendido,tipoProduto, nomeMarca, nomeFornecedor FROM produtos INNER JOIN tipoProdutos ON produtos.idTipoProduto = tipoProdutos.idTipoProduto INNER JOIN marcas ON produtos.idMarca = marcas.idMarca INNER JOIN fornecedores ON produtos.idFornecedor = fornecedores.idFornecedor')

    listaSite = [] # cria uma lista em branco e faz um loop a variavel querys adicionando a lista "ListaSite"
    cursor.execute(querys)
    for x in cursor:
        listaSite.append(x)

    f = open("Outros\index.html","w")  # Faz a abertura e a criação do ficherio em html
    r1 = len(listaSite) # retorna quantos objetos há na lista
    i = 0   #variavel de controle
    messageValores = ""

    messageHead = """   
        <html lang="pt">
            <head>
            <meta charset=UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="HTML2.css">
            <title>Produtos</title>
            </head>
        <body>
            <h1>Produtos  <img src="recurso2.jpg" id="imagem"></h1>
            <br>
            <br>
            <br>
        <table id="tabela">
            <tr class="osheaders">
                <th class="osheaders">Produto</th>
                <th class="osheaders">Tipo de  Produto</th>
                <th class="osheaders"> Marca</th>
                <th class="osheaders">Fornecedor</th>
                <th class="osheaders"> Stock Vendido</th>
                <th class="osheaders">Stock Comprado</th>
            </tr>
        """
    # faz um loop procurando todos os dados  na base de dddos  e enquanto o "i" que começa com o valor 0 avançe
    # senpre um row de dados ate que seja igual a r1
    for n in range(r1): #enquanto i não e igual a r1 escreve no html os dados da base de dados
        while i < r1:
            messageValores += f"""
                <tr class="ocontent">
                    <td class="produtos">{listaSite[i]['nomeProduto']}</td>
                    <td class="ocontent">{listaSite[i]['tipoProduto']}</td>
                    <td class="ocontent">{listaSite[i]['nomeFornecedor']}</td>
                    <td class="ocontent">{listaSite[i]['nomeMarca']}</td>
                    <td class="ocontent">{listaSite[i]['stockVendido']}</td>
                    <td class="ocontent">{listaSite[i]['stockComprado']}</td>
                    </tr>
                """

            i += 1

            messageFim = """
        </table>
        </body>
        </html>
        """
        # junta as diferentes partes de html em apenas uma só
        message = messageHead + messageValores + messageFim



    f.write (message)

    f.close()
#Faz a abertura e o fecho do separador
def botao_open(filename):
    keyboard.press_and_release('ctrl+w') #simula o input de um teclado
    webbrowser.open(filename)


def printit():
  threading.Timer(30.0, printit).start() # De 30 a 30 segundos fecha o separador e volta a abrir
  criarHtml()
  botao_open("Outros\index.html")