import subprocess
import os
import json

def run_poli_lagrange(
    empleados,
    computadora,
    monitor,
    impresora,
    aire_acondicionado,
    iluminacion,
    router,
    cafetera,
    proyector,
    modo,
    ciudad=None,
    precio_kw=None,
    dia=None,
    hora=None,
    temperatura=None,
    llueve=None,
    prob_lluvia=None
    
):
    """
    Ejecuta el script PoliLagrange.m con los datos proporcionados.

    Args:
        Todos los parámetros de entrada desde PredictionInput.

    Returns:
        dict: Resultado de la ejecución del script de Octave.
    """
    try:
        # Verificar si Octave está instalado
        is_installed, octave_cmd = verify_octave_installation()
        if not is_installed:
            raise RuntimeError("Octave no está instalado o no está disponible en el PATH del sistema.")

        # Ruta al script de Octave
        script_path = os.path.abspath("backend/octave/PoliLagrange.m")
        input_file = os.path.abspath("backend/octave/input_data.txt")
        output_file = os.path.abspath("backend/octave/resultado.json")

        # Verificar si el script existe
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"El script {script_path} no se encuentra en la ruta especificada o no existe.")

        # Crear el archivo de entrada para Octave
        os.makedirs(os.path.dirname(input_file), exist_ok=True)
        with open(input_file, "w") as f:
            f.write(f"{empleados}\n")
            f.write(f"{computadora}\n")
            f.write(f"{monitor}\n")
            f.write(f"{impresora}\n")
            f.write(f"{aire_acondicionado}\n")
            f.write(f"{iluminacion}\n")
            f.write(f"{router}\n")
            f.write(f"{cafetera}\n")
            f.write(f"{proyector}\n")
            f.write(f"{modo}\n")
            f.write(f"{ciudad}\n")
            f.write(f"{precio_kw}\n")
            f.write(f"{dia}\n")
            f.write(f"{hora if hora is not None else ''}\n") 
            f.write(f"{temperatura if temperatura is not None else ''}\n")
            f.write(f"{llueve if llueve is not None else ''}\n")
            f.write(f"{prob_lluvia if prob_lluvia is not None else ''}\n")
           

        # Limpiar el archivo de salida anterior si existe
        if os.path.exists(output_file):
            os.remove(output_file)

        # Comando para ejecutar Octave
        command = [
            octave_cmd,
            "--eval",
            f"addpath('{os.path.dirname(script_path)}'); PoliLagrange();"
        ]

        # Ejecutar desde el directorio raíz del proyecto para que las rutas relativas funcionen
        project_root = os.path.abspath(".")
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=project_root,
            timeout=60  # Timeout de 60 segundos
        )

        # Verificar si hubo errores
        if result.returncode != 0:
            raise RuntimeError(f"Error al ejecutar Octave: {result.stderr}")

        # Intentar leer el archivo JSON generado
        if os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8") as f:
                resultado_json = json.load(f)
            return resultado_json
        else:
            # Si no se generó el JSON, devolver la salida de texto
            return {
                "mensaje": "Ejecución completada pero no se generó archivo JSON",
                "salida": result.stdout.strip(),
                "error": result.stderr.strip() if result.stderr else None
            }

    except subprocess.TimeoutExpired:
        raise RuntimeError("Timeout ejecutando Octave - El proceso tomó demasiado tiempo")
    except FileNotFoundError as e:
        if "octave" in str(e).lower():
            raise RuntimeError("Octave no está instalado o no está disponible en el PATH del sistema")
        else:
            raise RuntimeError(f"Archivo no encontrado: {str(e)}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Error al leer el archivo JSON generado: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error ejecutando PoliLagrange: {str(e)}")


def verify_octave_installation():
    """
    Verifica si Octave está instalado y disponible.
    Returns:
        tuple: (bool, str) indicando si Octave está instalado y el comando a usar.
    """
    try:
        result = subprocess.run(['octave-cli', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            return True, "octave-cli"
    except FileNotFoundError:
        pass

    try:
        result = subprocess.run(['octave', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            return True, "octave"
    except FileNotFoundError:
        pass

    return False, None