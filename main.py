import os.path
import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Importa a função do seu outro ficheiro
from aviso_whatsapp import enviar_mensagem
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()


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
        maxResults=50,    # Aumentado para garantir que pega todos os eventos desses 3 dias
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
        
        print(f"Evento encontrado: {titulo} | Início: {start}")
        
        # Chama a sua automação do WhatsApp
        enviar_mensagem(titulo, start)

if __name__ == '__main__':
    listar_e_avisar()