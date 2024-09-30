from dash import html
import polars as pl


def retorna_tarjetas_tab3(df: pl.DataFrame) -> tuple:
    tarjeta_1 = html.Div([
        html.Div(html.Label('Variación Acc 100 Hog'), className='title_left'),
        html.Br(),
        html.Div(html.Label(f'{df["Crecimiento Accesos 100 Hog"][0]} %'), className='tarjetas')
    ], className='contenedor_tarjetas')

    tarjeta_2 = html.Div([
        html.Div(html.Label('Variación Acc 100 Hab'), className='title_left'),
        html.Br(),
        html.Div(html.Label(f'{df["Crecimineto Accesos 100 Hab"][0]} %'), className='tarjetas')
    ], className='contenedor_tarjetas')

    tarjeta_3 = html.Div([
        html.Div(html.Label('Variación MBPS Media'), className='title_left'),
        html.Br(),
        html.Div(html.Label(f'{df["Crecimineto MBPS Media Bajada"][0]} %'), className='tarjetas')
    ], className='contenedor_tarjetas')

    return (tarjeta_1, tarjeta_2, tarjeta_3)
