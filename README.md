# Proyecto Consumo Energético

**Proyecto Energía Inteligente: Predicción del Consumo en Oficinas con Métodos Numéricos**

Este proyecto utiliza métodos numéricos y herramientas de análisis para predecir el consumo energético en oficinas, considerando factores como la temperatura, la probabilidad de lluvia y el uso de equipos. Además, proporciona recomendaciones para optimizar el consumo y reducir costos.

---

## Características principales

- **Predicción del consumo energético:** Cálculo del consumo por hora basado en datos de temperatura y equipos.
- **Ajuste por condiciones climáticas:** Ajuste de temperaturas según probabilidad de lluvia utilizando interpolación de Lagrange.
- **Visualización de resultados:** Gráficas interactivas de consumo, costos y ahorros por hora.
- **Recomendaciones de ahorro:** Consejos personalizados para optimizar el uso de equipos.
- **Alertas:** Notificaciones de horas pico para evitar altos costos.

---

## Tecnologías utilizadas

- **Backend:**
  - Lenguaje: Octave
  - Framework: Flask
  - Métodos numéricos: Interpolación de Lagrange
- **Frontend:**
  - Framework: Streamlit
  - Visualización: Matplotlib
- **Infraestructura:**
  - Docker para contenedores
  - JSON para intercambio de datos

---

## Requisitos previos

Asegúrate de tener instalados los siguientes componentes:

- **Docker** (para ejecutar el proyecto en contenedores)
- **Python 3.9+**
- **Octave** (para cálculos numéricos)

---

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu-usuario/proyecto_consumo_energetico.git
   cd proyecto_consumo_energetico
   ```
2. Construye y ejecuta los contenedores de Docker:
   ```bash
   docker-compose up --build
   ```
3. Accede a la aplicación:
   - Abre tu navegador y ve a `http://localhost:8501`.

---

## Uso

1. **Configuración inicial:**
   - Selecciona la ciudad, el modo de operación (`día` o `hora`) y los equipos utilizados.
   - Ingresa la probabilidad de lluvia o si llueve (según modo), el precio del kWh y los dispositivos junto con su cantidad.

2. **Cálculo del consumo:**
   - Haz clic en el botón para calcular el consumo energético.
   - Visualiza los resultados en tablas y gráficas.

3. **Recomendaciones:**
   - Consulta los consejos personalizados para optimizar el uso de los equipos.

4. **Visualización de datos:**
   - Explora las gráficas de consumo, costos y ahorros por hora, ajustadas según las condiciones climáticas.

---

## Contribución

¡Las contribuciones son bienvenidas! Por favor, sigue estos pasos:

1. Realiza un fork de este repositorio.
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`).
3. Realiza tus cambios y haz commit (`git commit -m 'Agrega nueva característica'`).
4. Haz push a tu rama (`git push origin feature/nueva-caracteristica`).
5. Abre un Pull Request.

---

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

## Contacto

Para más información, contacta a los mantenedores del proyecto:

- **Tu Nombre** - [d.echever23@gmail.com](mailto:d.echever23@gmail.com)
- **Colaborador 1** - [colaborador1.email@ejemplo.com](mailto:colaborador1.email@ejemplo.com)
- **Colaborador 2** - [colaborador2.email@ejemplo.com](mailto:colaborador2.email@ejemplo.com)

---

¡Gracias por tu interés en el Proyecto Energía Inteligente! Juntos, podemos hacer un uso más eficiente de la energía en nuestras oficinas.
