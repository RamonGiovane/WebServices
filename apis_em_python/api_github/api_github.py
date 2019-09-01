import requests
import json
from datetime import datetime
#classe que guarda um usuário do github, seus seguidores e repositórios
class Usuario:
	API_URL = "https://api.github.com/users/"
	def __init__(self, username):
		self.username = username
		self.repos = []
		self.followers = []
	
	def add_rep(self, rep):
		self.repos.append(rep)
	
	def add_follower(self, follower):
		self.followers.append(follower)

	def get_repos(self):
		return self.repos
	
	def get_followers(self):
		return self.followers

	def get_username(self):
		return self.username
	
#consulta na API os repositórios do objeto usuário passado (identificado pelo atributo username).
#adiciona  então a esse objeto todos os seus repositórios
def consultar_repositorios(user):

	repos = "/repos"
	
	req = requests.get(Usuario.API_URL + user.get_username() + repos)
	json = req.json()

	for rep in json:
		user.add_rep(rep['name'])

#procura por um nome de usuário no cache local e exibe seu nome, e os seguidores + repositórios 
def exibir_seguidores(cache, username):
	print("Usuário da consulta: " + username)
	
	usr = cache[username]
	
	if len(usr.get_followers()) == 0:
		consultar_repositorios(username)

	seguidores = []
	seguidores = usr.get_followers().copy()
	print(str(len(seguidores)) + " seguidores:\n")
	
	for f in seguidores:
		print(f.get_username() + "\n")
		for r in f.get_repos():
			print("\t" + r)
		print("\n")

def consultar_seguidores(cache,username):
	
	user = Usuario(username)

	followers = "/followers"

	req = requests.get(Usuario.API_URL + username + followers)
	json = req.json()

	for seguidor in json:
		#se o json for uma mensagem da api, quando excede as requisicoes
		if "message" in seguidor:
			raise Exception("Número de requisções máximo atingido.\n(API rate limit exceeded)")
		follower = Usuario(seguidor["login"])
		consultar_repositorios(follower)
		user.add_follower(follower)

	cache[username] = user

#lê do terminal um username, guarda em cache todos os usuários e repositórios já pesquisados
def ler_usuario():
	cache = {}

	while True:
	
		print("Digite /exit ou /x para sair")
		username = input("Username do Github: ")
		
		if(username == '/x' or username == '/exit'):
			break
		elif (username not in cache):
			consultar_seguidores(cache, username)
		else:
			print(cache[username])
		exibir_seguidores(cache, username)	

		
def main():
	try:
		ler_usuario()
	except Exception as e:
		print("Um erro ocorreu! Cheque o arquivo 'bug.log' para detalhes.")
		today = datetime.now() 
		f= open("bug.log","w+")
		f.write(str(today) + "\n" + str(type(e)) +"\n" + str(e))
		f.close()

if __name__ == "__main__":
    main()	