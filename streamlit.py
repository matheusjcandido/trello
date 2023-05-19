import streamlit as st
from trello import TrelloClient
from openai import ChatCompletion

# Configure o cliente do Trello e a API do OpenAI
client = TrelloClient(
    api_key='d92cfcb705fb180c21d028fe5bf20cfa',
    #api_secret='your_api_secret',
    token='ATTAb5fe28ac6cb9faeffd52d0074b5d9b3091fd6e23752fd3fe7ce364f7b32df65b80BF8D42',
    #token_secret='your_oauth_token_secret'
)

openai_api_key = "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"
openai_model = "gpt-3.5-turbo"

# Crie um widget de botão para atualizar as informações do Trello
if st.button('Atualizar informações do Trello'):
    # Obtenha todos os quadros do Trello
    all_boards = client.list_boards()
    # Crie um widget de seleção para escolher um quadro
    selected_board = st.selectbox('Selecione um quadro', all_boards)

    # Obtenha todos os cartões do quadro selecionado
    all_cards = selected_board.list_cards()
    # Crie um widget de seleção para escolher um cartão
    selected_card = st.selectbox('Selecione um cartão', all_cards)

    # Crie um widget de botão para gerar um despacho
    if st.button('Gerar despacho'):
        # Obtenha a descrição do cartão selecionado
        description = selected_card.description

        # Use a descrição como prompt para a API do OpenAI
        chat = ChatCompletion.create(
          model=openai_model,
          messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": description},
            ]
        )

        # Obtenha a resposta da API do OpenAI
        response = chat['choices'][0]['message']['content']

        # Adicione a resposta como comentário no cartão selecionado
        selected_card.comment(response)

        # Mostre a resposta ao usuário
        st.write(response)
