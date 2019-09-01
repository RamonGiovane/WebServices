import requests

def exibir_cep(cep):
    print("\nLocalização encontrada:\n" + cep['logradouro'] + "\nBairro: " + cep['bairro'] + "\nLocalidade: " + cep['localidade'] + "\nEstado: " + cep['uf'])
	
def consultar_cep(cep, cache):
    if cep not in cache:
        request(cep, cache)
    exibir_cep(cache[cep])


def request(cep, cache):
    url_inicio = "https://viacep.com.br/ws/"
    url_final = "/json"

    cache[cep] = requests.get(url_inicio + cep + url_final).json()


def main():
    cache = {}
    while True:
        cep = input("\nEscreva um CEP:")
        consultar_cep(cep, cache)

if __name__ == "__main__":
    main()