import streamlit as st
import json
import random
import os
import pandas as pd

# Função para carregar dados de um arquivo JSON
def carregar_json(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)

# Função para salvar dados em um arquivo JSON
def salvar_json(caminho, dados):
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# Função para gerar sorteio aleatório
def gerar_sorteio(times):
    dias_da_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
    sorteio = {}
    
    for time in times:
        pessoas = time['pessoas']
        sorteio[time['nome']] = []
        
        # Embaralhar os dias para cada pessoa
        dias_sorteados = random.choices(dias_da_semana, k=len(pessoas))
        
        for pessoa, dia in zip(pessoas, dias_sorteados):
            sorteio[time['nome']].append({"nome": pessoa, "dia": dia})

    return sorteio

# Função para exibir tabelas
def exibir_tabelas(sorteio):
    for time, pessoas in sorteio.items():
        st.subheader(time)
        tabela = pd.DataFrame(pessoas)  # Cria DataFrame a partir dos dados
        st.dataframe(tabela[['nome', 'dia']], use_container_width=True)  # Exibe DataFrame sem índice

# Caminhos dos arquivos JSON
caminho_times = 'times.json'
caminho_sorteio = 'sorteio.json'

# Carregar dados do arquivo times.json
times = carregar_json(caminho_times)['times']

# Iniciar a aplicação Streamlit
st.title("Programação Semanal")

# Botão para realizar o sorteio
if st.button("SORTEIO"):
    sorteio = gerar_sorteio(times)
    salvar_json(caminho_sorteio, sorteio)
    st.success("Sorteio realizado e salvo em sorteio.json!")

# Verificar se o arquivo sorteio.json existe para exibir tabelas
if os.path.exists(caminho_sorteio):
    sorteio = carregar_json(caminho_sorteio)
    exibir_tabelas(sorteio)
else:
    st.write("Clique no botão 'SORTEIO' para gerar o sorteio.")
