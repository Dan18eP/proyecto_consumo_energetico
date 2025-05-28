import streamlit as st
import requests
import streamlit.components.v1 as components


# Mostrar resultados de la API en secciones organizadas
def mostrar_resultado_octave(api_url, payload):
    """
    Función para mostrar los resultados de la API Octave en la interfaz.
    :param api_url: URL de la API.
    :param payload: Datos enviados a la API.
    """
    try:
        # Enviar los datos a la API
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            resultado = response.json()
            #st.write("Respuesta de la API:", resultado)  # Mostrar el JSON completo
            prediccion = resultado.get("prediccion")
            if not prediccion:
                st.error("La clave 'prediccion' no está presente en la respuesta de la API.")
                return
        else:
            st.error(f"Error en la API: {response.status_code}")
            try:
                error_message = response.json().get("error", "No se proporcionó un mensaje de error.")
                st.write(f"Detalles del error: {error_message}")
            except ValueError:
                st.write("La respuesta de la API no contiene un JSON válido.")
            return
    except requests.exceptions.RequestException as e:
        st.error(f"Error al conectar con la API: {e}")
        return

    try:
        # Obtener el modo desde el payload
        modo = payload.get("modo", "dia")
        prediccion = resultado.get("prediccion")
        if not prediccion:
            st.error("No se encontraron datos de predicción en la respuesta.")
            return

        # Título principal - Solo se muestra una vez por sesión de cálculo
        if "titulo_mostrado" not in st.session_state:
            st.markdown(
                """
                <h1 style="color: #2e7d32; font-size: 2rem; font-weight: bold; text-align: center;">
                    📊 Resultados del Consumo Energético
                </h1>
                """,
                unsafe_allow_html=True
            )
            st.session_state["titulo_mostrado"] = True

        # Mostrar alertas ANTES del contenido (modo "día")
        if modo == "dia" and "alertas" in prediccion and prediccion["alertas"]:
            # Verificar si las alertas ya se han mostrado
            if "alertas_mostradas" not in st.session_state:
                st.markdown(
                    """
                    <h2 style="color: #2e7d32; font-size: 1.2rem; font-weight: bold; text-align: center;">
                        🚨 Alertas
                    </h2>
                    """,
                    unsafe_allow_html=True
                )
                for alerta in prediccion["alertas"]:
                    st.warning(alerta)
                st.session_state["alertas_mostradas"] = True  # Marcar las alertas como mostradas
            else:
                # Si ya se mostraron, no hacer nada
                pass
            st.markdown("---")  # Separador visual
    
        # Mostrar temperaturas y consumo por hora (modo "día")
        if modo == "dia":
            temperaturas = prediccion.get("ahorro_total_cop", {}).get("temperatura", [])
            if temperaturas:
                st.markdown(
                    """
                    <h2 style="color: #2e7d32; font-size: 1.2rem; font-weight: bold; text-align: center;">
                        🌡️ Temperaturas y Consumo por Hora
                    </h2>
                    """,
                    unsafe_allow_html=True
                )

                # 1. Definir los estilos CSS. Los incrustaremos directamente en el HTML.
                css_styles = """
                <style>
                .timeline-container {
                    display: flex;
                    flex-wrap: nowrap;
                    overflow-x: auto;
                    gap: 20px; /* Espacio entre las tarjetas */
                    padding: 15px 5px;
                    background: linear-gradient(90deg, #e3f2fd 0%, #f3e5f5 100%);
                    border-radius: 12px;
                    margin: 10px 0;
                    box-sizing: border-box;
                }

                .timeline-card {
                    flex: 0 0 auto;
                    background-color: #ffffff;
                    padding: 16px;
                    border-radius: 12px;
                    min-width: 180px;
                    max-width: 200px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    border-left: 4px solid #2e7d32;
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                    box-sizing: border-box;
                }

                .timeline-card:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
                }

                .timeline-card p {
                    margin: 6px 0;
                    font-size: 13px;
                    color: #333;
                }

                .timeline-card .hora {
                    font-size: 16px;
                    font-weight: bold;
                    color: #2e7d32;
                    text-align: center;
                    margin-bottom: 10px;
                }

                .timeline-card .temperatura {
                    font-size: 18px;
                    font-weight: bold;
                    color: #1976d2;
                    text-align: center;
                }

                /* Scrollbar personalizado */
                .timeline-container::-webkit-scrollbar {
                    height: 8px;
                }

                .timeline-container::-webkit-scrollbar-track {
                    background: #f1f1f1;
                    border-radius: 4px;
                }

                .timeline-container::-webkit-scrollbar-thumb {
                    background: #2e7d32;
                    border-radius: 4px;
                }

                .timeline-container::-webkit-scrollbar-thumb:hover {
                    background: #1b5e20;
                }
                </style>
                """

                # 2. Build the HTML string for all cards
                cards_html_content = ""
                for temp in temperaturas:
                    hora = temp.get('hora', 'N/A')
                    consumo = temp.get('consumo_kwh', 0)
                    costo = temp.get('costo_cop', 0)
                    ahorro = temp.get('ahorro_cop', 0)
                    temperatura = temp.get('temperatura', 'N/A')

                    temp_display = f"{float(temperatura):.1f}" if temperatura != 'N/A' else 'N/A'

                    cards_html_content += f"""
                    <div class="timeline-card">
                        <div class="hora">{hora}:00h</div>
                        <div class="temperatura">{temp_display}°C</div>
                        <p><strong>💡 Consumo:</strong> {consumo:,.2f} kWh</p>
                        <p><strong>💰 Costo:</strong> ${costo:,.0f}</p>
                        <p><strong>💚 Ahorro:</strong> ${ahorro:,.0f}</p>
                    </div>
                    """
                
                
                full_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    {css_styles}
                </head>
                <body>
                    <div class="timeline-container">
                        {cards_html_content}
                    </div>
                </body>
                </html>
                """
                
                components.html(full_html, height=250, scrolling=False) # Adjust height as per your card size

                st.markdown(
                    """
                    <p style="text-align: center; color: #666; font-size: 12px; margin-top: 5px;">
                        ← Desliza horizontalmente para ver todas las horas →
                    </p>
                    """,
                    unsafe_allow_html=True
                )
                
                        # Mostrar ahorro total (solo en modo "día")
                if "ahorro_total_cop" in prediccion.get("ahorro_total_cop", {}):
                    ahorro_total = prediccion["ahorro_total_cop"].get("ahorro_total_cop", {})
                    
                    # Extraer valores directamente del JSON
                    consumo_total_kwh = ahorro_total.get('consumo_total_kwh', None)
                    costo_total_cop = ahorro_total.get('costo_total_cop', None)
                    ahorro_total_kwh = ahorro_total.get('ahorro_total_kwh', None)
                    ahorro_total_cop = ahorro_total.get('ahorro_total_cop', None)

                    # Validar que los valores existan y sean numéricos
                    if consumo_total_kwh is not None and costo_total_cop is not None and \
                       ahorro_total_kwh is not None and ahorro_total_cop is not None:
                        st.markdown(
                            f"""
                            <div style="background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; color: #333;">
                                <h3 style="color: #388e3c;">💰 Resumen Total</h3>
                                <p><strong>Consumo Total:</strong> {float(consumo_total_kwh):,.2f} kWh</p>
                                <p><strong>Costo Total:</strong> ${float(costo_total_cop):,.2f}</p>
                                <p><strong>Ahorro Total kWh:</strong> {float(ahorro_total_kwh):,.2f} kWh</p>
                                <p><strong>Ahorro Total COP:</strong> ${float(ahorro_total_cop):,.2f}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.warning("Los datos de ahorro total no son válidos o están incompletos.")
                else:
                    st.warning("No se encontraron datos de ahorro total.")
            else:
                st.warning("No se encontraron datos de temperatura para mostrar en el modo 'día'.")
                
        
        elif modo == "hora":
            # Mostrar resultados para la hora específica
            hora = payload.get("hora", "N/A")
            temperaturas = prediccion.get("ahorro_total_cop", {}).get("temperatura", [])
            hora_especifica = next((temp for temp in temperaturas if temp.get("hora") == hora), None)
            if hora_especifica:
                st.markdown(
                """
                <h2 style="color: #2e7d32; font-size: 1rem; font-weight: bold; text-align: center;">
                    " ⏰ Resultados para la Hora Específica"
                </h2>
                """,
                unsafe_allow_html=True
            )
                
                st.markdown(
                    f"""
                    <div style="background-color: #f9f9f9; padding: 7px; border-radius: 7px; margin-bottom: 7px; color: #333;">
                        <p><strong>Hora:</strong> {hora_especifica.get('hora', 'N/A')}h</p>
                        <p><strong>Consumo kWh:</strong> {hora_especifica.get('consumo_kwh', 0):,.2f} kWh</p>
                        <p><strong>Costo COP:</strong> ${hora_especifica.get('costo_cop', 0):,.2f}</p>
                        <p><strong>Ahorro COP:</strong> ${hora_especifica.get('ahorro_cop', 0):,.2f}</p>
                        <p><strong>Temperatura:</strong> {float(hora_especifica.get('temperatura', 'N/A'))}°C</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.warning(f"No se encontraron datos para la hora {hora}.")

        
        # Mostrar ahorro por equipo (aplica para ambos modos)
        if "ahorro_cop" in prediccion.get("ahorro_total_cop", {}):
            st.markdown(
                """
                <h2 style="color: #2e7d32; font-size: 1.2rem; font-weight: bold; text-align: center;">
                    ⚙️ Desglose por Equipo
                </h2>
                """,
                unsafe_allow_html=True
            )
            
            ahorro_equipos = prediccion["ahorro_total_cop"]["ahorro_cop"]
            mostrar_tarjetas_por_equipo(ahorro_equipos)
        else:
            st.warning("No se encontraron datos de ahorro por equipo.")

        # Mostrar consejos (aplica para ambos modos)
        if "consejos" in prediccion and "consejo" in prediccion["consejos"]:
            st.markdown(
                """
                <h2 style="color: #2e7d32; font-size: 1.2rem; font-weight: bold; text-align: center;">
                    💡 Consejos de Ahorro
                </h2>
                """,
                unsafe_allow_html=True
            )
            consejos = prediccion["consejos"]["consejo"]
            for consejo in consejos:
                st.markdown(
                    f"""
                    <div style="background-color: #e3f2fd; padding: 10px; border-radius: 10px; margin-bottom: 10px; color: #333;">
                        <p><strong>Equipo:</strong> {consejo.get('equipo', 'Equipo desconocido').capitalize()}</p>
                        <p>{consejo.get('consejo', 'Sin consejo disponible.')}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No se encontraron consejos de ahorro.")
            
    except KeyError as e:
        st.error(f"Error al procesar los datos: clave faltante {e}")
    except Exception as e:
        st.error(f"Error inesperado: {e}")


def mostrar_tarjetas_por_equipo(equipos):
    """
    Muestra las tarjetas de ahorro por equipo en filas de 4 columnas.
    :param equipos: Lista de equipos con sus datos de ahorro.
    """
    # Dividir los equipos en filas de 4 columnas
    for i in range(0, len(equipos), 4):
        fila = equipos[i:i + 4]  # Obtener 4 equipos por fila
        cols = st.columns(4)  # Crear 4 columnas

        for col, equipo in zip(cols, fila):
            with col:
                st.markdown(
                    f"""
                    <div style="background-color: #f9f9f9; padding: 10px; border-radius: 10px; margin-bottom: 10px; color: #333; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
                        <h4 style="color: #2e7d32; font-size: 1rem; margin-bottom: 5px;">{equipo.get('nombre', 'Equipo desconocido').capitalize()}</h4>
                        <p style="margin: 0; font-size: 0.9rem;"><strong>Cantidad:</strong> {equipo.get('cantidad', 0)}</p>
                        <p style="margin: 0; font-size: 0.9rem;"><strong>Consumo kWh:</strong> {equipo.get('consumo_kwh', 0):,.2f} kWh</p>
                        <p style="margin: 0; font-size: 0.9rem;"><strong>Costo COP:</strong> ${equipo.get('costo_cop', 0):,.2f}</p>
                        <p style="margin: 0; font-size: 0.9rem;"><strong>Ahorro kWh:</strong> {equipo.get('ahorro_kwh', 0):,.2f} kWh</p>
                        <p style="margin: 0; font-size: 0.9rem;"><strong>Ahorro COP:</strong> ${equipo.get('ahorro_cop', 0):,.2f}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )