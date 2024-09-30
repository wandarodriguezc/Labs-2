from dash import Dash, dcc, html, Input, Output, callback, State
import polars as pl
from utils.retorna_dfs_grfaicos_tab4 import retorna_dfs_graficos_tab4
from components.component_home import component_home
from components.component_tab2 import component_tab_2
from components.component_tab2_textos import textos_left_tab2
from components.component_tab2_grafico import retorna_grafico_tab2
from components.component_tab3 import retorna_tab3
from components.component_tab3_tarjetas import retorna_tarjetas_tab3
from components.component_tab3_barras import retorna_barras_tab3
# from components.component_tab3_pies import retorna_pies_tab3
from components.component_tab3_donuts import retorna_pies_tab3
from components.component_tab4 import component_tab_4
from components.component_tab4_mapa import retorna_mapa
from components.component_tab4_donuts import retorna_graf_tab4
from components.component_tab4_retorna_texto import retorna_tab4_texto_resultado

accesos_localidades = pl.read_parquet('data/accesos_localidades_dash.parquet')
rangos_localidades = pl.read_parquet('data/rangos_localidades.parquet')
data_tablero = pl.read_parquet('data/data_tablero_dashboard.parquet')
tarjetas = pl.read_parquet('data/tarjetas.parquet')
lista_periodos = data_tablero['Periodo Tablero'].unique().to_list()
lista_periodos.sort()
lista_periodos = [item[7:] for item in lista_periodos]
periodos_dashboard = lista_periodos.copy()
periodos_dashboard.pop(0)


app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    title="Telecomunicaciones Argentina",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)


tabs_styles = {"height": "2em", "marginLeft": "0.5em", "marginRight": "1.5em"}
tab_style = {
    "border": "1px solid #656565",
    "color": "#d0d0d0",
    "backgroundColor": "#2b2b2b",
    "padding": "0.5em",
    "fontWeight": "bold",
}

tab_selected_style = {
    # "borderTop": "1px solid #70cbff",
    "borderTop": "1px solid #ffffff",
    "borderLeft": "1px solid #656565",
    "borderRight": "1px solid #656565",
    "backgroundColor": "#2b2b2b",
    "color": "#ffffff",
    "padding": "0.5em",
}

app.layout = html.Div(
    [
        dcc.Tabs(
            id="tabs-inline",
            value="tab-1",
            children=[
                dcc.Tab(
                    label="Home",
                    value="tab-1",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="Contexto",
                    value="tab-2",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="Tablero",
                    value="tab-3",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="Mapa",
                    value="tab-4",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
            ],
            style=tabs_styles,
        ),
        html.Div(id="tabs-content-inline-3"),
    ]
)


@callback(Output("tabs-content-inline-3", "children"), Input("tabs-inline", "value"))
def render_content(tab):
    if tab == "tab-1":
        return component_home
    elif tab == "tab-2":
        return component_tab_2
    elif tab == "tab-3":
        return retorna_tab3(periodos=periodos_dashboard)
    elif tab == "tab-4":
        return component_tab_4


@app.callback(
    Output('tab4_rangos_response', 'children'),
    Output('tab4_center', 'children'),
    Output('tab4_right', 'children'),
    Output('tab4_texto_resultados', 'children'),
    Output("store_tab4", "data"),
    Input('btn_tab4', 'n_clicks'),
    Input('drop-minimo_tab4', 'value'),
    Input('drop-maximo_tab4', 'value'),
    State("store_tab4", "data"),
    prevent_initial_call=True,
)
def update_tab_4(n_clicks, min_value, max_value, data):
    btn_tab4 = data.get("btn_tab4")
    if not n_clicks or n_clicks == btn_tab4:
        return (html.Br(), None, None, None, data)
    if n_clicks > btn_tab4:
        btn_tab4 += 1
        data["btn_tab4"] = btn_tab4
        if max_value > min_value:
            response = html.Br()
            df_mapa, df_pie_rangos, df_tecnologias, n_accesos, n_localidades = retorna_dfs_graficos_tab4(
                df_accesos_localidades=accesos_localidades,
                df_rangos=rangos_localidades,
                hab_minimo=min_value,
                hab_maximo=max_value
            )
            poblacion_total_rango = df_mapa['Población'].sum()
            componente_texto = retorna_tab4_texto_resultado(
                total_poblacion=poblacion_total_rango,
                total_localidades=n_localidades,
                total_accesos=n_accesos
            )
            mapa = retorna_mapa(df=df_mapa)
            graficos_tab4 = retorna_graf_tab4(
                df_pie_rangos=df_pie_rangos,
                df_tecnologias=df_tecnologias['ADSL', 'CABLEMODEM', 'FIBRA', 'WIRELESS']
            )
        else:
            response = html.Label('Rango no Permitido !!!')
            mapa = None
            graficos_tab4 = None
            componente_texto = None
        return (response, mapa, graficos_tab4, componente_texto, data)


@callback(
    Output('title_right_tab2', 'children'),
    Output('grafico_right_tab2', 'children'),
    Output('texto_tab2', 'children'),
    Input('control_slides_tab2', 'value'),
    prevent_initial_call=True,
)
def update_tab_2(value):
    titulos_diapositivas = [
        'Ingresos en Miles de Pesos Argentinos',
        'Ingresos en Miles de Dolares',
        'Comparación de Ingresos en Dolares por Tecnología',
        'Accesos por cada 100 Habitantes',
        'Accesos de Telefonía Movil',
        'Cantidad de Llamadas Telefonía Movil',
        'Cantidad de Minutos Consumidos Telefonía Movil',
        'Evolución en Accesos e Ingresos en la última Decada',
        'Evolución de los Accesos de las Tecnologías para el Acceso a Internet',
        'Evolución de los Accesos a Internet en los Distintos Rangos de Velocidad',
    ]
    if value in range(1, 11):
        componente = retorna_grafico_tab2(numero_graf=value)
        title = html.Label(titulos_diapositivas[value - 1])
        texto = textos_left_tab2[value - 1] if value in [1, 2, 3, 4, 7, 8, 9, 10] else None
        return (title, componente, texto)
    else:
        return (None, None, None)


@app.callback(
    Output('kpi_1', 'children'),
    Output('kpi_2', 'children'),
    Output('kpi_3', 'children'),
    Output('barras_tab3', 'children'),
    Output('pies_tab3', 'children'),
    # Output('tab4_right', 'children'),
    # Output('tab4_texto_resultados', 'children'),
    # Output("store_tab3", "data"),
    # Input('btn_tab3', 'n_clicks'),
    Input('drop-tab3', 'value'),
    # State("store_tab3", "data"),
)
def update_tab_3(value: str):
    mask = data_tablero['Periodo'] == value
    df = data_tablero.filter(mask)
    barras = retorna_barras_tab3(df=df)
    pies = retorna_pies_tab3(df=df)
    mask = tarjetas['Periodo'] == value
    df_tarjetas = tarjetas.filter(mask)
    tarjeta_1, tarjeta_2, tarjeta_3 = retorna_tarjetas_tab3(df=df_tarjetas)
    return (tarjeta_1, tarjeta_2, tarjeta_3, barras, pies)


if __name__ == "__main__":
    app.run(debug=True)


"""
BooleanSwitch:
import dash_daq as daq
app.layout = html.Div([
    daq.BooleanSwitch(id='our-boolean-switch', on=False),
    html.Div(id='boolean-switch-result')
])


@callback(
    Output('boolean-switch-result', 'children'),
    Input('our-boolean-switch', 'on')
)
def update_output(on):
    return f'The switch is {on}.'






VELOCIMETRO
app.layout = html.Div([
    daq.Gauge(
        id='our-gauge',
        label="Default",
        value=6
    ),
    dcc.Slider(
        id='our-gauge-slider',
        min=0,
        max=10,
        step=1,
        value=5
    ),
])

@callback(Output('our-gauge', 'value'), Input('our-gauge-slider', 'value'))
def update_output(value):
    return value


import dash_mantine_components as dmc











    # "borderTop": "1px solid #70cbff",
    # "borderBottom": "1px solid #70cbff",
    # "borderBottom": "1px solid #70cbff",
    # "borderBottom": "1px solid #70cbff",
"""
