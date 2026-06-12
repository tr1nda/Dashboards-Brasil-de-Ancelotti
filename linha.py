import streamlit as st
import pandas as pd
import plotly.express as px
import glob
import os

# 1. Configuração inicial da página (deve ser o primeiro comando Streamlit)
st.set_page_config(
    page_title="Dashboard Seleção Brasileira",
    page_icon="⚽",
    layout="wide"
)

# 2. Função para carregar e tratar os dados
# === INÍCIO DA CORREÇÃO DE NOMES ===
# O @st.cache_data faz com que o app não precise ler os CSVs toda vez que você clica em um botão
@st.cache_data
def carregar_dados():
    arquivo_excel = 'ERA ANCELOTTI - LINHA.xlsx'
    
    if not os.path.exists(arquivo_excel):
        st.error(f"Arquivo não encontrado: {arquivo_excel}")
        return pd.DataFrame()
        
    try:
        # Lê todas as abas
        todas_as_abas = pd.read_excel(arquivo_excel, sheet_name=None)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo Excel: {e}")
        return pd.DataFrame()
        
    dfs = []
    for nome_aba, df_aba in todas_as_abas.items():
        # LIMPEZA: Remove espaços em branco antes/depois e deixa tudo maiúsculo
        df_aba.columns = df_aba.columns.astype(str).str.strip().str.upper()
        
        # Agora a verificação fica à prova de erros de digitação na planilha
        if 'JOGADORES' in df_aba.columns:
            dfs.append(df_aba)

    # TRAVA DE SEGURANÇA: Se ainda assim ficar vazio, avisa na tela e para por aqui
    if len(dfs) == 0:
        st.warning("Nenhum dado válido encontrado. Verifique se o cabeçalho 'JOGADORES' está na primeira linha da planilha.")
        return pd.DataFrame()

    # Junta todos os dados das abas
    df_total = pd.concat(dfs, ignore_index=True)

    # Colunas que serão somadas
   # Atualize esta linha dentro de carregar_dados()
    cols_to_sum = ['GOLS', 'ASSISTENCIAS', 'MINUTOS EM CAMPO', 'FINALIZAÇÕES', 
                   'PASSES', 'PASSES CERTOS', 'CRUZAMENTOS', 'CRUZAMENTOS CERTOS',
                   'PERDAS DE POSSE', 'RECUPERAÇÕES DE BOLA', 'DESARMES', 
                   'DUELOS', 'DUELOS GANHOS']
    
    # Garantir que as colunas são numéricas e limpar caracteres estranhos
    for col in cols_to_sum:
        if col in df_total.columns:
            df_total[col] = pd.to_numeric(df_total[col], errors='coerce').fillna(0)

# === INÍCIO DA CORREÇÃO DE NOMES ===
    dicionario_correcao = {
        'Estêvão': 'Estevão',
        'Vinícius Júnior': 'Vinicius Junior'
    }
    
    # Aplica a correção na coluna JOGADORES
    df_total['JOGADORES'] = df_total['JOGADORES'].replace(dicionario_correcao)
    # === FIM DA CORREÇÃO DE NOMES ===

    # Agrupar por jogador e somar as estatísticas
    df_agrupado = df_total.groupby('JOGADORES')[cols_to_sum].sum().reset_index()
    
    return df_agrupado

# Carregar os dados
df = carregar_dados()

# 3. Interface do Dashboard
if df.empty:
    st.error("Nenhum dado encontrado. Certifique-se de que os arquivos .csv estão na mesma pasta que este script.")
else:
    # Cabeçalho
    st.title("⚽ Dashboard: Seleção Brasileira - Era Ancelotti")
    st.markdown("""
    Este dashboard interativo analisa o desempenho individual dos jogadores da Seleção Brasileira 
    durante o ciclo preparatório para a Copa do mundo sob o comando de Carlo Ancelotti.\n 
    *Dados retirados do aplicativo sofaScore*\n
    *Desenvolvido com Python, Pandas e Streamlit.*
    """)
    st.divider()

    # 4. Barra Lateral (Sidebar) para Filtros
    st.sidebar.header("⚙️ Configurações e Filtros")
    
    metrica_selecionada = st.sidebar.selectbox(
        "Selecione a métrica de destaque:",
        ['MINUTOS EM CAMPO', 'GOLS', 'ASSISTENCIAS', 'FINALIZAÇÕES', 
         'PASSES', 'PASSES CERTOS', 'CRUZAMENTOS', 'CRUZAMENTOS CERTOS',
         'DESARMES', 'RECUPERAÇÕES DE BOLA', 'PERDAS DE POSSE']
    )

    minutos_minimos = st.sidebar.slider(
        "Filtrar por Minutos Mínimos em Campo:",
        min_value=0, 
        max_value=int(df['MINUTOS EM CAMPO'].max()), 
        value=100
    )

    top_n = st.sidebar.number_input("Mostrar Top N jogadores no gráfico:", min_value=5, max_value=30, value=15)

    # Aplica o filtro de minutos
    df_filtrado = df[df['MINUTOS EM CAMPO'] >= minutos_minimos]

    # 5. Organização da tela em colunas para os "Cards" (Métricas rápidas)
    st.subheader("📌 Destaques Gerais")
    col1, col2, col3, col4 = st.columns(4)
    
    # Encontrar os líderes
    lider_minutos = df_filtrado.loc[df_filtrado['MINUTOS EM CAMPO'].idxmax()]
    lider_gols = df_filtrado.loc[df_filtrado['GOLS'].idxmax()]
    lider_assist = df_filtrado.loc[df_filtrado['ASSISTENCIAS'].idxmax()]
    lider_passes = df_filtrado.loc[df_filtrado['PASSES'].idxmax()]

    col1.metric("Mais Minutos", f"{lider_minutos['JOGADORES']}", f"{int(lider_minutos['MINUTOS EM CAMPO'])} min")
    col2.metric("Artilheiro", f"{lider_gols['JOGADORES']}", f"{int(lider_gols['GOLS'])} Gols")
    col3.metric("Garçom", f"{lider_assist['JOGADORES']}", f"{int(lider_assist['ASSISTENCIAS'])} Asts")
    col4.metric("Maior passador", f"{lider_passes['JOGADORES']}", f"{int(lider_passes['PASSES'])} Passes")

    st.divider()

    # 6. Gráfico Principal (Barras Horizontais)
    st.subheader(f"📊 Ranking: Top {top_n} por {metrica_selecionada}")
    
    df_top = df_filtrado.sort_values(by=metrica_selecionada, ascending=False).head(top_n)
    
    fig_bar = px.bar(
        df_top, 
        x=metrica_selecionada, 
        y='JOGADORES', 
        orientation='h',
        text=metrica_selecionada,
        color=metrica_selecionada,
        color_continuous_scale='Viridis'
    )
    # Ordenar o gráfico do maior pro menor de cima para baixo
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
    
    st.plotly_chart(fig_bar, use_container_width=True)

   # 7. Gráfico de Dispersão (Correlação e Eficiência)
    st.subheader("🎯 Correlação e Eficiência")
    st.markdown("Analise a taxa de conversão e eficiência dos jogadores. Bolhas maiores indicam mais minutos em campo.")
    
    # Dicionário com os atalhos que você pediu
    correlacoes = {
        "Duelos: Totais x Ganhos": ("DUELOS", "DUELOS GANHOS"),
        "Posse: Perdas x Recuperações": ("PERDAS DE POSSE", "RECUPERAÇÕES DE BOLA"),
        "Passes: Totais x Certos": ("PASSES", "PASSES CERTOS"),
        "Cruzamentos: Totais x Certos": ("CRUZAMENTOS", "CRUZAMENTOS CERTOS"),
        "Ataque: Finalizações x Gols": ("FINALIZAÇÕES", "GOLS"),
        "Livre (Escolha Manual)": ("LIVRE", "LIVRE")
    }

    # Menu de atalhos
    tipo_analise = st.selectbox("Selecione a análise de eficiência:", list(correlacoes.keys()))

    # Lista de todas as colunas para o modo manual
    todas_metricas = ['GOLS', 'ASSISTENCIAS', 'FINALIZAÇÕES', 'PASSES', 'PASSES CERTOS', 
                      'CRUZAMENTOS', 'CRUZAMENTOS CERTOS', 'PERDAS DE POSSE', 
                      'RECUPERAÇÕES DE BOLA', 'DESARMES', 'DUELOS', 'DUELOS GANHOS']

    # Lógica para definir X e Y
    if tipo_analise == "Livre (Escolha Manual)":
        c1, c2 = st.columns(2)
        with c1:
            eixo_x = st.selectbox("Eixo X (Horizontal):", todas_metricas, index=todas_metricas.index('PASSES'))
        with c2:
            eixo_y = st.selectbox("Eixo Y (Vertical):", todas_metricas, index=todas_metricas.index('PASSES CERTOS'))
    else:
        # Pega as colunas automaticamente com base na escolha do usuário
        eixo_x = correlacoes[tipo_analise][0]
        eixo_y = correlacoes[tipo_analise][1]

    # Criação do gráfico
    fig_scatter = px.scatter(
        df_filtrado,
        x=eixo_x,
        y=eixo_y,
        size='MINUTOS EM CAMPO',
        color='JOGADORES',
        hover_name='JOGADORES',
        text='JOGADORES',
        labels={eixo_x: eixo_x, eixo_y: eixo_y} # Melhora os nomes nos eixos
    )
    
    fig_scatter.update_traces(textposition='top center')
    fig_scatter.update_layout(showlegend=False, height=600) # Deixei o gráfico um pouco mais alto para os nomes não se sobreporem tanto
    
    # Adicionando uma linha de tendência ideal (opcional, deixa o gráfico mais rico)
    # Se X for igual a Y (100% de acerto), a linha mostra quem está mais próximo da perfeição
    if tipo_analise != "Livre (Escolha Manual)" and tipo_analise != "Posse: Perdas x Recuperações":
         fig_scatter.add_shape(
            type="line", line=dict(dash="dash", color="gray", width=1),
            x0=0, y0=0, x1=df_filtrado[eixo_x].max(), y1=df_filtrado[eixo_x].max()
         )

    st.plotly_chart(fig_scatter, use_container_width=True)

    # 8. Visualização dos Dados Brutos
    st.subheader("📋 Base de Dados Consolidada")
    with st.expander("Clique para visualizar ou baixar os dados da tabela"):
        st.dataframe(df_filtrado.sort_values(by='MINUTOS EM CAMPO', ascending=False), use_container_width=True)