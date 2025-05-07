import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

    # Dados fornecidos
def gerentes():
    data = {
        "REGIONAL": [
            "DANIELE", "DANIELE", "DANIELE", "DANIELE", "DANIELE", "DANIELE", "DANIELE",
            "DANIELE", "DANIELE", "DANIELE", "DANIELE", "DANIELE", "DANIELE", "DANIELE",
            "DANIELE", "DANIELE", "DANIELE", "DANIELE", "DANIELE", "DRAGÕES", "DRAGÕES",
            "DRAGÕES", "DRAGÕES", "DRAGÕES", "DRAGÕES", "DRAGÕES", "DRAGÕES", "DRAGÕES",
            "DRAGÕES", "DRAGÕES", "DRAGÕES", "DRAGÕES", "EDUARDO", "EDUARDO", "EDUARDO",
            "EDUARDO", "EDUARDO", "EDUARDO", "EDUARDO", "EDUARDO", "EDUARDO", "EDUARDO",
            "EDUARDO", "EDUARDO", "FÊNIX", "FÊNIX", "FÊNIX", "FÊNIX", "FÊNIX", "FÊNIX",
            "FÊNIX", "FÊNIX", "FÊNIX", "FÊNIX", "FÊNIX", "FÊNIX", "FÊNIX", "GUSTAVO",
            "GUSTAVO", "GUSTAVO", "GUSTAVO", "GUSTAVO", "GUSTAVO", "GUSTAVO", "GUSTAVO",
            "GUSTAVO", "GUSTAVO", "GUSTAVO", "GUSTAVO", "GUSTAVO", "GUSTAVO", "GUSTAVO",
            "GUSTAVO", "JUCILENE", "JUCILENE", "JUCILENE", "JUCILENE", "JUCILENE",
            "JUCILENE", "JUCILENE", "JUCILENE", "JUCILENE", "JUCILENE", "JUCILENE",
            "JUCILENE", "JUCILENE", "JUCILENE", "JUCILENE", "JUCILENE", "JUCILENE",
            "JULY", "JULY", "JULY", "JULY", "JULY", "JULY", "JULY", "JULY", "JULY", "JULY",
            "JULY", "JULY", "JULY", "JULY", "JULY", "JULY", "JULY", "LUIZ ALEXANDRE",
            "LUIZ ALEXANDRE", "LUIZ ALEXANDRE", "LUIZ ALEXANDRE", "LUIZ ALEXANDRE",
            "LUIZ ALEXANDRE", "LUIZ ALEXANDRE", "LUIZ ALEXANDRE", "LUIZ ALEXANDRE",
            "LUIZ ALEXANDRE", "LUIZ ALEXANDRE", "LUIZ ALEXANDRE", "LUIZ ALEXANDRE",
            "REGINALDO", "REGINALDO", "REGINALDO", "REGINALDO", "REGINALDO", "REGINALDO",
            "REGINALDO", "REGINALDO", "REGINALDO", "REGINALDO", "REGINALDO", "REGINALDO",
            "REGINALDO", "REGINALDO", "REGINALDO", "RODRIGO", "RODRIGO", "RODRIGO",
            "RODRIGO", "RODRIGO", "RODRIGO", "RODRIGO", "RODRIGO", "RODRIGO", "RODRIGO",
            "RODRIGO", "RODRIGO", "RODRIGO", "RODRIGO", "RODRIGO", "RODRIGO", "SAMUEL",
            "SAMUEL", "SAMUEL", "SAMUEL", "SAMUEL", "SAMUEL", "SAMUEL", "SAMUEL", "SAMUEL",
            "SAMUEL", "SAMUEL", "SAMUEL", "SAMUEL", "SAMUEL", "SAMUEL", "SAMUEL", "TAISE",
            "TAISE", "TAISE", "TAISE", "TAISE", "TAISE", "TAISE", "TAISE", "TAISE", "TAISE",
            "TAISE", "TAISE", "TAISE", "TARCIO", "TARCIO", "TARCIO", "TARCIO", "TARCIO",
            "TARCIO", "TARCIO", "TARCIO", "TARCIO", "TARCIO", "TARCIO", "TARCIO", "TARCIO",
            "TARCIO", "TARCIO", "TARCIO",
        ],
        "% UTILIZADO": [
            0.0004, 0.0007, 0.0012, 0.0018, 0.0018, 0.002, 0.0023, 0.0024, 0.0025, 0.0029,
            0.003, 0.0038, 0.004, 0.0041, 0.0042, 0.0043, 0.0056, 0.0058, 0.0067, 0.0079,
            0.0004, 0.0012, 0.0017, 0.002, 0.0021, 0.0022, 0.0025, 0.0036, 0.004, 0.0046,
            0.0047, 0.007, 0.0071, 0.0003, 0.0008, 0.0015, 0.0015, 0.0016, 0.0016, 0.0018,
            0.0025, 0.0031, 0.0036, 0.004, 0.0044, 0.0004, 0.0007, 0.0009, 0.0012, 0.0015,
            0.0017, 0.0019, 0.0021, 0.0022, 0.0024, 0.0034, 0.0052, 0.0293, 0.0002, 0.0007,
            0.001, 0.0011, 0.0013, 0.0015, 0.0018, 0.0019, 0.0023, 0.0024, 0.0028, 0.0028,
            0.0029, 0.0031, 0.0047, 0.005, 0.0089, 0.0000, 0.0006, 0.0008, 0.0012, 0.0014,
            0.0014, 0.0015, 0.0018, 0.0018, 0.0025, 0.0026, 0.0028, 0.0031, 0.0033, 0.0034,
            0.0036, 0.0041, 0.0004, 0.0005, 0.0009, 0.0011, 0.0012, 0.0019, 0.0021, 0.0023,
            0.0024, 0.0024, 0.0025, 0.0034, 0.0039, 0.0044, 0.0047, 0.0051, 0.0055, 0.0073,
            0.0013, 0.0017, 0.002, 0.002, 0.0022, 0.0023, 0.0024, 0.0025, 0.004, 0.0045,
            0.0049, 0.0051, 0.0052, 0.0011, 0.0016, 0.0022, 0.0025, 0.003, 0.0032, 0.0036,
            0.0037, 0.0038, 0.0046, 0.0046, 0.005, 0.0078, 0.0087, 0.0119, 0.0002, 0.0003,
            0.0006, 0.0009, 0.0015, 0.0022, 0.0023, 0.0031, 0.0031, 0.0044, 0.0045, 0.0052,
            0.0063, 0.0063, 0.0072, 0.0072, 0.0015, 0.0018, 0.003, 0.0034, 0.0042, 0.0047,
            0.0051, 0.0052, 0.0053, 0.0056, 0.0057, 0.0061, 0.0068, 0.0069, 0.0097, 0.0104,
            0.0002, 0.0014, 0.0022, 0.003, 0.003, 0.0041, 0.0048, 0.0056, 0.0058, 0.0065,
            0.0082, 0.0085, 0.0252, 0.0011, 0.0014, 0.0016, 0.0016, 0.0022, 0.0023, 0.0026,
            0.0034, 0.0044, 0.0045, 0.0053, 0.0062, 0.0071, 0.0098, 0.0102,
        ],
        "Total": [
            128012.34, 232343.79, 912282.88, 216440.26, 255864.6, 139532.05, 149831.22,
            175038.57, 225019.52, 282007.35, 118658.13, 104512.47, 184279.08, 199351.5,
            99618.91, 268659.32, 45932.67, 382841.78, 95953.73, 113234.75, 185235.5,
            158769.55, 193185.54, 252622.17, 172951.28, 194847.05, 134112.6, 608470.54,
            506030.95, 804979.41, 566948.88, 247523.88, 278806.11, 102616.81, 154864.64,
            134309.36, 428158.69, 242979.97, 194431.82, 222074.9, 182985.86, 158851.16,
            476658.1, 382547.82, 272399.68, 132638.46, 99022.27, 376461.67, 347808.82,
            210399.07, 135153.87, 188538.15, 243176.16, 114827.19, 212652.04, 376443.2,
            279598.28, 44840.86, 139996.07, 143642.48, 123006.25, 160282.72, 193597.09,
            124225.49, 175759.44, 296339.47, 128746.57, 172264.1, 200498.5, 211866.11,
            165857.53, 150461.14, 197394.44, 162108.86, 103828.77, 61183.44, 161500.68,
            175892.37, 643414.1, 351460.23, 154776.3, 339943.75, 190880.45, 337066.57,
            134587.54, 147456.94, 94031.37, 72354.45, 366988.2, 142562.28, 239047.2,
            261650.28, 278573.55, 128559.1, 301561.76, 308072.13, 192235.83, 361792.58,
            107394.66, 205359.04, 346872.87, 120563.4, 153457.49, 425956.68, 184872.77,
            74053.12, 97086.23, 121097.0, 259569.15, 112100.53, 213992.7, 499823.72,
            158137.4, 90717.77, 142863.11, 180619.36, 179109.45, 160085.82, 119641.32,
            180268.92, 473606.84, 238204.25, 330482.72, 197322.42, 125441.09, 122805.56,
            175644.27, 465906.63, 81960.92, 287988.75, 140576.67, 146617.48, 206107.43,
            349427.16, 304617.96, 521635.85, 98119.67, 87401.15, 165623.44, 131114.69,
            135113.13, 522937.14, 326072.4, 166305.43, 96864.02, 307113.34, 267659.64,
            276898.31, 127719.22, 128346.93, 185230.52, 146878.16, 110785.22, 61474.0,
            561910.59, 117982.32, 210749.25, 567272.15, 203850.29, 128859.35, 322302.48,
            218213.59, 96896.85, 324178.61, 328611.61, 200347.82, 298421.44, 202272.79,
            319841.14, 128625.15, 189840.66, 222582.21, 221029.98, 315465.89, 116565.32,
            743424.14, 363890.43, 239680.76, 144444.43, 364619.79, 42918.64, 101623.26,
            143746.09, 123271.27, 426082.82, 303915.37, 275120.56, 250047.84, 303390.54,
            368997.17, 520468.94, 275664.12, 116527.03, 152304.55, 349105.92, 186275.1,
            179323.47, 394391.28,
        ],
    }

    # Encontrar o tamanho do maior array
    max_length = max(len(v) for v in data.values())

    # Ajustar o tamanho de todos os arrays
    for key in data:
        length_difference = max_length - len(data[key])
        data[key].extend([None] * length_difference)  # Adiciona valores None até que o array tenha o mesmo tamanho

    # Criando o DataFrame
    df = pd.DataFrame(data)

    # Função para calcular os quartis por regional
    def calcular_quartis_por_regional(df, regional_col, value_col):
        return df.groupby(regional_col)[value_col].quantile([0.25, 0.5, 0.75]).unstack()

    # Calculando os quartis para a coluna "Total"
    quartis = calcular_quartis_por_regional(df, "REGIONAL", "Total")

    # Plotando os gráficos de dispersão para cada regional
    fig, axs = plt.subplots(len(quartis), 1, figsize=(8, 30), constrained_layout=True)

    for i, regional in enumerate(quartis.index):
        regional_data = df[df["REGIONAL"] == regional]
        x = regional_data["Total"]
        y = regional_data["% UTILIZADO"]

        axs[i].scatter(x, y, alpha=0.7, label=f"{regional}")
        axs[i].axvline(quartis.loc[regional, 0.25], color="green", linestyle="--", label="1º Quartil")
        axs[i].axvline(quartis.loc[regional, 0.5], color="blue", linestyle="--", label="Mediana")
        axs[i].axvline(quartis.loc[regional, 0.75], color="red", linestyle="--", label="3º Quartil")

        axs[i].set_title(f"Gráfico de Dispersão - {regional}")
        axs[i].set_xlabel("Total")
        axs[i].set_ylabel("% Utilizado")
        axs[i].legend()

    plt.show()
    st.pyplot(fig)