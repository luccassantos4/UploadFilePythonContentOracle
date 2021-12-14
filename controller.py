# funções
import PySimpleGUI as sg
import requests
import logging
import os
from os.path import isfile, join
import json
from os.path import isfile, join
from conexao import *


# configura o tipo de erro e o arquivo que será gerado
logging.basicConfig(handlers=[logging.FileHandler(filename="./app.log", encoding='utf-8', mode='a')],
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", level=logging.ERROR)


# cria a pasta no content
def criarPastaContent(pasta):
    pasta = json.dumps({'name': pasta, 'description': None})
    response = requests.request(
        "POST", conn_pasta.url, headers=conn_pasta.headers, data=pasta)
    if response.status_code == 401:
        return 'self'
    else:
        idPasta = json.loads(response.text)
    return idPasta['id']


def retornaPastaArquivos(diretorio):
    # retorna o nivel acima da pasta dos arquivo
    path = os.path.normpath(diretorio)
    nomePasta = path.split(os.sep)[-2]
    return nomePasta


def retornaPasta(diretorio):
    # retorna o nivel acima da pasta
    path = os.path.normpath(diretorio)
    nomePasta = path.split(os.sep)[-1]
    return nomePasta


def uploadArquivos(janela, values, progress_bar1):
    
        #thread_parte2 operação demorada
        print('[Script Upload Arquivos Iniciado... ]')

        janela['Enviar Arquivos'].update(disabled=True)
        janela['Escolher arquivos'].update(disabled=True)

        janela['Upload Pasta'].update(disabled=True)
        janela['Config'].update(disabled=True)

        diretorios = values['arquivos'].split(';')
        qtdArquivos = len(diretorios)
        i = 1
        for indice, diretorioList in enumerate(diretorios):
            diretorio = diretorioList.replace("/", f"{os.sep}")
            nomeArquivo = os.path.basename(diretorio)

            i = i + 100 / qtdArquivos
            progress_bar1.UpdateBar(i)

            if os.path.exists(diretorio) == False:
                logging.error(
                    f' Diretório não existe: [ {diretorio} ] \n \n')
                continue
            try:
                if indice == 0:
                    nomePasta = retornaPastaArquivos(diretorio)
                    idPastaContent = criarPastaContent(nomePasta)
                else:
                    idPastaContent = idPastaContent
            except ValueError as erro1:
                logging.error(
                    f' Erro na criação da pasta {nomePasta} | {erro1} \n \n')
            finally:
                
                if isfile(diretorio):
                    files = {'primaryFile': open(diretorio, 'rb')}
                    response = requests.request("POST", conn_upload.url, headers=conn_upload.headers, data={'jsonInputParameters': '{"parentID": "'+idPastaContent+'"}'}, files=files)
                    if response.status_code == 201:
                        print(
                            f'{indice + 1}. [{response.status_code}] Upload do arquivo [{nomeArquivo}] na pasta [{nomePasta}] realizado com sucesso!')
                    elif response.status_code == 401:
                        print(
                            f'{indice + 1}.[{response.status_code}] ERRO: Consulte o arquivo LOG')
                        logging.error(
                            f" [ Upload do arquivo ] Erro na requisição: {response.text} | Código [ {response.status_code} ] \n \n")
                    else:
                        print(
                            f"{indice + 1}. [{response.status_code}] ERRO: Consulte o arquivo LOG")
                        logging.error(
                            f" Erro na requisição: {response.text} | Diretório: [ {diretorio} ] \n \n")

        janela.write_event_value('thread1_finalizada', 'Finalizado')




def uploadPasta(janela, values, progress_bar2):
    #thread_parte2 operação demorada
    print('[ Script Upload Pasta Iniciado... ]')

    janela['Escolher Pasta'].update(disabled=True)
    janela['Enviar Pasta'].update(disabled=True)
    janela['Upload Arquivos'].update(disabled=True)
    janela['Config'].update(disabled=True)

    diretorio = values['pasta'].replace("/", f"{os.sep}")
    try:
        nomePasta = retornaPasta(diretorio)
        idPastaContent = criarPastaContent(nomePasta)
    except ValueError as erro1:
        logging.error(
            f' Erro na criação da pasta {nomePasta} | {erro1} \n \n')
    finally:

        i = 1
        qtdArquivos = len(os.listdir(diretorio))
        for indice, arquivo in enumerate(os.listdir(diretorio)):
            if os.path.exists(diretorio) == False:
                logging.error(f' Diretório não existe: [ {diretorio} ] \n \n')
                continue

            i = i + 100 / qtdArquivos
            progress_bar2.UpdateBar(i)

            if isfile(join(diretorio, arquivo)):
                files = {'primaryFile': open(os.path.join(
                    diretorio + os.sep + arquivo), 'rb')}
                response = requests.request("POST", conn_upload.url, headers=conn_upload.headers, data={
                    'jsonInputParameters': '{"parentID": "'+idPastaContent+'"}'}, files=files)
                if response.status_code == 201:
                    print(
                        f'{indice + 1}. [{response.status_code}] Upload do arquivo: {arquivo} na pasta {nomePasta} realizado com sucesso!')
                elif response.status_code == 401:
                    print(
                        f'{indice + 1}. [{response.status_code}] ERRO: Consulte o arquivo LOG')
                    logging.error(
                        f"[ Upload do arquivo ] Erro na requisição: {response.text} | Código [ {response.status_code} ] \n \n")
                else:
                    print(f'{indice + 1}. ERRO: Consulte o arquivo LOG')
                    logging.error(
                        f"Erro na requisição: {response.text} | Diretório: [ {diretorio} ] \n \n")

        janela.write_event_value('thread2_finalizada', 'Finalizado')
