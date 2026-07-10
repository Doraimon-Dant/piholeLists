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

		for line in tqdm(content.split('\n')):
			if not line.startswith('#'):
				sublines =line.split(' ')
				
				dominio=sublines[0].split('.')
				if len(sublines)>1:
					dominio=sublines[1].split('.')
				
				(text,subtext) =self.evaluar_dominio(dominio)

				self.addDominio(text,workingfile)
				self.addDominio(subtext,workingfile)
	def evaluar_dominio(self,dominio:list):
		text =''
		subtext=''
		tld='.'.join(dominio[-2:])
		dominios_especiales=['google.com','microsoft.com','microsoft.us']
		if(self.isTld(tld)):
			dominios_especiales=[f'google.{tld}',f'microsoft.{tld}',]
			text= '.'.join(dominio[-3:])
			if text in dominios_especiales :	
				text= '.'.join(dominio[-4:])
			else:
				text= '.'.join(dominio[-2:])
			subtext='.'.join(dominio[-3:-1])
		else:	
			text= '.'.join(dominio[-2:])
			
			if text in dominios_especiales and len(dominio)>=3:
				text= '.'.join(dominio[-3:])
		if subtext in dominios_especiales:
			subtext=''

		return (text,subtext)
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

	def save_file(self,fileName:str,content:list,encoding:str='utf-8'):
		save_route = self.get_save_route(f'{fileName}')
		print(f'Guardando archivo {fileName} en. \n{save_route}')
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
		dominios_por_archivo_origen:dict[str,list]={}

		for file_name in tqdm(files_names):
			self.load_domains(str(file_name))
			# self.save_file(str(file_name),)
		
		# print(self.dominios)
		# for file_name in files_names:
			# file_name_=self.getlistname(str(file_name))
		print(f"organizando archivo..")
		for dominio in tqdm(self.dominios.items()):
			origen =str(dominio[1].get("origen"))
			if origen is not None or origen!='':
				if origen not in dominios_por_archivo_origen:
					dominios_por_archivo_origen[origen]=[dominio[0]]
				else:
					dominios_por_archivo_origen[origen].append(dominio[0])
		
		for origen in dominios_por_archivo_origen:
			self.save_file(origen,dominios_por_archivo_origen[origen])
				# dominios_por_archivo_origen
				# print(dominio)
			# print(dominio)
		
			# filename=
	# def evaluarDominios(self)


if __name__=="__main__":
	piholeLists_E=piholeLists()
	piholeLists_E.launch()