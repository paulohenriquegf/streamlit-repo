import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import xlrd


#@st.cache
def load_data():
    df = pd.read_excel('Arquivo_split.xlsx')
    df['latitude']=pd.to_numeric(df['latitude'])
    df['longitude']=pd.to_numeric(df['longitude']) 
    df.dropna(inplace=True, axis=0)
    return df

def load_data2():
    df2 = pd.read_csv('estamos.csv')
    df2 = df2[df2['Nome'] == 'Estamos']

    return df2

df = load_data()
df2 = load_data2()

df['Legenda'] = "Odontologia"
df2['Legenda'] = "Estamos"

combined = pd.concat([df[['Nome', 'latitude', 'longitude', 'uf','municipio','Legenda', 'Telefone']], df2], ignore_index=False, axis=0)


# SIDEBAR
# Parâmetros e número de ocorrências
st.sidebar.header("Parâmetros")
info_sidebar = st.sidebar.empty()    # placeholder, para informações filtradas que só serão carregadas depois


# Checkbox da Tabela
st.sidebar.subheader("Tabela")
tabela = st.sidebar.empty()    # placeholder que só vai ser carregado com o df_filtered

# Multiselect com os lables únicos dos tipos de classificação
label_to_filter = st.sidebar.multiselect(
    label= "Escolha a UF desejada",
    options= combined['uf'].unique().tolist(),
    default= combined.uf.unique().tolist()
)

# Somente aqui os dados filtrados são atualizados em novo dataframe
filtered_df = combined[(combined.uf.isin(label_to_filter))]

# Multiselect com os lables únicos dos tipos de classificação
label_to_filter2 = st.sidebar.multiselect(
    label="Escolha o Municipio desejado",
    options=filtered_df['municipio'].unique().tolist(),
    default= filtered_df['municipio'].unique().tolist()
)

filtered_df2 = filtered_df[(filtered_df.uf.isin(label_to_filter))& (filtered_df.municipio.isin(label_to_filter2))]

#filtrando dataset pelo filtro municipio
#filtered_df2 = filtered_df[(filtered_df.municipio.isin(label_to_filter2))]

# Informação no rodapé da Sidebar
st.sidebar.markdown("""
Base de dados com região e telefone de ***Dentistas***.
""")

# Aqui o placehoder vazio finalmente é atualizado com dados do filtered_df
info_sidebar.info("{} ocorrências selecionadas.".format(filtered_df2.shape[0]))


# MAIN
st.title("Rede de Dentistas")
st.markdown(f"""
            ℹ️ Estão sendo exibidas as ocorrências classificadas como **{", ".join(label_to_filter)}**
            """)

# raw data (tabela) dependente do checkbox
if tabela.checkbox("Mostrar tabela de dados"):
    st.write(filtered_df2[['Nome','Telefone','municipio','uf']])


# mapa
try:
    fig2 = px.scatter_mapbox(filtered_df2, lat="latitude", lon="longitude", 
                            hover_name="Telefone",
                            hover_data= ["Nome"],
                            color='Legenda',
                            #labels=['Telefone'],
                            color_discrete_sequence=px.colors.qualitative.G10,
                            zoom=3, height=500, width=800)              
    fig2.update_layout(mapbox_style="carto-positron")
    fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig2.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0.01
    ))

    #fig2.write_html('MAPA.html')
    st.write(fig2)
except:
    pass
