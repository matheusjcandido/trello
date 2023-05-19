from trello import TrelloClient
import requests
import openai
import streamlit as st
import pyperclip


st.title('Geração de texto de despacho')

st.write('Este aplicativo gera uma sugestão de despacho para um cartão do Trello usando ChatGPT.')


key = st.secrets["key"]
token = st.secrets["token"]
openai_key = st.secrets["openai_key"]

client = TrelloClient(api_key=key, token=token)

board_id = 'S91JcAz2'

url = f"https://api.trello.com/1/boards/{board_id}/cards?key={key}&token={token}"

response = requests.get(url)

card_descriptions = {}  # Dicionário para armazenar as descrições

if response.status_code == 200:
    cards = response.json()
    for card in cards:
        card_id = card['id']
        card_name = card['name']

        card_url = f"https://api.trello.com/1/cards/{card_id}?key={key}&token={token}"
        card_response = requests.get(card_url)
        if card_response.status_code == 200:
            card_data = card_response.json()
            card_desc = card_data['desc']

            # Armazenando a descrição no dicionário
            card_descriptions[card_name] = card_desc

            print(f"Card Name: {card_name}\nCard Description: {card_desc}")

else:
    print(f"Request failed with status code {response.status_code}")

# possibilitar que o usuário escolha entre os cartões disponíveis por meio de um widget de seleção
st.write('Selecione um cartão para gerar um despacho:')
card_name = st.selectbox('Selecione um cartão', list(card_descriptions.keys()))

openai.api_key = openai_key

# adicionar um botão para gerar um despacho
def run_code():
    
    # Certifique-se de que o cartão existe no dicionário
    if card_name in card_descriptions:
        description = card_descriptions[card_name]

        messages = [
           {"role": "system", "content": "Você é um assistente que escreve despachos do Comandante-Geral do Corpo de Bombeiros Militar do Paraná. Sua tarefa é escrever um despacho de acordo com o contexto.\
             Escreva em um tom conciso, profissional e objetivo. Não expanda eventuais acrônimos, deixando-os em formato de sigla.\
            assine o despacho como 'Coronel QOBM Manoel Vasco de Figueiredo Junior, Comandante-Geral do Corpo de Bombeiros Militar do Paraná'.\
            O despacho deve ser escrito no seguinte formato: \
            'Ciente. \
            2. Decisão a ser tomada sobre o assunto. \
            3. Encaminhamento do expediente. \
            Assinatura do Comandante'. "},
            {"role": "user", "content": description},
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        generated_text = response.choices[0].message['content']
        st.write(generated_text)
        
        if st.button("Copiar"):
            pyperclip.copy(generated_text)
            st.info("Texto copiado para a área de transferência!")
    else:
        st.text(f"Card '{card_name}' not found in descriptions.")

# adicionar a resposta como texto em um widget de texto para que o usuário possa vê-lo
if st.button("Gerar Despacho"):
    run_code()
