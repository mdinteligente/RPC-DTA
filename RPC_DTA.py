import streamlit as st

# Definir los percentiles 99 de troponinas de alta sensibilidad
troponina_roche_99 = 14  # ng/L
troponina_abbott_99 = 26  # ng/L

# Definir sensibilidad y especificidad para cada puntuación
sensibilidad_heart = 0.90
especificidad_heart = 0.80

sensibilidad_edacs = 0.97
especificidad_edacs = 0.58

sensibilidad_hear = 0.91
especificidad_hear = 0.71

# Funciones para calcular HEART, HEAR y EDACS scores

def calcular_HEART_score(edad, historia_clinica, ekg, factores_riesgo, troponina):
    score = 0
    if edad >= 65:
        score += 2
    elif 45 <= edad < 65:
        score += 1
    score += historia_clinica
    score += ekg
    score += factores_riesgo
    if troponina > troponina_roche_99 or troponina > troponina_abbott_99:
        score += 2
    elif 0.5 * troponina_roche_99 < troponina <= troponina_roche_99 or 0.5 * troponina_abbott_99 < troponina <= troponina_abbott_99:
        score += 1
    return score

def calcular_EDACS_score(edad, sexo, diaforesis, irradiacion, inspiracion, palpacion):
    score = 0
    if sexo == "Hombre":
        score += 6
    if edad >= 50:
        score += 2
    if diaforesis:
        score += 3
    if irradiacion:
        score += 5
    if inspiracion:
        score += 4
    if palpacion:
        score += 6
    return score

def calcular_HEAR_score(edad, historia_clinica, ekg, factores_riesgo):
    score = 0
    if edad >= 65:
        score += 2
    elif 45 <= edad < 65:
        score += 1
    score += historia_clinica
    score += ekg
    score += factores_riesgo
    return score

# Función para calcular valores diagnósticos
def calcular_valores_diagnosticos(sensibilidad, especificidad, prevalencia, total_pacientes):
    lr_positivo = sensibilidad / (1 - especificidad)
    lr_negativo = (1 - sensibilidad) / especificidad
    verdaderos_positivos = sensibilidad * prevalencia * total_pacientes
    falsos_negativos = (1 - sensibilidad) * prevalencia * total_pacientes
    falsos_positivos = (1 - especificidad) * (1 - prevalencia) * total_pacientes
    return lr_positivo, lr_negativo, falsos_positivos, falsos_negativos

# Función para determinar el riesgo de MACE basado en el puntaje
def riesgo_mace_heart(score):
    if score <= 3:
        return "Bajo"
    elif 4 <= score <= 6:
        return "Medio"
    else:
        return "Alto"

def riesgo_mace_hear(score):
    if score <= 3:
        return "Bajo"
    elif 4 <= score <= 6:
        return "Medio"
    else:
        return "Alto"

def riesgo_mace_edacs(score):
    if score < 16:
        return "Bajo"
    elif 16 <= score <= 20:
        return "Medio"
    else:
        return "Alto"

# Interfaz de usuario con Streamlit
st.title("Calculadora de HEART, HEAR y EDACS Score")

st.header("Preguntas Clínicas")
edad = st.number_input("Edad del paciente", min_value=18, max_value=120)
sexo = st.radio("Sexo del paciente", ["Hombre", "Mujer"])
historia_clinica = st.radio("Historia clínica", ["No sospechosa (0)", "Sospechosa moderada (1)", "Altamente sospechosa (2)"])
historia_clinica = int(historia_clinica.split("(")[-1].replace(")", ""))
factores_riesgo = st.radio("Factores de riesgo", ["Ninguno (0)", "1-2 factores (1)", "3 o más factores (2)"])
factores_riesgo = int(factores_riesgo.split("(")[-1].replace(")", ""))

st.header("Síntomas y Signos (para EDACS)")
diaforesis = st.checkbox("¿Hay diaforesis?", value=False)
irradiacion = st.checkbox("¿Dolor irradiado al brazo, hombro, cuello o mandíbula?", value=False)
inspiracion = st.checkbox("¿Dolor que empeora con la inspiración?", value=False)
palpacion = st.checkbox("¿Dolor reproducido por palpación?", value=False)

st.header("Electrocardiograma")
ekg = st.radio("EKG", ["Normal (0)", "Anormal no específica (1)", "Anormal significativa (2)"])
ekg = int(ekg.split("(")[-1].replace(")", ""))

st.header("Troponina de alta sensibilidad")
troponina = st.number_input("Valor de la primera troponina de alta sensibilidad (ng/L)", min_value=0.0, format="%.2f")

# Cálculo de las puntuaciones
heart_score = calcular_HEART_score(edad, historia_clinica, ekg, factores_riesgo, troponina)
hear_score = calcular_HEAR_score(edad, historia_clinica, ekg, factores_riesgo)
edacs_score = calcular_EDACS_score(edad, sexo, diaforesis, irradiacion, inspiracion, palpacion)

# Mostrar resultados de las puntuaciones
st.write(f"Puntuación HEART: {heart_score} (Riesgo de MACE: {riesgo_mace_heart(heart_score)})")
st.write(f"Puntuación HEAR: {hear_score} (Riesgo de MACE: {riesgo_mace_hear(hear_score)})")
st.write(f"Puntuación EDACS: {edacs_score} (Riesgo de MACE: {riesgo_mace_edacs(edacs_score)})")

st.header("Cocientes de probabilidad y efectos absolutos de aplicar las escalas")
prevalencia = 0.15
total_pacientes = 1000

# Cálculos de HEART
lr_heart_pos, lr_heart_neg, falsos_positivos_heart, falsos_negativos_heart = calcular_valores_diagnosticos(
    sensibilidad_heart, especificidad_heart, prevalencia, total_pacientes
)
st.write("**HEART Score**")
st.write(f"LR(+): {lr_heart_pos:.2f}, LR(-): {lr_heart_neg:.2f}")
st.write(f"Falsos positivos por cada 1000 pacientes: {falsos_positivos_heart:.0f}")
st.write(f"Falsos negativos por cada 1000 pacientes: {falsos_negativos_heart:.0f}")

# Cálculos de EDACS
lr_edacs_pos, lr_edacs_neg, falsos_positivos_edacs, falsos_negativos_edacs = calcular_valores_diagnosticos(
    sensibilidad_edacs, especificidad_edacs, prevalencia, total_pacientes
)
st.write("**EDACS Score**")
st.write(f"LR(+): {lr_edacs_pos:.2f}, LR(-): {lr_edacs_neg:.2f}")
st.write(f"Falsos positivos por cada 1000 pacientes: {falsos_positivos_edacs:.0f}")
st.write(f"Falsos negativos por cada 1000 pacientes: {falsos_negativos_edacs:.0f}")

# Cálculos de HEAR
lr_hear_pos, lr_hear_neg, falsos_positivos_hear, falsos_negativos_hear = calcular_valores_diagnosticos(
    sensibilidad_hear, especificidad_hear, prevalencia, total_pacientes
)
st.write("**HEAR Score**")
st.write(f"LR(+): {lr_hear_pos:.2f}, LR(-): {lr_hear_neg:.2f}")
st.write(f"Falsos positivos por cada 1000 pacientes: {falsos_positivos_hear:.0f}")
st.write(f"Falsos negativos por cada 1000 pacientes: {falsos_negativos_hear:.0f}")




