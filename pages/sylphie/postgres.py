import pandas as pd
import streamlit as st
import pandasql

def post_page():
    st.write("Transação")
    exec = st.button("Executar transformação CSV SAP para CSV.")
    arquivo = "planilhas\jobs\zmm209 grandona.csv"
    headers = [
        'CodRebaixa',
        'Material',
        'Loja',
        'Grupo',
        "DataFim",
        'UsoLivre',
        'Valor1',
        'Valor2',
        'Montante',
        'Montante.1'
    ]
    if exec:
        file = pd.read_csv(filepath_or_buffer=arquivo, sep="\s+", encoding="utf-16", skiprows=3)
        file_208 = pd.read_excel(io='planilhas\jobs\REBAIXAS - 208.XLSX')
        file_estoque = pd.read_csv(filepath_or_buffer='planilhas/jobs/estoque dia 09.csv')
        
        df_209 = pd.DataFrame(data=file)
        df_209.columns = headers
        df_209['CodRebaixa'] = df_209['CodRebaixa'].astype(str)
        df_209['Material'] = df_209['Material'].astype(str)
        df_209['Loja'] = df_209['Loja'].astype(str)
        df_208 = pd.DataFrame(data=file_208)
        numeros_rebaixa = df_209['CodRebaixa'].unique()
        estoque_df = pd.DataFrame(data=file_estoque)
        estoque_df['cod_produto'] = estoque_df['cod_produto'].astype(str)
        estoque_df['cod_loja'] = estoque_df['cod_loja'].astype(str)

        novo = pandasql.sqldf("""
                              SELECT 
ZMM209.CodRebaixa, 
ZMM209.Material, 
ZMM209.Loja, 
ZMM209.Grupo, 
ZMM209.DataFim,
ZMM209.UsoLivre, 
ZMM209.Valor1,
estoque_df.cod_loja,
estoque_df.cod_produto,
estoque_df.quantidade

FROM df_209 as ZMM209
LEFT JOIN estoque_df
ON TRIM(ZMM209.Loja) = TRIM(estoque_df.cod_loja)
AND TRIM(ZMM209.Material) = TRIM(estoque_df.cod_produto)

                              """)


        # est_zero = pandasql.sqldf('SELECT * FROM novo WHERE quantidade = 0')
        est_null = pandasql.sqldf('SELECT * FROM novo WHERE quantidade IS NULL')
        est_sim = pandasql.sqldf('SELECT * FROM novo WHERE quantidade <> 0')
        # est_zero.to_excel("planilhas/jobs/estoque-zerado.xlsx")
        est_null.to_excel("planilhas/jobs/estoque-nulo.xlsx")
        est_sim.to_excel("planilhas/jobs/estoque-sim.xlsx")

        df_numeros_rebaixa = pd.DataFrame(numeros_rebaixa, columns=['CodRebaixa'])
        # df_numeros_rebaixa.to_csv('planilhas/jobs/numeros_rebaixa.csv', index=False)
        st.dataframe(df_209.head(10000))
        # st.dataframe(novo)
        st.dataframe(df_208)
        st.dataframe(numeros_rebaixa)
        st.dataframe(estoque_df)
        st.success("Transformação concluída com sucesso!")