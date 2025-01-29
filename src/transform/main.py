#importações
import pandas as pd
import sqlite3
from datetime import datetime

#caminho do jsonç
df = pd.read_json('../data/data.jsonl', lines=True)

#setando o pandas para mostrar todas as colunas
pd.options.display.max_columns = None

#novas colunas
df['source'] = "https://lista.mercadolivre.com.br/tenis-corrida-masculino"
df['data_coleta'] = datetime.now()

#tratamento das colunas 
df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_cents'] = df['old_price_cents'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_price_cents'] = df['new_price_cents'].fillna(0).astype(float)
df['review_rating_number'] = df['review_rating_number'].fillna(0).astype(float)

#removendo parênteses
df['reviews_amount'] = df['reviews_amount'].str.replace('[\(\)]', '', regex=True)
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

#tratamento de preços
df['old_price'] = df['old_price_reais'] + df['old_price_cents']/100
df['new_price'] = df['new_price_reais'] + df['new_price_cents']/100

#removendo colunas
df = df.drop(columns=['old_price_reais', 'old_price_cents', 'new_price_reais', 'new_price_cents'])

#conectando ao banco de dados 
conn = sqlite3.connect('../data/quotes.db')  

#salvando no banco de dados
df.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)

#fechando a conexão
conn.close()

print(df.head())