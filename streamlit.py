import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# Carregar o dataset de preços
data = pd.read_csv('dataset_precos_combustiveis.csv')

# Criar o modelo de regressão linear para a previsão
X = data[['Ano', 'Inflação (%)', 'Preço do Petróleo (R$/L)', 'Taxa de Câmbio (R$)']]
y_gasolina = data['Preço Gasolina (R$/L)']
y_etanol = data['Preço Etanol (R$/L)']

# Treinar o modelo de regressão linear para gasolina
model_gasolina = LinearRegression()
model_gasolina.fit(X, y_gasolina)

# Treinar o modelo de regressão linear para etanol
model_etanol = LinearRegression()
model_etanol.fit(X, y_etanol)

# Função para calcular o preço futuro baseado na inflação
def prever_preco_futuro(inflacao, ano):
    entrada = [[ano, inflacao, data['Preço do Petróleo (R$/L)'].mean(), data['Taxa de Câmbio (R$)'].mean()]]
    preco_gasolina = model_gasolina.predict(entrada)
    preco_etanol = model_etanol.predict(entrada)
    return preco_gasolina[0], preco_etanol[0]

# Configurações do Streamlit
st.title("Calculadora de Economia de Combustível")



# Página principal
menu = st.sidebar.selectbox("Escolha uma página", ["Calculadora de Combustível", "Previsão de Preço Futuro"])

if menu == "Calculadora de Combustível":
    st.header("Calculadora: Etanol ou Gasolina?")
    
    # Entrada do usuário
    preco_gasolina = st.number_input("Preço da Gasolina (R$/L):", min_value=0.0, step=0.01)
    preco_etanol = st.number_input("Preço do Etanol (R$/L):", min_value=0.0, step=0.01)
    consumo_gasolina = st.number_input("Consumo de Gasolina (Km/L):", min_value=0.0, step=0.01)
    consumo_etanol = st.number_input("Consumo de Etanol (Km/L):", min_value=0.0, step=0.01)
    
    if st.button("Calcular"):
        # Calcular o custo por km
        custo_km_gasolina = preco_gasolina / consumo_gasolina
        custo_km_etanol = preco_etanol / consumo_etanol
        
        st.write(f"Custo por Km com Gasolina: R$ {custo_km_gasolina:.2f}")
        st.write(f"Custo por Km com Etanol: R$ {custo_km_etanol:.2f}")
        
        if custo_km_gasolina < custo_km_etanol:
            st.success("Gasolina compensa mais!")
        else:
            st.success("Etanol compensa mais!")
            
elif menu == "Previsão de Preço Futuro":
    st.header("Previsão de Preço Futuro com Base na Inflação")
    
    # Entrada para previsão
    ano = st.number_input("Insira o ano futuro para previsão:", min_value=2024, step=1)
    inflacao_futura = st.slider("Insira a inflação estimada (%):", min_value=0.0, max_value=20.0, step=0.1)
    
    if st.button("Prever Preços"):
        preco_gasolina_futuro, preco_etanol_futuro = prever_preco_futuro(inflacao_futura, ano)
        
        st.write(f"Previsão de preço da Gasolina em {ano}: R$ {preco_gasolina_futuro:.2f}/L")
        st.write(f"Previsão de preço do Etanol em {ano}: R$ {preco_etanol_futuro:.2f}/L")
