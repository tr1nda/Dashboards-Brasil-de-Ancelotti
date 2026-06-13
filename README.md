# ⚽ Dashboard Analytics: Seleção Brasileira (Era Ancelotti)

Este projeto é um dashboard interativo desenvolvido para analisar estatísticas de desempenho dos jogadores da Seleção Brasileira durante os jogos do ciclo de Copa do Mundo sob o comando de Carlo Ancelotti. 

## 🎯 Objetivos do Projeto
O foco principal foi aplicar conceitos de **Extração, Transformação e Carga (ETL)** e **Sports Analytics** para consolidar dados brutos de múltiplas partidas (espalhados em planilhas) e transformá-los em visualizações interativas de fácil interpretação.

## 🛠️ Tecnologias Utilizadas
* **Python** - Linguagem principal.
* **Pandas** - Limpeza, tratamento (higienização de strings) e consolidação dos dados.
* **Streamlit** - Criação da interface web e componentes interativos.
* **Plotly** - Geração de gráficos dinâmicos e de correlação.
* **Openpyxl** - Leitura e extração de dados do arquivo Excel.

## 📊 Funcionalidades
* **Consolidação Inteligente:** O script lê automaticamente múltiplas abas do arquivo Excel, corrige divergências de nomenclatura (como acentuação e nomes compostos) e agrega os números de cada atleta.
* **Destaques Gerais:** Cards com métricas rápidas mostrando os líderes em minutos jogados, gols, assistências e passes.
* **Ranking Dinâmico:** Gráficos de barras horizontais que ranqueiam os atletas com base na métrica selecionada no menu lateral.
* **Matriz de Correlação e Eficiência:** Gráficos de dispersão (Scatter Plots) para avaliar a taxa de conversão dos atletas (ex: *Passes vs Passes Certos*, *Duelos vs Duelos Ganhos*), incluindo uma linha de tendência ideal para facilitar a visualização de quem se aproxima dos 100% de aproveitamento.

## 🚀 Como executar o projeto localmente

Rode o código e dê o comando: python -m streamlit run linha.py
