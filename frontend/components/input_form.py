import streamlit as st

def get_user_inputs():
    """
    Función para recolectar los parámetros de entrada del usuario en el sidebar.
    Retorna un diccionario con los valores ingresados.
    """
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

    ciudad= st.selectbox(
        "Ciudad",
        options=["Barranquilla", "Cartagena", "Medellín", "Cali", "Bogotá"],
        index=0
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
    
    # Retornar los valores como un diccionario
    return {
        "empleados": empleados,
        "dia": dia,
        "precio_kw": precio_kw,
        "ciudad": ciudad,
        "opcion": opcion,
        "temperatura_inicial": temperatura_inicial,
        "prob_lluvia": prob_lluvia,
        "hora": hora,
        "llueve": llueve,
        "computadora": computadora,
        "monitor": monitor,
        "impresora": impresora,
        "aire_acondicionado": aire_acondicionado,
        "iluminacion": iluminacion,
        "router": router,
        "cafetera": cafetera,
        "proyector": proyector
    }
