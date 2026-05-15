import sqlite3
import os.path
import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pywhatkit

# Importa a função do seu outro ficheiro
from aviso_whatsapp import enviar_mensagem
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()



# ==========================================
# 1. FUNÇÕES DE BANCO DE DADOS
# ==========================================

def cadastrar_cliente(nome_cliente, id_grupo):
    """Conecta ao banco e insere um novo cliente na tabela Clientes."""
    try:
        # Abre a conexão com o banco que criamos
        conexao = sqlite3.connect('banco_whatsapp.db')
        cursor = conexao.cursor()
        
        # Comando SQL para inserir dados. 
        # ATENÇÃO: Os pontos de interrogação (?) são espaços reservados.
        sql_insert = "INSERT INTO Clientes (cliente, id_grupo_whatsapp) VALUES (?, ?)"
        
        # Executa o comando trocando os '?' pelas variáveis que recebemos
        cursor.execute(sql_insert, (nome_cliente, id_grupo))
        
        # Salva as alterações no arquivo do banco de dados
        conexao.commit()
        print(f"\n✅ Sucesso! Cliente '{nome_cliente}' foi salvo no banco de dados.")
        
    except sqlite3.Error as erro:
        # Se algo der errado, mostramos o erro sem quebrar o programa
        print(f"\n❌ Erro ao tentar salvar no banco de dados: \n{erro}")
        
    finally:
        # Garante que a conexão será fechada, dando erro ou não
        if conexao:
            conexao.close()


# ==========================================
# 2. INTERFACE COM O TERMINAL (MENU)
# ==========================================

def iniciar_sistema():
    """Mostra um menu no terminal para o usuário interagir."""
    print("🤖 Bem-vindo ao Sistema de Agendamentos do WhatsApp!")
    
    # O 'while True' cria um loop infinito para o menu não fechar sozinho
    while True:
        print("\n" + "="*30)
        print("Menu de Opções:")
        print("1 - Cadastrar novo Cliente")
        print("9 - Enviar mensagens de aviso para os próximos compromissos")
        print("0 - Sair do programa")
        print("="*30)
        
        # Pega a resposta que o usuário digitar no terminal
        opcao = input("👉 Escolha uma opção: ")
        
        if opcao == '1':
            # Pede os dados do cliente
            print("\n--- Novo Cadastro ---")
            nome = input("Digite o nome do cliente: ")
            grupo = input("Digite o ID do grupo do WhatsApp: ")
            
            # Chama a função que salva no banco de dados
            cadastrar_cliente(nome, grupo)

        elif opcao == '9':
            print("\n🚀 Enviando mensagens de aviso para os próximos compromissos...")
            listar_e_avisar()
            
        elif opcao == '0':
            print("\n👋 Saindo do sistema. Até logo!")
            break # Quebra o 'while True' e encerra o programa
            
        else:
            print("\n⚠️ Opção inválida. Tente novamente digitando 1 ou 0.")



# ============================================================
# 3. FUNÇÃO PRINCIPAL PARA LISTAR AGENDAS E ENVIAR AVISOS
# ============================================================


# Escopos de acesso (Leitura e escrita na agenda)
SCOPES = ['https://www.googleapis.com/auth/calendar']

def obter_credenciais():
    """
    Função responsável por ler ou criar o token.json com as permissões do usuário.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def listar_e_avisar():
    """
    Função principal que busca as agendas num intervalo de 3 dias (Hoje até Depois de Amanhã)
    e envia para o WhatsApp.
    """
    creds = obter_credenciais()
    service = build('calendar', 'v3', credentials=creds)

    # 1. Obter a data e hora local do seu computador (para respeitar o seu fuso horário)
    agora_local = datetime.datetime.now().astimezone()

    # 2. Definir o início de "hoje" (00h:00min:00s)
    inicio_hoje = agora_local.replace(hour=0, minute=0, second=0, microsecond=0)

    # 3. Definir o final do período (hoje + 2 dias = 3 dias no total, às 23h:59min:59s)
    # Exemplo: Se hoje é dia 14, isso vai calcular o dia 16 às 23:59:59
    fim_periodo = (inicio_hoje + datetime.timedelta(days=2)).replace(hour=23, minute=59, second=59)

    # 4. Converter essas datas locais para UTC (padrão que o Google Calendar exige)
    time_min = inicio_hoje.astimezone(datetime.timezone.utc).isoformat().replace('+00:00', 'Z')
    time_max = fim_periodo.astimezone(datetime.timezone.utc).isoformat().replace('+00:00', 'Z')
    
    # Exibe no terminal o período que está sendo buscado para facilitar o seu controle
    print(f"A procurar eventos de {inicio_hoje.strftime('%d/%m/%Y %H:%M')} até {fim_periodo.strftime('%d/%m/%Y %H:%M')}...")
    
    # 5. Procura os eventos no intervalo de tempo definido
    events_result = service.events().list(
        calendarId= os.getenv('ID_CALENDAR'), # Substitua pelo seu email do Google Calendar # type: ignore
        timeMin=time_min,
        timeMax=time_max, # Novo parâmetro: Limite máximo de data e hora!
        maxResults=20,    # Aumentado para garantir que pega todos os eventos desses 3 dias
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])

    if not events:
        print('Nenhum evento encontrado para os próximos 3 dias.')
        return

    print('\n--- Suas agendas para os próximos 3 dias ---')
    
    # 6. Varre todos os eventos encontrados e envia para a automação
    for event in events:
        # Pega a data/hora de início
        start = event['start'].get('dateTime', event['start'].get('date'))
        titulo = event.get('summary', 'Sem título')
        
        print(f"Compromisso: {titulo}\nInício: {start}")
        
        start_datetime = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
        start_formatted = start_datetime.strftime('%d/%m/%Y')
        
        mensagem = f"""
        Bom dia Tudo bem?
        Gostaria de confirmar nossa agenda para o dia {start_formatted} à partir das {start_datetime.strftime('%H:%M')}h.
        
        """
        mensagem_cliente = f"{titulo} abaixo."


        # Chama a sua automação do WhatsApp com a mensagem, fechando a aba do navegador após 2 segundos
        pywhatkit.sendwhatmsg_instantly("+5565996107333", mensagem_cliente, tab_close=True, close_time=4)
        pywhatkit.sendwhatmsg_instantly("+5565996107333", mensagem, tab_close=True, close_time=4)  # Substitua meu número pelo número do WhatsApp do cliente.
        # pywhatkit.sendwhatmsg_to_group_instantly("false_120363424733276564@g.us_3078658027create1776397806_269341794770973@lid", "Oi delicia", tab_close=True, close_time=2)  # Substitua pelo ID do grupo do WhatsApp


if __name__ == '__main__':
    iniciar_sistema()
    listar_e_avisar()