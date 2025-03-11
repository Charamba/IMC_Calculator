import streamlit as st

st.header("IMC Calculator")

st.write("*BMI Calculator*")

def imc_status(imc):
    imc_status = ""
    caution_status = 1
    if imc > 40.0:
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

peso = st.number_input("Peso (kg):", min_value=0.0)
altura = st.number_input("Altura (m):", min_value=0.0)


if st.button("Calcular"):
    if altura > 0:
        imc = peso/(altura*altura)
        formatted_imc = f"{imc:.2f}"

        imc_status, caution_status = imc_status(imc)

        st.write("----------")
        st.write("Seu IMC é:")
        st.subheader(formatted_imc + "kg/m²")

        if caution_status == 3:
            st.error(imc_status)
        elif caution_status == 2:
            st.warning(imc_status)
        elif caution_status == 1:
            st.success(imc_status)
    else:
        st.warning("Digite um valor para altura.")
