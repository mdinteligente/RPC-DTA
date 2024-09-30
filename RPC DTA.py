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

# Función para calcular HEAR score (sin troponina)
def calcular_HEAR_score(edad, historia_clinica, ekg, factores_riesgo):
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
st.title("Calculadora de HEART, HEAR y EDACS Score")

# HEART score
st.header("HEART Score")
edad = st.number_input("Edad del paciente", min_value=18, max_value=120)
historia_clinica = st.selectbox("Historia clínica", ["No sospechosa (0)", "Sospechosa moderada (1)", "Altamente sospechosa (2)"], index=0)
historia_clinica = int(historia_clinica.split()[-1])

ekg = st.selectbox("EKG", ["Normal (0)", "Anormal no específica (1)", "Anormal significativa (2)"], index=0)
ekg = int(ekg.split()[-1])

factores_riesgo = st.selectbox("Factores de riesgo", ["Ninguno (0)", "1-2 factores (1)", "3 o más factores (2)"], index=0)
factores_riesgo = int(factores_riesgo.split()[-1])

troponina = st.number_input("Valor de la primera troponina de alta sensibilidad (ng/L)", min_value=0.0, format="%.2f")

# Cálculo HEART Score
heart_score = calcular_HEART_score(edad, historia_clinica, ekg, factores_riesgo, troponina)
st.write(f"Puntuación HEART: {heart_score}")

# HEAR score
st.header("HEAR Score")
hear_score = calcular_HEAR_score(edad, historia_clinica, ekg, factores_riesgo)
st.write(f"Puntuación HEAR: {hear_score}")

# EDACS Score
st.header("EDACS Score")
sexo = st.selectbox("Sexo del paciente", ["Hombre", "Mujer"])
diaforesis = st.checkbox("¿Hay diaforesis?", value=False)
irradiacion = st.checkbox("¿Dolor irradiado al brazo, hombro, cuello o mandíbula?", value=False)
inspiracion = st.checkbox("¿Dolor que empeora con la inspiración?", value=False)
palpacion = st.checkbox("¿Dolor reproducido por palpación?", value=False)

# Cálculo EDACS Score
edacs_score = calcular_EDACS_score(edad, sexo, diaforesis, irradiacion, inspiracion, palpacion)
st.write(f"Puntuación EDACS: {edacs_score}")

# Cálculos diagnósticos
st.header("Cálculos Diagnósticos")
sensibilidad = 0.90  # Ejemplo para HEART, ajustar según los datos específicos de las otras escalas
especificidad = 0.80  # Ejemplo, ajustar según los datos específicos
prevalencia = 0.15  # Prevalencia de infarto

def calcular_valores_diagnosticos(sens, esp, preval):
    # Calcular LR+
    lr_positivo = sens / (1 - esp)
    # Calcular LR-
    lr_negativo = (1 - sens) / esp
    return lr_positivo, lr_negativo

# Mostrar valores diagnósticos
lr_positivo, lr_negativo = calcular_valores_diagnosticos(sensibilidad, especificidad, prevalencia)
st.write(f"LR(+): {lr_positivo}")
st.write(f"LR(-): {lr_negativo}")

# Falsos positivos y negativos
total_pacientes = st.number_input("Número de pacientes evaluados", min_value=1, value=100)
verdaderos_positivos = sensibilidad * prevalencia * total_pacientes
falsos_negativos = (1 - sensibilidad) * prevalencia * total_pacientes
falsos_positivos = (1 - especificidad) * (1 - prevalencia) * total_pacientes

st.write(f"Falsos positivos: {falsos_positivos}")
st.write(f"Falsos negativos: {falsos_negativos}")

