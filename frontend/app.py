import streamlit as st
import requests

# Configuración de la página
st.set_page_config(
    page_title="Energía Inteligente",
    layout="centered",
    page_icon="⚡"
)


API_URL = "http://localhost:5000/api/predict"


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
        step=50.0,
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

    st.markdown("---")  # Separador visual
    
    # Botón de cálculo solo si todos los campos son válidos
    if campos_ok:
        calcular_clicked = st.button(
            "🔄 Calcular consumo", 
            type="primary", 
            use_container_width=True,
            key="calcular_button_enabled"
        )
    else:
        calcular_clicked= st.button(
            "🔄 Calcular consumo", 
            type="primary", 
            disabled=True, 
            use_container_width=True,
            key="calcular_button_disabled"
        )
        st.warning("⚠️ Complete todos los campos obligatorios")

                
    if calcular_clicked:
     # Resetear el estado de título mostrado para permitir recálculos
        if "titulo_mostrado" in st.session_state:
            del st.session_state["titulo_mostrado"]
            
        # Crear el payload con los datos ingresados
        payload = {
            "empleados": empleados,
            "computadora": computadora,
            "monitor": monitor,
            "impresora": impresora,
            "aire_acondicionado": aire_acondicionado,
            "iluminacion": iluminacion,
            "router": router,
            "cafetera": cafetera,
            "proyector": proyector,
            "modo": opcion,
            "ciudad": ciudad,
            "precio_kw": precio_kw,
            "dia": dia,
            "hora": hora if opcion == "hora" else None,
            "temperatura": temperatura_inicial if opcion == "hora" else None,
            "llueve": llueve if opcion == "hora" else None,
            "prob_lluvia": prob_lluvia if opcion == "dia" else None
         }
            
        st.session_state.mostrar_resultados = True
        st.session_state.payload = payload
    

# Resetear resultados si hay cambios en los parámetros (detectar cambio de estado)
current_params = {
    "empleados": empleados,
    "dia": dia,
    "precio_kw": precio_kw,
    "ciudad": ciudad,
    "opcion": opcion,
    "computadora": computadora,
    "monitor": monitor,
    "impresora": impresora,
    "aire_acondicionado": aire_acondicionado,
    "iluminacion": iluminacion,
    "router": router,
    "cafetera": cafetera,
    "proyector": proyector,
    "hora": hora if opcion == "hora" else None,
    "temperatura_inicial": temperatura_inicial if opcion == "hora" else None,
    "llueve": llueve if opcion == "hora" else None,
    "prob_lluvia": prob_lluvia if opcion == "dia" else None
}

# Verificar si hay cambios en los parámetros
if "last_params" not in st.session_state:
    st.session_state.last_params = current_params
elif st.session_state.last_params != current_params:
    # Si hay cambios, resetear los resultados
    st.session_state.mostrar_resultados = False
    if "payload" in st.session_state:
        del st.session_state.payload
    if "titulo_mostrado" in st.session_state:
        del st.session_state.titulo_mostrado
    st.session_state.last_params = current_params

        
    # Inicializar el estado para controlar la visualización
if "mostrar_resultados" not in st.session_state:
    st.session_state.mostrar_resultados = False  # Por defecto, no se muestran los resultados

# Mostrar el resumen de parámetros solo si no se están mostrando los resultados
if not st.session_state.mostrar_resultados:
    # Título y descripción con color personalizado usando HTML directamente
    st.markdown(
        """
        <h1 style="color: #2e7d32; font-size: 2.5rem; font-weight: bold; text-align: center;">
            Energía Inteligente ⚡
        </h1>
        <h2 style="color: #388e3c; font-size: 1.5rem; font-weight: bold; text-align: center;">
            Predicción del consumo energético en oficinas
        </h2>
        """,
        unsafe_allow_html=True
    )
        
    # Mostrar resumen de parámetros ingresados
    st.markdown(
        """
        <h1 style="color: #2e7d32; font-size: 1.6rem; font-weight: bold; text-align: center; margin-bottom: 20px;">
            📋 Resumen de Parámetros
        </h1>
        """,
        unsafe_allow_html=True
    )

    # Crear las tarjetas usando columnas de Streamlit para mejor control
    col1, col2, col3 = st.columns([1, 1, 1], gap="small")

    with col1:
        st.markdown(
            f"""
            <div class="card">
                <h4>📌 Parámetros Generales</h4>
                <ul>
                    <li><strong>Empleados:</strong> {empleados}</li>
                    <li><strong>Día:</strong> {dia}</li>
                    <li><strong>Ciudad:</strong> {ciudad}</li>
                    <li><strong>Precio kWh:</strong> ${precio_kw:.2f}</li>
                    <li><strong>Opción de cálculo:</strong> {'Por hora' if opcion == 'hora' else 'Por día'}</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        if opcion == "hora":
            st.markdown(
                f"""
                <div class="card">
                    <h4>⏰ Información por Hora</h4>
                    <ul>
                        <li><strong>Hora:</strong> {hora}:00</li>
                        <li><strong>Temperatura ambiente:</strong> {temperatura_inicial} °C</li>
                        <li><strong>¿Llueve?:</strong> {'Sí' if llueve else 'No'}</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="card">
                    <h4>🌧️ Información por Día</h4>
                    <ul>
                        <li><strong>Probabilidad de lluvia:</strong> {prob_lluvia}</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )

    with col3:
        st.markdown(
            f"""
            <div class="card">
                <h4>💻 Equipos en Uso</h4>
                <ul>
                    <li><strong>Computadoras:</strong> {computadora}</li>
                    <li><strong>Monitores:</strong> {monitor}</li>
                    <li><strong>Impresoras:</strong> {impresora}</li>
                    <li><strong>Aires acondicionados:</strong> {aire_acondicionado}</li>
                    <li><strong>Luminarias:</strong> {iluminacion}</li>
                    <li><strong>Routers:</strong> {router}</li>
                    <li><strong>Cafeteras:</strong> {cafetera}</li>
                    <li><strong>Proyectores:</strong> {proyector}</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True)
                    # Nota informativa
    st.markdown(
        """
            <div style="background-color: #e3f2fd; padding: 15px; border-radius: 15px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-top: 20px; color: #333;">
                💡 <strong>Nota:</strong> Si deseas un cálculo más preciso para una hora específica, usa la opción "Cálculo por hora" e ingresa tú mismo la temperatura ambiente. En el modo "todo el día", las temperaturas se estiman automáticamente con base en promedios históricos de la ciudad.
            </div>
            """,
            unsafe_allow_html=True)

        
# Mostrar resultados si ya se han calculado
if st.session_state.mostrar_resultados and "payload" in st.session_state:
    with st.spinner("Calculando consumo energético..."):
        # Importar mostrar_resultado_octave y generar_graficas
        from components.result_display import mostrar_resultado_octave
        from utils.plots import generar_graficas
        
        try:
            response = requests.post(API_URL, json=st.session_state.payload)
            if response.status_code == 200:
                resultado = response.json()
                # Mostrar mensaje de éxito
                st.success("¡Cálculo completado!")
                        
                mostrar_resultado_octave(API_URL, st.session_state.payload)

                # Botón para visualizar gráficas
                if st.session_state.payload.get("modo") == "dia": 
                    if st.button("📊 Visualizar gráficas"):
                        generar_graficas(resultado)

            else:
                st.error(f"Error en la API: {response.status_code}")
                st.write(response.json())
        except Exception as e:
            st.error(f"Error al conectar con la API: {e}")
            
elif st.session_state.mostrar_resultados and "payload" not in st.session_state:
    # Si se solicita mostrar resultados pero no hay payload, resetear el estado
    st.session_state.mostrar_resultados = False
    st.rerun()

# Divisor para separar secciones
st.divider()

# Configuración de estilo global para el fondo y las tarjetas
st.markdown(
    """
    <style>
        .stApp {
            background-color: #e3f2fd;
        }
        .card {
            background-color: #ffffff;
            padding: 12px 15px;
            border-radius: 12px;
            box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
            text-align: left;
            border: 1px solid #e8f5e8;
            height: 100%;
            font-size: 0.85rem;
        }
        .card h4 {
            color: #388e3c;
            margin-bottom: 10px;
            font-size: 1rem;
            font-weight: 600;
            border-bottom: 1px solid #e8f5e8;
            padding-bottom: 5px;
        }
        .card ul {
            list-style-type: none;
            padding: 0;
            margin: 0;
        }
        .card ul li {
            margin-bottom: 6px;
            color: #555;
            padding: 2px 0;
            font-size: 0.8rem;
            line-height: 1.3;
        }
        .card ul li:last-child {
            margin-bottom: 0;
        }
        .card ul li strong {
            color: #2e7d32;
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True
)


