import streamlit as st

def get_user_inputs():
    """
    Función para recolectar los parámetros de entrada del usuario en el sidebar.
    Retorna un diccionario con los valores ingresados.
    """
    with st.sidebar:
        st.header("📊 Parámetros de Consumo Energético")
        
        inputs = {
            'empleados': st.number_input(
                "Número de empleados",
                min_value=0,
                max_value=100,
                value=10,
                step=1,
                help="Cantidad de personas en la oficina"
            ),
            'dispositivos': st.number_input(
                "Dispositivos electrónicos activos",
                min_value=0,
                max_value=50,
                value=15,
                step=1,
                help="Computadoras, impresoras, luces, etc."
            ),
            'hora': st.slider(
                "Hora del día",
                min_value=0,
                max_value=23,
                value=9,
                step=1,
                help="Hora actual (formato 24h)"
            ),
            'dia': st.selectbox(
                "Día de la semana",
                options=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
                index=0
            ),
            'temperatura': st.number_input(
                "Temperatura ambiente (°C)",
                min_value=10.0,
                max_value=40.0,
                value=22.0,
                step=0.5,
                help="Temperatura interior de la oficina"
            )
        }
    
    return inputs
