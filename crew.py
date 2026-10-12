import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import (
    FileReadTool,
    DirectoryReadTool,
    FileWriterTool,
)

load_dotenv()

llm = LLM(
    model="openrouter/meta-llama/llama-3.3-70b-instruct",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.3,
    max_tokens=4000,
    timeout=90,
)

directorio_tool = DirectoryReadTool(directory='C:/QuienLoTiene')
archivo_tool = FileReadTool(base_dir='C:/QuienLoTiene')
escritor_tool = FileWriterTool()

cto_agent = Agent(
    role="CTO y Arquitecto de Software",
    goal=(
        "Disenar, escribir y mantener el codigo real del proyecto "
        "QuienLoTiene. Usar SIEMPRE las herramientas para leer archivos "
        "antes de escribir codigo nuevo. Nunca inventar contenido de "
        "archivos que no ha leido."
    ),
    backstory=(
        "Eres un CTO senior especializado en marketplaces inversos (RFQ), "
        "FastAPI y Supabase/PostgreSQL. "
        "Trabajas escribiendo codigo real en archivos reales. "
        "Reglas estrictas: "
        "1) Antes de escribir codigo, LEE los archivos existentes. "
        "2) Nunca sobrescribas el archivo .env. "
        "3) Nunca sobrescribas crew.py ni este mismo prompt. "
        "4) Documenta en el codigo lo que haces. "
        "5) Cuando escribas un archivo, di exactamente cual y donde. "
        "6) Nunca inventes tablas ni archivos que no hayas leido."
    ),
    llm=llm,
    tools=[directorio_tool, archivo_tool, escritor_tool],
    verbose=True,
    allow_delegation=False,
)

if __name__ == "__main__":
    print("\n=================================================")
    print("  Sistema de Agentes QuienLoTiene Activo")
    print("=================================================")
    print("  Herramientas cargadas:")
    print("  - DirectoryReadTool: listar archivos")
    print("  - FileReadTool: leer archivos")
    print("  - FileWriterTool: escribir archivos")
    print("=================================================")

    while True:
        user_input = input("\n Tu (CEO): ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("Cerrando sesion del CTO...")
            break

        task = Task(
            description=user_input,
            expected_output=(
                "Respuesta ejecutiva con acciones REALES sobre el proyecto. "
                "Si escribiste archivos, indica exactamente cuales. "
                "Si solo informaste, di que no se modifico nada."
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