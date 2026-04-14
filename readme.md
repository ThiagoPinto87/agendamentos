# O que é o Agendamento
É um aplicativo de agendamento padrão que utiliza o google calendário para enviar aos clientes a confirmação de agendamento para que todos possam ficar preparados para as reuniões.


## Ações para desenvolver:

1 - Capturar atualizações no google calendário à medida que o usuário atualiza (pode ser sempre ao final do dia)
1.1 - Foi feito, porém, não está enviando a mensagem para cada cliente, o que está sendo feito é o resumo dos próximos 10 eventos para mim como um resumo.

1.2 - Identificar quais clientes são e pegar o telefone deles e enviar mensagem para cada patrocinador.

2 - Enviar toda a amanhã a agenda dos próximos dois dias confirmando a agenda com o cliente através do whatsapp

3 - Permitir que o usuário agende através do whatsapp com um comando específico como `/`

4 - Receber a resposta do cliente como confirmado ou algo do tipo: "Digite 1 para confirmado ou 2 para remarcar".







## Ações essenciais
É necessário criar uma credencial no google agenda utilizando dos seguintes passos:


### 1. Configuração no Google Cloud Console
Antes de codar, você precisa habilitar a API e obter suas credenciais:

- Acesse o Google Cloud Console.

- Crie um novo projeto (ou selecione um existente).

- Vá em APIs e Serviços > Biblioteca e pesquise por "Google Calendar API". Clique em Ativar.

- Vá em Tela de consentimento OAuth:

  - Escolha "External" (ou Internal se tiver Google Workspace).

  - Preencha os dados básicos e adicione seu e-mail como Test User.

- Vá em Credenciais:

  - Clique em Criar Credenciais > ID do cliente OAuth.

  - Tipo de aplicativo: Desktop App.

  - Baixe o arquivo JSON e renomeie-o para credentials.json. Guarde-o na pasta do seu projeto.