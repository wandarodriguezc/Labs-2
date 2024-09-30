import polars as pl
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def crear_graf_pie(df: pl.DataFrame, width: int):
    proporcion = df["Ingresos 2024"].sum() / df["Ingresos 2014"].sum() * 100

    # Colores personalizados
    colors_4 = ['#22D3EE', '#38C172', '#F6993F', '#FFED4A']

    # Crear subplots
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'pie'}, {'type': 'pie'}]],
                        subplot_titles=("Ingresos 2014", "Ingresos 2024"))

    # Gráfico de Pie para Ingresos 2014
    fig.add_trace(go.Pie(labels=df["Tecnología"], values=df["Ingresos 2014"],
                         name="Ingresos 2014", marker=dict(colors=colors_4), scalegroup='one'), row=1, col=1)

    # Gráfico de Pie para Ingresos 2024 con tamaño proporcional
    fig.add_trace(go.Pie(labels=df["Tecnología"], values=df["Ingresos 2024"],
                         name="Ingresos 2024", marker=dict(colors=colors_4), scalegroup='one'), row=1, col=2)

    pie_pagina = f'Nota: Para el Año 2024 el total de Ingresos en dolares representa un {proporcion:.2f}% con respecto al 2014'
    # Actualizar el layout
    fig.update_layout(title_text="Comparación de Ingresos (en Dolares) por Tecnología",
                      width=width,
                      #   height=600,
                      annotations=[dict(text='2014', x=0.18, y=0.5, font_size=20, showarrow=False),
                                   dict(text='2024', x=0.82, y=0.5, font_size=20, showarrow=False),
                                   dict(text=pie_pagina, x=0.45, y=-0.3, font_size=14,
                                        showarrow=False, xanchor='center')])

    return fig


def crear_grafica(df_list: list, y_column: str, list_names: list, colors: list) -> px.line:
    """Crear gráfica: Función para crear gráficas de tendencias

    Args:
        df_list (list): Lista de Dataframes
        y_column (str): Columna del dataframe a graficar
        title (str): Título del gráfico
        list_names (list): Lista de Nombres de los gráficos
        colors (list): Lista de Colores
        width (int): Ancho del gráfico en pixeles

    Returns:
        px.line: Grafica de linea de la Libreria plotly
    """
    fig = px.line()
    # Aca esto es como 3 ciclos for en paralelo cada variable
    for df, name, color in zip(df_list, list_names, colors):
        fig.add_scatter(x=df["fecha"], y=df[y_column], mode='lines', name=name, line=dict(color=color))
    fig.update_layout(xaxis_title='Periodo', yaxis_title=y_column)
    return fig


def crear_graf_df(
    columns: list,
    names: list,
    colors: list,
    width: int,
    y_title: str,
    df: pl.DataFrame,
    titulo: str
) -> px.line:
    """crear_graf_df: recibe de un mismo Dataframe la inf necesaria para graficar la tendencia de varias
                      columnas

    Args:
        columns (list): Lista con los nombres de las columnas a Graficar
        names (list): Lista con los nombres de Cada Linea en el Gráfico
        colors (list): Lista con los colores  usar en el Gráfico
        width (int): ancho del Gráfico de Pixeles
        y_title (str): Titulo del eje y
        df (pl.DataFrame): Dataframe del cual se sacarán los datos a graficar
        titulo (str): Titulo del gráfico

    Returns:
        px.line: Grafico tipo linea de la libreria plotly
    """

    fig = px.line()
    for i in range(3):
        fig.add_scatter(x=df['fecha'], y=df[columns[i]],
                        name=names[i], mode='lines', line=dict(color=colors[i]))
    fig.update_layout(title=titulo, xaxis_title='Periodo', yaxis_title=y_title, width=width)
    return fig
