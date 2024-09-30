from dash import html
from components.component_tab3_drop import retorna_tab3_drop


def retorna_tab3(periodos: list):
    component_tab_3 = html.Div([
        # html.Div([retorna_tab3_left(periodos=periodos)], className='tab_subcontainers', id='tab3_left'),
        html.Div([
            html.Div([
                html.Div([retorna_tab3_drop(periodos=periodos)], className='tab_subcontainers', id='drop_tab3'),
                html.Div([], className='tab_subcontainers', id='kpi_1'),
                html.Div([], className='tab_subcontainers', id='kpi_2'),
                html.Div([], className='tab_subcontainers', id='kpi_3'),
            ], id='zona_kpi_tab3'),
            html.Div([
                html.Div([
                    html.Div([], className='tab_subcontainers', id='barras_tab3'),
                ], id='zona_barras_tab3'),
                html.Div([
                    html.Div([], className='tab_subcontainers', id='pies_tab3'),
                    # html.Div([], className='tab_subcontainers', id='pies_tab3'),
                    # html.Div([], className='tab_subcontainers', id='pie2_tab3'),
                ], id='zona_pies_tab3')

            ], id='zona_grafica_tab3')
        ], id='tab3_right')
    ], className='work_container', id='tab3_component')
    return component_tab_3
