import plotly.express as px
from dash import dcc, html
import polars as pl
import pandas as pd


def retorna_barras_tab3(df: pl.DataFrame):
    df = df.to_pandas()

    df_grouped = df.melt(id_vars='Provincia',
                         value_vars=['Accesos 100 Hog', 'MBPS Media Bajada'],
                         var_name='Metrica',
                         value_name='Valor')

    df_grouped = pd.merge(df_grouped, df[['Provincia', 'Accesos 100 Hog Anterior', 'KPI 100 Hog',
                                          'Accesos 100 Hog', 'Cumplimineto KPI 100 Hog',
                                          'Crecimiento Trimestral Accesos 100 Hog',
                                          'Total Accesos', 'MBPS Anterior', 'KPI MBPS',
                                          'MBPS Media Bajada', 'Cumplimineto KPI MBPS',
                                          'Crecimiento Trimestral MBPS']],
                          on='Provincia', how='left')

    custom_data_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

    fig = px.bar(df_grouped, x='Provincia', y='Valor', color='Metrica', barmode='group',
                 custom_data=df_grouped.iloc[:, custom_data_indices])

    fig.update_traces(
        hovertemplate="<br>".join([
            "Provincia: %{customdata[0]}",
            "Métrica: %{customdata[1]}",
            "Valor: %{customdata[2]}",
            "Accesos 100 Hog Anterior: %{customdata[3]}",
            "KPI 100 Hog: %{customdata[4]}",
            "Accesos 100 Hog: %{customdata[5]}",
            "Cumplimiento KPI 100 Hog: %{customdata[6]}",
            "Crecimiento Trimestral Accesos 100 Hog: %{customdata[7]}",
            "Total Accesos: %{customdata[8]}",
            "MBPS Anterior: %{customdata[9]}",
            "KPI MBPS: %{customdata[10]}",
            "MBPS Media Bajada: %{customdata[11]}",
            "Cumplimineto KPI MBPS: %{customdata[12]}",
            "Crecimiento Trimestral MBPS: %{customdata[13]}",
        ]),
        hoverlabel=dict(bgcolor="white", font_color="black"),
        width=0.4,
    )

    fig.update_layout(
        xaxis_title="",
        yaxis_title="Accesos",
        font=dict(color='#ffffff', size=14),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=True, linecolor='#ffffff', tickangle=-90),
        yaxis=dict(showgrid=False, zeroline=True, linecolor='#ffffff'),
        legend=dict(
            x=0.8,
            y=1.1,
            orientation='v'
        )
    )

    componente = html.Div([
        html.Label("Accesos a Internet por cada 100 Hogares y Velocidad Media de Bajada", className='title_left'),
        html.Br(),
        dcc.Graph(figure=fig, config={'displayModeBar': False})
    ], style={'width': '100%', 'height': '80%'}, id='grafico_barras_tab3')

    return componente
