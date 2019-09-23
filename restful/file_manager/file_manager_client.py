import file_manager_api
import json
import requests

SERVER_URL = "http://127.0.0.1:7777"
def menu(dir):
    #print(path + '\n')
    while True:
        print("\nSELECIONE UMA OPÇÃO:\n1. Listar arquivos\n2. Exibir arquivo\n3. Remover arquivo")
        print("4. Remover todos os arquivos\n5. Criar arquivo\n6. Atualizar arquivo")
        opcao =  input("Opção: ")
        path = SERVER_URL + dir
        
        if opcao == "1":
            listar(path)
        elif opcao == "2":
             exibir(path)
        elif opcao == "3":
             remover(path)
        elif opcao == "4":
            remover_tudo(path)
        elif opcao == "5":
            criar(path)
        elif opcao == "6":
            atualizar(path)
        else:
            print("Opção incorreta")


def get_files(path):
    v = []
    r = requests.get(path + "/json")

    for f in r.json()['files']:
        v.append(f)

    return v

def listar(path):
  
    for x in get_files(path):
        print(x)
    print("")

def exibir(dir):
    f = dir + input("Nome do arquivo:") 
    print(f)
    try:
        r = requests.get(f + "/content")
        print("Conteúdo de : " + f + "\n")
        print(r.json()['file-content'])
        print("")
    except Exception:
        print("Arquivo não encontrado")

def remover(dir):
    f = dir + input("Nome do arquivo:") 
    print(f)
    try:
        if input("Tem certeza de que deseja apagar o arquivo? Isto não pode ser desfeito. S/N") != 'S':
            return
        r = requests.delete(f)
       
        if r.json()[0]['status'] == '200':
            print(f + " foi deletado.\n")
            return 

    except Exception as e:
        print(e)
        pass
    
    print("Arquivo não encontrado")

def remover_tudo(dir):
    try:
        v = get_files(dir)

        if input("Tem certeza de que deseja apagar todos os arquivos? Isto não pode ser desfeito. S/N") != 'S':
            return
        
        for f in v:
            requests.delete(dir + f)
       
    except Exception as e:
        print(e)
        pass

def input_to_json(message):
    dic = {}
    dic['file-content'] = input(message)
    return json.dumps(dic)

def criar(dir):
    try:
        f = input("Nome do arquivo: ")
        requests.put(dir+f, data=input_to_json("Conteúdo do arquivo:"))
    except Exception as e:
        print("Erro: " + str(e))

def atualizar(dir):
    f = input("Nome do arquivo: ")
   
    try:
        if f in get_files(dir):
            requests.put(dir+f, data=input_to_json("Novo conteúdo do arquivo:"))
        else:
            print("Arquvio não encontrado.")
    except Exception as e:
        print("Erro: " + e)

def definir_diretorio():
    dir = input("Informe o diretório: ")
    #dir = "/home/aluno/Desktop"
    #dir = "C:\\Users\\ramon\\Desktop\\teste"
    if "\\" in dir:
        dir = dir.replace('\\', '/')
    if dir[-1] != '/': 
        dir = dir + '/'
    if dir[0] != '/':
        dir = '/' + dir
    print(dir)
    return dir

if __name__ == "__main__":
    try:
        menu(definir_diretorio())
    except Exception as e:
        print("Um erro ocorreu! Tente novamente.")
        print(e)