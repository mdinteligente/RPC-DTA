import streamlit as st

# Función para convertir de ng/mL a ng/L sin realizar ninguna aproximación
def convertir_a_ngL(valor, unidad):
    if unidad == "ng/mL":
        return valor * 1000  # Conversión exacta de ng/mL a pg/mL (ng/L)
    return valor  # Si es pg/mL, ya está en ng/L

# Función para asegurar que el valor decimal use puntos y no comas
def leer_valor_decimal(prompt):
    valor = prompt.replace(',', '.')
    try:
        return float(valor)
    except ValueError:
        st.error("Registro no válido. Debe emplear puntos en lugar de comas para decimales.")
        return None

# Función para calcular valores diagnósticos
def calcular_falsos(sensibilidad, especificidad, prevalencia, total_pacientes):
    lr_positivo = sensibilidad / (1 - especificidad)
    lr_negativo = (1 - sensibilidad) / especificidad
    falsos_positivos = (1 - especificidad) * (1 - prevalencia) * total_pacientes
    falsos_negativos = (1 - sensibilidad) * prevalencia * total_pacientes
    return lr_positivo, lr_negativo, falsos_positivos, falsos_negativos

# Encabezado para coeficientes de probabilidad
st.header("Coeficientes de probabilidad y efectos absolutos de aplicar las escalas, asumiendo prevalencia de infarto del 15%, n: 1000")
prevalencia = 0.15
total_pacientes = 1000

# Datos proporcionados para HEART, HEAR y EDACS
sensibilidad_heart = 0.97
especificidad_heart = 0.45
sensibilidad_hear = 0.99
especificidad_hear = 0.18
sensibilidad_edacs = 0.97
especificidad_edacs = 0.58

# Cálculos para HEART Score
lr_heart_pos, lr_heart_neg, falsos_positivos_heart, falsos_negativos_heart = calcular_falsos(
    sensibilidad_heart, especificidad_heart, prevalencia, total_pacientes
)
st.write("**HEART Score < 3**")
st.write(f"LR(+): {lr_heart_pos:.2f}, Especificidad: {especificidad_heart*100:.1f}%")
st.write(f"LR(-): {lr_heart_neg:.2f}, Sensibilidad: {sensibilidad_heart*100:.1f}%")
st.write(f"Falsos positivos por cada 1000 pacientes: {falsos_positivos_heart:.0f}, Falsos negativos por cada 1000 pacientes: {falsos_negativos_heart:.0f}")

# Cálculos para HEAR Score
lr_hear_pos, lr_hear_neg, falsos_positivos_hear, falsos_negativos_hear = calcular_falsos(
    sensibilidad_hear, especificidad_hear, prevalencia, total_pacientes
)
st.write("**HEAR Score < 2**")
st.write(f"LR(+): {lr_hear_pos:.2f}, Especificidad: {especificidad_hear*100:.1f}%")
st.write(f"LR(-): {lr_hear_neg:.2f}, Sensibilidad: {sensibilidad_hear*100:.1f}%")
st.write(f"Falsos positivos por cada 1000 pacientes: {falsos_positivos_hear:.0f}, Falsos negativos por cada 1000 pacientes: {falsos_negativos_hear:.0f}")

# Cálculos para EDACS Score
lr_edacs_pos, lr_edacs_neg, falsos_positivos_edacs, falsos_negativos_edacs = calcular_falsos(
    sensibilidad_edacs, especificidad_edacs, prevalencia, total_pacientes
)
st.write("**EDACS Score < 16**")
st.write(f"LR(+): {lr_edacs_pos:.2f}, Especificidad: {especificidad_edacs*100:.1f}%")
st.write(f"LR(-): {lr_edacs_neg:.2f}, Sensibilidad: {sensibilidad_edacs*100:.1f}%")
st.write(f"Falsos positivos por cada 1000 pacientes: {falsos_positivos_edacs:.0f}, Falsos negativos por cada 1000 pacientes: {falsos_negativos_edacs:.0f}")

# Opción para la segunda troponina en EDACS
st.header("Troponinas en EDACS (a 0 y 2 horas)")
troponina_0h = leer_valor_decimal(st.text_input("Ingrese troponina a 0 horas"))
troponina_2h = leer_valor_decimal(st.text_input("Ingrese troponina a 2 horas"))



