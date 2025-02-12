import streamlit as st
from utils.functions import (
    create_title, 
    create_about_member
)

create_title("Sobre a equipe")
create_about_member('Carlos Santos', 'carlos', '', 'Engenheiro Civil, atuando em gestão de projetos de construção, considera a análise de dados uma ferramenta valiosa para agregar valor ao trabalho,  obter melhores resultados e maior vantagem competitiva.')
create_about_member('Fabia Bocayuva', 'fabia', '', '')
create_about_member('Lucas Santos Mathias', 'lucas', 'http://www.linkedin.com/in/lucas-santos-mathias-990a54173', 'Atua com análise de dados educacionais há mais de 5 anos e acredita que para uma gestão educacional transformadora os dados são fundamentais.')
