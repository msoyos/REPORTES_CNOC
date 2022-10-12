sql_r=""" SELECT 
DISTINCT(fr_kpi_outsourcing1.TICKET),
semana_claro.semana SEMANA,
catalogo_areas_cnoc.responsable RESPONSABLE,
date_format(fr_kpi_outsourcing1.FECHA_CIERRE, "%Y") YEAR_,
date_format(fr_kpi_outsourcing1.FECHA_CIERRE, "%m")MES 
FROM `fr_kpi_outsourcing1` 
INNER JOIN semana_claro on semana_claro.fecha = date_format(fr_kpi_outsourcing1.FECHA_CIERRE, "%Y-%m-%d")
INNER JOIN catalogo_areas_cnoc on catalogo_areas_cnoc.nombre_area_claro=fr_kpi_outsourcing1.RESPONSABLE 
WHERE catalogo_areas_cnoc.responsable NOT IN('NO INCLUIR')) SQL1 """

def sql_semanal():
    sql="""
SELECT 
SQL1.SEMANA,
YEAR_,
MES,
COUNT(CASE
WHEN SQL1.RESPONSABLE = 'REACTIVO' THEN 1 END) REACTIVO,
COUNT(CASE
WHEN SQL1.RESPONSABLE = 'PROACTIVO' THEN 1 END) PROACTIVO,
COUNT(CASE
WHEN SQL1.RESPONSABLE = 'ACCESO_EMPRESARIALES' THEN 1 END) ACCESO_EMPRESARIALES
FROM("""+str(sql_r)+"""
GROUP BY SQL1.SEMANA,YEAR_,MES
ORDER BY SQL1.SEMANA DESC,YEAR_ DESC,MES
"""
    return sql

def sql_semana():
    sql_semana_="""SELECT
    SQL1.SEMANA
FROM(
"""+str(sql_r)+"""
GROUP BY SQL1.SEMANA
ORDER BY SQL1.SEMANA DESC
    """    
    return sql_semana_

def sql_year():
    sql_year_="""SELECT
    
YEAR_
FROM(
"""+str(sql_r)+"""
GROUP BY YEAR_
ORDER BY YEAR_ DESC
    """    
    return sql_year_

def sql_mes():
    sql_mes_="""SELECT
MES
FROM(
"""+str(sql_r)+"""
GROUP BY MES 
ORDER BY MES desc
    """    
    return sql_mes_

def procesar_week(result):
    store_list = []
    for i in result:
            store_details = {"week":None}
            store_details['week'] = i[0]
            store_list.append(store_details)
    return store_list

def procesar_year(result):
    store_list = []
    for i in result:
            store_details = {"years":None}
            store_details['years'] = i[0]
            store_list.append(store_details)
    return store_list
def procesar_month(result):
    store_list = []
    for i in result:
            store_details = {"month":None}
            store_details['month'] = i[0]
            store_list.append(store_details)
    return store_list

def procesar_filtros(filtro):
    filtro_list=[]
    for i in filtro:
        store_details ={"semana":None, "year":None, "mes":None}
        store_details['semana'] = i[0]
        store_details['year'] = i[1]
        store_details['mes'] = i[2]
        filtro_list.append(store_details)
    
    return filtro_list

def procesar_items(result):
    store_list = []
    for item in result:
            store_details = {"semana":None}
            store_details['semana'] = item[0]
            store_details['year'] = item[1]
            store_details['mes'] = item[2]
            store_details['reactivo'] = item[3]
            store_details['proactivo'] = item[4]
            store_details['accesos_empresariales'] = item[5]
            store_list.append(store_details)
    return store_list

def respuesta(data,semana,year,mes):
    if not data:
        msj="ERROR, NO HAY DATOS QUE MOSTRAR"
        filtros=[]
        week="no" 
        years="no"
        month="no"   
    else:
        msj="SE GENERADO REPORTE, DE TIKETS CERRADOS POR SEMANA"
        cargar="si"
        week=semana
        years=year 
        month=mes
    respuesta={"code":200,
               "procesar":cargar,
               "data":data,
               "week":week,
               "year":years,
               "month":month,
               "msj":msj}
    return respuesta

def sql_enlace_default():
    sql="""
    SELECT 
SQL1.SEMANA,
YEAR_,
MES,
COUNT(CASE
WHEN SQL1.RESPONSABLE = 'REACTIVO' THEN 1 END) REACTIVO,
COUNT(CASE
WHEN SQL1.RESPONSABLE = 'PROACTIVO' THEN 1 END) PROACTIVO,
COUNT(CASE
WHEN SQL1.RESPONSABLE = 'ACCESO_EMPRESARIALES' THEN 1 END) ACCESO_EMPRESARIALES
FROM(
SELECT 
DISTINCT(fr_kpi_outsourcing1.TICKET),
semana_claro.semana SEMANA,
catalogo_areas_cnoc.responsable RESPONSABLE,
date_format(fr_kpi_outsourcing1.FECHA_CIERRE, "%Y") YEAR_,
date_format(fr_kpi_outsourcing1.FECHA_CIERRE, "%m")MES 
FROM `fr_kpi_outsourcing1` 
INNER JOIN semana_claro on semana_claro.fecha = date_format(fr_kpi_outsourcing1.FECHA_CIERRE, "%Y-%m-%d")
INNER JOIN catalogo_areas_cnoc on catalogo_areas_cnoc.nombre_area_claro=fr_kpi_outsourcing1.RESPONSABLE 
WHERE catalogo_areas_cnoc.responsable NOT IN('NO INCLUIR') and `ID_SERVICIO` like "%default%")  SQL1 
GROUP BY SQL1.SEMANA,YEAR_,MES
ORDER BY SQL1.SEMANA DESC,YEAR_ DESC,MES;"""
    return sql

def procesar_enlaces_default(result):
    store_list = []
    for item in result:
            store_details = {"semana":None,"year":None,"mes":None,"reactivo":None,"proactivo":None,"accesos_empresariales":None}
            store_details['semana'] = item[0]
            store_details['year'] = item[1]
            store_details['mes'] = item[2]
            store_details['reactivo'] = item[3]
            store_details['proactivo'] = item[4]
            store_details['accesos_empresariales'] = item[5]
            store_list.append(store_details)
    return store_list

def respuesta2(data):
    if not data:
        msj="ERROR, NO HAY DATOS QUE MOSTRAR"
        cargar="no"
    else:
        msj="SE GENERADO REPORTE, DE ENLACES POR DEFAULT"
        cargar="si"
       
    respuesta2={"code":200,
               "procesar":cargar,
               "data":data,
               "msj":msj}
    return respuesta2

def sql_enlaces_default():
    sql="""
    SELECT 
SQL1.SEMANA,
YEAR_,
MES,
COUNT(*),
enlaces
FROM(
SELECT 
DISTINCT(fr_kpi_outsourcing1.TICKET),
semana_claro.semana SEMANA,
catalogo_areas_cnoc.responsable RESPONSABLE,
date_format(fr_kpi_outsourcing1.FECHA_CIERRE, "%Y") YEAR_,
date_format(fr_kpi_outsourcing1.FECHA_CIERRE, "%m")MES,
fr_kpi_outsourcing1.`ID_SERVICIO` enlaces
FROM `fr_kpi_outsourcing1` 
INNER JOIN semana_claro on semana_claro.fecha = date_format(fr_kpi_outsourcing1.FECHA_CIERRE, "%Y-%m-%d")
INNER JOIN catalogo_areas_cnoc on catalogo_areas_cnoc.nombre_area_claro=fr_kpi_outsourcing1.RESPONSABLE 
WHERE catalogo_areas_cnoc.responsable NOT IN('NO INCLUIR') and `ID_SERVICIO` like "%default%")  SQL1 
GROUP BY SQL1.SEMANA,YEAR_,MES,enlaces
ORDER BY SQL1.SEMANA DESC,YEAR_ DESC,MES;"""
    return sql

def procesar_item_default(result):
    store_list = []
    for item in result:
            store_details = {"semana":None,"year":None,"mes":None,"cantidad":None,"enlaces":None}
            store_details['semana'] = item[0]
            store_details['year'] = item[1]
            store_details['mes'] = item[2]
            store_details['cantidad'] = item[3]
            store_details['enlaces'] = item[4]
           
            store_list.append(store_details)
    return store_list

def sql_masivo():
    sql="""SELECT 
SQL1.SEMANA,
YEAR_,
MES,
COUNT(CASE
WHEN SQL1.RESPONSABLE = 'MASIVO_REACTIVO' OR  SQL1.RESPONSABLE = 'MASIVO_PROACTIVO' THEN 1 END) FALLA_MASIVA,
COUNT(CASE
WHEN SQL1.RESPONSABLE = 'MASIVO_CORPORATIVO' THEN 1 END) MASIVO,
COUNT(CASE
WHEN SQL1.RESPONSABLE = 'ACCESO_EMPRESARIALES' OR SQL1.RESPONSABLE = 'PROACTIVO' OR SQL1.RESPONSABLE = 'REACTIVO' THEN 1 END) NORMAL
FROM(
SELECT 
DISTINCT(fr_kpi_outsourcing1.TICKET),
semana_claro.semana SEMANA,
catalogo_areas_cnoc.responsable2 RESPONSABLE,
date_format(fr_kpi_outsourcing1.FECHA_CIERRE, "%Y") YEAR_,
date_format(fr_kpi_outsourcing1.FECHA_CIERRE, "%m")MES 
FROM `fr_kpi_outsourcing1` 
INNER JOIN semana_claro on semana_claro.fecha = date_format(fr_kpi_outsourcing1.FECHA_CIERRE, "%Y-%m-%d")
INNER JOIN catalogo_areas_cnoc on catalogo_areas_cnoc.nombre_area_claro=fr_kpi_outsourcing1.RESPONSABLE ) SQL1
GROUP BY SQL1.SEMANA,YEAR_,MES
ORDER BY SQL1.SEMANA DESC,YEAR_ DESC,MES"""
    return sql

def procesar_item_masiva(result):
    store_list = []
    for item in result:
            store_details = {"semana":None,"year":None,"mes":None,"falla_masiva":None,"masiva":None,"normal":None}
            store_details['semana'] = item[0]
            store_details['year'] = item[1]
            store_details['mes'] = item[2]
            store_details['falla_masiva'] = item[3]
            store_details['masiva'] = item[4]
            store_details['normal'] = item[5]
            store_list.append(store_details)
    return store_list
