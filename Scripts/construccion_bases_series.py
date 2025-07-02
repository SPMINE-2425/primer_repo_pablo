import pandas as pd 
import numpy as np

def verificar_base(df:pd.DataFrame) -> pd.DataFrame:
    """
    Valida y procesa una tabla de secuestros, generando agregados por municipio y departamento.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame de entrada que debe contener exactamente las columnas:
        ['FECHA HECHO', 'COD_DEPTO', 'DEPARTAMENTO',
         'COD_MUNI', 'MUNICIPIO', 'TIPO DELITO', 'CANTIDAD'].

    Returns
    -------
    secuestros_departamentos : pandas.DataFrame
        DataFrame agrupado por fecha y departamento, con las columnas:
        ['FECHA HECHO', 'COD_DEPTO', 'DEPARTAMENTO', 'N_SIMPLE', 'N_EXTORSIVO'].
    secuestros_municipios : pandas.DataFrame
        DataFrame agrupado por fecha, departamento y municipio, con las columnas:
        ['FECHA HECHO', 'COD_DEPTO', 'DEPARTAMENTO', 'COD_MUNI',
         'MUNICIPIO', 'N_SIMPLE', 'N_EXTORSIVO'].
    df1 : pandas.DataFrame
        Copia del DataFrame original, con:
        - Columna 'FECHA HECHO' convertida a datetime (coerce para formatos inválidos).
        - Columnas auxiliares 'N_SIMPLE' y 'N_EXTORSIVO' con conteos por tipo de secuestro.
    """

    df1 = df.copy()

    columnas = ['FECHA HECHO', 'COD_DEPTO', 'DEPARTAMENTO', 'COD_MUNI', 'MUNICIPIO',
       'TIPO DELITO', 'CANTIDAD']

    if not df1.columns.equals(pd.Index(columnas)):
        return 'Ingreso la base incorrecta'
    
    #Verificar y convertir la columna de fecha
    df1['FECHA HECHO'] = pd.to_datetime(df1['FECHA HECHO'],
        format='%d/%m/%Y',dayfirst=True,errors='coerce')
    
    # Verificar fechas invalidas
    invalid_dates = df1['FECHA HECHO'].isna().sum()
    print(f'Fechas inválidas: {invalid_dates}')

    # Dado que tenemos dos tipos de secuestro, separameslas para desagregar por tipo de secuestro 
    df1['N_SIMPLE'] = np.where(df1['TIPO DELITO'] == 'SECUESTRO SIMPLE',df1['CANTIDAD'],0)
    df1['N_EXTORSIVO'] = np.where(df1['TIPO DELITO'] == 'SECUESTRO EXTORSIVO',df1['CANTIDAD'],0)

    # Agrupemos la base por municipios 
    secuestros_municipios = (df1.groupby(['FECHA HECHO', 'COD_DEPTO', 'DEPARTAMENTO', 'COD_MUNI', 'MUNICIPIO'],
        as_index=False)[['N_SIMPLE', 'N_EXTORSIVO']].sum().sort_values(['MUNICIPIO', 'FECHA HECHO']))

    # Agrupemos la base por deartamentos 
    secuestros_departamentos = (df1.groupby(['FECHA HECHO', 'COD_DEPTO', 'DEPARTAMENTO'],
        as_index=False)[['N_SIMPLE', 'N_EXTORSIVO']].sum().sort_values(['DEPARTAMENTO', 'FECHA HECHO']))
    
    return secuestros_departamentos , secuestros_municipios , df1 


def crear_series_de_tiempo(f, df:pd.DataFrame) -> pd.DataFrame:
    """
    Genera series temporales agregadas de secuestros a nivel de municipio, departamento y nacional.

    Parameters
    ----------
    f : callable
        Función que recibe el DataFrame original y devuelve una tupla de tres elementos:
        (secuestros_departamentos, secuestros_municipios, df1), donde:
        - secuestros_departamentos: DataFrame agrupado por fecha y departamento
        - secuestros_municipios: DataFrame agrupado por fecha, departamento y municipio
        - df1: DataFrame procesado con fechas y contadores por tipo de secuestro
    df : pandas.DataFrame
        DataFrame original con las columnas procesadas por `f`.

    Returns
    -------
    municipios_mensual : pandas.DataFrame
        Panel mensual de secuestros por municipio, con columnas:
        ['MES', 'COD_DEPTO', 'DEPARTAMENTO', 'COD_MUNI', 'MUNICIPIO',
         'N_SIMPLE', 'N_EXTORSIVO', 'TOTAL'].
        El índice ‘MES’ corresponde al último día de cada mes (`freq='ME'`).
    departamentos_mensual : pandas.DataFrame
        Panel mensual de secuestros por departamento, con columnas:
        ['MES', 'COD_DEPTO', 'DEPARTAMENTO', 'N_SIMPLE', 'N_EXTORSIVO', 'TOTAL'].
    municipios_anual : pandas.DataFrame
        Panel anual de secuestros por municipio, con columnas:
        ['AÑO', 'COD_DEPTO', 'DEPARTAMENTO', 'COD_MUNI', 'MUNICIPIO',
         'N_SIMPLE', 'N_EXTORSIVO', 'TOTAL'].
        El índice ‘AÑO’ corresponde al último día de cada año (`freq='YE'`).
    departamentos_anual : pandas.DataFrame
        Panel anual de secuestros por departamento, con columnas:
        ['AÑO', 'COD_DEPTO', 'DEPARTAMENTO', 'N_SIMPLE', 'N_EXTORSIVO', 'TOTAL'].
    serie_colombia_mensual : pandas.DataFrame
        Serie mensual agregada para todo el país, con columnas:
        ['AÑO', 'N_SIMPLE', 'N_EXTORSIVO', 'TOTAL'].
        Aquí ‘AÑO’ es en realidad la última fecha del mes, usada como etiqueta.
    """

    # Obtengamos los datos de la funcion creada arriba
    secuestros_departamentos , secuestros_municipios , df1 = f(df)

    # Crear Panel Mensual para municipios 
    municipios_mensual = (secuestros_municipios.set_index('FECHA HECHO').groupby([
        pd.Grouper(freq='ME'),
        'COD_DEPTO', 'DEPARTAMENTO',
        'COD_MUNI', 'MUNICIPIO'])[['N_SIMPLE', 'N_EXTORSIVO']].sum().reset_index().rename(columns={'FECHA HECHO': 'MES'}))
    municipios_mensual['TOTAL'] = municipios_mensual['N_SIMPLE'] + municipios_mensual['N_EXTORSIVO']


    # Crear Panel Mensual para departamentos 
    departamentos_mensual = (secuestros_departamentos.set_index('FECHA HECHO').groupby([
        pd.Grouper(freq='ME'),
        'COD_DEPTO', 'DEPARTAMENTO'])[['N_SIMPLE', 'N_EXTORSIVO']].sum().reset_index().rename(columns={'FECHA HECHO': 'MES'}))
    departamentos_mensual['TOTAL'] = departamentos_mensual['N_SIMPLE'] + departamentos_mensual['N_EXTORSIVO']


    # Crear Panel Anual para municipios
    municipios_anual = (secuestros_municipios.set_index('FECHA HECHO').groupby([
        pd.Grouper(freq='YE'),
        'COD_DEPTO', 'DEPARTAMENTO',
        'COD_MUNI', 'MUNICIPIO'])[['N_SIMPLE', 'N_EXTORSIVO']].sum().reset_index().rename(columns={'FECHA HECHO': 'AÑO'}))
    municipios_anual['TOTAL'] = municipios_anual['N_SIMPLE'] + municipios_anual['N_EXTORSIVO']

    # Crear Panel Anual para departamentos 
    departamentos_anual = (secuestros_departamentos.set_index('FECHA HECHO').groupby([
        pd.Grouper(freq='YE'),
        'COD_DEPTO', 'DEPARTAMENTO'])[['N_SIMPLE', 'N_EXTORSIVO']].sum().reset_index().rename(columns={'FECHA HECHO': 'AÑO'}))
    departamentos_anual['TOTAL'] = departamentos_anual['N_SIMPLE'] + departamentos_anual['N_EXTORSIVO']

    # Crear la serie total de secuestros para Colombia 
    serie_colombia_mensual = (df1.set_index('FECHA HECHO').resample('ME')[['N_SIMPLE', 'N_EXTORSIVO']]
    .sum().reset_index().rename(columns={'FECHA HECHO': 'AÑO'}))
    serie_colombia_mensual['TOTAL'] = serie_colombia_mensual['N_SIMPLE'] + serie_colombia_mensual['N_EXTORSIVO']

    return municipios_mensual , departamentos_mensual , municipios_anual , departamentos_anual  , serie_colombia_mensual