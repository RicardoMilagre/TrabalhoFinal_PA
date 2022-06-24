
from fpdf import FPDF
import pymssql
import webbrowser

def LoadPDF():
    class PDF(FPDF):
        pass
        def lines(self):
            self.set_line_width(0.0)
            self.line(5.0, 5.0, 205.0, 5.0)  # top one
            self.line(5.0, 292.0, 205.0, 292.0)  # bottom one
            self.line(5.0, 5.0, 5.0, 292.0)  # left one
            self.line(205.0, 5.0, 205.0, 292.0)  # right one
            self.rect(5.0, 5.0, 200.0, 287.0)
            self.rect(8.0, 8.0, 194.0, 282.0)
            self.set_xy(0.0, 0.0)
            self.set_font('Arial', 'B', 24)
            self.set_text_color(255, 20, 147)
            self.cell(w=210.0, h=40.0, align='C', txt="ROTURAS", border=0)
    mydb = pymssql.connect('srvsql-ipt.ddns.net', '81818', '81818', "PA_81750_81810_81817_81818")
    cursor = mydb.cursor(as_dict=True)
    cursor.execute('SELECT nomeProduto, stockAtual, stockSeguranca FROM produtos WHERE stockAtual < stockSeguranca')
    listaRotura = []
    pdf = PDF()
    pdf.add_page()
    pdf.lines()
    pdf.set_font('Arial', '', 14)
    pdf.set_text_color(0, 0, 255)
    pdf.write(6, "\n\n\n\n\nEstes produtos estão em rotura: \n\n")
    pdf.set_text_color(0, 0, 0)
    for x in cursor:
        listaRotura.append(x)
    pre = len(listaRotura)
    i = 0
    while i < pre:
        pdf.set_font('Arial', '', 14)
        pdf.set_text_color(0, 0, 0)
        pdf.write(10, listaRotura[i]['nomeProduto'] + '\nStock atual: ' + str(
            listaRotura[i]['stockAtual']) + '\n Stock Segurança: ' + str(listaRotura[i]['stockSeguranca']) + '\n\n')
        i += 1
    mydb.close()
    pdf.output('roturas.pdf', 'F')
    webbrowser.open_new('roturas.pdf')