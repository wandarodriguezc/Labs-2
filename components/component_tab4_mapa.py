from dash import dcc
import plotly.express as px
import polars as pl
import pandas as pd


def retorna_mapa(df: pl.DataFrame):
    df = df.to_pandas()

    # Definir los nuevos rangos de población
    bins = [2000, 5000, 10000, 20000, 50000, 100000, 500000, 10000000]
    labels = [
        '2.000-5.000 Hab',
        '5.001-10.000 Hab',
        '10.001-20.000 Hab',
        '20.001-50.000 Hab',
        '50.001-100.000 Hab',
        '100.001-500.000 Hab',
        'Más de 500.000 Hab'
    ]
    df['Rango'] = pd.cut(df['Población'], bins=bins, labels=labels)

    # Asignar tamaños y colores basados en los nuevos rangos
    size_map = {
        '2.000-5.000 Hab': 0.01,
        '5.001-10.000 Hab': 0.01,
        '10.001-20.000 Hab': 0.01,
        '20.001-50.000 Hab': 0.01,
        '50.001-100.000 Hab': 0.01,
        '100.001-500.000 Hab': 0.01,
        'Más de 500.000 Hab': 0.01,
    }
    color_map = {
        '2.000-5.000 Hab': '#1f77b4',
        '5.001-10.000 Hab': '#ff7f0e',
        '10.001-20.000 Hab': '#2ca02c',
        '20.001-50.000 Hab': '#d62728',
        '50.001-100.000 Hab': '#9467bd',
        '100.001-500.000 Hab': '#8c564b',
        'Más de 500.000 Hab': '#e377c2'
    }
    df['Size'] = df['Rango'].map(size_map)
    df['Size'] = 0.01
    df['Color'] = df['Rango'].map(color_map)

    fig = px.scatter_mapbox(
        df,
        # marker=dict(size=12, sizemode="diameter", sizeref=8),
        lat="Latitud",
        lon="Longitud",
        hover_name="Localidad",
        hover_data={"Provincia": True, "Partido": True, "Población": True, "Accesos 100 Hab": True,
                    "Size": False, "Rango": False, "Latitud": False, "Longitud": False},
        size="Size",
        size_max=5,
        color="Rango",
        color_discrete_map=color_map,
        category_orders={"Rango": labels},  # Ordenar las categorías en la leyenda
        zoom=3.5,
        height=660
    )

    # Configurar el estilo del mapa
    fig.update_layout(mapbox_style="carto-darkmatter")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(mapbox=dict(center=dict(lat=-38.4161, lon=-63.6167), zoom=3.5))

    # Mover la leyenda y ajustar su estilo
    fig.update_layout(
        legend=dict(
            title="Rango de Población",
            x=0.60,  # Posición horizontal
            y=0.08,  # Posición vertical
            traceorder="normal",
            font=dict(color="#d2d0ce"),  # Color de la fuente
            bgcolor='rgba(0,0,0,0)'  # Fondo transparente
        )
    )

    fig.update_layout(clickmode='event+select')

    # Desactivar el zoom
    fig.update_layout(mapbox_zoom=3.5)
    config = {'displayModeBar': False}
    mapa = dcc.Graph(id='mapa', figure=fig, config=config)
    return mapa


'''
“open-street-map”: El estilo actual que estás usando.    SI CORRE
“carto-positron”: Un estilo claro y minimalista.         SI CORRE
“carto-darkmatter”: Un estilo oscuro y minimalista.      SI CORRE
“stamen-terrain”: Un estilo que resalta el terreno.       NO CORRE
“stamen-toner”: Un estilo en blanco y negro con líneas claras.   NO CORRE
“stamen-watercolor”: Un estilo artístico que parece pintado con acuarelas.  NO CORRE
“basic”: Un estilo básico y limpio.           NO CORRE
“streets”: Un estilo que resalta las calles.   NO CORRE
“outdoors”: Un estilo que resalta las áreas al aire libre.  NO CORRE
“light”: Un estilo claro.
“dark”: Un estilo oscuro.     No corre
“satellite”: Un estilo de imagen satelital.  NO CORRE
“satellite-streets”: Imagen satelital con calles resaltadas.  NO CORRE



'''
