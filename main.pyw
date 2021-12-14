import PySimpleGUI as sg
import logging
import threading
import webbrowser
from conexao import *
from controller import *

# pyinstaller main.pyw --icon=upload-file.ico --upx-dir=..\upx391w -y --onefile

# configura o tipo de erro e o arquivo que será gerado
logging.basicConfig(handlers=[logging.FileHandler(filename="./app.log", encoding='utf-8', mode='a')],
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", level=logging.ERROR)


sg.theme('LightGrey1')

tabArquivos = [
    [sg.FilesBrowse('Escolher arquivos', target='arquivos'),
     sg.Input(key='arquivos', size=(50, 10), disabled=True)],
    [sg.ProgressBar(max_value=100, orientation='h',
                    size=(50, 10), metadata='Teste', key='progressbar1', bar_color=['Green', 'Grey'])],
    [sg.Button('Enviar Arquivos')]
]

tabPastas = [
    [sg.FolderBrowse('Escolher Pasta', target='pasta'),
     sg.Input(key='pasta', size=(50, 10), disabled=True)],
    [sg.ProgressBar(max_value=100, orientation='h',
                    size=(50, 10), metadata='Teste', key='progressbar2', bar_color=['Green', 'Grey'])],
    [sg.Button('Enviar Pasta')]
]


tabConfig = [
    [sg.Text('Informe seu token:')],
    [sg.Input(key='token', size=(50, 10))],
    [sg.Button('Salvar Token'), sg.Button('Buscar Token', button_color='Green'),
     sg.Button('Excluir Token', button_color='Grey')]
]


tab_principal = [

    [sg.TabGroup([
        [sg.Tab('Upload Arquivos', tabArquivos)],
        [sg.Tab('Upload Pasta', tabPastas)],
        [sg.Tab('Config', tabConfig)],
    ], tab_background_color='Grey', tab_location='topleft', enable_events=True, key="output_tabgroup")],
    [sg.Text('Log:')],
    [sg.Output(size=(80, 4))]

]


janela = sg.Window('Upload Arquivos Content', tab_principal,
                   finalize=True, size=(500, 250))

progress_bar1 = janela['progressbar1']
progress_bar2 = janela['progressbar2']

thread1 = None
thread2 = None

while True:
    event, values = janela.Read()

    if event == sg.WIN_CLOSED:
        janela.close()
        break

    if event == 'Enviar Arquivos' and thread1 == None:
        # upload de multiplos arquivos
        if(values['token'] == ''):
            sg.popup('Insira seu token na aba config.')
        else:
            # thread_parte1 inicialização
            thread1 = threading.Thread(target=uploadArquivos, args=(
                janela, values, progress_bar1,), daemon=True)
            thread1.start()

    elif event == 'thread1_finalizada':
        # thread_parte3 finalização
        thread1.join()
        thread1 = None

        print('[Script Upload Arquivos Finalizado... ]')

        janela['Enviar Arquivos'].update(disabled=False)
        janela['Escolher arquivos'].update(disabled=False)

        janela['Upload Pasta'].update(disabled=False)
        janela['Config'].update(disabled=False)
        # # Fim Upload arquivos

    if event == 'Enviar Pasta' and thread2 == None:
        if(values['token'] == ''):
            sg.popup('Insira seu token na aba config.')
        else:
            # thread_parte1 inicialização
            thread2 = threading.Thread(target=uploadPasta, args=(
                janela, values, progress_bar2,), daemon=True)
            thread2.start()

    if event == 'thread2_finalizada':
        # thread_parte3 finalização
        thread2.join()
        thread2 = None

        janela['Escolher Pasta'].update(disabled=False)
        janela['Enviar Pasta'].update(disabled=False)
        janela['Upload Arquivos'].update(disabled=False)
        janela['Config'].update(disabled=False)

        print("[ Script Upload Pasta Finalizado... ]")

        # fim upload de pasta

    if event == 'Salvar Token':
        if values['token'] != '':
            tokenVal = values['token']
            tokenEsp = tokenVal.replace(" ", "")
            tokenStr = 'Bearer ' + tokenEsp
            conn_upload.headers = {'Authorization': tokenStr,
                                   'Content-Disposition': 'form-data; name="jsonInputParameters"'}
            conn_pasta.headers = {'Authorization': tokenStr,
                                  'Content-Type': 'application/json'}
            print(f'Token inserido: {tokenStr}')

    if event == 'Excluir Token':
        if values['token'] != '':
            janela['token'].update('')
            print('Token excluido')

    if event == 'Buscar Token':
        broswer = webbrowser.open_new_tab(
            'https://solvigedtest-solvioracle.cec.ocp.oraclecloud.com/documents/web?IdcService=GET_OAUTH_TOKEN')
