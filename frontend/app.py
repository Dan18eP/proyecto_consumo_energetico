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

with st.sidebar:
    st.header("Parámetros de entrada")

    # Campos generales
    empleados = st.number_input(
        "Número de empleados",
        min_value=0,
        value=1,
        step=1
    )

    dia = st.selectbox(
        "Día de la semana",
        ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    )

    precio_kw = st.number_input(
        "Precio del kWh ($)",
        min_value=0.0,
        value=0.0,
        step=0.01,
        format="%.2f"
    )

    opcion = st.radio(
        "¿Qué desea calcular?",
        options=["hora", "dia"],
        format_func=lambda x: "Por hora" if x == "hora" else "Por día"
    )

    # Variables condicionales
    temperatura_inicial = None
    prob_lluvia = None
    hora = None
    llueve = None

    if opcion == "hora":
        hora = st.slider(
            "Hora del día",
            min_value=7,
            max_value=19,
            value=9,
            step=1
        )
        temperatura_inicial = st.number_input(
            "Temperatura ambiente actual (°C)",
            min_value=10.0,
            max_value=45.0,
            value=22.0,
            step=0.5
        )
        llueve = st.checkbox("¿Está lloviendo en ese momento?", value=False)
    else:
        prob_lluvia = st.number_input(
            "Probabilidad de lluvia durante el día (0 a 1)",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.01
        )

    st.markdown("#### Equipos en uso")
    computadora = st.number_input("Computadoras", min_value=0, value=0, step=1)
    monitor = st.number_input("Monitores", min_value=0, value=0, step=1)
    impresora = st.number_input("Impresoras", min_value=0, value=0, step=1)
    aire_acondicionado = st.number_input("Aires acondicionados", min_value=0, value=0, step=1)
    iluminacion = st.number_input("Luminarias", min_value=0, value=0, step=1)
    router = st.number_input("Routers", min_value=0, value=0, step=1)
    cafetera = st.number_input("Cafeteras", min_value=0, value=0, step=1)
    proyector = st.number_input("Proyectores", min_value=0, value=0, step=1)

    # Validación de campos obligatorios
    campos_ok = (
        empleados >= 0 and
        precio_kw > 0 and
        (opcion == "hora" and temperatura_inicial is not None or opcion == "dia") and
        (opcion == "hora" and hora is not None or opcion == "dia" and prob_lluvia is not None) and
        all(x >= 0 for x in [
            computadora, monitor, impresora, aire_acondicionado,
            iluminacion, router, cafetera, proyector
        ])
    )

    # Mostrar botón solo si todo está completo
    if campos_ok:
        if st.button("Calcular consumo", type="primary"):
            st.success("¡Cálculo enviado!")
    else:
        st.info("Completa todos los campos para continuar.")

st.divider()
st.write("### Resumen de parámetros:")
st.write(f"- Empleados: {empleados}")
st.write(f"- Día: {dia}")
st.write(f"- Precio kWh: ${precio_kw:.2f}")
st.write(f"- Opción de cálculo: {'Por hora' if opcion == 'hora' else 'Por día'}")
if opcion == "hora":
    st.write(f"- Hora: {hora}:00")
    st.write(f"- Temperatura ambiente: {temperatura_inicial} °C")
    st.write(f"- ¿Llueve?: {'Sí' if llueve else 'No'}")
else:
    st.write(f"- Probabilidad de lluvia: {prob_lluvia}")
st.write("#### Equipos en uso:")
st.write(f"- Computadoras: {computadora}")
st.write(f"- Monitores: {monitor}")
st.write(f"- Impresoras: {impresora}")
st.write(f"- Aires acondicionados: {aire_acondicionado}")
st.write(f"- Luminarias: {iluminacion}")
st.write(f"- Routers: {router}")
st.write(f"- Cafeteras: {cafetera}")
st.write(f"- Proyectores: {proyector}")

st.info("💡 Nota: Si deseas un cálculo más preciso para una hora específica, usa la opción 'Cálculo por hora' e ingresa tú mismo la temperatura ambiente. En el modo 'todo el día', las temperaturas se estiman automáticamente con base en promedios históricos de la ciudad.")