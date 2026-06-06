#  Mesa de Ayuda TI Universitaria
Que ofrece soporte TI a estudiantes, docentes y personal administrativo. El área de mesa de ayuda atiende 
solicitudes relacionadas con acceso a cuentas, uso de plataformas educativas, problemas de conectividad y 
soporte general de sistemas.  


--Datos disponibles o que se pueden obtener--
    -Tickets históricos de soporte TI.  

--Restricciones o requerimientos particulares--
-El sistema implementa memoria de corto plazo mediante
ConversationBufferWindowMemory y persistencia de consultas
mediante SQLite. Sin embargo, no mantiene perfiles
individuales por usuario ni personaliza respuestas entre sesiones.


# Explicación para ejecutar este sistema
1.- Clonar el repositorio en la terminal:
``bash
git clone 

2.- En la terminal de Bash, entrar al directorio del proyecto:
``bash
cd Evaluaci-n2_Ing._de_soluciones_con_inteligencia_artificial

3.- Para que el código funcione sin problemas, es necesario instalar unas dependencias:
``bash
pip install -r requirements.txt
pip install openai

4.- Crear un archivo .env en la raíz del proyecto:

GITHUB_TOKEN=tu_token_aqui

5.- Ejecutar el sistema:

python Mesa_TIOriginal.py


# Explicación del código
El sistema presenta un menú principal con opciones de soporte TI:
-Ayuda estudiantil
-Chat general
-Ver historial
-Ver historial en BD
-Salir


Cada opción da un contexto específico a la IA para responder de forma adecuada.

El usuario puede elegir entre 3 estilos de respuesta de la IA:
Zero-shot > respuesta directa y breve.
Few-shot > respuesta guiada con ejemplos.
Chain-of-Thought > explicación paso a paso con recomendaciones finales.

--Implementación de base de datos local--
El sistema incluye una base de datos SQLite (duoc.db) con información de carreras y profesores. Si el usuario pregunta por profesores de una carrera:
    -Si la carrera existe se muestran los profesores y la IA complementa la respuesta.
    -Si la carrera no existe se informa y se listan las carreras disponibles.

# Frameworks utilizados
--LangChain:
  Utilizado para implementar memoria conversacional
  mediante ConversationBufferWindowMemory.

--OpenAI SDK:
  Utilizado para la comunicación con el modelo GPT-4o.

--SQLite:
  Utilizado para almacenamiento persistente de datos
  académicos e historial de consultas.

# Gestión de Memoria

El sistema utiliza ConversationBufferWindowMemory de
LangChain para mantener las últimas interacciones del usuario
durante una sesión.

Además, cada consulta es almacenada en SQLite,
permitiendo mantener un historial persistente de conversaciones.

# Arquitectura de Orquestación
El sistema incorpora un orquestador encargado de analizar
la consulta del usuario y decidir qué herramienta ejecutar.

Herramientas disponibles:

--FAQ
--Buscar carrera
--Buscar profesor
--Planificador de tareas
--Consulta mediante GPT-4o

Dependiendo de la intención detectada, el agente selecciona
automáticamente la herramienta más adecuada.

# Diagrama

Usuario
   |
   V
Orquestador
   |
   +---- FAQ
   |
   +---- Buscar Profesor u carrera
   |
   |
   +---- Planificador
   |
   +---- GPT
   |
   V
SQLite

# Planificación de tareas

El agente incorpora un planificador simple que divide
consultas complejas en múltiples pasos.

Ejemplo:

Usuario:
"Necesito información de Ingeniería en Informática y sus profesores"

Plan generado:

1. Buscar carrera.
2. Buscar profesores asociados.
3. Construir respuesta.
4. Entregar resultado al usuario.

# Problemática
La problemática que se busca resolver es facilitar las consultas de soporte TI y académicas para estudiantes y personal universitario.
Con este sistema, los usuarios pueden acceder rápidamente a información de carreras, profesores y soporte técnico, optimizando procesos y mejorando la experiencia de atención gracias al ChatBOT.

--Motivación para el uso de agentes de IA y LLMs--
El sistema utiliza un modelo LLM para generar respuestas
y un conjunto de herramientas conectadas a una base de
datos SQLite para recuperar información académica.
La combinación de recuperación de datos y generación
de lenguaje permite entregar respuestas contextualizadas.

--Referencias o anexos relevantes--
    --[GitHub Models Documentation](https://docs.github.com/en/github-models)
    --[GitHub de la asignatura](https://github.com/davila7/Ingenier-a-de-Soluciones-con-Inteligencia-Artificial.git)

    LangChain. (2025). LangChain Documentation.
    https://python.langchain.com/

    OpenAI. (2025). OpenAI API Documentation.
    https://platform.openai.com/docs

    SQLite. (2025). SQLite Documentation.
    https://www.sqlite.org/docs.html



