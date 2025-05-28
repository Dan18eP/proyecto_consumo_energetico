function resultado = PoliLagrange()
    % Ruta al archivo de entrada
    input_file = '/app/backend/octave/input_data.txt';
    output_file = '/app/backend/octave/resultado.json';

    try
        % Verificar si el archivo de entrada existe
        if ~exist(input_file, 'file')
            error('El archivo de entrada no existe: %s', input_file);
        end

        % Abrir el archivo de entrada
        fileID = fopen(input_file, 'r');
        if fileID == -1
            error('No se pudo abrir el archivo de entrada: %s', input_file);
        end

        % Leer las primeras líneas comunes
        empleados = str2double(strtrim(fgetl(fileID)));
        computadora = str2double(strtrim(fgetl(fileID)));
        monitor = str2double(strtrim(fgetl(fileID)));
        impresora = str2double(strtrim(fgetl(fileID)));
        aire_acondicionado = str2double(strtrim(fgetl(fileID)));
        iluminacion = str2double(strtrim(fgetl(fileID)));
        router = str2double(strtrim(fgetl(fileID)));
        cafetera = str2double(strtrim(fgetl(fileID)));
        proyector = str2double(strtrim(fgetl(fileID)));
        modo = strtrim(fgetl(fileID)); % Leer el modo como texto
        ciudad = strtrim(fgetl(fileID)); % texto
        precio_kw = str2double(strtrim(fgetl(fileID)));
        dia = strtrim(fgetl(fileID)); % Cambiar a string para consistencia        

        % Validar el modo
        if ~any(strcmpi(modo, {"hora", "dia"})) % Validar que sea "hora" o "dia"
            error('El valor de "modo" no es válido. Debe ser "hora" o "dia".');
        end

        % Inicializar variables opcionales
        hora = NaN;
        temperatura = NaN;
        llueve_usuario = NaN;
        prob_lluvia = NaN;

        % Leer las líneas adicionales dependiendo del modo
        if strcmpi(modo, "hora")
            % Modo hora específica
            hora = str2double(strtrim(fgetl(fileID)));
            temperatura = str2double(strtrim(fgetl(fileID)));
            llueve_str = strtrim(fgetl(fileID)); % Leer como texto

            % Validar si es "True" o "False"
            if strcmpi(llueve_str, "true")
                llueve_usuario = true;
            elseif strcmpi(llueve_str, "false")
                llueve_usuario = false;
            else
                error("El valor de 'llueve' ingresado no es válido. Debe ser 'True' o 'False'.");
            end

            [horas, temperaturas, mensaje] = simular_temperaturas_con_lluvia(ciudad, 0, hora, llueve_usuario);
        elseif strcmpi(modo, "dia")
            % Modo día completo
            prob_lluvia = str2double(strtrim(fgetl(fileID)));
            [horas, temperaturas, mensaje] = simular_temperaturas_con_lluvia(ciudad, prob_lluvia, 'dia', NaN);
        end

        % Validar que los valores numéricos básicos no sean NaN
        datos_basicos = [empleados, computadora, monitor, impresora, aire_acondicionado, ...
                        iluminacion, router, cafetera, proyector, precio_kw];

        if any(isnan(datos_basicos))
            error('Uno o más valores numéricos básicos no se leyeron correctamente. Revisa el archivo.');
        end

    catch 
        err = lasterror();
        disp(['Error al leer el archivo de entrada: ', err.message]);

        % Cerrar el archivo si está abierto
        if exist('fileID', 'var') && fileID ~= -1
            fclose(fileID);
        end
        rethrow(err);
    end

    % Asegurarse de cerrar el archivo si no hubo errores
    if exist('fileID', 'var') && fileID ~= -1
        fclose(fileID);
    end

    % Validar que la ciudad sea válida
    ciudades_validas = {'bogotá', 'cali', 'medellín', 'barranquilla', 'cartagena'};
    if ~any(strcmpi(ciudad, ciudades_validas))
        error('Ciudad no reconocida. Usa Bogotá, Cali, Medellín, Barranquilla o Cartagena.');
    end

    % Datos de equipos
    nombres_equipos = {"computadora", "monitor", "impresora", "aire_acondicionado", "iluminacion", "router", "cafetera", "proyector"};
    consumos_base = [0.15, 0.03, 0.5, 1.3, 0.015, 0.012, 0.8, 0.3];  % Consumo en kW por equipo
    total_equipos = length(nombres_equipos);
    
    % Configurar equipos usando los datos del archivo
    equipos = [computadora, monitor, impresora, aire_acondicionado, iluminacion, router, cafetera, proyector];

    % Validar que las dimensiones de `equipos` y `consumos_base` coincidan
    if length(equipos) ~= length(consumos_base)
        error('Dimensiones incompatibles: `equipos` y `consumos_base` deben tener el mismo tamaño.');
    end

    % Validar que los valores numéricos no sean NaN
    if any(isnan(equipos)) || isnan(precio_kw)
        error('Uno o más valores numéricos no se leyeron correctamente. Revisa el archivo de entrada.');
    end

    % Consejos por equipo con porcentaje de ahorro
    consejos_generales = {
      "Apaga o usa modo suspensión si no se usa por largos periodos. (Ahorro: 30%)",
      "Reduce el brillo y apaga cuando no lo necesites. (Ahorro: 20%)",
      "Apaga si no se usa frecuentemente. Imprime en lotes. (Ahorro: 25%)",
      "Mantén entre 24–25 °C. Apaga si no hay gente. Realiza mantenimiento. (Ahorro: 40%)",
      "Usa sensores de movimiento. Cambia a bombillas LED. (Ahorro: 50%)",
      "Usa switches inteligentes. Apaga fuera de horario laboral. (Ahorro: 15%)",
      "Desenchufa cuando no se use. Usa temporizador. (Ahorro: 10%)",
      "Apaga inmediatamente después de uso. No lo dejes en modo espera. (Ahorro: 20%)"
    };

    % Consejos adicionales por equipo dependiendo de la hora
    consejos_horarios_data = {
      "computadora", {
        "Usa el modo ahorro de energía durante la mañana. (Ahorro: 10%)",
        "Evita usar múltiples aplicaciones pesadas al mismo tiempo. (Ahorro: 15%)",
        "Apaga la computadora si no la usarás por más de 30 minutos. (Ahorro: 20%)"
      };
      "monitor", {
        "Reduce el brillo en horas de la mañana. (Ahorro: 5%)",
        "Apaga el monitor durante el almuerzo. (Ahorro: 10%)",
        "Usa protectores de pantalla oscuros en la noche. (Ahorro: 8%)"
      };
      "aire_acondicionado", {
        "Mantén la temperatura en 24°C durante la mañana. (Ahorro: 10%)",
        "Apaga el aire acondicionado si hay ventilación natural. (Ahorro: 20%)",
        "Usa ventiladores en lugar del aire acondicionado en la noche. (Ahorro: 15%)"
      };
      "iluminacion", {
        "Usa sensores de movimiento para apagar luces automáticamente. (Ahorro: 30%)",
        "Aprovecha la luz natural durante el día. (Ahorro: 25%)",
        "Cambia a bombillas LED para mayor eficiencia. (Ahorro: 50%)"
      };
      "router", {
        "Apaga el router fuera del horario laboral. (Ahorro: 15%)",
        "Usa routers con modo de ahorro de energía. (Ahorro: 10%)",
        "Desactiva redes inalámbricas no utilizadas. (Ahorro: 5%)"
      };
      "cafetera", {
        "Desenchufa la cafetera cuando no esté en uso. (Ahorro: 10%)",
        "Usa temporizadores para limitar el tiempo de uso. (Ahorro: 15%)",
        "Evita recalentar café varias veces. (Ahorro: 5%)"
      };
      "proyector", {
        "Apaga el proyector inmediatamente después de usarlo. (Ahorro: 20%)",
        "Usa proyectores con modo de ahorro de energía. (Ahorro: 15%)",
        "Reduce el brillo del proyector si es posible. (Ahorro: 10%)"
      }
    };

    hora_pico = 13; % Hora pico definida

    % Generar temperaturas estimadas para todo el día o una hora específica
    if strcmpi(modo, "dia")
      % Modo día completo
      [horas, temperaturas, llueve, mensaje] = simular_temperaturas_con_lluvia(ciudad, prob_lluvia, 'dia');
      fprintf("\n%s\n", mensaje);
    else
      % Modo hora específica
      [horas, temperaturas, llueve_str, mensaje] = simular_temperaturas_con_lluvia(ciudad, 0, hora);
      fprintf("\n%s\n", mensaje);
    end

        % Inicializar estructura de resultados para JSON
    resultado_json = struct();
    resultado_json.parametros = struct();
    resultado_json.calculos = struct();
    resultado_json.consejos = struct();
    resultado_json.alertas = {};

    % Guardar parámetros
    resultado_json.parametros.empleados = empleados;
    resultado_json.parametros.modo = modo;
    if ~isnan(hora)
        resultado_json.parametros.hora = hora;
    end
    resultado_json.parametros.ciudad = ciudad;
    if ~isnan(temperatura)
        resultado_json.parametros.temperatura = temperatura;
    end
    resultado_json.parametros.precio_kw = precio_kw;
    resultado_json.parametros.dia = dia;
    resultado_json.parametros.equipos = struct();
    for i = 1:total_equipos
        if equipos(i) > 0
            campo = nombres_equipos{i};
            resultado_json.parametros.equipos.(campo) = equipos(i);
        end
    end

    % Inicializar variables de acumulación UNA SOLA VEZ
    consumo_total_kwh = 0;
    costo_total_cop = 0;
    ahorro_total_kwh = 0;
    ahorro_total_cop = 0;

    resultado_json.calculos.consumo_por_hora = {};

    if strcmpi(modo, "hora")
        % Modo hora específica
        temperatura_actual = temperaturas(1);
        llueve_actual = llueve_usuario; 
        
        total = sum(equipos .* consumos_base);
        ajuste_temp = 1 + (temperatura_actual - 25) * 0.02;
        total = total * ajuste_temp;
        costo = total * precio_kw;
        ahorro = 0.15 * costo;

        fprintf("\n Consumo estimado a las %d:00 = %.3f kW\n", hora, total);
        fprintf(" Costo: %.2f COP\n", costo);
        fprintf("Costo con ahorro: %.2f COP\n", costo - ahorro);
        fprintf("Ahorro estimado: %.2f COP\n", ahorro);

        % Actualizar totales para modo hora
        consumo_total_kwh = total;
        costo_total_cop = costo;
        ahorro_total_kwh = total * 0.15;
        ahorro_total_cop = ahorro;

        % Guardar en JSON
        consumo_hora = struct();
        consumo_hora.hora = hora;
        consumo_hora.consumo_kwh = total;
        consumo_hora.costo_cop = costo;
        consumo_hora.ahorro_cop = ahorro;
        consumo_hora.temperatura = temperatura_actual;
        resultado_json.calculos.consumo_por_hora{1} = consumo_hora;

        if abs(hora - hora_pico) <= 1
            mensaje_alerta = sprintf("¡Alerta! Se aproxima una hora pico (%d:00)", hora_pico);
            fprintf("⚠️  %s\n", mensaje_alerta);
            resultado_json.alertas{end+1} = mensaje_alerta;
        end

    else
        % Modo día completo
        fprintf("\n📊 Consumo de 7:00 a 19:00\n");

        % Cálculos por hora (estos YA acumulan en las variables totales)
        for i = 1:length(horas)
            h = horas(i);
            temperatura_actual = temperaturas(i);

            % Calcular consumo base por hora
            consumo_hora = sum(equipos .* consumos_base); 
            ajuste_temp = 1 + (temperatura_actual - 25) * 0.02;
            consumo_hora = consumo_hora * ajuste_temp;

            % Calcular costo y ahorro por hora
            costo_hora = consumo_hora * precio_kw;
            ahorro_hora_kwh = consumo_hora * 0.15;
            ahorro_hora_cop = ahorro_hora_kwh * precio_kw;

            % ACUMULAR en las variables totales
            consumo_total_kwh = consumo_total_kwh + consumo_hora;
            costo_total_cop = costo_total_cop + costo_hora;
            ahorro_total_kwh = ahorro_total_kwh + ahorro_hora_kwh;
            ahorro_total_cop = ahorro_total_cop + ahorro_hora_cop;

            fprintf("%02d:00 - Consumo: %.3f kWh | Costo: %.2f COP | Ahorro: %.2f COP | Temp: %.1f°C\n", h, consumo_hora, costo_hora, ahorro_hora_cop, temperatura_actual);

            % Guardar en JSON
            consumo_hora_data = struct();
            consumo_hora_data.hora = h;
            consumo_hora_data.consumo_kwh = consumo_hora;
            consumo_hora_data.costo_cop = costo_hora;
            consumo_hora_data.ahorro_cop = ahorro_hora_cop;
            consumo_hora_data.temperatura = temperatura_actual;
            resultado_json.calculos.consumo_por_hora{end+1} = consumo_hora_data;

            % Generar alerta si está cerca de la hora pico
            if abs(h - hora_pico) <= 1
                mensaje_alerta = sprintf("¡Alerta! Se aproxima una hora pico (%d:00)", hora_pico);
                fprintf("⚠️  %s\n", mensaje_alerta);
                resultado_json.alertas{end+1} = mensaje_alerta;
            end
        end

        fprintf("\n Consumo total: %.3f kWh\n", consumo_total_kwh);
        fprintf("💰 Costo total: %.2f COP\n", costo_total_cop);
        fprintf("💰 Ahorro total estimado: %.2f COP\n", ahorro_total_cop);
    end

    % Desglose del ahorro por equipo (SOLO UNA VEZ)
    fprintf("\n📋 Desglose del ahorro por equipo:\n");
    resultado_json.calculos.desglose_equipos = {};

    for i = 1:total_equipos
        if equipos(i) > 0
            consumo_equipo = equipos(i) * consumos_base(i);
            ahorro_equipo_kwh = consumo_equipo * 0.15;
            ahorro_equipo_cop = ahorro_equipo_kwh * precio_kw;
            fprintf("- %s: Ahorro = %.3f kWh | Ahorro en dinero = %.2f COP\n", nombres_equipos{i}, ahorro_equipo_kwh, ahorro_equipo_cop);

            % Guardar en JSON
            desglose_equipo = struct();
            desglose_equipo.nombre = nombres_equipos{i};
            desglose_equipo.cantidad = equipos(i);
            desglose_equipo.consumo_kwh = consumo_equipo;
            desglose_equipo.costo_cop = consumo_equipo * precio_kw;
            desglose_equipo.ahorro_kwh = ahorro_equipo_kwh;
            desglose_equipo.ahorro_cop = ahorro_equipo_cop;
            resultado_json.calculos.desglose_equipos{end+1} = desglose_equipo;
        end
    end

    % Mostrar el consumo total y el costo por cada tipo de equipo
    fprintf("\n📋 Consumo total y costo por equipo:\n");
    for i = 1:total_equipos
        if equipos(i) > 0
            consumo_equipo = equipos(i) * consumos_base(i);
            costo_equipo = consumo_equipo * precio_kw;
            fprintf("- %s: Consumo = %.3f kWh | Costo = %.2f COP\n", nombres_equipos{i}, consumo_equipo, costo_equipo);
        end
    end

    fprintf("\n Consumo total antes de aplicar consejos: %.3f kWh\n", consumo_total_kwh);
    fprintf("💰 Costo total antes de aplicar consejos: %.2f COP\n", costo_total_cop);

    % Guardar totales en JSON
    resultado_json.calculos.totales = struct();
    resultado_json.calculos.totales.consumo_total_kwh = consumo_total_kwh;
    resultado_json.calculos.totales.costo_total_cop = costo_total_cop;
    resultado_json.calculos.totales.ahorro_total_kwh = ahorro_total_kwh;
    resultado_json.calculos.totales.ahorro_total_cop = ahorro_total_cop;

    % Mostrar consejos por equipo
    fprintf("\n Consejos para ahorrar energía por equipo:\n");
    resultado_json.consejos.generales = {};

    for i = 1:total_equipos
        if equipos(i) > 0
            fprintf("- %s: %s\n", nombres_equipos{i}, consejos_generales{i});
            
            % Guardar en JSON
            consejo_general = struct();
            consejo_general.equipo = nombres_equipos{i};
            consejo_general.consejo = consejos_generales{i};
            resultado_json.consejos.generales{end+1} = consejo_general;
        end
    end

    % Mostrar consejos adicionales según la hora
    fprintf("\n📌 Consejos adicionales según la hora:\n");
    resultado_json.consejos.horarios = {};

    for i = 1:total_equipos
        if equipos(i) > 0
            equipo = nombres_equipos{i};
            idx = find(strcmp(consejos_horarios_data(:, 1), equipo));
            if ~isempty(idx)
                fprintf("\n%s:\n", equipo);
                
                % Estructura para JSON
                consejo_horario = struct();
                consejo_horario.equipo = equipo;
                consejo_horario.consejos = {};
                
                for j = 1:length(consejos_horarios_data{idx, 2})
                    fprintf("- %s\n", consejos_horarios_data{idx, 2}{j});
                    consejo_horario.consejos{end+1} = consejos_horarios_data{idx, 2}{j};
                end
                resultado_json.consejos.horarios{end+1} = consejo_horario;
            else
                fprintf("\n%s: No hay consejos adicionales definidos.\n", equipo);
            end
        end
    end

    % Mostrar mensaje final
    fprintf("\n Implementar estos consejos puede ayudar a reducir significativamente el consumo energético y los costos asociados.\n");
    fprintf(" Además, contribuirás a un menor impacto ambiental al reducir las emisiones de CO₂.\n");
    
    % Agregar mensaje de clima
    resultado_json.clima = struct();
    resultado_json.clima.mensaje = mensaje;
    
    % Guardar resultado en archivo JSON
    json_file = '/app/backend/octave/resultado.json';
    
    if isempty(resultado_json)
        error('Los datos para escribir en el archivo JSON están vacíos.');
    end
    
    try
        guardar_json(resultado_json, json_file);
        fprintf("\n📄 Resultados guardados en: %s\n", json_file);
        
        % Crear resultado estructurado para retornar (compatibilidad)
        resultado = struct();
        resultado.consumo_total_kwh = consumo_total_kwh;
        resultado.costo_total_cop = costo_total_cop;
        resultado.ahorro_total_kwh = ahorro_total_kwh;
        resultado.ahorro_total_cop = ahorro_total_cop;
        resultado.mensaje = "Cálculo completado exitosamente";

    catch
        err = lasterror();
        if exist('fileID', 'var') && fileID ~= -1
            fclose(fileID);
        end
        rethrow(err);
    end
    

   % Función para guardar JSON (implementación corregida)
    function guardar_json(datos, archivo)
        fileID = -1; % Inicializar fileID para evitar problemas si fopen falla
        try
            % Abrir el archivo para escritura
            fileID = fopen(archivo, 'w');
            if fileID == -1
                error('No se pudo abrir el archivo %s para escritura.', archivo);
            end

            % Escribir JSON usando función simplificada
            escribir_json_simple(fileID, datos);

        catch
            % Capturar el error y mostrar el mensaje
            err = lasterror();
            disp(['Error al guardar JSON: ', err.message]);

            % Cerrar el archivo si está abierto
            if fileID ~= -1
                fclose(fileID);
            end
            rethrow(err);
        end
        
        % Cerrar archivo al final
        if fileID ~= -1
            fclose(fileID);
        end
    end % Cierre de la función guardar_json

    % Función simplificada para escribir JSON
    function escribir_json_simple(fileID, datos)
        json_str = convertir_a_json_string(datos);
        fprintf(fileID, '%s', json_str);
    end

    % Función para convertir estructura a string JSON
    function json_str = convertir_a_json_string(datos)
        if isstruct(datos)
            campos = fieldnames(datos);
            elementos = {};
            for i = 1:length(campos)
                campo = campos{i};
                valor_str = convertir_a_json_string(datos.(campo));
                elementos{end+1} = sprintf('"%s":%s', campo, valor_str);
            end
            json_str = sprintf('{%s}', strjoin(elementos, ','));
            
        elseif iscell(datos)
            elementos = {};
            for i = 1:length(datos)
                elementos{end+1} = convertir_a_json_string(datos{i});
            end
            json_str = sprintf('[%s]', strjoin(elementos, ','));
            
        elseif ischar(datos) || isstring(datos)
            % Escapar caracteres especiales en strings
            datos_escaped = strrep(datos, char(92), [char(92) char(92)]); % Escapar barra invertida
            datos_escaped = strrep(datos_escaped, '"', '\"');
            datos_escaped = strrep(datos_escaped, char(10), '\n');
            datos_escaped = strrep(datos_escaped, char(13), '\r');
            json_str = sprintf('"%s"', datos_escaped);
            
        elseif isnumeric(datos)
            if length(datos) == 1
                if isnan(datos) || isinf(datos)
                    json_str = 'null';
                else
                    json_str = sprintf('%.6g', datos);
                end
            else
                elementos = {};
                for i = 1:length(datos)
                    if isnan(datos(i)) || isinf(datos(i))
                        elementos{end+1} = 'null';
                    else
                        elementos{end+1} = sprintf('%.6g', datos(i));
                    end
                end
                json_str = sprintf('[%s]', strjoin(elementos, ','));
            end
            
        elseif islogical(datos)
            if datos
                json_str = 'true';
            else
                json_str = 'false';
            end
            
        else
            json_str = 'null';
        end
    end

    % Función para simular temperaturas con lluvia 
    function [horas, temperaturas, llueve, mensaje] = simular_temperaturas_con_lluvia(ciudad, prob_lluvia, modo, llueve_usuario)
        % Definir datos por ciudad (horas base y temperaturas estimadas)
        switch lower(ciudad)
            case 'bogotá'
                horas_muestra = 7:19;
                temp_muestra = [9 9.5 10 11 12.5 14 15 14.5 13.5 12 11.5 10.5 10];
            case 'cali'
                horas_muestra = 7:19;
                temp_muestra = [21 22 23 24 25.5 27 29 28.5 27.5 26.5 25 24.5 24];
            case 'medellín'
                horas_muestra = 7:19;
                temp_muestra = [17 17.5 18 19 20.5 22 23 22.5 21.5 20 19.5 18.5 18];
            case 'barranquilla'
                horas_muestra = 7:19;
                temp_muestra = [26 26.5 27 28 29.5 31 33 33 32.5 31.5 30.5 29.5 29];
            case 'cartagena'
                horas_muestra = 7:19;
                temp_muestra = [27 27.5 28 29 30.5 32 34 34 33.5 32.5 31.5 30.5 30];
            otherwise
                error('Ciudad no reconocida. Usa Bogotá, Cali, Medellín, Barranquilla o Cartagena.');
        end

        % Inicializar valores por defecto
        llueve = NaN; % Valor por defecto para llueve

        % Rango de horas: 7 AM a 7 PM
        if strcmp(modo, 'dia')
            horas = 7:1:19;
            llueve = rand(size(horas)) < prob_lluvia; % Generar valores aleatorios según probabilidad
        elseif isnumeric(modo)
            horas = modo;
        else
            error("Modo inválido: debe ser 'dia' o una hora numérica.");
        end

        temperaturas = zeros(size(horas));
        for i = 1:length(horas)
            temp = temp_muestra(horas_muestra == horas(i));
            if strcmp(modo, 'dia')
                % Ajuste por lluvia según probabilidad
                if llueve(i)
                    x_prob = [0, 0.25, 0.5, 0.75, 1];
                    y_ajuste = [0, -0.5, -1, -1.5, -2];
                    ajuste = PoliLagrange_interpolacion(x_prob, y_ajuste, prob_lluvia);
                    temp = temp + ajuste;
                end
                temperaturas(i) = temp;

                % Guardar información de lluvia en JSON
                lluvia_data = struct();
                lluvia_data.hora = horas(i);
                lluvia_data.llueve = llueve(i);
                lluvia_data.temperatura_ajustada = temp;
                resultado_json.clima.lluvia{end+1} = lluvia_data;

            elseif isnumeric(modo)
                % En modo hora se usa la temperatura dada y se ajusta ligeramente si llueve
                temp = temperatura;
                if llueve_usuario == true
                    temp = temp - 0.5;  % Reducción mínima por lluvia
                    llueve = true; % Asignar valor explícito
                else
                    llueve = false; % Asignar valor explícito
                end
                temperaturas(i) = temp;

                % Guardar información de lluvia en JSON
                lluvia_data = struct();
                lluvia_data.hora = horas;
                lluvia_data.llueve = llueve;
                lluvia_data.temperatura_ajustada = temp;
                resultado_json.clima.lluvia{1} = lluvia_data;
            end
        end

        % Mensaje
        if strcmp(modo, 'dia')
            horas_lluvia = horas(llueve);
            if isempty(horas_lluvia)
                mensaje = "No se espera lluvia durante el día.";
            else
                horas_str = sprintf('%d, ', horas_lluvia);
                mensaje = sprintf("Llueve en las horas: %scon posible disminución de temperatura.", horas_str);
            end
        else
            if llueve_usuario == true
                mensaje = sprintf("Llueve a las %d h. Se aplicó un ajuste suave a la temperatura.", horas);
            else
                mensaje = sprintf("No llueve a las %d h. La temperatura se mantiene según lo ingresado.", horas);
            end
        end
    end % Cierre de la función simular_temperaturas_con_lluvia

    % Función de interpolación de Lagrange 
    function y = PoliLagrange_interpolacion(x, f, valor)
      n = length(x);
      y = 0;
      for i = 1:n
        L = 1;
        for j = 1:n
          if j != i
            L *= (valor - x(j)) / (x(i) - x(j));
          end
        end
        y += f(i) * L;
      end
    end

end % Cierre de la función principal