import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Energía Inteligente",
    layout="centered",
    page_icon="⚡"
)

# Título y descripción
st.title("Energía Inteligente")
st.subheader("Predicción del consumo energético en oficinas")

# Sidebar: Inputs del usuario
with st.sidebar:
    st.header("Parámetros de entrada")
    
    num_empleados = st.number_input(
        "Número de empleados",
        min_value=1,
        max_value=100,
        value=10,
        step=1
    )
    
    num_dispositivos = st.number_input(
        "Dispositivos encendidos",
        min_value=1,
        max_value=50,
        value=15,
        step=1
    )
    
    hora = st.slider(
        "Hora del día",
        min_value=0,
        max_value=23,
        value=9,
        step=1
    )
    
    dia_semana = st.selectbox(
        "Día de la semana",
        ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    )
    
    temperatura = st.number_input(
        "Temperatura ambiente (°C)",
        min_value=10.0,
        max_value=40.0,
        value=22.0,
        step=0.5
    )

# Mostrar resumen de inputs
st.divider()
st.write("### Resumen de parámetros:")
st.write(f"- Empleados: {num_empleados}")
st.write(f"- Dispositivos encendidos: {num_dispositivos}")
st.write(f"- Hora: {hora}:00")
st.write(f"- Día: {dia_semana}")
st.write(f"- Temperatura: {temperatura} °C")

# Botón para calcular
if st.button("Calcular consumo", type="primary"):
    # Placeholder para la conexión con la API
    st.success("¡Cálculo completado!")
    
    # Aquí iría la llamada a la API y la visualización de resultados
    # Ejemplo:
    # response = requests.post("http://localhost:5000/calcular", json={
    #     "empleados": num_empleados,
    #     "dispositivos": num_dispositivos,
    #     "hora": hora,
    #     "dia": dia_semana,
    #     "temperatura": temperatura
    # })
    # display_chart(response.json())  # Usar función de utils/plots.py