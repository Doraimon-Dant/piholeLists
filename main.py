from tqdm import tqdm

import os

dirpath=os.path.dirname(__file__)
files_name=['nsfw.txt','extense.txt']
tld_file_name='tlds.txt'
file_result='nsfw_optimized.txt'
tlds_file=os.path.join(dirpath,tld_file_name)
result_file=os.path.join(dirpath,file_result)
# dominioRemplazo='192.168.1.9'
dominioRemplazo='0.0.0.0'
dominios={}
tlds=[]
encabezado=''

print('cargando tlds..')
with open(tlds_file,"r",encoding='utf-8') as tldsx:
	content_file = tldsx.read()
	tlds=['.'.join(tld.split('.')[1:]) for tld in tqdm(content_file.split('\n'))]

# print(tlds)
print('Cargando Dominios..')
for file_name in files_name:
	workingfile=os.path.join(dirpath,file_name)
	print(f'Archivo actual {file_name}')
	with open(workingfile,"r",encoding='utf-8') as file:
		file_content=file.read()
		for line in tqdm(file_content.split('\n')):
			if not line.startswith('#'):
				sublines =line.split(' ')
				
				dominio=sublines[0].split('.')
				if len(sublines)>1:
					dominio=sublines[1].split('.')
				
				countDominio=len(dominio)
				
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


print('Guardando archivo..')
with open(result_file,"w",encoding='utf-8') as file:
		for dominio in tqdm(dominios):
			
			file.write(f'{dominioRemplazo} ||{dominio}^\n')
			

	# print(file_content)
