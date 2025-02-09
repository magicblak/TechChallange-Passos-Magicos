import pandas as pd
from crewai import (
    Agent,
    Task,
    Process,
    Crew
)
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
            memory=True,
            backstory=(
                backstory
            ),
            tools=tools,
            allow_delegation=True
        )
        return agent
    
    def __create_task(self, agent, description, expected_output, tools=[], context=[]):
        task = Task(
            description=(
                description
            ),
            expected_output=expected_output,
            tools=tools,
            agent=agent,
            context=context
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
            max_execution_time=50000,
            verbose=True,
            share_crew=True
        )
        return crew
    
    async def request_analysis(self, base_explain, indicators_explanation, cluster_explanation):
        self.__get_credentials()

        data_explorer = self.__create_agent(
            role="Especialista de Dados de Educacionais",
            goal="Construir análises educacionais robustas para análise de Orientadores Educacionais",
            backstory=f"""Especialista em analisar dados para construir uma visualização da 
                jornada acadêmica de estudantes do ensino básico, 
                adora identificar lacunas e oportunidades de crescimento por meio de dados. 
                Focado em trazer insights precisos, mas com empatia.
                Seu trabalho visto com excelência, pois você descomplica termos técnicos, e elabora análises de forma democrática e assecivel.
                {base_explain}"""
        )
        educational_coah = self.__create_agent(
            role=f"Orientador Educacional",
            goal=f"""Interpretar análises educacionais com o objetivo de construir a jornada do
                estudante na instituição de ensino, e buscar hipoteses para aprimoramento dos resultados
                do estudante.""",
            backstory=f"""Trabalha a 20 anos com estudantes em situação de vulnerabilidade social
                e de baixa renda, seu trabalho sempre foi reconhecido pelo seu olhar humanizado, e acompanhamento
                detalhado de estudantes, além de ser referência em elaboração de hipoteses para apoiar decisões
                da coordenação pedagógica. Além disso, é estremamente questionador e crítico quanto aos dados, adicionalmente
                é estremamente questionador e busca exelência em todo o trabalho que executa.
                {base_explain}"""
        )

        data_explorer_task = self.__create_task(
            agent=data_explorer,
            description=f"""Análisar dados do desempenho acadêmico, indicadores e comparações
                de 1 estudante e criar uma análise educacional individualizada.
                Se houver dúvidas sobre a interpretação dos dados observados, consulte o Orientador Educacional.
                Dados: {indicators_explanation}
                Após a análise, deve-se elaborar uma predição de resultados com base na
                análise de cluster, tentando entender qual o padrão de comportanmento do estudante análisado
                Cluster: {cluster_explanation}""",
            expected_output="Relatório completo abordando todos os tópicos observados para análise educacional do Orientado Pedagógico."
        )
        educational_coach_task = self.__create_task(
            agent=educational_coah,
            description=f"""Receber a análise de dados educacionais, questionando o Analista de dados educaionais
                caso haja necessidade de complemento na análise e criar um relatório completo da jornada do estudante contendo incusive hipoteses
                para melhoria de desempenho e/ou incentivo do desempenho atual""",
            expected_output="Jornada completa do estudante formatada para Markdown contendo todas os destaques positivos/negativos, além de hipoteses para aprimorar ou manter o desempenho dos estudantes. O Relatório deve estar organizado para leitura do Coordenador Pedagógico, e deve possuir 2 minutos de leitura no máximo",
            context=[data_explorer_task]
        )

        crew = self.__create_crew(
            agents=[data_explorer, educational_coah],
            tasks=[data_explorer_task, educational_coach_task]
        )

        return crew
