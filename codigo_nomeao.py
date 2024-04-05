import PyPDF2
import pandas as pd

caminho_pdf = 'main.pdf'

columns = ['cod_uorg','nome_uorg','cod_funcao','nome_funcao','matricula',
           'nome_titular','data_titular','exe_titular','matricula_subs','nome_subs','data_subs']

with open(caminho_pdf, 'rb') as arquivo:
    # Criar um objeto leitor de PDF
    leitor = PyPDF2.PdfReader(arquivo)
    num_paginas = len(leitor.pages)

    # Inicializar variáveis para armazenar os dados tabulares
    df = pd.DataFrame(columns=columns)
    registro = []

    print(df)
    # Iterar por cada página do PDF
    for pag_num in range(num_paginas):
        pagina = leitor.pages[pag_num]
        texto = pagina.extract_text()
        lista_linhas = texto.split('\n')
        print(f'PAGINA {pag_num}')

        for i, linha in enumerate(lista_linhas):
            inicio = linha[0:4].strip()
    
            id = linha[:6].strip()
            codigo = linha[6:14].strip()
            nome = linha[14:56].strip()
            data = linha[56:65].strip()
            exe = linha[65:].strip()
            print(i)

            if inicio == 'UORG':
                registro.extend((codigo,nome))
            elif inicio == 'DENO':
                registro.extend((codigo,nome))
            elif inicio == 'TITU':
                registro.extend((codigo, nome, data, exe))
            elif inicio == 'SUBS':
                registro.extend((codigo, nome, data))
            elif inicio == 'RESP':
                if len(registro) != len(columns):
                    print(f"Incompatibilidade de colunas no registro para a página {pag_num}, linha {i}: {registro}")
                else:
                    df.loc[len(df)] = registro
                registro.clear()
            else:
                pass 

df.to_excel('main.xlsx')
print(df)
