import subprocess 
import os


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
    hora=None,
    temperatura=None,
    llueve=None,
    prob_lluvia=None,
    ciudad=None,
    precio_kw=None,
    dia=None
):
    """
    Ejecuta el script PoliLagrange.m con los datos proporcionados.

    Args:
        Todos los parámetros de entrada desde PredictionInput.

    Returns:
        str: Resultado de la ejecución del script de Octave.
    """
   
    
    try:
        #Ruta absoluta al script octave
        script_path= os.path.abspath("backend/octave/PoliLagrange.m")
        
        #Verificar si el script existe
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"El script {script_path} no se encuentra en la ruta especificada o no existe.")
        # Crear un archivo temporal para pasar los datos a Octave
        input_file = os.path.abspath("backend/octave/input_data.txt")
        
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
            f.write(f"{hora if hora is not None else ''}\n")
            f.write(f"{dia if dia is not None else ''}\n")
            f.write(f"{temperatura if temperatura is not None else ''}\n")
            f.write(f"{llueve if llueve is not None else ''}\n")
            f.write(f"{prob_lluvia if prob_lluvia is not None else ''}\n")
            f.write(f"{ciudad if ciudad is not None else ''}\n")
            f.write(f"{precio_kw if precio_kw is not None else ''}\n")

        # Comando para ejecutar Octave
        command = [
            "octave-cli",
            "--eval",
            (
                f"addpath('{os.path.dirname(script_path)}'); "
                f"resultado = PoliLagrange(); disp(resultado);"
            )
        ]

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"Error al ejecutar Octave: {result.stderr}")

        return result.stdout.strip()

    except Exception as e:
        raise RuntimeError(f"Error ejecutando PoliLagrange: {str(e)}")