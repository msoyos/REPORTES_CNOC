
from time import sleep
import db
from datetime import datetime
import re


def sql_script(r=1):
    if(r==1):
        #se actualiza todo a media noche de cada dia 
        sql="""  select  
    incident_id                                                                      AS sd,
    ticket,
    brief_description                                                                "PROBLEMA REPORTADO",
    "CATEGORÍA",
    probsummarym1.subcategory                                                        AS subcategoria,
    "ID SERVICIO",
    tg_enlace_destino                                                                AS ubicacion,
    "GRUPO WO",
    proveedor,
    "FECHA APERTURA"                                                                 AS "FECHA DE APERTURA",
    "FECHA CIERRE"                                                                   AS "FECHA DE CIERRE",
    company                                                                          AS cliente,
    "MES CIERRE",
    "AFECTACIÓN",
    responsable,
    assignment                                                                       AS "GRUPO ASIGNADO",
    resolved_group                                                                   AS "GRUPO QUE CERRO",
    iniciador                                                                        AS "COLABORADOR ASIGNADO",
    resolved_by                                                                      AS "COLABORADOR QUE CERRO",
    "Open",
    "Work In Progress",
    "Pending Vendor",
    "Pending Other",
    "Pending Customer",
    "WO Not Assigned",
    "WO Open",
    "WO Pending Supervisor",
    "WO Worker Assigned",
    "WO Pending Worker",
    "WO Work In Progress",
    "WO Pending Vendor",
    "WO Pending Other",
    "WO Resolved",
    "Resolved",
    "WO Pending Customer",
    "Monitoreo",
    "Otros",
    "Dictamen",
    tt_tk_min,
    tipo_servicio,
    pais                                                                             AS "PAIS CLARO",
    res_anal_code                                                                    AS "CODIGO DE CIERRE",
    resolution_code                                                                  AS "CODIGO DE RESOLUCION",
    tg_ttarearesp                                                                    AS "AREA RESPONSABLE",
    tg_ttservespecifico                                                              AS "SERVICIO ESPECIFICO",
    tg_ttresolucion                                                                  AS "RESOLUCION",
    to_date(to_char(systimestamp, 'DD/MM/YYYY HH24:MI:SS'), 'DD/MM/YYYY HH24:MI:SS') AS fecha_reporte,
    (
        SELECT
            to_date(to_char(closed_total, 'DD/MM/YYYY HH24:MI:SS'), 'DD/MM/YYYY HH24:MI:SS') - TO_DATE('01/01/4000 00:00:00', 'DD/MM/YYYY HH24:MI:SS')
        FROM
            clocksm1
        WHERE
                ticket = clocksm1.key_char
            AND name = 'Tiempo T1 de Atención. CNOC_MASIVO'
    )                                                                                AS "Tiempo T1. CNOC_MASIVO",
    (
        SELECT
            ( to_date(to_char(closed_total, 'DD/MM/YYYY HH24:MI:SS'), 'DD/MM/YYYY HH24:MI:SS') - TO_DATE('01/01/4000 00:00:00', 'DD/MM/YYYY HH24:MI:SS') ) *
            24
        FROM
            clocksm1
        WHERE
                ticket = clocksm1.key_char
            AND name = 'Tiempo T1 de Atención. CNOC_MASIVO'
    )                                                                                AS "Tiempo T1. CNOC_MASIVO (hor)",
    (
        SELECT
            ( to_date(to_char(closed_total, 'DD/MM/YYYY HH24:MI:SS'), 'DD/MM/YYYY HH24:MI:SS') - TO_DATE('01/01/4000 00:00:00', 'DD/MM/YYYY HH24:MI:SS') ) *
            24 * 24
        FROM
            clocksm1
        WHERE
                ticket = clocksm1.key_char
            AND name = 'Tiempo T1 de Atención. CNOC_MASIVO'
    )                                                                                AS "Tiempo T1. CNOC_MASIVO (min)"
FROM
    fr_kpi_outsourcing1,
    probsummarym1,
    probsummarym2
WHERE
        fr_kpi_outsourcing1.ticket = probsummarym1."NUMBER"
    AND probsummarym1."NUMBER" = probsummarym2."NUMBER"
        AND  probsummarym1.close_time  BETWEEN '16/08/22' AND '23/08/22'"""
    elif(r==2):
        # se actualiza lo del mes cada 12 horas 
        sql="""                                             
SELECT F. *, PM1.ASSIGNMENT  
FROM FR_KPI_OUTSOURCING1 F, PROBSUMMARYM1 PM1

WHERE 
 PM1."NUMBER"=F.TICKET 
 AND F."FECHA CIERRE" >= TO_DATE(TO_CHAR(ADD_MONTHS(SYSDATE, -1), 'DD/MM/YYYY' ), 'DD/MM/YYYY' )
AND  F."FECHA CIERRE" <= TO_DATE(TO_CHAR(SYSDATE, 'DD/MM/YYYY' ), 'DD/MM/YYYY' ) ORDER BY F."MES CIERRE" DESC;"""
    elif(r==3):
        # se actualiza lo del mes cada 20 minutos 
        sql="""SELECT F. *, PM1.ASSIGNMENT  
FROM FR_KPI_OUTSOURCING1 F, PROBSUMMARYM1 PM1

WHERE 
 PM1."NUMBER"=F.TICKET 
 AND F."FECHA CIERRE" >= TO_DATE(TO_CHAR(SYSDATE, 'DD/MM/YYYY' ), 'DD/MM/YYYY' )-1
		AND  F."FECHA CIERRE" <= TO_DATE(TO_CHAR(SYSDATE, 'DD/MM/YYYY' ), 'DD/MM/YYYY' )+1 
        order by F."FECHA CIERRE" desc"""
    return sql
        

def Actualizar_vista_fr_kpi_outsourcing1(sqltxt,job):
    print(datetime.now())
    r=db.select(sql_script(sqltxt))
    print(r) 
    
    vueltas=0
    lineas_update=0
    lineas_insert=0
    for item in r:
        
        #verificar si existe en base de datos, si existe eliminar he insetar de nuevo
        vueltas+=1
        print("-..."+str(vueltas))
        # validamos cambio fecha de cierre si cambia se actuliza la data , si no existe lo insertameos
        
        sql_validar=""" SELECT TICKET,FECHA_DE_APERTURA FROM `FR_KPI_OUTSOURCING1_` WHERE TICKET='"""+str(item[1])+"""' AND FECHA_DE_APERTURA='"""+str(item[9])+"""'"""
        res_validar = db.dbmysql(sql_validar)
        if item[2] ==None:
	        text=""
        else:
            text=item[2]
        a= re.sub("['""]"," ",text)
        
        if item[6] ==None:
	        txt=""
        else:
            txt=item[6]
        b=re.sub("['""]"," ",txt)
        
        if not res_validar:
            lineas_insert+=1 
           
            sql=f"""INSERT INTO FR_KPI_OUTSOURCING1_ VALUES ('"""+str(item[0])+"','"""+str(item[1])+"','"""+str(a)+"','"""+str(item[3])+"','"""+str(item[4])+"','"""+str(item[5])+"','"""+str(b)+"','"""+str(item[7])+"','"""+str(item[8])+"','"""+str(item[9])+"','"""+str(item[10])+"','"""+str(item[11])+"','"""+str(item[12])+"','"""+str(item[13])+"','"""+str(item[14])+"','"""+str(item[15])+"','"""+str(item[16])+"','"""+str(item[17])+"','"""+str(item[18])+"','"""+str(item[19])+"','"""+str(item[20])+"','"""+str(item[21])+"','"""+str(item[22])+"','"""+str(item[23])+"','"""+str(item[24])+"','"""+str(item[25])+"','"""+str(item[26])+"','"""+str(item[27])+"','"""+str(item[28])+"','"""+str(item[29])+"','"""+str(item[30])+"','"""+str(item[31])+"','"""+str(item[32])+"','"""+str(item[33])+"','"""+str(item[34])+"','"""+str(item[35])+"','"""+str(item[36])+"','"""+str(item[37])+"','"""+str(item[38])+"','"""+str(item[39])+"','"""+str(item[40])+"','"""+str(item[41])+"','"""+str(item[42])+"','"""+str(item[43])+"','"""+str(item[44])+"','"""+str(item[45])+"','"""+str(item[46])+"','"""+str(item[47])+"','"""+str(item[48])+"','"""+str(item[49])+"')"
            print(sql)
            res=db.dbmysql(sql,1)
        else:
            lineas_update+=1
            sql=""" UPDATE fr_kpi_outsourcing1_ SET `SD`='"""+str(item[0])+"""',TICKET='"""+str(item[1])+"""',PROBLEMA_REPORTADO='"""+str(a)+"""',CATEGORÍA='"""+str(item[3])+"""',SUBCATEGORIA='"""+str(item[4])+"""',ID_SERVICIO='"""+str(item[5])+"""',UBICACION='"""+str(b)+"""',GRUPO_WO='"""+str(item[7])+"""',PROVEEDOR='"""+str(item[8])+"""',FECHA_DE_APERTURA='"""+str(item[9])+"""',FECHA_DE_CIERRE='"""+str(item[10])+"""',CLIENTE='"""+str(item[11])+"""',MES_CIERRE='"""+str(item[12])+"""',AFECTACIÓN='"""+str(item[13])+"""',RESPONSABLE='"""+str(item[14])+"""',GRUPO_ASIGNADO='"""+str(item[15])+"""',GRUPO_QUE_CERRO='"""+str(item[16])+"""',COLABORADOR_ASIGNADO='"""+str(item[17])+"""',COLABORADOR_QUE_CERRO='"""+str(item[18])+"""',Open='"""+str(item[19])+"""',Work_In_Progress='"""+str(item[20])+"""',Pending_Vendor='"""+str(item[21])+"""',Pending_Other='"""+str(item[22])+"""',Pending_Customer='"""+str(item[23])+"""',WO_Not_Assigned='"""+str(item[24])+"""',WO_Open='"""+str(item[25])+"""',WO_Pending_Supervisor='"""+str(item[26])+"""',WO_Worker_Assigned='"""+str(item[27])+"""',WO_Pending_Worker='"""+str(item[28])+"""',WO_Work_In_Progress='"""+str(item[29])+"""',WO_Pending_Vendor='"""+str(item[30])+"""',WO_Pending_Other='"""+str(item[31])+"""',WO_Resolved='"""+str(item[32])+"""',Resolved='"""+str(item[33])+"""',WO_Pending_Customer='"""+str(item[34])+"""',Monitoreo='"""+str(item[35])+"""',Otros='"""+str(item[36])+"""',Dictamen='"""+str(item[37])+"""',TT_TK_MIN='"""+str(item[38])+"""',TIPO_SERVICIO='"""+str(item[39])+"""',PAIS_CLARO='"""+str(item[40])+"""',CODIGO_DE_CIERRE='"""+str(item[41])+"""',CODIGO_DE_RESOLUCION='"""+str(item[42])+"""',AREA_RESPONSABLE='"""+str(item[43])+"""',SERVICIO_ESPECIFICO='"""+str(item[44])+"""',RESOLUCION='"""+str(item[45])+"""',FECHA_REPORTE='"""+str(item[46])+"""',Tiempo_T1_CNOC_MASIVO='"""+str(item[47])+"""',Tiempo_T1_CNOC_MASIVO_hor='"""+str(item[48])+"""',Tiempo_1_CNOC_MASIVO_min='"""+str(item[49])+"""' WHERE TICKET='"""+str(item[1])+"""' AND FECHA_DE_APERTURA='"""+str(item[9])+"""'"""
            res=db.dbmysql(sql,2)
            print(sql)
        print(res)
        
        
    sql_log=""" INSERT INTO `log_actualizaciones`( `name_job`, `lineas_actualizadas`, `lineas_nuevas`) VALUES ('"""+str(job)+"""',"""+str(lineas_update)+""","""+str(lineas_insert)+""")""" 
    db.dbmysql(sql_log,1)   
      
    print(datetime.now())

Actualizar_vista_fr_kpi_outsourcing1(1,'job2')