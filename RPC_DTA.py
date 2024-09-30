import streamlit as st

# Definir los percentiles 99 de troponinas de alta sensibilidad
troponina_roche_99 = 14  # ng/L
troponina_abbott_99 = 26  # ng/L

# Función para calcular HEART score
def calcular_HEART_score(edad, historia_clinica, ekg, factores_riesgo, troponina):
    score = 0
    # Edad
    if edad >= 65:
        score += 2
    elif 45 <= edad < 65:
        score += 1
    
    # Historia clínica
    score += historia_clinica
    
    # EKG
    score += ekg
    
    # Factores de riesgo
    score += factores_riesgo
    
    # Troponina
    if troponina > troponina_roche_99 or troponina > troponina_abbott_99:
        score += 2
    elif 0.5 * troponina_roche_99 < troponina <= troponina_roche_99 or 0.5 * troponina_abbott_99 < troponina <= troponina_abbott_99:
        score += 1
    
    return score

# Función para calcular EDACS score
def calcular_EDACS_score(edad, sexo, diaforesis, irradiacion, inspiracion, palpacion):
    score = 0
    # Edad y sexo
    if sexo == "Hombre":
        score += 6
    # Edad
    if edad >= 50:
        score += 2
    
    # Síntomas y signos
    if diaforesis:
        score += 3
    if irradiacion:
        score += 5
    if inspiracion:
        score += 4
    if palpacion:
        score += 6
    
    return score

# Definir la interfaz con Streamlit
st.title("Calculadora de HEART y EDACS Score")

# HEART score
st.header("HEART Score")
edad = st.number_input("Edad del paciente", min_value=18, max_value=120)

# Cambié el tipo de datos a enteros de manera más directa
historia_clinica = st.radio("Historia clínica", ["No sospechosa (0)", "Sospechosa moderada (1)", "Altamente sospechosa (2)"])
historia_clinica = int(historia_clinica.split("(")[-1].replace(")", ""))  # Extracción más robusta del número

ekg = st.radio("EKG", ["Normal (0)", "Anormal no específica (1)", "Anormal significativa (2)"])
ekg = int(ekg.split("(")[-1].replace(")", ""))

factores_riesgo = st.radio("Factores de riesgo", ["Ninguno (0)", "1-2 factores (1)", "3 o más factores (2)"])
factores_riesgo = int(factores_riesgo.split("(")[-1].replace(")", ""))

troponina = st.number_input("Valor de la primera troponina de alta sensibilidad (ng/L)", min_value=0.0, format="%.2f")

# Cálculo HEART Score
heart_score = calcular_HEART_score(edad, historia_clinica, ekg, factores_riesgo, troponina)
st.write(f"Puntuación HEART: {heart_score}")

# EDACS Score
st.header("EDACS Score")
sexo = st.radio("Sexo del paciente", ["Hombre", "Mujer"])
diaforesis = st.checkbox("¿Hay diaforesis?", value=False)
irradiacion = st.checkbox("¿Dolor irradiado al brazo, hombro, cuello o mandíbula?", value=False)
inspiracion = st.checkbox("¿Dolor que empeora con la inspiración?", value=False)
palpacion = st.checkbox("¿Dolor reproducido por palpación?", value=False)

# Cálculo EDACS Score
edacs_score = calcular_EDACS_score(edad, sexo, diaforesis, irradiacion, inspiracion, palpacion)
st.write(f"Puntuación EDACS: {edacs_score}")


