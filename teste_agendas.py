import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Usamos o mesmo escopo do seu projeto principal
SCOPES = ['https://www.googleapis.com/auth/calendar']

def verificar_minhas_agendas():
    """
    Função simples para listar todas as agendas que o código consegue ler
    e exibir os seus respetivos IDs.
    """
    # Lê o token que já está salvo e funcionando
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        print("Erro: Arquivo token.json não encontrado. Rode o Main.py primeiro.")
        return

    service = build('calendar', 'v3', credentials=creds)

    print("A procurar as suas agendas autorizadas...\n")
    
    # Pede ao Google a lista de todas as agendas do utilizador
    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get('items', [])

    if not calendars:
        print('Nenhuma agenda encontrada nesta conta.')
        return

    # Imprime o Nome e o ID de cada agenda
    for calendar in calendars:
        nome = calendar.get('summary', 'Sem nome')
        agenda_id = calendar.get('id', 'Sem ID')
        
        print(f"Nome da Agenda: {nome}")
        print(f"ID exato: {agenda_id}")
        print("-" * 40)

if __name__ == '__main__':
    verificar_minhas_agendas()
    