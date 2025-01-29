#improtações
import streamlit as st 
import pandas as pd
import sqlite3

# conectando ao banco de dado
conn = sqlite3.connect('../data/quotes.db')

#carregando a tabela
df = pd.read_sql('SELECT * FROM mercadolivre_items', conn)

#fechando a conexão
conn.close()

#título
st.title('Pesquisa de mercado - Tênis do Mercado Livre')
st.subheader("Principais KPI's da pesquisa")
col1, col2, col3 = st.columns(3)

#KIP 1 - número total de itens
total_items = df.shape[0] #calculando itens totais
col1.metric(label="Número total de itens", value=total_items)

#KIP 2 - número de marcas unicas
unique_brands = df['brand'].nunique() #calculando itens totais
col2.metric(label="Número de marcas únicas", value=unique_brands)

#KIP 3 - preço médio novo (em reais)
avarage_new_price = df['new_price'].mean() #calculando itens totais
col3.metric(label="Preço médio novo (R$)", value=f"{avarage_new_price:.2f}")

#Quiais marcas são mais encontradas até a 10° página
st.subheader('Marcas mais encontradas até a 10° página')
col1,col2 = st.columns([4,2])
top_10_pages_brands = df['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_10_pages_brands)
col2.write(top_10_pages_brands)

#qual o preço médio por marca
st.subheader('Preço médio por marca')
col1,col2 = st.columns([4,2])
df_non_zero_prices = df[df['new_price'] > 0]
avarege_price_by_brand = df_non_zero_prices.groupby('brand')['new_price'].mean().sort_values(ascending=False)
col1.bar_chart(avarege_price_by_brand)
col2.write(avarege_price_by_brand)

#qual a satisfação por marca
st.subheader('Satisfação por marca')
col1,col2 = st.columns([4,2])  
df_non_zero_reviews = df[df['review_rating_number'] > 0]
satisfaction_by_bran = df_non_zero_reviews.groupby('brand')['review_rating_number'].mean().sort_values(ascending=False)
col1.bar_chart(satisfaction_by_bran)    
col2.write(satisfaction_by_bran)