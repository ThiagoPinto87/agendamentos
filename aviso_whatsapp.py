
def enviar_mensagem(evento_titulo, horario):
    # Me avisa do evento que será enviado para o WhatsApp.
    mensagem = f"Lembrete: Você tem o evento '{evento_titulo}' agendado para {horario}."
    
    print(f"--- Simulação de WhatsApp ---")
    print(f"Enviando: {mensagem}")
    # Exemplo com print, mas aqui entraria sua integração de Zap
    print(f"-----------------------------")