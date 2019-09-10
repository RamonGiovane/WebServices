import requests
import json
import webbrowser
from bs4 import BeautifulSoup

def lerNomeProduto():
    print("\nConsulte os preços de um produto online:")
    return input("Nome do produto:")

def formatarRequisicao(nomeDoProduto):
    url_requisicao1 = "https://www.buscape.com.br/search/"
    url_requisicao2 = "?fromSearchBox=true&produto="
    nomeSeparadoPor_ = nomeDoProduto.replace(" ", "-")
    nomeSeparadoPorMais = nomeDoProduto.replace(" ", "+")

    return url_requisicao1 + nomeSeparadoPor_ + url_requisicao2 + nomeSeparadoPorMais

def requisicaoHTTP(nomeDoProduto):
    r = requests.get(formatarRequisicao(nomeDoProduto))
    interpretarResposta(r.text)

def formatarNumeroComVirgula(numero):
    return numero.replace(".", "").replace(",",".")

def interpretarResposta(text):
    produtos = {}
    names = []
    prices = []
    soup = BeautifulSoup(text, "html.parser")
    
    names = soup.findAll('div', class_= 'card--product__name u-truncate-multiple-line')
    prices = soup.find_all('span', {"itemprop" : "lowPrice"})
    
    
    i = 0
    for hit in names:
        preco = float(formatarNumeroComVirgula(prices[i].text.strip()))
        hit = hit.text.strip()
        
        if hit not in produtos:
            produtos[hit] = preco
        else:
            if preco < produtos[hit]:
                produtos[hit] = preco
 
        i = i+1
    
    exportarComoJSON(produtos)
    webbrowser.open("index.html")

    
def exportarComoJSON(dados):
    with open('data.js', 'w') as fp:
        fp.write("json = " + str(json.dumps(dados)))

def main():
    while True:
        requisicaoHTTP(lerNomeProduto())

if __name__ == "__main__":
    main()