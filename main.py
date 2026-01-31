# import datetime
# import os.path
# import os.path
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.discovery import build
# from aviso_whatsapp import enviar_mensagem  # Importando sua automação

# # Se alterar estes escopos, exclua o arquivo token.json.
# SCOPES = ['https://www.googleapis.com/auth/calendar']

# def main():
#     creds = None

#     # O arquivo token.json armazena os tokens de acesso e atualização do usuário
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
#     # Se não houver credenciais válidas, peça ao usuário para fazer login.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
        
#         # Salva as credenciais para a próxima execução
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())

#     # Constrói o serviço da API
#     service = build('calendar', 'v3', credentials=creds)

#     # Exemplo: Listar os próximos 10 eventos da agenda principal
#     print('Obtendo os próximos 10 eventos...')
#     events_result = service.events().list(calendarId='primary', maxResults=10).execute()
#     events = events_result.get('items', [])

#     if not events:
#         print('Nenhum evento encontrado.')
#     for event in events:
#         start = event['start'].get('dateTime', event['start'].get('date'))
#         print(f"{start} - {event['summary']}")


# def listar_e_avisar():
#     # ... (lógica de autenticação aqui)
#     service = build('calendar', 'v3', credentials=creds)

#     # "now" no formato ISO 8601 (ex: 2023-10-27T10:00:00Z)
#     now = datetime.datetime.utcnow().isoformat() + 'Z' 

#     print('Buscando eventos futuros...')
    
#     # timeMin=now garante que só pegamos o que começa a partir de agora
#     # singleEvents=True expande eventos recorrentes em instâncias individuais
#     # orderBy='startTime' organiza do mais próximo ao mais distante
#     events_result = service.events().list(calendarId='primary', timeMin=now,
#                                         maxResults=10, singleEvents=True,
#                                         orderBy='startTime').execute()
#     events = events_result.get('items', [])

#     if not events:
#         print('Nenhum evento futuro encontrado.')
#         return

#     for event in events:
#         start = event['start'].get('dateTime', event['start'].get('date'))
#         titulo = event.get('summary', 'Sem título')
        
#         print(f"Evento encontrado: {titulo} em {start}")
        
#         # Chama a automação do WhatsApp para cada evento
#         enviar_mensagem(titulo, start)




# if __name__ == '__main__':
#     main()
#     listar_e_avisar()




import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timezone

# Importa a função do seu outro ficheiro
from aviso_whatsapp import enviar_mensagem

# Escopos de acesso (Leitura e escrita na agenda)
SCOPES = ['https://www.googleapis.com/auth/calendar']

def obter_credenciais():
    creds = None
    # O ficheiro token.json guarda as suas permissões já autorizadas
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Se não houver credenciais válidas, pede login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Guarda o token para a próxima vez
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def listar_e_avisar():
    # Aqui preenchemos a lógica de autenticação que faltava:
    creds = obter_credenciais()
    
    service = build('calendar', 'v3', credentials=creds)

    # Define o horário atual em formato UTC
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')

    print('A procurar eventos futuros...')
    
    # Procura os próximos 10 eventos a partir de "agora"
    events_result = service.events().list(
        calendarId='primary', 
        timeMin=now,
        maxResults=10, 
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])

    if not events:
        print('Nenhum evento futuro encontrado.')
        return

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        titulo = event.get('summary', 'Sem título')
        
        print(f"Evento encontrado: {titulo} em {start}")
        
        # Chama a sua automação do WhatsApp
        enviar_mensagem(titulo, start)

if __name__ == '__main__':
    listar_e_avisar()