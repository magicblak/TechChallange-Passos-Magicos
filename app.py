import streamlit as st
import json
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


# Leitura de itens do menu
file_path = 'menu.json'
with open(file_path, 'r', encoding='utf-8') as file:
    menu_pages = json.load(file)

# Criação dos itens do menu
menu = []
pages_folder = 'views/'
icons_folder = ':material/'
for key, menu_page in menu_pages.items():
    menu.append(
        st.Page(
            pages_folder + menu_page['file'],
            title=menu_page['title'],
            icon=icons_folder + menu_page['icon'],
            default=bool(menu_page['default'])
        )
    )
pg = st.navigation(
    {
        "Inicio": [menu[0]],
        "Menu": menu[1:],
    }
)

# Itens estáticos
st.logo("assets/logo.png")
st.sidebar.markdown("Acesse o código no [Github](https://github.com/magicblak/TechChallange-Passos-Magicos)")

pg.run()
