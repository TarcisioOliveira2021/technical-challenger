from bs4 import BeautifulSoup
import requests
import os
import zipfile
import pdfplumber
import pandas as pd

webSiteURL = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'
customHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

govPage = requests.get(webSiteURL, headers=customHeaders)
soup = BeautifulSoup(govPage.content, 'html.parser')

govPageInternalLinks = soup.find_all('a', {'class': 'internal-link'})
anexo01PDF_URL = govPageInternalLinks[0]['href']
anexo02PDF_URL = govPageInternalLinks[2]['href']
anexo01PDF = requests.get(anexo01PDF_URL, headers=customHeaders, stream=True)
anexo02PDF = requests.get(anexo02PDF_URL, headers=customHeaders, stream=True)

downloadFolder = 'download'
os.makedirs(downloadFolder, exist_ok=True)

def criar_nome_arquivo(nomepath:str,basepath:str):
    return os.path.join(basepath,nomepath)

def criar_arquivo_byte(path:str, content:bytes):
    with open(path,"wb") as file:
        file.write(content)

def criar_arquivo_zip(path:str, arquivo:list):
    zipath = os.path.join(downloadFolder, path)
    with zipfile.ZipFile(zipath, 'w') as zipf:
        for file_name in arquivo:
            zipf.write(file_name, os.path.basename(file_name))

def criar_csv(path:str,pdfpath:str):
    data = []
    siglas = {
        "OD" : 'Seg. Odontológica',
        "AMB": 'Seg. Ambulatorial',
    }

    with pdfplumber.open(pdfpath) as arquivopdf:
        for pagina in arquivopdf.pages:
            tables = pagina.extract_table()
            if tables:
                for row in tables:
                    data.append(row)
    
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df.replace(siglas)
    df.to_csv(path, index=False, encoding="utf-8", sep=",")


anexo01Path = criar_nome_arquivo('anexo01.pdf', downloadFolder)
anexo02Path = criar_nome_arquivo('anexo02.pdf', downloadFolder)
criar_arquivo_byte(anexo01Path, anexo01PDF.content)
criar_arquivo_byte(anexo02Path, anexo02PDF.content)
criar_arquivo_zip('anexos.zip', [anexo01Path, anexo02Path])

#Transformação
csvPath = criar_nome_arquivo('data.csv', downloadFolder)
criar_csv(csvPath, anexo01Path)
criar_arquivo_zip('Teste_Tarcisio.zip', [csvPath])



