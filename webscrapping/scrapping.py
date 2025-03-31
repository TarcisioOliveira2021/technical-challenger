from bs4 import BeautifulSoup
import requests

webSiteURL = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'
customHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

govPage = requests.get(webSiteURL, headers=customHeaders)
soup = BeautifulSoup(govPage.content, 'html.parser')

govPageInternalLinks = soup.find_all('a', {'class': 'internal-link'})
anexo01PDF_URL = govPageInternalLinks[0]['href']
anexo02PDF_URL = govPageInternalLinks[2]['href']
print(anexo01PDF_URL)
print(anexo02PDF_URL)



