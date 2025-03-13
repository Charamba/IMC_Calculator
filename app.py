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

def imc_result_text(imc_status):
    result_text = ""

    if imc_status == "Abaixo do normal":
        result_text = "Procure um médico. Algumas pessoas têm um baixo peso por características do seu organismo e tudo bem. Outras podem estar enfrentando problemas, como a desnutrição. É preciso saber qual é o caso."
    elif imc_status == "Normal":
        result_text = "Que bom que você está com o peso normal! E o melhor jeito de continuar assim é mantendo um estilo de vida ativo e uma alimentação equilibrada."
    elif imc_status == "Sobrepeso":
        result_text = "Ele é, na verdade, uma pré-obesidade e muitas pessoas nessa faixa já apresentam doenças associadas, como diabetes e hipertensão. Importante rever hábitos e buscar ajuda antes de, por uma série de fatores, entrar na faixa da obesidade pra valer."
    elif imc_status == "Obesidade grau 1":
        result_text = "Sinal de alerta! Chegou na hora de se cuidar, mesmo que seus exames sejam normais. Vamos dar início a mudanças hoje! Cuide de sua alimentação. Você precisa iniciar um acompanhamento com nutricionista e/ou endocrinologista."
    elif imc_status == "Obesidade grau 2":
        result_text = "Mesmo que seus exames aparentem estar normais, é hora de se cuidar, iniciando mudanças no estilo de vida com o acompanhamento próximo de profissionais de saúde."
    elif imc_status == "Obesidade grau 3":
        result_text =  "Aqui o sinal é vermelho, com forte probabilidade de já existirem doenças muito graves associadas. O tratamento deve ser ainda mais urgente."
    
    return result_text



# Função para calcular a TMB
def calcular_tmb(sexo, peso, altura, idade):
    if sexo == "Homem":
        return 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * idade)
    else:
        return 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * idade)

# 
def calcular_get(tmb, atividade):
    if atividade == "Sedentário":
        return tmb*1.2
    elif atividade == "Levemente ativo":
        return tmb*1.375
    elif atividade == "Moderadamente ativo":
        return tmb*1.55
    elif atividade == "Muito ativo":
        return tmb*1.725
    elif atividade == "Extremamente ativo":
        return tmb*1.9

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
aba = st.sidebar.radio("Escolha uma calculadora", ["IMC", "Gasto Energético", "Gordura Corporal", "Peso Ideal", "Macronutrientes"])

if aba == "IMC":
    st.header("📏 Calculadora de Índice de Massa Corporal (IMC)")
    st.write("O **Índice de Massa Corporal (IMC)**, é um parâmetro utilizado para avaliar se seu peso está dentro do valor ideal para a sua altura. O IMC é calculado dividindo seu peso pelo o quadrado da sua altura.")
    peso = st.number_input("Peso (kg)", min_value=10.0, max_value=300.0, step=0.1)
    altura = st.number_input("Altura (m)", min_value=0.5, max_value=2.5, step=0.01)
    
    if st.button("Calcular IMC"):
        imc = calcular_imc(peso, altura)
        st.write("Seu IMC é:")
        st.subheader(f"{imc:.2f} kg/m²")

        imc_status, caution_status = imc_status(imc)

        if caution_status == 3:
            st.error("**" + imc_status + "**", icon="🚨")
        elif caution_status == 2:
            st.warning("**" + imc_status + "**", icon="⚠️")
        elif caution_status == 1:
            st.success("**" + imc_status + "**", icon="✅")

        st.write(imc_result_text(imc_status))

elif aba == "Gasto Energético":
    st.header("🔋Calculadora de Gasto Energético")
    st.subheader("🔥 Taxa Metabólica Basal (TMB)")
    st.write("A **Taxa Metabólica Basal (TMB)** é a quantidade mínima de energia que o corpo precisa para manter as funções vitais em repouso, como respiração, circulação e temperatura corporal. Ela representa cerca de 60% a 70% do gasto energético total diário e varia de acordo com sexo, idade, peso e altura.")
    sexo = st.selectbox("Sexo", ["Homem", "Mulher"])
    peso = st.number_input("Peso (kg)", min_value=10.0, max_value=300.0, step=0.1)
    altura = st.number_input("Altura (m)", min_value=0.5, max_value=2.5, step=0.01)
    idade = st.number_input("Idade", min_value=10, max_value=120, step=1)

    altura_cm = altura*100

    st.subheader("⚡ Multiplique pelo Nível de Atividade Física")
    st.write("Depois de calcular a TMB, multiplicamos esse valor por um fator de atividade para obter o **Gasto Energético Total (GET)**, que representa o total de calorias diárias considerando seu estilo de vida:")

    st.write("🛋️ **Sedentário** (pouco ou nenhum exercício): TMB × 1.2")
    st.write("🚶 **Levemente ativo** (exercício leve 1-3 dias/semana): TMB × 1.375")
    st.write("🏃 **Moderadamente ativo** (exercício moderado 3-5 dias/semana): TMB × 1.55")
    st.write("🏋️ **Muito ativo** (exercício intenso 6-7 dias/semana): TMB × 1.725")
    st.write("🏆 **Extremamente ativo** (atletas ou trabalho físico intenso): TMB × 1.9")

    atividade = st.selectbox("Nível de Atividade Física", ["Sedentário", "Levemente ativo", "Moderadamente ativo", "Muito ativo", "Extremamente ativo"])

    if st.button("Calcular Gasto Energético"):
        tmb = calcular_tmb(sexo, peso, altura_cm, idade)
        st.write("Sua Taxa Metabólica Basal é:")
        st.subheader(f"{tmb:.2f} kcal/dia")

        get = calcular_get(tmb, atividade)
        st.write("Seu Gasto Energético Total é:")
        st.subheader(f"{get:.2f} kcal/dia")


elif aba == "Gordura Corporal":
    st.header("⚖️ Calculadora de Gordura Corporal")
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
    st.header("🏋️ Calculadora de Peso Ideal")
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

