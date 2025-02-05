import streamlit as st
from utils.function import create_title, create_section_title


create_title("Passos Mágicos")

create_section_title("Disclaimer")
st.write("""
Este trabalho é de caráter exclusivamente acadêmico, elaborado no contexto de uma atividade sob a metodologia de Aprendizagem Baseada em Problemas (PBL).

As informações, análises e conclusões apresentadas têm como único propósito o aprendizado e desenvolvimento dos participantes e não devem ser utilizadas para outros fins.
""")

create_section_title("Dados são histórias")
st.write("""
O dashboard foi desenvolvido com o propósito de traduzir dados em histórias de apoio ao acompanhamento individualizado dos(as) estudantes, permitindo que docentes, diretores e psicólogos compreendam suas trajetórias de forma mais humana e empática.

Nossa proposta com o painel é potencializar a visão dos educadores, proporcionando um acompanhamento personalizado e sensível às necessidades e particularidades de cada estudante.

A plataforma oferece:

- **Clusterização:** Identifica padrões e classifica os(as) estudantes, com base nos principais indicadores. A partir dessa classificação, é possível prever potenciais trajetórias e resultados futuros. Essa análise permite uma atuação preventiva e estratégica, seja para destacar talentos e oportunidades de crescimento ou para oferecer apoio direcionado às necessidades específicas.

- **Análises Descritivas (Transversal e Longitudinal):** Apresenta uma visão clara do perfil atual do(a) estudante (análise transversal) e de sua evolução ao longo do tempo (análise longitudinal), facilitando a compreensão de seu desenvolvimento escolar, social e emocional.

- **Integração com IAGen:** Gera narrativas personalizadas que contam a história do(a) estudante e sugerem intervenções.

Ao final, nosso compromisso é garantir que cada estudante seja visto(a) como um(a) indivíduo com histórias, desafios e conquistas únicas. O painel é uma ponte para um olhar mais cuidadoso e atento, promovendo intervenções assertivas e transformadoras.
""")

create_section_title("Educação baseada em evidências")
st.write("""
Falar e referenciar artigos sobre a gestão da aprendizagem com dados.
""")

create_section_title("Concepção e estratégia")
st.write("""
Porque decidimos usar cluster, e as análises?? Quais estratégias que abordamos?
""")