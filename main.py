from tqdm import tqdm
from pathlib import Path
# from pydantic import BaseModel, EmailStr,SecretStr
import os

class piholeLists:
	dirpath=os.path.dirname(__file__)
	tlds:list=[]
	dominioRemplazo:str='0.0.0.0'
	dominios:dict[str,dict]={}
	def get_file_route(self,filename:str):
		return os.path.join(self.dirpath,filename)
	
	def get_save_route(self,filename:str):
		return os.path.join(self.dirpath,'results',filename)

	def load_lists(self):
		print('Cargando Listas de archivos..')
		lists_dir=self.get_file_route('lists')
		folder = Path(lists_dir)
		return [file for file in tqdm(folder.glob('*.txt'))]

	def readlist(self,filename:str,encodign:str='utf-8'):
		content=''
		with open(filename,'r',encoding=encodign) as file:
			content=file.read()

		return content

	def load_domains(self,file:str):
		print(f'Cargando dominios de {file}')
		workingfile=self.get_file_route(file)
		content =self.readlist(workingfile)
		
		
		if self.getlistname(str(workingfile))=="nsfw.txt" or self.getlistname(str(workingfile))=="extense.txt":
			workingfile=self.get_file_route('nsfw.txt')
			
		for line in tqdm(content.split('\n')):
			if not line.startswith('#'):
				sublines =line.split(' ')
				
				dominio=sublines[0].split('.')
				if len(sublines)>1:
					dominio=sublines[1].split('.')
				
				text =''
				subtext=''
				if(self.isTld('.'.join(dominio[-2:]))):
					if len(dominio)>=3:
						text= '.'.join(dominio[-3:])
					else:
						text= '.'.join(dominio[-2:])
					subtext='.'.join(dominio[-3:-1])
				else:	
					text= '.'.join(dominio[-2:])
					if text=='google.com' and len(dominio)>=3:
						text= '.'.join(dominio[-3:])

				self.addDominio(text,workingfile)
				self.addDominio(subtext,workingfile)

	def addDominio(self,dominio:str,workingfile:str):
		if dominio is not None and dominio!='':
			if dominio in self.dominios.keys():
				self.dominios[dominio]["count"]+=1
			else:
				self.dominios[dominio]={"count":1,"origen":self.getlistname(workingfile)}

	def loadTLDS(self):
		print('cargando tlds..')
		tld_file=self.get_file_route('tlds.txt')
		content=self.readlist(tld_file)
		self.tlds=['.'.join(tld.split('.')[1:]) for tld in tqdm(content.split('\n'))]
		


	def isTld(self,text:str):
		
		return text in self.tlds 

	def save_file(self,fileName:str,content:dict,encoding:str='utf-8'):
		save_route = self.get_save_route(f'{fileName}')
		print(f'Guardando archivo {fileName} en. \n{save_route}')
		print(self.get_save_route(f'{fileName}'))
		with open(save_route,"w",encoding='utf-8') as file:
				for dominio in tqdm(content):
					file.write(f'{self.dominioRemplazo} ||{dominio}^\n')	

	def getlistname(self,list_route:str):
		list_name=list_route.split("/")[-1:]
		
		if "\\"in list_route:
			list_name=list_route.split("\\")[-1:]
		
		return list_name[0]

	def launch(self):
		print('Iniciando proceso de refactorizacion de listas')
		self.loadTLDS()
		
		files_names= self.load_lists()

		for file_name in tqdm(files_names):
			self.load_domains(str(file_name))
		# print(self.dominios)
		for dominio in self.dominios.items():
			print(dominio)
			# print(dominio)
		
			# filename=
	# def evaluarDominios(self)


if __name__=="__main__":
	piholeLists_E=piholeLists()
	piholeLists_E.launch()