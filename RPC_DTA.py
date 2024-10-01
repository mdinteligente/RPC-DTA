import streamlit as st

# Valores P99 de troponinas T e I
ensayos_troponinas = {
    "T": {
        "P99_global": 14,  # ng/L
        "P99_hombres": 9,  # ng/L
        "P99_mujeres": 16,  # ng/L
    },
    "I": {
        "P99_global": 28,  # pg/mL
        "P99_hombres": 17,  # pg/mL
        "P99_mujeres": 35,  # pg/mL
    }
}

# Función para convertir de ng/mL a ng/L (sin aproximaciones)
def convertir_a_ngL(valor, unidad):
    if unidad == "ng/mL":
        return valor * 1000  # Conversión exacta de ng/mL a pg/mL (ng/L)
    return valor  # Si es pg/mL, ya está en ng/L

# Función para seleccionar el valor de P99 según el tipo de ensayo y el género
def seleccionar_P99(ensayo, genero, referencia):
    if referencia == "Global":
        return ensayos_troponinas[ensayo]["P99_global"]
    elif genero == "Hombre":
        return ensayos_troponinas[ensayo]["P99_hombres"]
    elif genero == "Mujer":
        return ensayos_troponinas[ensayo]["P99_mujeres"]

# Función para asegurar que el valor decimal use puntos
def leer_valor_decimal(valor):
    valor = valor.replace(',', '.')  # Reemplaza comas por puntos
    try:
        return float(valor)
    except ValueError:
        st.error("Registro no válido, debe emplear puntos en lugar de comas.")
        return None

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

# Funciones para calcular HEART, HEAR y EDACS scores
def calcular_HEART_score(edad, historia_clinica, ekg, factores_riesgo, troponina, P99):
    score = 0
    if edad >= 65:
        score += 2
    elif 45 <= edad < 65:
        score += 1
    score += historia_clinica
    score += ekg
    score += factores_riesgo
    if troponina > P99:
        score += 2
    elif 0.5 * P99 < troponina <= P99:
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

# Interfaz de usuario con Streamlit
st.title("Calculadora de HEART, HEAR y EDACS Score")

# Descargo de responsabilidad
st.subheader("Descargo de Responsabilidad")
acepta_descargo = st.checkbox("He leído y acepto los términos y condiciones del uso de esta herramienta.")
if acepta_descargo:
    # Solicitar usuario y contraseña
    st.subheader("Acceso restringido")
    usuario = st.text_input("Usuario")
    clave = st.text_input("Contraseña", type="password")

    if usuario == "javierapp" and clave == "rpcdta":
        st.success("Acceso permitido")

        # Preguntas clínicas
        st.header("Preguntas Clínicas")
        edad = st.number_input("Edad del paciente", min_value=18, max_value=120)
        sexo = st.radio("Sexo del paciente", ["Hombre", "Mujer"])
        historia_clinica = st.radio("Historia clínica", ["No sospechosa (0)", "Sospechosa moderada (1)", "Altamente sospechosa (2)"])
        historia_clinica = int(historia_clinica.split("(")[-1].replace(")", ""))

        # Factores de riesgo para HEART score
        st.subheader("Factores de riesgo")
        st.write("""
        **Factores de riesgo**: HTA, hipercolesterolemia, DM, obesidad (IMC >30 kg/m²), tabaquismo (actual o cese ≤3 meses),
        historia familiar positiva (padre o hermano con enfermedad cardiovascular antes de los 65 años), enfermedad aterosclerótica (infarto previo, ICP/CABG, ACV/AIT o enfermedad arterial periférica).
        """)
        factores_riesgo = st.radio("Seleccione los factores de riesgo presentes:", ["Ninguno (0)", "1-2 factores (1)", "3 o más factores (2)"])
        factores_riesgo = int(factores_riesgo.split("(")[-1].replace(")", ""))

        # Síntomas específicos para EDACS
        st.header("Síntomas y Signos (para EDACS)")
        diaforesis = st.checkbox("¿Hay diaforesis?", value=False)
        irradiacion = st.checkbox("¿Dolor irradiado al brazo, hombro, cuello o mandíbula?", value=False)
        inspiracion = st.checkbox("¿Dolor que empeora con la inspiración?", value=False)
        palpacion = st.checkbox("¿Dolor reproducido por palpación?", value=False)

        # EKG para HEART score
        st.subheader("Electrocardiograma (HEART score)")
        st.write("""
        1 punto: No hay desviación del ST, pero presenta BRI, HVI o cambios de repolarización (ej. digoxina).
        2 puntos: Desviación del ST no debida a BRI, HVI o digoxina.
        """)
        ekg = st.radio("Seleccione el hallazgo en el EKG:", ["Normal (0)", "No desviación del ST pero BRI, HVI, repolarización (1)", "Desviación del ST no debida a BRI, HVI, o digoxina (2)"])
        ekg = int(ekg.split("(")[-1].replace(")", ""))

        # Sección de troponinas
        st.header("Troponina de alta sensibilidad")
        
        # Preguntar al usuario qué tipo de ensayo va a usar
        ensayo = st.radio("Seleccione el tipo de ensayo que va a usar:", ["T", "I"])

        # Preguntar si el P99 es global o específico para hombre o mujer
        referencia_P99 = st.radio("Seleccione el tipo de referencia P99:", ["Global", "Hombre", "Mujer"])

        # Pedir al usuario que seleccione las unidades del P99 que reporta el laboratorio
        unidad_troponina = st.radio("Seleccione las unidades del P99 reportadas por su laboratorio:", ["ng/mL", "pg/mL"])

        troponina = st.number_input("Valor de la primera troponina de alta sensibilidad", min_value=0.0, format="%.2f")
        troponina = leer_valor_decimal(str(troponina))
        troponina = convertir_a_ngL(troponina, unidad_troponina)  # Conversión de unidades si es necesario

        # Seleccionar el P99 según el ensayo y la referencia seleccionada
        P99 = seleccionar_P99(ensayo, sexo, referencia_P99)

        # Cálculo de las puntuaciones
        heart_score = calcular_HEART_score(edad, historia_clinica, ekg, factores_riesgo, troponina, P99)
        hear_score = calcular_HEAR_score(edad, historia_clinica, ekg, factores_riesgo)
        edacs_score = calcular_EDACS_score(edad, sexo, diaforesis, irradiacion, inspiracion, palpacion)

        # Mostrar resultados de las puntuaciones
        st.write(f"Puntuación HEART: {heart_score} (Riesgo de MACE: {riesgo_mace_heart(heart_score)})")
        st.write(f"Puntuación HEAR: {hear_score} (Riesgo de MACE: {riesgo_mace_hear(hear_score)})")
        st.write(f"Puntuación EDACS: {edacs_score} (Riesgo de MACE: {riesgo_mace_edacs(edacs_score)})")

        st.header("Cálculo de riesgo de MACE y valores diagnósticos")
        prevalencia = 0.15
        total_pacientes = 1000

        # Definir sensibilidad y especificidad para cada score
        sensibilidad_heart = 0.90
        especificidad_heart = 0.80

        sensibilidad_edacs = 0.97
        especificidad_edacs = 0.58

        sensibilidad_hear = 0.91
        especificidad_hear = 0.71

        # Cálculos de HEART
        lr_heart_pos, lr_heart_neg, falsos_positivos_heart, falsos_negativos_heart = calcular_valores_diagnosticos(
            sensibilidad_heart, especificidad_heart, prevalencia, total_pacientes
        )
        st.write("**HEART Score**")
        st.write(f"LR(+): {lr_heart_pos:.2f}, LR(-): {lr_heart_neg:.2f}")
        st.write(f"Falsos positivos por cada 1000 pacientes: {falsos_positivos_heart}")
        st.write(f"Falsos negativos por cada 1000 pacientes: {falsos_negativos_heart}")

        # Cálculos de EDACS
        lr_edacs_pos, lr_edacs_neg, falsos_positivos_edacs, falsos_negativos_edacs = calcular_valores_diagnosticos(
            sensibilidad_edacs, especificidad_edacs, prevalencia, total_pacientes
        )
        st.write("**EDACS Score**")
        st.write(f"LR(+): {lr_edacs_pos:.2f}, LR(-): {lr_edacs_neg:.2f}")
        st.write(f"Falsos positivos por cada 1000 pacientes: {falsos_positivos_edacs}")
        st.write(f"Falsos negativos por cada 1000 pacientes: {falsos_negativos_edacs}")

        # Cálculos de HEAR
        lr_hear_pos, lr_hear_neg, falsos_positivos_hear, falsos_negativos_hear = calcular_valores_diagnosticos(
            sensibilidad_hear, especificidad_hear, prevalencia, total_pacientes
        )
        st.write("**HEAR Score**")
        st.write(f"LR(+): {lr_hear_pos:.2f}, LR(-): {lr_hear_neg:.2f}")
        st.write(f"Falsos positivos por cada 1000 pacientes: {falsos_positivos_hear}")
        st.write(f"Falsos negativos por cada 1000 pacientes: {falsos_negativos_hear}")

        # Agregar referencias
        st.header("Referencias")
        st.write("""
        1. O'Rielly CM, Harrison TG, Andruchow JE, Ronksley PE, Sajobi T, Robertson HL, Lorenzetti D, McRae AD. Risk Scores for Clinical Risk Stratification of Emergency Department Patients With Chest Pain but No Acute Myocardial Infarction: A Systematic Review. Can J Cardiol. 2023 Mar;39(3):304-310. doi: 10.1016/j.cjca.2022.12.028.
        
        2. Khaleghi Rad M, Pirmoradi MM, Doosti-Irani A, Thiruganasambandamoorthy V, Mirfazaelian H. The performance of HEAR score for identification of low-risk chest pain: a systematic review and meta-analysis. Eur J Emerg Med. 2022 Jun 1;29(3):173-187. doi: 10.1097/MEJ.00000000000009213.
        
        3. Wang M, Hu Z, Miao L, Shi M, Gao Q. A systematic review of the applicability of emergency department assessment of chest pain score-accelerated diagnostic protocol for risk stratification of patients with chest pain. Clin Cardiol. 2023 Nov;46(11):1303-1309. doi: 10.1002/clc.24126.
        """)




