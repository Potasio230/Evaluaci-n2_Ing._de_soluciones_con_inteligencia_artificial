#Imports y configuración de cliente OpenAI
import os
import warnings
from difflib import get_close_matches #nuevo import
from openai import OpenAI
from dotenv import load_dotenv
import sqlite3

#BufferWindowMemory
from langchain_classic.memory import ConversationBufferWindowMemory




#Cargar variables de entorno desde .env
load_dotenv()

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN")    
)



#Base de datos
def conectar_duoc():
    return sqlite3.connect("duoc.db")

def crear_tablas_duoc():
    conn = conectar_duoc()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS carreras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        sede TEXT NOT NULL
    )
    """)

    #Tabla para guardar el historial de consultas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial_consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consulta TEXT NOT NULL,
            respuesta TEXT NOT NULL,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profesores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        carrera TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS preguntas_frecuentes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pregunta TEXT NOT NULL,
        respuesta TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

#Poblado de tablas
def insertar_datos():
    conn = conectar_duoc()
    cursor = conn.cursor()

    #Verificar si existen datos en las tablas
    cursor.execute("SELECT COUNT(*) FROM carreras")
    total = cursor.fetchone()[0]

    if total > 0:   
        conn.close()
        return

    #Carreras
    cursor.execute("INSERT INTO carreras (nombre, sede) VALUES (?, ?)", 
                    ("Ingeniería en Informática", "Sede Puerto Montt"))
    cursor.execute("INSERT INTO carreras (nombre, sede) VALUES (?, ?)", 
                    ("Diseño Gráfico", "Sede San Carlos de Apoquindo"))
    cursor.execute("INSERT INTO carreras (nombre, sede) VALUES (?, ?)", 
                    ("Administración de Empresas", "Sede Concepción"))
    cursor.execute("INSERT INTO carreras (nombre, sede) VALUES (?, ?)", 
                    ("Ingeniería Civil Industrial", "Sede Valparaíso"))
    cursor.execute("INSERT INTO carreras (nombre, sede) VALUES (?, ?)", 
                    ("Medicina Veterinaria", "Sede La Florida"))
    cursor.execute("INSERT INTO carreras (nombre, sede) VALUES (?, ?)", 
                    ("Psicología", "Sede Maipú"))
    cursor.execute("INSERT INTO carreras (nombre, sede) VALUES (?, ?)", 
                    ("Ingeniería en Mecatrónica", "Sede San Joaquín"))
    cursor.execute("INSERT INTO carreras (nombre, sede) VALUES (?, ?)", 
                    ("Periodismo", "Sede Viña del Mar"))
    cursor.execute("INSERT INTO carreras (nombre, sede) VALUES (?, ?)",
                ("Analista Programador Computacional", "Sede Plaza Vespucio"))
    cursor.execute("INSERT INTO carreras (nombre, sede) VALUES (?, ?)",
                    ("Ciberseguridad", "Sede San Joaquín"))
    cursor.execute("INSERT INTO carreras (nombre, sede) VALUES (?, ?)",
                    ("Contabilidad General", "Sede Puente Alto"))
    cursor.execute("INSERT INTO carreras (nombre, sede) VALUES (?, ?)",
                    ("Publicidad", "Sede Viña del Mar"))
    cursor.execute("INSERT INTO carreras (nombre, sede) VALUES (?, ?)",
                    ("Prevención de Riesgos", "Sede Concepción"))
    cursor.execute("INSERT INTO carreras (nombre, sede) VALUES (?, ?)",
                    ("Turismo y Hotelería", "Sede Antonio Varas"))
    cursor.execute("INSERT INTO carreras (nombre, sede) VALUES (?, ?)",
                    ("Gastronomía Internacional", "Sede Padre Alonso de Ovalle"))
    cursor.execute("INSERT INTO carreras (nombre, sede) VALUES (?, ?)",
                    ("Ingeniería en Construcción", "Sede Valparaíso"))

    # Profesores
    cursor.execute("INSERT INTO profesores (nombre, carrera) VALUES (?, ?)", 
                    ("Juan Pérez", "Ingeniería en Informática"))
    cursor.execute("INSERT INTO profesores (nombre, carrera) VALUES (?, ?)", 
                    ("María González", "Diseño Gráfico"))
    cursor.execute("INSERT INTO profesores (nombre, carrera) VALUES (?, ?)", 
                    ("Carlos Ramírez", "Administración de Empresas"))
    cursor.execute("INSERT INTO profesores (nombre, carrera) VALUES (?, ?)", 
                    ("Ana Torres", "Ingeniería Civil Industrial"))
    cursor.execute("INSERT INTO profesores (nombre, carrera) VALUES (?, ?)", 
                    ("Pedro Morales", "Medicina Veterinaria"))
    cursor.execute("INSERT INTO profesores (nombre, carrera) VALUES (?, ?)", 
                    ("Laura Fernández", "Psicología"))
    cursor.execute("INSERT INTO profesores (nombre, carrera) VALUES (?, ?)", 
                    ("Ricardo Soto", "Ingeniería en Mecatrónica"))
    cursor.execute("INSERT INTO profesores (nombre, carrera) VALUES (?, ?)", 
                    ("Claudia Herrera", "Periodismo"))
    cursor.execute("INSERT INTO profesores (nombre, carrera) VALUES (?, ?)",
                ("Miguel Fuentes", "Analista Programador Computacional"))
    cursor.execute("INSERT INTO profesores (nombre, carrera) VALUES (?, ?)",
                    ("Camila Rojas", "Ciberseguridad"))
    cursor.execute("INSERT INTO profesores (nombre, carrera) VALUES (?, ?)",
                    ("Patricia Silva", "Contabilidad General"))
    cursor.execute("INSERT INTO profesores (nombre, carrera) VALUES (?, ?)",
                    ("Sebastián López", "Publicidad"))
    cursor.execute("INSERT INTO profesores (nombre, carrera) VALUES (?, ?)",
                    ("Jorge Medina", "Prevención de Riesgos"))
    cursor.execute("INSERT INTO profesores (nombre, carrera) VALUES (?, ?)",
                    ("Valentina Araya", "Turismo y Hotelería"))
    cursor.execute("INSERT INTO profesores (nombre, carrera) VALUES (?, ?)",
                    ("Francisco Vargas", "Gastronomía Internacional"))
    cursor.execute("INSERT INTO profesores (nombre, carrera) VALUES (?, ?)",
                    ("Daniela Castillo", "Ingeniería en Construcción"))
    
    #Preguntas frecuentes
    cursor.execute("INSERT INTO preguntas_frecuentes (pregunta, respuesta) VALUES (?, ?)",
                    ("¿Cómo recuperar mi contraseña institucional?",
                     "Debes ingresar al portal DUOC y seleccionar la opción recuperar contraseña."))
    cursor.execute("INSERT INTO preguntas_frecuentes (pregunta, respuesta) VALUES (?, ?)",
                    ("¿Dónde puedo revisar mis notas?",
                     "Puedes revisar tus notas en el portal académico del estudiante."))
    cursor.execute("INSERT INTO preguntas_frecuentes (pregunta, respuesta) VALUES (?, ?)",
                    ("¿Cómo contactar soporte TI?",
                     "Puedes comunicarte mediante la mesa de ayuda institucional."))
    cursor.execute("INSERT INTO preguntas_frecuentes (pregunta, respuesta) VALUES (?, ?)",
                    ("¿Cómo descargar Microsoft Office gratis?",
                     "Puedes descargar Office desde el portal institucional usando tu correo DUOC."))
    cursor.execute("INSERT INTO preguntas_frecuentes (pregunta, respuesta) VALUES (?, ?)",
                ("¿Cómo obtener mi certificado de alumno regular?",
                 "Puedes descargarlo desde el portal académico institucional."))
    cursor.execute("INSERT INTO preguntas_frecuentes (pregunta, respuesta) VALUES (?, ?)",
                    ("¿Cómo cambiar mi contraseña institucional?",
                    "Debes acceder al portal institucional y seleccionar la opción de cambio de contraseña."))
    cursor.execute("INSERT INTO preguntas_frecuentes (pregunta, respuesta) VALUES (?, ?)",
                    ("¿Cómo acceder a Microsoft Teams?",
                    "Puedes iniciar sesión con tu correo institucional y contraseña DUOC."))
    cursor.execute("INSERT INTO preguntas_frecuentes (pregunta, respuesta) VALUES (?, ?)",
                    ("¿Dónde veo mi horario de clases?",
                    "El horario se encuentra disponible en el portal académico del estudiante."))
    cursor.execute("INSERT INTO preguntas_frecuentes (pregunta, respuesta) VALUES (?, ?)",
                    ("¿Cómo solicitar soporte técnico?",
                    "Debes crear un ticket mediante la mesa de ayuda institucional."))
    cursor.execute("INSERT INTO preguntas_frecuentes (pregunta, respuesta) VALUES (?, ?)",
                    ("¿Cómo actualizar mis datos personales?",
                    "Puedes actualizar tus datos desde tu perfil en el portal académico."))
    conn.commit()
    conn.close()


def obtener_profesores(carrera=None, nombre=None):

    conn = conectar_duoc()
    cursor = conn.cursor()

    if carrera:

        cursor.execute(
            "SELECT nombre FROM profesores WHERE carrera = ?",
            (carrera,)
        )
        resultado = [p[0] for p in cursor.fetchall()]

    elif nombre:

        cursor.execute(
            """
            SELECT nombre, carrera
            FROM profesores
            WHERE nombre LIKE ?
            """,
            (f"%{nombre}%",)
        )

        resultado = cursor.fetchone()

    else:
        resultado = None

    conn.close()
    return resultado

#Esto sirve para que al momento de hacer una pregunta en el chat general,
#si la pregunta tiene que ver con alguna de las preguntas frecuentes, se busque directamente en la base de datos
# y se entregue la respuesta sin necesidad de consultar a la IA.
def buscar_faq(pregunta_usuario):

    pregunta_usuario = pregunta_usuario.lower()

    conn = conectar_duoc()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT pregunta, respuesta FROM preguntas_frecuentes"
    )

    preguntas = cursor.fetchall()

    conn.close()

    # Contraseña
    if "contraseña" in pregunta_usuario:
        for pregunta, respuesta in preguntas:
            if "contraseña" in pregunta.lower():
                return respuesta

    # Notas
    elif "notas" in pregunta_usuario:
        for pregunta, respuesta in preguntas:
            if "notas" in pregunta.lower():
                return respuesta

    # Office
    elif "office" in pregunta_usuario or "microsoft" in pregunta_usuario:
        for pregunta, respuesta in preguntas:
            if "office" in pregunta.lower():
                return respuesta

    # Soporte
    elif "soporte" in pregunta_usuario:
        for pregunta, respuesta in preguntas:
            if "soporte" in pregunta.lower():
                return respuesta

    return None

#IMPORTANTE
#Funcion para guardar cada consulta realizada por el estudiante en la base de datos 
def guardar_consulta(consulta, respuesta):

    conn = conectar_duoc()
    cursor = conn.cursor()

    #Aca se guardan las consultas
    cursor.execute("""
        INSERT INTO historial_consultas
        (consulta, respuesta)
        VALUES (?, ?)
    """, (consulta, respuesta))

    conn.commit()
    conn.close()


#Buscar la carrera más similar de nuestra búsqueda
def buscar_carrera_similar(nombre_ingresado):
    conn = conectar_duoc()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM carreras")
    carreras = [c[0] for c in cursor.fetchall()]
    conn.close()

    coincidencias = get_close_matches(
        nombre_ingresado,
        carreras,
        n=1,
        cutoff=0.4
    )

    if coincidencias:
        return coincidencias[0], 1
    
    return None, 0

def obtener_info_carrera(nombre_carrera):

    conn = conectar_duoc()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT nombre, sede
        FROM carreras
        WHERE nombre = ?
        """,
        (nombre_carrera,)
    )

    carrera = cursor.fetchone()
    conn.close()
    return carrera



def ayuda_estudiantil():
    print("\n=== AYUDA ESTUDIANTIL ===")
    print("1. Ver carreras")
    print("2. Ver profesores por carrera")
    print("3. Preguntas frecuentes")

    opcion = input("Elige una opción: ")

    if opcion == "1":
        conn = conectar_duoc()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, sede FROM carreras")
        carreras = cursor.fetchall()
        conn.close()
        if carreras:
            print("\n Carreras disponibles en DUOC:")
            for c in carreras:
                print(f"- {c[0]} (Sede: {c[1]})")
        else:
            print("No hay carreras registradas en la base de datos.")

    elif opcion == "2":
        carrera_ingresada = input("Ingresa el nombre de la carrera: ")
        carrera_similar, score = buscar_carrera_similar(carrera_ingresada)

        if score > 0.65:  # umbral de similitud
            profesores = obtener_profesores(carrera=carrera_similar)
            if profesores:
                print(f"\n Detectamos que quisiste decir: {carrera_similar}")
                print(f" Profesores de {carrera_similar}: {', '.join(profesores)}")
                #Conectar con la IA para enriquecer respuesta
                contexto = (
                    f"Eres un asistente universitario. "
                    f"La carrera detectada es {carrera_similar}. "
                    f"Los profesores son: {', '.join(profesores)}."
                )
                
                consultar_ti(
                    f"Háblame brevemente sobre la carrera {carrera_similar}",
                    contexto,
                    "few-shot"
                )
            else:
                print("No se encontraron profesores para esa carrera.")
        else:
            print("No se encontró una carrera similar. Intenta de nuevo.")

    elif opcion == "3":

        conn = conectar_duoc()
        cursor = conn.cursor()
        cursor.execute("SELECT pregunta, respuesta FROM preguntas_frecuentes")
        preguntas = cursor.fetchall()
        conn.close()
        print("\n=== PREGUNTAS FRECUENTES ===")
        for i, p in enumerate(preguntas, 1):
            print(f"{i}. {p[0]}")
        seleccion = int(input("Selecciona una pregunta: "))

        if 1 <= seleccion <= len(preguntas):
            pregunta, respuesta = preguntas[seleccion - 1]
            print(f"\nPregunta: {pregunta}")
            print(f"Respuesta: {respuesta}")

    else:
        print("Opción inválida.")

#Función general de la IA con diferentes tipos de respuesta (zero-shot, few-shot, chain-of-thought)
def consultar_ti(pregunta, contexto, tipo="zero-shot"):
    try:
        #Zero-shot (respuesta directa sin ejemplos)
        if tipo == "zero-shot":
            messages = [
                {
                    "role": "system",
                    "content": contexto + 
                    ". Responde de forma clara, breve y útil para estudiantes y personal universitario."
                },
                {"role": "user", "content": pregunta}
            ]

        #Few-shot (respuesta con ejemplos previos para guiar el formato)
        elif tipo == "few-shot":
            messages = [
                {
                    "role": "system",
                    "content": contexto + 
                    ". Responde como asistente de mesa de ayuda TI claro y práctico."
                },
                {"role": "user", "content": pregunta}
            ]

        #Chain-of-thought (respuesta con explicación paso a paso para problemas más complejos)
        elif tipo == "chain-of-thought":
            messages = [
                {
                    "role": "system",
                    "content": contexto + 
                    ". Responde siguiendo este formato:\n"
                    "1. Explicación breve\n"
                    "2. Pasos a seguir\n"
                    "3. Recomendación final"
                },
                {"role": "user", "content": pregunta}
            ]

        else:
            messages = [
                {"role": "system", "content": contexto},
                {"role": "user", "content": pregunta}
            ]

        #config IA
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )

        print("\nRespuesta:")
        print(response.choices[0].message.content, "\n")

    except Exception as e:
        print("Error:", e)


#Elección de tipo de respuesta para la IA 
def elegir_tipo_respuesta():
    print("\nTipo de respuesta:")
    print("1. Zero-shot")
    print("2. Few-shot")
    print("3. Chain of Thought")

    tipo_op = input("Elige tipo: ")

    tipo_map = {
        "1": "zero-shot",
        "2": "few-shot",
        "3": "chain-of-thought"
    }

    return tipo_map.get(tipo_op, "zero-shot")

#IMPORTANTE
#Orquestador para determinar qué herramienta usar según la pregunta del usuario.
def orquestador(pregunta):

    #Convierte la pregunta a minúsculas para facilitar la detección de palabras clave
    pregunta_lower = pregunta.lower()

    # Herramienta: cantidad de carreras
    if "cuantas carreras" in pregunta_lower:
        return "cantidad_carreras"

    # Herramienta: cantidad de profesores
    elif "cuantos profesores" in pregunta_lower:
        return "cantidad_profesores"
    
    #IMPORTANTE
    #Herramienta: para que la ia analice la tarea y decida que pasos ejecutar de 
    #manera autonoma
    elif (
        "profesores" in pregunta_lower
        or "carrera" in pregunta_lower
    ):
        return "planificador"
    
    #Herramienta: Para que el estudiante al momento de preguntar el orquestador
    #entienda sin problemas la consulta
    elif (
    "mostrar carreras" in pregunta_lower
    or "lista de carreras" in pregunta_lower
    or "cuales son las carreras" in pregunta_lower
    or "qué carreras" in pregunta_lower
    or "que carreras" in pregunta_lower
    ):
        return "listar_carreras"

    # Herramienta: búsqueda de carrera
    elif "carrera" in pregunta_lower:
        return "buscar_carrera"

    # Herramienta: preguntas frecuentes
    elif (
        "contraseña" in pregunta_lower
        or "notas" in pregunta_lower
        or "office" in pregunta_lower
        or "microsoft" in pregunta_lower
        or "soporte" in pregunta_lower
    ):
        return "faq"
    
    #Herramienta: Detectar cualquier carrera similar mencionada en la pregunta
    elif buscar_carrera_similar(pregunta)[0]:
        return "buscar_carrera"
    
    # Herramienta: Chat general 
    else:
        return "ia"

#Chat general 
#Aca es donde se guardan las conversaciones 
def chat_general(memory):
    print("\nEstas en el chat general, para salir escribe 'salir'\n")
    tipo = elegir_tipo_respuesta()

    while True:
        user_input = input("Escribe tu mensaje: ")

        if user_input.lower() == "salir":
            break


        try:
            pregunta = user_input.lower()

            #IMPORTANTE
            #Configuracion del orquestador
            herramienta = orquestador(user_input)

            #Aca muestro de manera explicita qué herramienta se ha seleccionado
            print(f"\n[ORQUESTADOR]")
            print(f"Herramienta seleccionada: {herramienta}\n")
            
            
            #Aca la IA actúa como planificador, es decir, analiza la pregunta del usuario
            #y decide qué pasos seguir para entregar una respuesta completa
            if herramienta == "planificador":
                
                #IMPORTANTE
                #Aca se llama a la funcion de carrera similar para detectar si en la pregunta del usuario se menciona alguna carrera
                
                print("\n[PLANIFICADOR]")
                print("Paso 1: Buscar carrera")

                carrera_similar, score = buscar_carrera_similar(user_input)

                if score > 0:

                    print("Paso 2: Buscar profesores")

                    profesores = obtener_profesores(carrera=carrera_similar)

                    print("Paso 3: Generar respuesta")

                    respuesta = (
                        f"La carrera encontrada es "
                        f"{carrera_similar}. "
                        f"Los profesores asociados son: "
                        f"{', '.join(profesores)}"
                    )

                else:

                    respuesta = (
                        "No encontré una carrera relacionada."
                    )

                print("Asistente:", respuesta)

                #IMPORTANTE
                #Aca se guarda el contexto de la pregunta y respuesta en la memoria de conversación
                memory.save_context(
                    {"input": user_input},
                    {"output": respuesta}
                )

                guardar_consulta(
                    user_input,
                    respuesta
                )

                continue

            #Cantidad de carreras
            if herramienta == "cantidad_carreras":

                conn = conectar_duoc()
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM carreras")
                total = cursor.fetchone()[0]
                conn.close()
                respuesta = f"Actualmente hay {total} carreras registradas en la base de datos."
                print("Asistente:", respuesta, "\n")
                
                memory.save_context(
                    {"input": user_input},
                    {"output": respuesta}
                ) 

                #IMPORTANTE
                #Aca se guarda la consulta y respuesta en la base de datos para tener un historial persistente
                guardar_consulta(user_input, respuesta)
                continue

            elif herramienta == "cantidad_profesores":

                conn = conectar_duoc()
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM profesores")
                total = cursor.fetchone()[0]
                conn.close()
                respuesta = f"Actualmente hay {total} profesores registrados."
                print("Asistente:", respuesta, "\n")

                memory.save_context(
                    {"input": user_input},
                    {"output": respuesta}
                )

                guardar_consulta(user_input, respuesta)
                continue

            if herramienta == "buscar_carrera":

                carrera_similar, score = buscar_carrera_similar(
                    user_input
                )

                if carrera_similar:

                    carrera = obtener_info_carrera(
                        carrera_similar
                    )

                    profesores = obtener_profesores(
                        carrera=carrera_similar
                    )

                    contexto = f"""
                    Carrera: {carrera[0]}
                    Sede: {carrera[1]}
                    Profesores: {', '.join(profesores)}
                    """

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content":
                                "Eres un asistente universitario. "
                                "Usa exclusivamente la información entregada "
                                "para describir brevemente la carrera."
                            },
                            {
                                "role": "user",
                                "content":
                                f"""
                                Información disponible:

                                {contexto}

                                Describe brevemente la carrera,
                                menciona la sede y los profesores.
                                """
                            }
                        ],
                        temperature=0.5,
                        max_tokens=200
                    )

                    respuesta = response.choices[0].message.content

                else:

                    respuesta = (
                        "No encontré información "
                        "sobre esa carrera."
                    )

                print("Asistente:")
                print(respuesta)

                memory.save_context(
                    {"input": user_input},
                    {"output": respuesta}
                )

                guardar_consulta(
                    user_input,
                    respuesta
                )

                continue

            elif herramienta == "faq":

                respuesta = buscar_faq(user_input)

                if respuesta is None:
                    respuesta = (
                        "No encontré una respuesta específica en las preguntas frecuentes."
                    )
                print("Asistente:", respuesta, "\n")

                memory.save_context(
                    {"input": user_input},
                    {"output": respuesta}
                )

                guardar_consulta(user_input, respuesta)
                continue

            if herramienta == "listar_carreras":

                conn = conectar_duoc()
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT nombre FROM carreras"
                )

                carreras = cursor.fetchall()
                conn.close()
                respuesta = "Carreras disponibles:\n"

                for carrera in carreras:
                    respuesta += f"- {carrera[0]}\n"

                print("Asistente:")
                print(respuesta)

                memory.save_context(
                    {"input": user_input},
                    {"output": respuesta}
                )

                guardar_consulta(user_input, respuesta)

                continue

            if herramienta == "buscar_profesor":

                nombre_busqueda = (
                    user_input
                    .replace("profesor", "")
                    .replace("Profesor", "")
                    .strip()
                )

                resultado = obtener_profesores(
                    nombre=nombre_busqueda
                )

                if resultado:

                    profesor, carrera = resultado
                    respuesta = (
                        f"El profesor {profesor} "
                        f"pertenece a la carrera "
                        f"{carrera}."
                    )

                else:

                    respuesta = (
                        "No encontré un profesor "
                        "con ese nombre."
                    )

                print("Asistente:", respuesta)

                memory.save_context(
                    {"input": user_input},
                    {"output": respuesta}
                )

                guardar_consulta(
                    user_input,
                    respuesta
                )
                continue

            
            #New
            history_messages = memory.load_memory_variables({})["chat_history"]
            messages = []
            #Elección de tipo de respuesta para la IA
            if tipo == "zero-shot":

                messages.append({
                    "role": "system",
                    "content":
                    "Eres un asistente de mesa de ayuda TI universitaria. "
                    "Solo puedes responder preguntas relacionadas con: "
                    "tecnología, informática, programación, redes, soporte técnico, "
                    "carreras universitarias, estudios y temas académicos."
                })

            elif tipo == "few-shot":

                messages.append({
                    "role": "system",
                    "content":
                    "Eres un asistente de mesa de ayuda TI universitaria.\n"
                    "Solo respondes temas académicos y tecnológicos.\n\n"
                    "Ejemplo:\n"
                    "Usuario: Mi internet no funciona\n"
                    "Asistente: Reinicia el router y verifica la conexión."
                })

            elif tipo == "chain-of-thought":

                messages.append({
                    "role": "system",
                    "content":
                    "Eres un asistente de mesa de ayuda TI universitaria.\n"
                    "Responde siguiendo este formato:\n"
                    "1. Explicación breve\n"
                    "2. Pasos a seguir\n"
                    "3. Recomendación final"
                })

            for msg in history_messages:

                if msg.type == "human":
                    messages.append({
                        "role": "user",
                        "content": msg.content
                    })

                elif msg.type == "ai":
                    messages.append({
                        "role": "assistant",
                        "content": msg.content
                    })
            
            messages.append({
                "role": "user",
                "content": user_input
            })
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages, 
                temperature=0.7,
                max_tokens=200
            )

            respuesta = response.choices[0].message.content
            #Aca el historial lo guarda:
            memory.save_context(
                {"input": user_input},
                {"output": respuesta}
            )
            
            guardar_consulta(user_input, respuesta)

            print("Asistente:", respuesta, "\n")


        except Exception as e:
            print("Error:", e)

#Historial
def ver_historial(memory):

    print("\n=== HISTORIAL ===")

    historial = memory.load_memory_variables({})["chat_history"]

    if not historial:
        print("No hay mensajes guardados.")
        return

    for msg in historial:

        if msg.type == "human":
            print(f"Usuario: {msg.content}")

        elif msg.type == "ai":
            print(f"Asistente: {msg.content}")

#IMPORTANTE
#Funcion para ver el historial guardado en la base de datos
def ver_historial_bd():

    conn = conectar_duoc()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT consulta, fecha
        FROM historial_consultas
        ORDER BY id DESC
        LIMIT 10
    """)

    registros = cursor.fetchall()

    conn.close()

    print("\n=== HISTORIAL GUARDADO EN BD ===")

    if not registros:
        print("No existen consultas guardadas.")
        return

    for consulta, fecha in registros:
        print(f"[{fecha}] {consulta}")




#Menú principal
def menu():

    #Esto sirve para eliminar las advertencias de deprecación que puedan surgir al usar la memoria de conversación,
    # ya que algunas funciones podrían estar marcadas como obsoletas en futuras versiones de la biblioteca. 
    warnings.filterwarnings(
        "ignore",
        category=DeprecationWarning
    )

    #BufferWindowMemory 
    #Acá se inicializa la configuracion de la memoria para el chat general,
    #con un tamaño de ventana de 5 mensajes
    memory = ConversationBufferWindowMemory(
        k=5,
        memory_key="chat_history",
        return_messages=True
    )

    while True:
        print("\n====== MESA DE AYUDA TI UNIVERSITARIA ======")
        print("1. Ayuda Estudiantil")
        print("2. Chat General")
        print("3. Ver historial")
        print("4. Ver historial en BD")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            ayuda_estudiantil()
        elif opcion == "2":
            chat_general(memory)
        elif opcion == "3":
            ver_historial(memory)
        elif opcion == "4":
            ver_historial_bd()
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Opción inválida")

#Inicialización
crear_tablas_duoc()
insertar_datos()
print("Importaciones y configuraciones realizadas correctamente.")
print("Sistema iniciado correctamente.") 
menu()


