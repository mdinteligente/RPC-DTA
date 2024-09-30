import streamlit as st

# Definir los percentiles 99 de troponinas de alta sensibilidad
troponina_roche_99 = 14  # ng/L
troponina_abbott_99 = 26  # ng/L

# Funciones para calcular HEART, HEAR y EDACS scores

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

# Función para calcular HEAR score (que es un subcomponente del HEART score sin la troponina)
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

# Función para calcular valores diagnósticos
def calcular_valores_diagnosticos(sensibilidad, especificidad, prevalencia, total_pacientes):
    # Calcular LR+
    lr_positivo = sensibilidad / (1 - especificidad)
    # Calcular LR-
    lr_negativo = (1 - sensibilidad) / especificidad
    
    # Calcular verdaderos positivos, falsos negativos y falsos positivos
    verdaderos_positivos = sensibilidad * prevalencia * total_pacientes
    falsos_negativos = (1 - sensibilidad) * prevalencia * total_pacientes
    falsos_positivos = (1 - especificidad) * (1 - prevalencia) * total_pacientes
    
    return lr_positivo, lr_negativo, falsos_positivos, falsos_negativos

# Interfaz de usuario con Streamlit
st.title("Calculadora de HEART, HEAR y EDACS Score")

# Preguntas clínicas (primero para EDACS y HEART)
st.header("Preguntas Clínicas")
edad = st.number_input("Edad del paciente", min_value=18, max_value=120)
sexo = st.radio("Sexo del paciente", ["Hombre", "Mujer"])

historia_clinica = st.radio("Historia clínica", ["No sospechosa (0)", "Sospechosa moderada (1)", "Altamente sospechosa (2)"])
historia_clinica = int(historia_clinica.split("(")[-1].replace(")", ""))

factores_riesgo = st.radio("Factores de riesgo", ["Ninguno (0)", "1-2 factores (1)", "3 o más factores (2)"])
factores_riesgo = int(factores_riesgo.split("(")[-1].replace(")", ""))

# Síntomas específicos para EDACS
st.header("Síntomas y Signos (para EDACS)")
diaforesis = st.checkbox("¿Hay diaforesis?", value=False)
irradiacion = st.checkbox("¿Dolor irradiado al brazo, hombro, cuello o mandíbula?", value=False)
inspiracion = st.checkbox("¿Dolor que empeora con la inspiración?", value=False)
palpacion = st.checkbox("¿Dolor reproducido por palpación?", value=False)

# Preguntas sobre EKG
st.header("Electrocardiograma")
ekg = st.radio("EKG", ["Normal (0)", "Anormal no específica (1)", "Anormal significativa (2)"])
ekg = int(ekg.split("(")[-1].replace(")", ""))

# Preguntas sobre troponina
st.header("Troponina de alta sensibilidad")
troponina = st.number_input("Valor de la primera troponina de alta sensibilidad (ng/L)", min_value=0.0, format="%.2f")

# Cálculo de las puntuaciones
heart_score = calcular_HEART_score(edad, historia_clinica, ekg, factores_riesgo, troponina)
hear_score = calcular_HEAR_score(edad, historia_clinica, ekg, factores_riesgo)
edacs_score = calcular_EDACS_score(edad, sexo, diaforesis, irradiacion, inspiracion, palpacion)

# Mostrar resultados de las puntuaciones
st.write(f"Puntuación HEART: {heart_score}")
st.write(f"Puntuación HEAR: {hear_score}")
st.write(f"Puntuación EDACS: {edacs_score}")

# Cálculos de riesgo de MACE a 30 días, falsos positivos y falsos negativos
st.header("Cálculo de riesgo de MACE y valores diagnósticos")

sensibilidad = 0.90  # Asumida, ajustar según datos específicos
especificidad = 0.80  # Asumida, ajustar según datos específicos
prevalencia = 0.15  # Prevalencia de infarto
total_pacientes = st.number_input("Número de pacientes evaluados", min_value=1, value=100)

lr_positivo, lr_negativo, falsos_positivos, falsos_negativos = calcular_valores_diagnosticos(
    sensibilidad, especificidad, prevalencia, total_pacientes
)

# Mostrar los resultados
st.write(f"Riesgo de MACE a 30 días: {prevalencia * 100}%")
st.write(f"LR(+): {lr_positivo}")
st.write(f"LR(-): {lr_negativo}")
st.write(f"Falsos positivos: {falsos_positivos}")
st.write(f"Falsos negativos: {falsos_negativos}")


