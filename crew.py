import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import (
    FileReadTool,
    DirectoryReadTool,
    FileWriterTool,
)
from tools import herramientas_otc

# Cargar variables del entorno (.env)
load_dotenv()

# Configurar OpenRouter con modelo estable
llm = LLM(
    model="openrouter/meta-llama/llama-3.3-70b-instruct",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.3,
    max_tokens=4000,
    timeout=90,
)

# ============================================================
# HERRAMIENTAS DEL AGENTE
# ============================================================

# Herramientas de archivos
directorio_tool = DirectoryReadTool(directory='C:/QuienLoTiene')
archivo_tool = FileReadTool(base_dir='C:/QuienLoTiene')
escritor_tool = FileWriterTool()

# Lista completa: archivos + herramientas_otc (Supabase + web + email)
todas_las_herramientas = [
    directorio_tool,
    archivo_tool,
    escritor_tool,
    *herramientas_otc,
]

# ============================================================
# AGENTE CTO
# ============================================================

cto_agent = Agent(
    role="CTO y Asistente Ejecutivo de QuienLoTiene",
    goal=(
        "Supervisar el desarrollo de QuienLoTiene, analizar la base de datos, "
        "enviar comunicaciones a usuarios cuando se solicite, "
        "investigar en internet cuando sea necesario. "
        "Usa SIEMPRE las herramientas disponibles antes de responder."
    ),
    backstory=(
        "Eres un CTO senior especializado en marketplaces inversos (RFQ), "
        "FastAPI y Supabase/PostgreSQL. Tambien actúas como asistente ejecutivo "
        "del fundador. Trabajas con datos REALES, no inventas. "
        "\n\nHERRAMIENTAS DISPONIBLES:"
        "\n- DirectoryReadTool: listar archivos del proyecto"
        "\n- FileReadTool: leer contenido de archivos"
        "\n- FileWriterTool: escribir/actualizar archivos"
        "\n- listar_tablas: ver que tablas existen en Supabase"
        "\n- consultar_tabla: leer filas de una tabla (SOLO LECTURA)"
        "\n- contar_filas: contar registros de una tabla"
        "\n- buscar_web: buscar informacion en internet (gratis)"
        "\n- enviar_email: enviar correos a usuarios via Resend"
        "\n\nREGLAS ESTRICTAS:"
        "\n1) Antes de escribir codigo, LEE los archivos existentes con FileReadTool"
        "\n2) Antes de hablar de datos, CONSULTA las tablas con consultar_tabla"
        "\n3) Antes de enviar un email, CONFIRMA con el usuario el destinatario y contenido"
        "\n4) Nunca sobrescribas el archivo .env ni crew.py"
        "\n5) Nunca modifiques datos de Supabase (solo lectura por ahora)"
        "\n6) Cuando escribas un archivo, di exactamente cual y donde"
        "\n7) Nunca inventes datos ni tablas que no hayas verificado"
        "\n8) Si no sabes algo, admítelo o buscalo en la web"
        "\n9) Para correos: usa HTML simple y bonito, no texto plano"
    ),
    llm=llm,
    tools=todas_las_herramientas,
    verbose=True,
    allow_delegation=False,
)

# ============================================================
# EJECUCION PRINCIPAL
# ============================================================

if __name__ == "__main__":
    print("\n=================================================")
    print("  Sistema de Agentes QuienLoTiene Activo")
    print("=================================================")
    print(f"  Herramientas cargadas: {len(todas_las_herramientas)}")
    print("  - 3 de archivos (leer/escribir/listar)")
    print("  - 3 de Supabase (solo lectura)")
    print("  - 1 de busqueda web")
    print("  - 1 de envio de correos")
    print("=================================================")

    while True:
        user_input = input("\n Tu (CEO): ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("Cerrando sesion del CTO...")
            break

        task = Task(
            description=user_input,
            expected_output=(
                "Respuesta ejecutiva basada en informacion REAL. "
                "Si usaste herramientas, indica cuales. "
                "Si no pudiste hacer algo, dilo claramente."
            ),
            agent=cto_agent,
        )

        crew = Crew(
            agents=[cto_agent],
            tasks=[task],
            process=Process.sequential,
        )

        resultado = crew.kickoff()
        print(f"\n CTO: \n{resultado}")