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

class StudentDashboardAgents():
    def __init__(self):
        return
    
    def __get_credentials(self):
        with open(".streamlit/secrets.toml", "rb") as toml_file:
            toml_data = tomli.load(toml_file)
            json_data = json.dumps(toml_data)
            keys = json.loads(json_data)
            os.environ["OPENAI_API_KEY"] = keys['OPENAI_KEY']
            os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o-mini'
    
    def __create_agent(self, role, goal, backstory, tools=[]):
        agent = Agent(
            role=role,
            goal=goal,
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
            max_rpm=50,
            max_execution_time=5000,
            verbose=True,
            share_crew=True
        )
        return crew
    
    def request_analysis(self, base_explain, indicators_explanation, cluster_explanation):
        self.__get_credentials()

        indicator_explorer = self.__create_agent(
            role="Especialista de Dados de Desempenho Acadêmico",
            goal="Observar e analisar os dados de desempenho acadêmico, buscando nuances que podem ser importantes na captura de comportamento do aluno",
            backstory=f"""Especialista em avaliar a jornada acadêmica no ensino básico, adora identificar lacunas e oportunidades de crescimento por meio de dados objetivos. 
                Focado em trazer insights precisos, mas com empatia.
                Trabalha em uma ong que possui algumas informações importantes: {base_explain}"""
        )
        cluster_explorer = self.__create_agent(
            role="Especialista em Clusterização e Padrões",
            goal="Fornecer insights sobre como o comportamento do grupo onde o aluno se encontra e qual relação existe com os demais grupos, seja relação de igualdade ou divergência",
            backstory=f"""Especialista em predição e análise de padrões/comportamento, adora identificar lacunas e oportunidades de crescimento por meio de dados objetivos. 
                Focado em trazer insights precisos, mas com empatia.
                Trabalha em uma ong que possui algumas informações importantes: {base_explain}"""
        )
        coach = self.__create_agent(
            role="Mentor Pedagógico Individual",
            goal="Propor ações específicas de apoio e desenvolvimento pedagógico, considerando as áreas de dificuldade e pontos fortes do aluno.",
            backstory=f"""Um orientador com experiência prática em sala de aula, preocupado com o desenvolvimento integral dos alunos na ONG. Ele traduz dados em história
                para que educadores possam avaliar e tomar ações
                Trabalha em uma ong que possui algumas informações importantes: {base_explain}"""
        )

        indicator_explorer_task = self.__create_task(
            agent=indicator_explorer,
            description="Avaliar as notas e indicadores de aprendizagem do aluno e/ou comparando seu desempenho com a média da turma. Identificar pontos fortes e áreas de dificuldade." + indicators_explanation,
            expected_output="Relatório em texto apresentando evidências de lacunas e potenciais do estudante, incluindo análises longitudinais e comparativas, observando não só os indicadores, como também as notas de discplina do aluno (inglês, português e matemática)."
        )
        cluster_explorer_task = self.__create_task(
            agent=cluster_explorer,
            description="Analisar o cluster ao qual o aluno pertence e identificar padrões de desempenho associados a esse grupo. Comparar suas características principais com outros alunos do mesmo cluster. E quais principais caracteristicas do melhor clustes em desempenho acadêmico." + cluster_explanation,
            expected_output="Relatório em texto da análise de cluster, contendo padrões identificados e possibilidades de previsão futura, com a comparação de alunos que já passaram pela mesma fase."
        )
        coach_task = self.__create_task(
            agent=coach,
            description="""Construir um storytelling do aluno por meio de informações do time de dados, e consolidar todas as análises em linguagem educacional seja de clusterização ou idicadores de desempenho acadêmico""" + base_explain,
            expected_output="Texto em português brasileiro formato de storytelling, com o público alvo coordenadores e diretores de uma escola de ensino básico, para contar a história existente do aluno presente nos numeros, e plano de ação considerando a consolidação das análises em linguagem educacional, contendo: o futura análisado na clusterização e o presente e passado análisado nos inidicadores para potencializar e/ou auxiliar o launo"
        )

        crew = self.__create_crew(
            agents=[indicator_explorer, cluster_explorer, coach],
            tasks=[indicator_explorer_task, cluster_explorer_task, coach_task]
        )

        return crew.kickoff()
