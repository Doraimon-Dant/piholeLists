from tqdm import tqdm
from pathlib import Path
import os

dirpath=os.path.dirname(__file__)
# file_result='nsfw_optimized.txt'
# tlds_file=os.path.join(dirpath,tld_file_name)
# result_file=os.path.join(dirpath,file_result)
# dominioRemplazo='192.168.1.9'
dominioRemplazo='0.0.0.0'
tlds=[]
encabezado=''

def get_file_route(filename:str):
	return os.path.join(dirpath,filename)
def get_save_route(filename:str):
	return os.path.join(dirpath,'results',filename)

def load_lists():
	print('Cargando Listas de archivos..')
	lists_dir=get_file_route('lists')
	folder = Path(lists_dir)
	return [file for file in tqdm(folder.glob('*.txt'))]

def readlist(filename:str,encodign:str='utf-8'):
	content=''
	with open(filename,'r',encoding=encodign) as file:
		content=file.read()

	return content

def load_domains(file:str):
	print(f'Cargando dominios de {file}')
	workingfile=get_file_route(file)
	content =readlist(workingfile)
	dominios={}

	for line in tqdm(content.split('\n')):
		if not line.startswith('#'):
			sublines =line.split(' ')
			
			dominio=sublines[0].split('.')
			if len(sublines)>1:
				dominio=sublines[1].split('.')
			
			text =''
			subtext=''
			
			if('.'.join(dominio[-2:]) in tlds):
				text= '.'.join(dominio[-2:])
				if len(dominio)>=3:
					text= '.'.join(dominio[-3:])
				
				subtext='.'.join(dominio[-3:-1])
			else:	
				text= '.'.join(dominio[-2:])
			if text is not None and text!='':					
				if text in dominios.keys():
					dominios[text]+=1
				else:
					dominios[text]=1

			if subtext is not None and subtext!='':
				dominios[subtext]=1
	return dominios



def loadTLDS():
	print('cargando tlds..')
	tld_file=get_file_route('tlds.txt')
	content=readlist(tld_file)
	tlsd=['.'.join(tld.split('.')[1:]) for tld in tqdm(content.split('\n'))]


def isTld(text:str):
	return text in tlds 

def save_file(fileName:str,content:dict,encoding:str='utf-8'):
	print(f'Guardando archivo {fileName}')
	save_route = get_file_route(f'{fileName}')
	print(get_file_route(f'{fileName}'))
	with open(save_route,"w",encoding='utf-8') as file:
			for dominio in tqdm(content):
				
				file.write(f'{dominioRemplazo} ||{dominio}^\n')	

def getlistname(list_route:str):
	list_name=list_route.split("/")[-1:]
	
	if "\\"in list_route:
		list_name=list_route.split("\\")[-1:]
	
	return list_name[0]

def launch():
	print('Iniciando proceso de refactorizacion de listas')
	loadTLDS()
	files_names= load_lists()

	for file_name in tqdm(files_names):
		domains=load_domains(str(file_name))
		parts_file_name=str(getlistname(str(file_name))).split('.')
		
		fileName=f'{parts_file_name[0]}_refactored.{parts_file_name[1]}'
		# print(fileName)
		save_file(fileName,domains)

	
		# filename=



if __name__=="__main__":
	launch()