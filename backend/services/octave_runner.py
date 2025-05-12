import subprocess 
import os

def run_poli_lagrange(empleados, dispositivos, hora, dia, temperatura):
    """
    Ejecuta el script PoliLagrange.m con los datos proporcionados.

    Args:
        empleados (int): Número de empleados.
        dispositivos (int): Número de dispositivos.
        hora (int): Hora del día.
        dia (int): Día de la semana.
        temperatura (float): Temperatura ambiente.

    Returns:
        str: Resultado de la ejecución del script de Octave.
    """
    # Simulación de un resultado mientras se implementa Octave
    return empleados * 0.5 + dispositivos * 0.3 + hora * 0.2 + dia * 0.1 + temperatura * 0.05
    
    try:
        #Ruta absoluta al script octave
        script_path= os.path.abspath("backend/octave/PoliLagrange.m")
        
        #Verificar si el script existe
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"El script {script_path} no se encuentra en la ruta especificada o no existe.")
        # Crear un archivo temporal para pasar los datos a Octave
        input_file = os.path.abspath("backend/octave/input_data.txt")
        with open(input_file, "w") as f:
            f.write(f"{empleados} {dispositivos} {hora} {dia} {temperatura}\n")
        
        #Ejecutar el script de Octave
        command= [
            "octave-cli",
            "--eval",
            f"addpath('{os.path.dirname(script_path)}');"
            f"data = dimread('{input_file}');"
            f"empleados = data(1); dispositivos = data(2); hora = data(3); dia = data(4); temperatura = data(5); " 
            f"resultado = PoliLagrange(empleados, dispositivos, hora, dia, temperatura);"
           
        ]
        
        result= subprocess.run(command, capture_output=True, text=True)
        
        #Verificar si hubo errores
        if result.returncode != 0:
            raise Exception(f"Error al ejecutar Octave: {result.stderr}")

        #Procesar la salida de Octave
        return result.stdout.strip()
    
    except Exception as e:
        raise RuntimeError(f"Error ejecutando PoliLagrange: {str(e)}")