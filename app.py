import streamlit as st
import numpy as np

st.set_page_config(page_title="Fit Calculator", layout="wide")

st.title("💪 Fit Calculator")

# Função para calcular o IMC
def calcular_imc(peso, altura):
    return peso / (altura*altura)

def imc_status(imc):
    imc_status = ""
    caution_status = 1
    if imc >= 40.0:
        imc_status = "Obesidade grau 3"
        caution_status = 3
    elif 35.0 <= imc < 40.0:
        imc_status = "Obesidade grau 2"
        caution_status = 3
    elif 30.0 <= imc < 35.0:
        imc_status = "Obesidade grau 1"
        caution_status = 3
    elif 25.0 <= imc < 30.0:
        imc_status = "Sobrepeso"
        caution_status = 2
    elif 18.5 <= imc < 25.0:
        imc_status = "Normal"
        caution_status = 1
    elif  imc < 18.5:
        imc_status = "Abaixo do normal"
        caution_status = 2
    return imc_status, caution_status

# Função para calcular a TMB
def calcular_tmb(sexo, peso, altura, idade):
    if sexo == "Homem":
        return 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * idade)
    else:
        return 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * idade)

# Função para calcular o percentual de gordura corporal
def calcular_gordura(sexo, altura, pescoco, cintura, quadril=None):
    if sexo == "Homem":
        return 86.01 * np.log10(cintura - pescoco) - 70.041 * np.log10(altura) + 36.76
    else:
        return 163.205 * np.log10(cintura + quadril - pescoco) - 97.684 * np.log10(altura) - 78.387

# Função para calcular o peso ideal
def calcular_peso_ideal(sexo, altura):
    altura_pol = altura / 2.54  # Converter cm para polegadas
    if sexo == "Homem":
        return 50 + (2.3 * (altura_pol - 60))
    else:
        return 45.5 + (2.3 * (altura_pol - 60))

# Função para calcular os macronutrientes
def calcular_macros(calorias, objetivo):
    if objetivo == "Manutenção":
        carbs, prot, gord = 50, 20, 30
    elif objetivo == "Ganho de Massa":
        carbs, prot, gord = 40, 30, 30
    else:  # Perda de Peso
        carbs, prot, gord = 20, 40, 40

    carbs_g = (calorias * carbs / 100) / 4
    prot_g = (calorias * prot / 100) / 4
    gord_g = (calorias * gord / 100) / 9

    return carbs_g, prot_g, gord_g

# Criando abas no Streamlit
aba = st.sidebar.radio("Escolha uma calculadora", ["IMC", "TMB", "Gordura Corporal", "Peso Ideal", "Macronutrientes"])

if aba == "IMC":
    st.header("📏 Índice de Massa Corporal (IMC)")
    peso = st.number_input("Peso (kg)", min_value=10.0, max_value=300.0, step=0.1)
    altura = st.number_input("Altura (m)", min_value=0.5, max_value=2.5, step=0.01)
    
    if st.button("Calcular IMC"):
        imc = calcular_imc(peso, altura)
        st.write("Seu IMC é:")
        st.subheader(f"{imc:.2f} kg/m²")

        imc_status, caution_status = imc_status(imc)

        if caution_status == 3:
            st.error(imc_status)
        elif caution_status == 2:
            st.warning(imc_status)
        elif caution_status == 1:
            st.success(imc_status)

elif aba == "TMB":
    st.header("🔥 Taxa Metabólica Basal (TMB)")
    sexo = st.selectbox("Sexo", ["Homem", "Mulher"])
    peso = st.number_input("Peso (kg)", min_value=10.0, max_value=300.0, step=0.1)
    altura = st.number_input("Altura (m)", min_value=0.5, max_value=2.5, step=0.01)
    idade = st.number_input("Idade", min_value=10, max_value=120, step=1)

    altura_cm = altura*100
    
    if st.button("Calcular TMB"):
        tmb = calcular_tmb(sexo, peso, altura_cm, idade)
        st.write("Sua TMB é:")
        st.subheader(f"{tmb:.2f} kcal/dia")

elif aba == "Gordura Corporal":
    st.header("⚖️ Gordura Corporal")
    sexo = st.selectbox("Sexo", ["Homem", "Mulher"])
    altura = st.number_input("Altura (m)", min_value=0.5, max_value=2.5, step=0.01)
    pescoco = st.number_input("Circunferência do Pescoço (cm)", min_value=20.0, max_value=70.0, step=0.1)
    cintura = st.number_input("Circunferência da Cintura (cm)", min_value=50.0, max_value=200.0, step=0.1)

    altura_cm = altura*100

    if sexo == "Mulher":
        quadril = st.number_input("Circunferência do Quadril (cm)", min_value=50.0, max_value=200.0, step=0.1)
    else:
        quadril = None
    
    if st.button("Calcular Gordura Corporal"):
        gordura = calcular_gordura(sexo, altura_cm, pescoco, cintura, quadril)
        st.write("Seu percentual de gordura corporal é:")
        st.subheader(f"{gordura:.2f} %")

elif aba == "Peso Ideal":
    st.header("🏋️ Peso Ideal")
    sexo = st.selectbox("Sexo", ["Homem", "Mulher"])
    altura = st.number_input("Altura (m)", min_value=0.5, max_value=2.5, step=0.01)

    altura_cm = altura*100

    if st.button("Calcular Peso Ideal"):
        peso_ideal = calcular_peso_ideal(sexo, altura_cm)
        st.write("Seu peso ideal é:")
        st.subheader(f"{peso_ideal:.2f} kg")

elif aba == "Macronutrientes":
    st.header("🍎 Calculadora de Macronutrientes")
    calorias = st.number_input("Calorias diárias recomendadas (kcal)", min_value=500, max_value=5000, step=10)
    objetivo = st.selectbox("Objetivo", ["Manutenção", "Ganho de Massa", "Perda de Peso"])

    if st.button("Calcular Macronutrientes"):
        carbs, prot, gord = calcular_macros(calorias, objetivo)
        st.write(f"**Quantidades:**\n - Carboidratos: {carbs:.2f}g\n - Proteínas: {prot:.2f}g\n - Gorduras: {gord:.2f}g")

