import matplotlib.pyplot as plt
import streamlit as st
import requests


def mostrar_resultado_octave(api_url, payload):
    try:
        # Enviar los datos a la API
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            resultado = response.json()
            prediccion = resultado.get("prediccion")
            if not prediccion:
                st.error("La clave 'prediccion' no está presente en la respuesta de la API.")
                return
        else:
            st.error(f"Error en la API: {response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        st.error(f"Error al conectar con la API: {e}")
        return

    try:
        modo = payload.get("modo", "dia")
        prediccion = resultado.get("prediccion")
        if not prediccion:
            st.error("No se encontraron datos de predicción en la respuesta.")
            return

        # Mostrar resultados existentes
        # ... (código existente para mostrar resultados)

        # Mostrar gráficas solo si el modo es "día"
        if modo == "dia":
            if st.button("📊 Visualizar gráficas"):
                temperaturas = prediccion.get("ahorro_total_cop", {}).get("temperatura", [])
                if temperaturas:
                    horas = [temp.get("hora") for temp in temperaturas]
                    consumos = [temp.get("consumo_kwh") for temp in temperaturas]
                    costos = [temp.get("costo_cop") for temp in temperaturas]
                    ahorros = [temp.get("ahorro_cop") for temp in temperaturas]

                    # Crear gráficas usando matplotlib
                    fig, ax = plt.subplots(3, 1, figsize=(10, 12))

                    # Gráfica de consumo por hora
                    ax[0].plot(horas, consumos, marker="o", color="blue", label="Consumo (kWh)")
                    ax[0].set_title("Consumo por Hora")
                    ax[0].set_xlabel("Hora")
                    ax[0].set_ylabel("Consumo (kWh)")
                    ax[0].grid(True)
                    ax[0].legend()

                    # Gráfica de costo por hora
                    ax[1].plot(horas, costos, marker="o", color="green", label="Costo (COP)")
                    ax[1].set_title("Costo por Hora")
                    ax[1].set_xlabel("Hora")
                    ax[1].set_ylabel("Costo (COP)")
                    ax[1].grid(True)
                    ax[1].legend()

                    # Gráfica de ahorro por hora
                    ax[2].plot(horas, ahorros, marker="o", color="orange", label="Ahorro (COP)")
                    ax[2].set_title("Ahorro por Hora")
                    ax[2].set_xlabel("Hora")
                    ax[2].set_ylabel("Ahorro (COP)")
                    ax[2].grid(True)
                    ax[2].legend()

                    # Mostrar las gráficas en Streamlit
                    st.pyplot(fig)
                else:
                    st.warning("No se encontraron datos de temperatura para generar gráficas.")
        else:
            st.info("Las gráficas solo están disponibles en el modo 'día'.")

    except KeyError as e:
        st.error(f"Error al procesar los datos: clave faltante {e}")
    except Exception as e:
        st.error(f"Error inesperado: {e}")


def generar_graficas(resultado):
    """
    Genera gráficas de consumo, costo y ahorro por hora usando matplotlib.
    :param resultado: Diccionario con los datos de predicción obtenidos de la API.
    """
    prediccion = resultado.get("prediccion", {})
    temperaturas = prediccion.get("ahorro_total_cop", {}).get("temperatura", [])
    if temperaturas:
        horas = [temp.get("hora") for temp in temperaturas]
        consumos = [temp.get("consumo_kwh") for temp in temperaturas]
        costos = [temp.get("costo_cop") for temp in temperaturas]
        ahorros = [temp.get("ahorro_cop") for temp in temperaturas]

        # Calcular el costo ajustado con los consejos
        costos_con_consejos = [costo - ahorro for costo, ahorro in zip(costos, ahorros)]

        # Crear gráficas usando matplotlib
        fig, ax = plt.subplots(3, 1, figsize=(10, 12))

        # Gráfica de consumo por hora
        ax[0].plot(horas, consumos, marker="o", color="blue", label="Consumo (kWh)")
        ax[0].set_title("Consumo por Hora")
        ax[0].set_xlabel("Hora")
        ax[0].set_ylabel("Consumo (kWh)")
        ax[0].grid(True)
        ax[0].legend()

        # Gráfica de costo por hora
        ax[1].plot(horas, costos, marker="o", color="green", label="Costo (COP)")
        ax[1].set_title("Costo por Hora")
        ax[1].set_xlabel("Hora")
        ax[1].set_ylabel("Costo (COP)")
        ax[1].grid(True)
        ax[1].legend()

        # Gráfica comparativa de ahorro por hora
        ax[2].plot(horas, costos, marker="o", color="red", label="Costo Normal (COP)")
        ax[2].plot(horas, costos_con_consejos, marker="o", color="orange", label="Costo con Consejos (COP)")
        ax[2].set_title("Comparativa de Costo por Hora")
        ax[2].set_xlabel("Hora")
        ax[2].set_ylabel("Costo (COP)")
        ax[2].grid(True)
        ax[2].legend()

        # Ajustar el diseño para agregar espacio entre las gráficas
        plt.tight_layout(pad=3.0)

        # Mostrar las gráficas en Streamlit
        st.pyplot(fig)
    else:
        st.warning("No se encontraron datos de temperatura para generar gráficas.")