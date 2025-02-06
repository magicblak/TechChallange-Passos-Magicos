import pandas as pd
from crewai import (
    Agent,
    Task,
    Process,
    Crew
)
from crewai_tools import SerperDevTool
import tomli
import json
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

class StudentDashboardAgents():
    def __init__(self):
        return
    
    def __get_credentials(self):
        with open(".streamlit/secrets.toml", "rb") as toml_file:
            toml_data = tomli.load(toml_file)
            json_data = json.dumps(toml_data)
            keys = json.loads(json_data)
            os.environ["OPENAI_API_KEY"] = keys['OPENAI_KEY']
            os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
    
    def __create_agent(self, role, goal, backstory, tools=[]):
        agent = Agent(
            role=role,
            goal=goal,
            verbose=False,
            memory=False,
            backstory=(
                backstory
            ),
            tools=tools,
            allow_delegation=True
        )
        return agent
    
    def __create_task(self, agent, description, expected_output, tools=[]):
        task = Task(
            description=(
                description
            ),
            expected_output=expected_output,
            tools=tools,
            agent=agent,
        )
        return task
    
    def __create_crew(self, agents=[], tasks=[]):
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            memory=True,
            cache=True,
            max_rpm=100,
            share_crew=True
        )
        return crew
    
    async def __async_kickoff(self, crew):
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            result = await loop.run_in_executor(pool, crew.kickoff)
        return result
    
    def request_analysis(self, indicators_explanation, cluster_explanation):
        self.__get_credentials()

        indicator_explorer = self.__create_agent(
            role="Explorador de Dados de Desempenho Acadêmico",
            goal="Analisar os dados individuais do aluno e fornecer uma visão clara sobre onde ele está se destacando ou apresentando dificuldades em relação à média da turma.",
            backstory="Especialista em avaliar o progresso acadêmico, adora identificar lacunas e oportunidades de crescimento por meio de dados objetivos. Focado em trazer insights precisos, mas com empatia."
        )
        cluster_explorer = self.__create_agent(
            role="Especialista em Clusterização e Padrões",
            goal="Fornecer insights sobre como o aluno se compara a outros grupos e como isso pode influenciar seu plano pedagógico.",
            backstory="Especialista em analisar clusters de aprendizagem, identificar padrões relevantes e categorizar o aluno em grupos de similaridade.Apaixonado por descobrir padrões ocultos, este profissional traduz informações técnicas em dados simples e compreensíveis para educadores."
        )
        coach = self.__create_agent(
            role="Mentor Pedagógico Individual",
            goal="Propor ações específicas de apoio e desenvolvimento pedagógico, considerando as áreas de dificuldade e pontos fortes do aluno.",
            backstory="Um orientador com experiência prática em sala de aula, preocupado com o desenvolvimento integral dos alunos. Ele traduz dados em estratégias concretas e humanas"
        )
        communicator = self.__create_agent(
            role="Comunicador Educacional",
            goal="Criar uma sintetização de informações que permita que diretores e coordenadores entendam rapidamente a situação acadêmica do aluno e saibam como agir.",
            backstory="Com forte senso de empatia, este agente acredita que o segredo de um bom plano educacional é a comunicação clara entre dados e educadores."
        )

        indicator_explorer_task = self.__create_task(
            agent=indicator_explorer,
            description="Avaliar as notas e indicadores de aprendizagem do aluno, comparando seu desempenho com a média da turma. Identificar pontos fortes e áreas de dificuldade.",
            expected_output="Relatório em texto com as seguintes informações: Desempenho do aluno na fase (com destaque para áreas de alto e baixo desempenho). Comparação percentual com a média da turma. Pontos que precisam de atenção."
        )
        cluster_explorer_task = self.__create_task(
            agent=cluster_explorer,
            description="Analisar o cluster ao qual o aluno pertence e identificar padrões de desempenho associados a esse grupo. Comparar suas características principais com outros alunos do mesmo cluster.",
            expected_output="Relatório em texto de clusterização contendo: Cluster identificado e sua descrição (por exemplo, “Alunos com dificuldades no indicador X). Padrões comuns no grupo. Diferenças específicas do aluno em relação ao cluster."
        )
        coach_task = self.__create_task(
            agent=coach,
            description="Construir um plano pedagógico individualizado com base nos dados de desempenho, evolução e clusterização. Sugerir intervenções específicas para reforçar as áreas de dificuldade e potencializar os pontos fortes.",
            expected_output="Plano de intervenção  em texto contendo: Objetivos pedagógicos claros. Estratégias de apoio específicas (por exemplo, tutoria individual, práticas colaborativas). Recursos sugeridos (ex.: materiais adicionais ou sessões de reforço). Indicadores de monitoramento do progresso."
        )
        communicator_task = self.__create_task(
            agent=communicator,
            description="Compilar todas as informações geradas pelos outros agentes e sintetizá-las em uma ficha do estudante clara, objetiva e de fácil leitura para diretores e coordenadores.",
            expected_output="Texto consolidado das informações do estudante, incluindo: Resumo geral do desempenho e evolução. Principais pontos de atenção e recomendações. Sugestão de acompanhamento pedagógico."
        )

        crew = self.__create_crew(
            agents=[indicator_explorer, cluster_explorer, coach, communicator],
            tasks=[indicator_explorer_task, cluster_explorer_task, coach_task, communicator_task]
        )

        return asyncio.run(self.__async_kickoff(crew))
