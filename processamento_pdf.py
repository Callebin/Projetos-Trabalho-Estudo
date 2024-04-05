import PyPDF2
import pandas as pd

columns = ['cod_uorg','nome_uorg','cod_funcao','nome_funcao','matricula',
           'nome_titular','data_titular','exe_titular','matricula_subs','nome_subs','data_subs']

## a fazer: iterar múltiplos pdfs. ajustar leitura e salvamento de objetos arquivo

def extrai_nomeacoes(arquivos):
    df = pd.DataFrame(columns=columns)
    
    for a in range(len(arquivos)):
        with arquivos[a]:
            # Criar um objeto leitor de PDF
            leitor = PyPDF2.PdfReader(arquivos[a])
            num_paginas = len(leitor.pages)

            registro = []

            # Iterar por cada página do PDF
            for pag_num in range(num_paginas):
                pagina = leitor.pages[pag_num]
                texto = pagina.extract_text()
                lista_linhas = texto.split('\n')

                for i, linha in enumerate(lista_linhas):
                    inicio = linha[0:4].strip()
            
                    id = linha[:6].strip()
                    codigo = linha[6:14].strip()
                    nome = linha[14:56].strip()
                    data = linha[56:65].strip()
                    exe = linha[65:].strip()

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
    return df