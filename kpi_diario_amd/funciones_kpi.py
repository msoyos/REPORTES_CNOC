
from pydantic import BaseModel

class KPI_model(BaseModel):
    fecha : str
    fecha2 : str
    area:str
    
    class Config:
        schema_extra={
            "example":{
                "fecha":"2022-08-16",
                "fecha2":"2022-08-16",
                "area":"REACTIVO",
                
            }
        }
        
def catidad_de_tickets():
    sql="""
    SET @total:= (SELECT count(*) FROM fr_kpi_outsourcing1 WHERE FECHA_CIERRE BETWEEN '20220629' AND '20220630' );
    SELECT 
    catalogo_areas_cnoc.responsable2, 
    COUNT(*) c, 
    ROUND((COUNT(*) / @total * 100), 0) AS porcentaje,
    @total 
    FROM fr_kpi_outsourcing1 
    INNER JOIN catalogo_areas_cnoc ON catalogo_areas_cnoc.nombre_area_claro=fr_kpi_outsourcing1.RESPONSABLE 
    WHERE FECHA_CIERRE BETWEEN '20220629' AND '20220630' 
    GROUP BY catalogo_areas_cnoc.responsable2 
    ORDER BY c DESC;
    """
    return sql 
def areas_cnoc(areas_cnoc,tipo):
    #responsable="""tickets_formateados.responsable LIKE '%REACTIVO%' """
    if areas_cnoc=='REACTIVO' and tipo==1:
        responsable="""tickets_formateados.responsable LIKE '%REACTIVO%'
        
        """
    elif areas_cnoc=='REACTIVO' and tipo==2:
        responsable="""tickets_formateados.responsable IN ('REACTIVO_XT','REACTIVO','MASIVO_REACTIVO')"""
    elif areas_cnoc=='ACCESOS' and tipo==1 :
         responsable="""tickets_formateados.responsable LIKE '%ACCESO%' """
    elif areas_cnoc=='ACCESOS' and tipo==2:
        responsable="""tickets_formateados.responsable IN ('ACCESO_EMPRESARIAL')"""
    elif areas_cnoc=='PROACTIVO' and tipo==1:
        responsable="""tickets_formateados.responsable  LIKE'%PROACTIVO%'"""
    elif areas_cnoc=='PROACTIVO' and tipo==2:
        responsable="""tickets_formateados.responsable IN ('PROACTIVO')"""
    else:
        responsable="""tickets_formateados.responsable IN ('REACTIVO','MASIVO_REACTIVO','ACCESO_EMPRESARIALES','PROACTIVO')"""
    return responsable


def data_trasformada(d1,d2):
    sql="""
            SELECT *,
												 CASE 
												    WHEN MONTH_CIERRE = MES_CIERRE and YEAR_APERTURA = YEAR_CIERRE then 'TICKET ABIERTO Y CERRADO EN MISMO PERIODO' 
												                else 'TICKET ABIERTO Y CERRADO EN DISTINTO PERIODO' END VALIDACION_FECHA2
											FROM 
		            							(
		            								SELECT*, 
															CASE 
																WHEN T_RESOLUCION_AFECTACION_AND_SIN_AFECTACION_horas <=8 THEN 'T<=8 horas'
																WHEN T_RESOLUCION_AFECTACION_AND_SIN_AFECTACION_horas >8 THEN 'T>8 horas'
																ELSE NULL END T_8_HORAS_RESOLUCION_AFECTACION_AND_SIN_AFECTACION,
															CASE 
																WHEN T_RESOLUCION_AFECTACION_AND_SIN_AFECTACION_horas <=12 THEN 'T<=12 horas'
																WHEN T_RESOLUCION_AFECTACION_AND_SIN_AFECTACION_horas >12 THEN 'T>12 horas'
																ELSE NULL END T_12_HORAS_RESOLUCION_AFECTACION_AND_SIN_AFECTACION,
																-- VALIDACION SI LA ESCALACION A BO FUE CORRECTA
															CASE 
															    WHEN CATEGORÍA = 'DX - CLIENTE' then 'NO VALIDA' 
															    WHEN CATEGORÍA = 'DX - AFECTACION MASIVA' then 'NO VALIDA' 
															    WHEN CATEGORÍA = 'DX - BOLETA MAL ABIERTA' then 'NO VALIDA' 
															    else 'VALIDA' END  VALIDACION_ESCALADO_A_BO,
															  -- VALIDACION DE CATEGORIA SE DESCARTA DX Y AFECTACION MASIVO
															CASE
		    													WHEN CATEGORÍA <> 'DX - AFECTACION MASIVA' then 'SIN DX AFECTACION MASIVA' else 'CON DX AFECTACION MASIVA' 
																END VALIDACION_CATEGORIA,
															YEAR(FECHA_DE_CIERRE) YEAR_CIERRE,
															MONTH(FECHA_DE_CIERRE) MONTH_CIERRE,
															YEAR(FECHA_DE_APERTURA) YEAR_APERTURA,
															-- VALIDACION DE FECHAS
															CASE 
																WHEN MES_CIERRE <> NULL AND YEAR(FECHA_DE_CIERRE) <> NULL THEN 'FECHA INVALIDA'
																ELSE 'FECHA VALIDA' END VALIDACION_FECHA
															 
														 FROM (
							            								SELECT *,
																					(T_RESOLUCION_AFECTACION_AND_SIN_AFECTACION_minutos/60) T_RESOLUCION_AFECTACION_AND_SIN_AFECTACION_horas												
																				 FROM (
							            								SELECT *,
							            										CASE
																					    WHEN T_RESOLUCION <= 30 then 't<=30 min' 
																					    WHEN T_RESOLUCION > 30 then 't>30 min' 
																					    else null END T_30_RESOLUCION,
																					CASE
																					    WHEN T_RESOLUCION <= 60 then 't<=60 min' 
																					    WHEN T_RESOLUCION > 60 then 't>60 min' 
																					    else null END T_60_RESOLUCION,
																					CASE
																					    WHEN T_RESOLUCION <= 120 then 't<=120 min' 
																					    WHEN T_RESOLUCION > 120 then 't>120 min' 
																					    else null END T_120_RESOLUCION,
																					-- PENDIENTE EN VERIFICAR SI, ES MASIVO O NO. PREGUNTAR CUANDO CUMPLE Y CUANDO NO Y QUE CAMPOS SON A COMPARA    
																					CASE 
                                                                                        WHEN ID_SERVICIO = '0'  AND  CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'
                                                                                        WHEN ID_SERVICIO = ' 0'  AND  CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'
                                                                                        WHEN ID_SERVICIO = ' '  AND  CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'
                                                                                        WHEN ID_SERVICIO = 'None'  AND  CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'
                                                                                        WHEN ID_SERVICIO LIKE '%F%' AND  FEMTOCELDA = 'FEMTOCELDA' AND  CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'
                                                                                        WHEN ID_SERVICIO LIKE '%DEFAULT%' AND  CATEGORÍA <>'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'
                                                                                        WHEN ID_SERVICIO LIKE '%MASIVO%'  AND  CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'
                                                                                        WHEN ID_SERVICIO LIKE 'ESC_HN_DEF001'  AND  CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'
                                                                                        WHEN ID_SERVICIO = 'XT - ACCESO EMPRESARIAL'  AND  CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'                                                                                                                
                                                                                    WHEN ID_SERVICIO = 'XT - ACCESO ACTIVOS'  AND  CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'                                                                                                                 
                                                                                    WHEN ID_SERVICIO = 'XT - ACCESO DATA_CENTER'  AND CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'                                                                                                                   
                                                                                    WHEN ID_SERVICIO = 'XT - DATOS'   AND  CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'                                                                                                                  
                                                                                    WHEN ID_SERVICIO = 'XT - INTERNET'  AND  CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'
                                                                                        ELSE 'VALIDO'	END VALIDACION_REINCIDENCIA,
																						
																					        Open+Work_In_Progress+Pending_Vendor+Pending_Other+WO_Open+WO_Not_Assigned+WO_Pending_Supervisor+WO_Worker_Assigned+WO_Pending_Worker+WO_Work_In_Progress+WO_Pending_Vendor+WO_Pending_Other+WO_Resolved+Resolved T_RESOLUCION_AFECTACION_AND_SIN_AFECTACION_minutos
																							
							            								FROM (
							            									SELECT *,
																						T_RESOLUCION_DX_AFECTACION_MASIVA+T_RESOLUCION_WO_PENDING_VENDOR+T_RESOLUCION_WO_PENDING_OTHER T_RESOLUCION												
																				FROM( 
																					SELECT *, 
																								CASE 
																								    WHEN  MASIVO='ASOCIADO A MASIVA' or MASIVO='MASIVA' then
																								        Open+Work_In_Progress+Pending_Vendor+Pending_Other+WO_Not_Assigned+WO_Resolved    
																								    ELSE
																								        Open+Work_In_Progress+Pending_Vendor+Pending_Other+WO_Not_Assigned+WO_Resolved+Resolved
																								        END T_RESOLUCION_DX_AFECTACION_MASIVA,
																								CASE 
																									 WHEN Upper(PROVEEDOR) ='UNKNOWN' and WO_Pending_Vendor>0 then WO_Pending_Vendor
																									 else 0 END T_RESOLUCION_WO_PENDING_VENDOR,
																								WO_Pending_Other T_RESOLUCION_WO_PENDING_OTHER 
																							FROM(
																								SELECT *, 
																									CASE 
																										WHEN  (RESPONSABLE = 'MASIVO_REACTIVO'  or 
																												RESPONSABLE = 'MASIVO_PROACTIVO' OR  
																												CATEGORÍA = 'DX - MASIVO' or 
																												GRUPO_ASIGNADO= 'CNOC_MASIVO') AND 
																												(RESPONSABLE <> 'MASIVO_CORPORATIVO') then 'ASOCIADO A MASIVA'
																										
																										WHEN  (RESPONSABLE <> 'MASIVO_REACTIVO' and 
																												RESPONSABLE <> 'MASIVO_PROACTIVO' and 
																												RESPONSABLE <> 'MASIVO_CORPORATIVO' and   
																												CATEGORÍA <> 'DX - MASIVO') and 
																												(GRUPO_ASIGNADO <> 'CNOC_MASIVO' AND 
																												RESPONSABLE = 'ACCESO_EMPRESARIAL' or 
																												RESPONSABLE = 'PROACTIVO' or 
																												RESPONSABLE = 'REACTIVO' OR RESPONSABLE = 'REACTIVO_XT')  then 'NO ASOCIADO A MASIVA'
																										WHEN  RESPONSABLE = 'MASIVO_CORPORATIVO' or ID_SERVICIO LIKE '%MASIVO%' THEN 'MASIVO' END MASIVO,
																										CASE 
																											WHEN SUBCATEGORIA = "CLIENTE" then "CLIENTE" else "CLARO" END ATRIBUCION,
																										CASE
																											WHEN TIPO_SERVICIO LIKE '%F%' then 'FEMTOCELDA' 
																											WHEN TIPO_SERVICIO NOT LIKE '%F%' then 'NO FEMTOCELDA' 
																											else NULL END FEMTOCELDA,
																										CASE
																											WHEN GRUPO_WO = 'None' then 'RESUELTO POR CNOC'  
																											WHEN GRUPO_WO <> 'None' then 'RESUELTO POR OTRAS AREAS' else null
																											END VALIDACION_RESOLUCION,
																										CASE 
																										    WHEN GRUPO_WO LIKE '%B.O%' then 'ESCALADO A BO' 
																										    WHEN GRUPO_WO LIKE '%SEGURIDAD%' then 'ESCALADO A BO' 
																										    WHEN GRUPO_WO LIKE '%GESTION DATOS SV%' then 'ESCALADO A BO' 
																										    WHEN GRUPO_WO LIKE '%WIMAX%' then 'ESCALADO A BO' 
																										    ELSE 'NO ESCALADO A BO' END ESCALADO_A_BO,
																										CASE 
																											when Open>0 then 'OPEN VALIDO' 
																											ELSE 'OPEN INVALIDO' END VALIDACION_OPEN,
																										CASE
																										    	WHEN  Open <=10 then "t<=10 min"
																												WHEN  Open > 10  then "t>10 min"
																										    ELSE '' END T_10_OPEN,
																									   CASE
																										    	WHEN  OPEN <=15 then "t<=15 min"
																												WHEN  OPEN > 15  then "t>15 min"
																										    ELSE '' END T_15_OPEN
																										
									 													FROM fr_kpi_outsourcing1_ WHERE FECHA_DE_CIERRE BETWEEN """+ str(d1)+""" AND """+ str(d2)+""")A 
																					)B
																					)C 
																		)D
																		)E 
																		)F 
    """
    return sql

def RESOLUCION_70(d1,d2,a):
    sql="""
        SELECT *,ROUND(PORCENTAJE_RESOLUCION_70)APROXIMADO, CONCAT(ROUND(PORCENTAJE_RESOLUCION_70), "%" ) APROXIMADO_T
        FROM (
                SELECT C.pais,RESOLUCION_70_G, RESOLUCION_70_P,((RESOLUCION_70_G / (RESOLUCION_70_G + RESOLUCION_70_P)) *100 ) PORCENTAJE_RESOLUCION_70
                FROM (
                                SELECT B.pais, SUM(RESOLUCION_70_1) RESOLUCION_70_G,SUM(RESOLUCION_70_2) RESOLUCION_70_P,(SUM(RESOLUCION_70_1)+SUM(RESOLUCION_70_2))TOTAL
                                FROM (
                                                SELECT
                                                A.pais,
                                                CASE
                                                         WHEN VALIDACION_RESOLUCION='RESUELTO POR CNOC' THEN CONTAR
                                                         ELSE 0 END RESOLUCION_70_1,
                                                CASE
                                                    WHEN VALIDACION_RESOLUCION='RESUELTO POR OTRAS AREAS' THEN CONTAR
                                                    ELSE 0
                                                    END RESOLUCION_70_2
                                                FROM (
                                                                SELECT tickets_formateados.pais_claro pais,tickets_formateados.VALIDACION_RESOLUCION,COUNT(*) AS CONTAR
                                                                FROM tickets_formateados
                                                                WHERE
                                                                
                                                                 tickets_formateados.TIPO_SERVICIO   NOT IN ('FEMTOCELDA','NO_CMDB','SERVICIO INTERNO')
                                                                AND  """+str(a)+"""
                                                                AND  tickets_formateados.FEMTOCELDA    IN ('NO FEMTOCELDA')
                                                                AND  tickets_formateados.MASIVO NOT IN ('MASIVO')    
                                                                GROUP BY tickets_formateados.VALIDACION_RESOLUCION,tickets_formateados.pais_claro
                                                                ) A
                                                ) B  GROUP BY B.pais ORDER BY FIELD(B.pais,'GT','SV','HN','NI','CR','PA')
                                ) C
                ) D
    
    """
    return sql


def ESCALADO_A_BO(d1,d2,a):
    
    sql="""
    SELECT *,ROUND(PORCENTAJE_BO)APROXIMADO, CONCAT(ROUND(PORCENTAJE_BO), "%" ) APROXIMADO_BO_T
        FROM (
		SELECT C.pais,ESCALADO_G, ESCALADO_P,((ESCALADO_G / (ESCALADO_G + ESCALADO_P)) *100 ) PORCENTAJE_BO
		FROM (
				SELECT B.pais, SUM(ESCALADO_1) ESCALADO_G, SUM(ESCALADO_2) ESCALADO_P,(SUM(ESCALADO_1)+SUM(ESCALADO_2)) TOTAL
				FROM (
						SELECT
						A.pais,
						CASE 
							WHEN ESCALADO_A_BO='NO ESCALADO A BO' THEN CONTAR 
							ELSE 0 END ESCALADO_1, 
						CASE 
							WHEN ESCALADO_A_BO='ESCALADO A BO' THEN CONTAR 
							ELSE 0 END ESCALADO_2
						FROM (
								SELECT tickets_formateados.pais_claro pais,tickets_formateados.ESCALADO_A_BO, COUNT(*) AS CONTAR
								FROM tickets_formateados
								WHERE
								 tickets_formateados.TIPO_SERVICIO NOT IN ('FEMTOCELDA','NO_CMDB','SERVICIO INTERNO') 
								 AND """+str(a)+"""  
                                 AND tickets_formateados.FEMTOCELDA IN ('NO FEMTOCELDA') 
								 AND tickets_formateados.MASIVO IN ('NO ASOCIADO A MASIVA') 
								 AND tickets_formateados.ATRIBUCION IN ('CLARO') 
								 AND tickets_formateados.VALIDACION_ESCALADO_A_BO 
         ='VALIDA'
								GROUP BY tickets_formateados.ESCALADO_A_BO,tickets_formateados.pais_claro
								) A
						) B GROUP BY B.pais
				) C
		) D
    """
    return sql

def OPEN_10(d1,d2,a):
    sql="""
        SELECT *,ROUND(PORCENTAJE_OPEN_10)APROXIMADO, CONCAT(ROUND(PORCENTAJE_OPEN_10), "%" ) APROXIMADO_OPEN_10_T
            FROM (
		SELECT
			C.pais,OPEN_10_G, OPEN_10_P,((OPEN_10_G / (OPEN_10_G + OPEN_10_P)) *100 ) PORCENTAJE_OPEN_10
			 
		FROM (
				SELECT 
				B.pais, SUM(T_10_OPEN_1) OPEN_10_G, SUM(T_10_OPEN_2) OPEN_10_P,(SUM(T_10_OPEN_1)+SUM(T_10_OPEN_2)) TOTAL
				FROM (
						SELECT 
						A.pais,
						CASE 
							WHEN T_10_OPEN='t<=10 min' THEN CONTAR 
							ELSE 0 END T_10_OPEN_1, 
						CASE 
							WHEN T_10_OPEN='t>10 min' THEN CONTAR 
							ELSE 0 END T_10_OPEN_2
						FROM ( 
								SELECT tickets_formateados.pais_claro pais,tickets_formateados.T_10_OPEN,COUNT(*) AS CONTAR
								                                                FROM tickets_formateados
								                                                
								                                                WHERE
								                                                 tickets_formateados.TIPO_SERVICIO    NOT IN ('FEMTOCELDA','NO_CMDB','SERVICIO INTERNO')
								                                                AND  tickets_formateados.VALIDACION_OPEN='OPEN VALIDO'
								                                                AND  """+str(a)+"""
								                                                AND  tickets_formateados.FEMTOCELDA     IN ('NO FEMTOCELDA')
								                                                AND  tickets_formateados.MASIVO NOT IN ('MASIVO')
								                                                GROUP BY tickets_formateados.T_10_OPEN,tickets_formateados.pais_claro
								                                                ) A
						) B GROUP BY B.pais
				) C
		) D
    """
    return sql

def OPEN_15(d1,d2,a):
    sql="""
        SELECT *,
        ROUND(PORCENTAJE_OPEN_15)APROXIMADO, CONCAT(ROUND(PORCENTAJE_OPEN_15), "%" ) APROXIMADO_OPEN_15_T
        FROM (
            SELECT
            C.pais,OPEN_15_G, OPEN_15_P,((OPEN_15_G / (OPEN_15_G + OPEN_15_P)) *100 ) PORCENTAJE_OPEN_15 
            FROM (
            SELECT 
            B.pais, SUM(T_15_OPEN_1) OPEN_15_G, SUM(T_15_OPEN_2) OPEN_15_P,(SUM(T_15_OPEN_1)+SUM(T_15_OPEN_2)) TOTAL
            FROM (
                SELECT
                A.pais, 
                CASE 
                    WHEN T_15_OPEN='t<=15 min' THEN CONTAR 
                    ELSE 0 END T_15_OPEN_1, 
                CASE WHEN T_15_OPEN='t>15 min' THEN CONTAR ELSE 0 
                END T_15_OPEN_2
                FROM (

                        SELECT tickets_formateados.pais_claro pais,tickets_formateados.T_15_OPEN,COUNT(*) AS CONTAR
                        FROM tickets_formateados
                        WHERE
                         tickets_formateados.TIPO_SERVICIO    NOT IN ('FEMTOCELDA','NO_CMDB','SERVICIO INTERNO')
                        AND  tickets_formateados.VALIDACION_OPEN='OPEN VALIDO'
                        AND  """+str(a)+"""
                        AND  tickets_formateados.FEMTOCELDA     IN ('NO FEMTOCELDA')
                        AND  tickets_formateados.MASIVO NOT IN ('MASIVO')
                        GROUP BY tickets_formateados.T_15_OPEN,tickets_formateados.pais_claro
                    ) A 
                ) B GROUP BY B.pais
            ) C
    )DATOS
    """
    return sql

def SOLUCION_30(d1,d2,a):
    sql="""
        SELECT *,
    ROUND(PORCENTAJE_SOLUCION_30)APROXIMADO, CONCAT(ROUND(PORCENTAJE_SOLUCION_30), "%" ) APROXIMADO_SOLUCION_30_T
    FROM (
            SELECT
            C.pais,T_30_RESOLUCION_G, T_30_RESOLUCION_P,((T_30_RESOLUCION_G / (T_30_RESOLUCION_G + T_30_RESOLUCION_P)) *100 ) PORCENTAJE_SOLUCION_30 
            FROM (
    SELECT B.pais, SUM(T_30_RESOLUCION_1) T_30_RESOLUCION_G, SUM(T_30_RESOLUCION_2) T_30_RESOLUCION_P,(SUM(T_30_RESOLUCION_1)+SUM(T_30_RESOLUCION_2)) TOTAL 
    FROM(
    SELECT 
    A.pais,
    CASE
                                    WHEN T_30_RESOLUCION='t<=30 min' THEN CONTAR
                                    ELSE 0
                                    END T_30_RESOLUCION_1,
                                    CASE
                                    WHEN T_30_RESOLUCION='t>30 min' THEN CONTAR
                                    ELSE 0
                                    END T_30_RESOLUCION_2
                                    FROM (
            SELECT tickets_formateados.pais_claro pais,tickets_formateados.T_30_RESOLUCION,COUNT(*) AS CONTAR
            FROM tickets_formateados
            
            WHERE
             tickets_formateados.TIPO_SERVICIO    NOT IN ('FEMTOCELDA','NO_CMDB','SERVICIO INTERNO')
            
            AND  """+str(a)+"""
            AND  tickets_formateados.FEMTOCELDA     IN ('NO FEMTOCELDA')
            AND  tickets_formateados.MASIVO IN ('NO ASOCIADO A MASIVA')
            GROUP BY tickets_formateados.T_30_RESOLUCION,tickets_formateados.pais_claro)A 
            ) B GROUP BY B.pais
            ) C
    )D
    """
    return sql

def SOLUCION_60(d1, d2,a):
    sql="""
        SELECT 
    *,
    ROUND(PORCENTAJE_SOLUCION_60) APROXIMADO, CONCAT(ROUND(PORCENTAJE_SOLUCION_60), "%" ) APROXIMADO_SOLUCION_60_T
    FROM (
            SELECT
            C.pais,T_60_RESOLUCION_G, T_60_RESOLUCION_P,((T_60_RESOLUCION_G / (T_60_RESOLUCION_G + T_60_RESOLUCION_P)) *100 ) PORCENTAJE_SOLUCION_60  
            FROM ( 
            SELECT B.pais,SUM(T_60_RESOLUCION_1) T_60_RESOLUCION_G, SUM(T_60_RESOLUCION_2) T_60_RESOLUCION_P,(SUM(T_60_RESOLUCION_1)+SUM(T_60_RESOLUCION_2)) TOTAL 
            FROM(
                    SELECT A.pais,CASE
                                            WHEN T_60_RESOLUCION='t<=60 min' THEN CONTAR
                                            ELSE 0
                                            END T_60_RESOLUCION_1,
                                            CASE
                                            WHEN T_60_RESOLUCION='t>60 min' THEN CONTAR
                                            ELSE 0
                                            END T_60_RESOLUCION_2
                                            FROM (
                    SELECT tickets_formateados.pais_claro pais,tickets_formateados.T_60_RESOLUCION,COUNT(*) AS CONTAR
                    FROM tickets_formateados
                    
                    WHERE
                    tickets_formateados.TIPO_SERVICIO    NOT IN ('FEMTOCELDA','NO_CMDB','SERVICIO INTERNO')
                    
                    AND  """+str(a)+"""
                    AND  tickets_formateados.FEMTOCELDA     IN ('NO FEMTOCELDA')
                    AND  tickets_formateados.MASIVO IN ('NO ASOCIADO A MASIVA')
                    GROUP BY tickets_formateados.T_60_RESOLUCION,tickets_formateados.pais_claro
                    )A 
                    ) B GROUP BY B.pais
            ) C
    ) D
    """
    return sql

def SOLUCION_120(d1,d2,a):
    sql=""" SELECT 
    *,
    ROUND(PORCENTAJE_SOLUCION_120) APROXIMADO, CONCAT(ROUND(PORCENTAJE_SOLUCION_120), "%" ) APROXIMADO_SOLUCION_120_T
    FROM (
            SELECT
            C.pais,T_120_RESOLUCION_G, T_120_RESOLUCION_P,((T_120_RESOLUCION_G / (T_120_RESOLUCION_G + T_120_RESOLUCION_P)) *100 ) PORCENTAJE_SOLUCION_120  
            FROM ( 
            SELECT B.pais,SUM(T_120_RESOLUCION_1) T_120_RESOLUCION_G, SUM(T_120_RESOLUCION_2) T_120_RESOLUCION_P,(SUM(T_120_RESOLUCION_1)+SUM(T_120_RESOLUCION_2)) TOTAL 
            FROM(
                    SELECT A.pais,CASE
                                            WHEN T_120_RESOLUCION='t<=120 min' THEN CONTAR
                                            ELSE 0
                                            END T_120_RESOLUCION_1,
                                            CASE
                                            WHEN T_120_RESOLUCION='t>120 min' THEN CONTAR
                                            ELSE 0
                                            END T_120_RESOLUCION_2
                                            FROM (
                    SELECT tickets_formateados.pais_claro pais,tickets_formateados.T_120_RESOLUCION,COUNT(*) AS CONTAR
                    FROM tickets_formateados
                    
                    WHERE
                    tickets_formateados.TIPO_SERVICIO    NOT IN ('FEMTOCELDA','NO_CMDB','SERVICIO INTERNO')
                    
                    AND  """+str(a)+"""
                    AND  tickets_formateados.FEMTOCELDA     IN ('NO FEMTOCELDA')
                    AND  tickets_formateados.MASIVO IN ('NO ASOCIADO A MASIVA')
                    GROUP BY tickets_formateados.T_120_RESOLUCION,tickets_formateados.pais_claro)A 
                    ) B GROUP BY B.pais
            ) C
    ) D """
    return sql

def SOLUCION_8H(d1,d2,a):
    sql=""" SELECT 
        *,
        ROUND(PORCENTAJE_SOLUCION_8_H) APROXIMADO, CONCAT(ROUND(PORCENTAJE_SOLUCION_8_H), "%" ) APROXIMADO_SOLUCION_8_H_T
        FROM (
                SELECT
                C.pais,T_8_H_RESOLUCION_G, T_8_H_RESOLUCION_P,((T_8_H_RESOLUCION_G / (T_8_H_RESOLUCION_G + T_8_H_RESOLUCION_P)) *100 ) PORCENTAJE_SOLUCION_8_H  
                FROM ( 
                SELECT B.pais,SUM(T_8_HORAS_1) T_8_H_RESOLUCION_G, SUM(T_8_HORAS_2) T_8_H_RESOLUCION_P,(SUM(T_8_HORAS_1)+SUM(T_8_HORAS_2)) TOTAL 
                FROM(
                        SELECT A.pais,CASE
                                            WHEN T_8_HORAS_RESOLUCION_AFECTACION_AND_SIN_AFECTACION='t<=8 horas' THEN CONTAR   
                                            ELSE 0
                                            END T_8_HORAS_1,
                                            CASE
                                            WHEN T_8_HORAS_RESOLUCION_AFECTACION_AND_SIN_AFECTACION='t>8 horas' THEN CONTAR    
                                            ELSE 0
                                            END T_8_HORAS_2
                                            FROM (
                    SELECT tickets_formateados.pais_claro pais,tickets_formateados.T_8_HORAS_RESOLUCION_AFECTACION_AND_SIN_AFECTACION,COUNT(*) AS CONTAR
                    FROM tickets_formateados
                    
                    WHERE
                    tickets_formateados.TIPO_SERVICIO    NOT IN ('FEMTOCELDA','NO_CMDB','SERVICIO INTERNO')
                    AND  tickets_formateados.AFECTACIÓN='CAIDA TOTAL'
                    AND  """+str(a)+"""
                    AND  tickets_formateados.FEMTOCELDA     IN ('NO FEMTOCELDA')
                    AND  tickets_formateados.MASIVO IN ('NO ASOCIADO A MASIVA')
                    GROUP BY tickets_formateados.T_8_HORAS_RESOLUCION_AFECTACION_AND_SIN_AFECTACION,tickets_formateados.pais_claro)A 
                        ) B GROUP BY B.pais
                ) C
        ) D """
    return sql

def SOLUCION_12H(d1,d2,a):
    sql=""" 
                SELECT 
        *,
        ROUND(PORCENTAJE_SOLUCION_12_H) APROXIMADO, CONCAT(ROUND(PORCENTAJE_SOLUCION_12_H), "%" ) APROXIMADO_SOLUCION_12_H_T
        FROM (
                SELECT
                C.pais,T_12_H_RESOLUCION_G, T_12_H_RESOLUCION_P,((T_12_H_RESOLUCION_G / (T_12_H_RESOLUCION_G + T_12_H_RESOLUCION_P)) *100 ) PORCENTAJE_SOLUCION_12_H  
                FROM ( 
                SELECT B.pais,SUM(T_12_HORAS_1) T_12_H_RESOLUCION_G, SUM(T_12_HORAS_2) T_12_H_RESOLUCION_P,(SUM(T_12_HORAS_1)+SUM(T_12_HORAS_2)) TOTAL 
                FROM(
                        SELECT A.pais,
                        CASE
                                                                                        WHEN T_12_HORAS_RESOLUCION_AFECTACION_AND_SIN_AFECTACION='t<=12 horas' THEN CONTAR 
                                                                                        ELSE 0
                                                                                        END T_12_HORAS_1,
                                                                                        CASE
                                                                                        WHEN T_12_HORAS_RESOLUCION_AFECTACION_AND_SIN_AFECTACION='t>12 horas' THEN CONTAR  
                                                                                        ELSE 0
                                                                                        END T_12_HORAS_2
                                                                                        FROM (
                                        SELECT tickets_formateados.pais_claro pais,tickets_formateados.T_12_HORAS_RESOLUCION_AFECTACION_AND_SIN_AFECTACION,COUNT(*) AS CONTAR
                                        FROM tickets_formateados
                                        
                                        WHERE
                                        tickets_formateados.TIPO_SERVICIO    NOT IN ('FEMTOCELDA','NO_CMDB','SERVICIO INTERNO')
                                        AND  tickets_formateados.AFECTACIÓN NOT IN ('CAIDA TOTAL')
                                        AND  """+str(a)+"""
                                        AND  tickets_formateados.FEMTOCELDA     IN ('NO FEMTOCELDA')
                                        AND  tickets_formateados.MASIVO IN ('NO ASOCIADO A MASIVA')
                                        GROUP BY tickets_formateados.T_12_HORAS_RESOLUCION_AFECTACION_AND_SIN_AFECTACION,tickets_formateados.pais_claro)A 
                        ) B GROUP BY B.pais
                ) C
        ) D
            """
    return sql
def calculos(tickets_g,tickets_p,porcentaje):
    sql ="""
        		SELECT 
			*, 
			CASE 
				WHEN JUSTIFICAR_P>0 THEN PORCENTAJE_GANAR - P_APROXIMADO
				ELSE '' END JUSTIFICAR_P,
					CASE 
				WHEN JUSTIFICAR_R>0 THEN PORCENTAJE_GANAR - R_APROXIMADO
				ELSE '' END JUSTIFICAR_R,
					CASE 
				WHEN JUSTIFICAR_A>0 THEN PORCENTAJE_GANAR - A_APROXIMADO
				ELSE '' END JUSTIFICAR_A
			
			FROM (
			SELECT 
			*, 
			CASE 
				 WHEN P_APROXIMADO <"""+str(porcentaje)+""" THEN ROUND((((SUMA_PROACTIVO*"""+str(porcentaje)+""")/100)/1)-PROACTIVO_G)
					  	ELSE '' END JUSTIFICAR_P,
			CASE 
				 WHEN R_APROXIMADO <"""+str(porcentaje)+""" THEN ROUND((((SUMA_REACTIVO*"""+str(porcentaje)+""")/100)/1)-REACTIVO_G)
					  	ELSE '' END JUSTIFICAR_R,
			CASE 
				 WHEN A_APROXIMADO <"""+str(porcentaje)+""" THEN ROUND((((SUMA_ACCEOSO*"""+str(porcentaje)+""")/100)/1)-ACCESOS_G)
					  	ELSE '' END JUSTIFICAR_A,
			"""+str(porcentaje)+""" PORCENTAJE_GANAR
				
			FROM (
		   SELECT 
			*,PROACTIVO_G+PROACTIVO_P SUMA_PROACTIVO,REACTIVO_G+REACTIVO_P SUMA_REACTIVO,ACCESOS_G+ACCESOS_P SUMA_ACCEOSO
			
			FROM (
			SELECT
                pais,
					 sum("""+str(tickets_g)+"""_PROACTIVO) PROACTIVO_G , sum("""+str(tickets_p)+"""_PROACTIVO) PROACTIVO_P , SUM(APROXIMADO_PROACTIVO) P_APROXIMADO,
                sum("""+str(tickets_g)+"""_REACTIVO) REACTIVO_G , sum("""+str(tickets_p)+"""_REACTIVO) REACTIVO_P, SUM(APROXIMADO_REACTIVO) R_APROXIMADO,
                sum("""+str(tickets_g)+"""_ACCESOS) ACCESOS_G , sum("""+str(tickets_p)+"""_ACCESOS) ACCESOS_P,SUM(APROXIMADO_ACCESOS) A_APROXIMADO
        FROM (
 		  SELECT
        pais,
        CASE
        WHEN pais ="GT" AND PROACTIVO="PROACTIVO" THEN """+str(tickets_g)+"""
        WHEN pais ="SV" AND PROACTIVO="PROACTIVO" THEN """+str(tickets_g)+"""
        WHEN pais ="HN" AND PROACTIVO="PROACTIVO" THEN """+str(tickets_g)+"""
        WHEN pais ="NI" AND PROACTIVO="PROACTIVO" THEN """+str(tickets_g)+"""
        WHEN pais ="CR" AND PROACTIVO="PROACTIVO" THEN """+str(tickets_g)+"""
        WHEN pais ="PA" AND PROACTIVO="PROACTIVO" THEN """+str(tickets_g)+"""
        ELSE 0 END """+str(tickets_g)+"""_PROACTIVO,
        CASE
        WHEN pais ="GT" AND PROACTIVO="PROACTIVO" THEN """+str(tickets_p)+"""
        WHEN pais ="SV" AND PROACTIVO="PROACTIVO" THEN """+str(tickets_p)+"""
        WHEN pais ="HN" AND PROACTIVO="PROACTIVO" THEN """+str(tickets_p)+"""
        WHEN pais ="NI" AND PROACTIVO="PROACTIVO" THEN """+str(tickets_p)+"""
        WHEN pais ="CR" AND PROACTIVO="PROACTIVO" THEN """+str(tickets_p)+"""
        WHEN pais ="PA" AND PROACTIVO="PROACTIVO" THEN """+str(tickets_p)+"""
        ELSE 0 END """+str(tickets_p)+"""_PROACTIVO,
        CASE
        WHEN pais ="GT" AND PROACTIVO="PROACTIVO" THEN APROXIMADO
        WHEN pais ="SV" AND PROACTIVO="PROACTIVO" THEN APROXIMADO
        WHEN pais ="HN" AND PROACTIVO="PROACTIVO" THEN APROXIMADO
        WHEN pais ="NI" AND PROACTIVO="PROACTIVO" THEN APROXIMADO
        WHEN pais ="CR" AND PROACTIVO="PROACTIVO" THEN APROXIMADO
        WHEN pais ="PA" AND PROACTIVO="PROACTIVO" THEN APROXIMADO
        ELSE 0 END APROXIMADO_PROACTIVO,
        CASE
        WHEN pais ="GT" AND PROACTIVO="REACTIVO" THEN """+str(tickets_g)+"""
        WHEN pais ="SV" AND PROACTIVO="REACTIVO" THEN """+str(tickets_g)+"""
        WHEN pais ="HN" AND PROACTIVO="REACTIVO" THEN """+str(tickets_g)+"""
        WHEN pais ="NI" AND PROACTIVO="REACTIVO" THEN """+str(tickets_g)+"""
        WHEN pais ="CR" AND PROACTIVO="REACTIVO" THEN """+str(tickets_g)+"""
        WHEN pais ="PA" AND PROACTIVO="REACTIVO" THEN """+str(tickets_g)+"""
        ELSE 0
        END """+str(tickets_g)+"""_REACTIVO,
        CASE
        WHEN pais ="GT" AND PROACTIVO="REACTIVO" THEN """+str(tickets_p)+"""
        WHEN pais ="SV" AND PROACTIVO="REACTIVO" THEN """+str(tickets_p)+"""
        WHEN pais ="HN" AND PROACTIVO="REACTIVO" THEN """+str(tickets_p)+"""
        WHEN pais ="NI" AND PROACTIVO="REACTIVO" THEN """+str(tickets_p)+"""
        WHEN pais ="CR" AND PROACTIVO="REACTIVO" THEN """+str(tickets_p)+"""
        WHEN pais ="PA" AND PROACTIVO="REACTIVO" THEN """+str(tickets_p)+"""
        ELSE 0
        END """+str(tickets_p)+"""_REACTIVO,
        CASE
        WHEN pais ="GT" AND PROACTIVO="REACTIVO" THEN APROXIMADO
        WHEN pais ="SV" AND PROACTIVO="REACTIVO" THEN APROXIMADO
        WHEN pais ="HN" AND PROACTIVO="REACTIVO" THEN APROXIMADO
        WHEN pais ="NI" AND PROACTIVO="REACTIVO" THEN APROXIMADO
        WHEN pais ="CR" AND PROACTIVO="REACTIVO" THEN APROXIMADO
        WHEN pais ="PA" AND PROACTIVO="REACTIVO" THEN APROXIMADO
        ELSE 0
        END APROXIMADO_REACTIVO,
		  CASE
        WHEN pais ="GT" AND PROACTIVO="ACCESOS" THEN """+str(tickets_g)+"""
        WHEN pais ="SV" AND PROACTIVO="ACCESOS" THEN """+str(tickets_g)+"""
        WHEN pais ="HN" AND PROACTIVO="ACCESOS" THEN """+str(tickets_g)+"""
        WHEN pais ="NI" AND PROACTIVO="ACCESOS" THEN """+str(tickets_g)+"""
        WHEN pais ="CR" AND PROACTIVO="ACCESOS" THEN """+str(tickets_g)+"""
        WHEN pais ="PA" AND PROACTIVO="ACCESOS" THEN """+str(tickets_g)+"""
        ELSE 0
                END """+str(tickets_g)+"""_ACCESOS,
        CASE
        WHEN pais ="GT" AND PROACTIVO="ACCESOS" THEN """+str(tickets_p)+"""
        WHEN pais ="SV" AND PROACTIVO="ACCESOS" THEN """+str(tickets_p)+"""
        WHEN pais ="HN" AND PROACTIVO="ACCESOS" THEN """+str(tickets_p)+"""
        WHEN pais ="NI" AND PROACTIVO="ACCESOS" THEN """+str(tickets_p)+"""
        WHEN pais ="CR" AND PROACTIVO="ACCESOS" THEN """+str(tickets_p)+"""
        WHEN pais ="PA" AND PROACTIVO="ACCESOS" THEN """+str(tickets_p)+"""
        ELSE 0
        END """+str(tickets_p)+"""_ACCESOS,
        CASE
        WHEN pais ="GT" AND PROACTIVO="ACCESOS" THEN APROXIMADO
        WHEN pais ="SV" AND PROACTIVO="ACCESOS" THEN APROXIMADO
        WHEN pais ="HN" AND PROACTIVO="ACCESOS" THEN APROXIMADO
        WHEN pais ="NI" AND PROACTIVO="ACCESOS" THEN APROXIMADO
        WHEN pais ="CR" AND PROACTIVO="ACCESOS" THEN APROXIMADO
        WHEN pais ="PA" AND PROACTIVO="ACCESOS" THEN APROXIMADO
        ELSE 0
        END APROXIMADO_ACCESOS
                FROM(
    
    """
    return sql
def pivot_porcentaje():
    sql="""
    
        SELECT 
            pais,sum(PROACTIVO_) PROACTIVO , sum(REACTIVO_) REACTIVO, sum(ACCESOS_) ACCESOS
        FROM (
        SELECT
        pais, 
    CASE 
        WHEN pais ="GT" AND PROACTIVO="PROACTIVO" THEN APROXIMADO
        WHEN pais ="SV" AND PROACTIVO="PROACTIVO" THEN APROXIMADO
        WHEN pais ="HN" AND PROACTIVO="PROACTIVO" THEN APROXIMADO
        WHEN pais ="NI" AND PROACTIVO="PROACTIVO" THEN APROXIMADO
        WHEN pais ="CR" AND PROACTIVO="PROACTIVO" THEN APROXIMADO
        WHEN pais ="PA" AND PROACTIVO="PROACTIVO" THEN APROXIMADO
        ELSE 0
            END PROACTIVO_,
            CASE 
        WHEN pais ="GT" AND PROACTIVO="REACTIVO" THEN APROXIMADO
        WHEN pais ="SV" AND PROACTIVO="REACTIVO" THEN APROXIMADO
        WHEN pais ="HN" AND PROACTIVO="REACTIVO" THEN APROXIMADO
        WHEN pais ="NI" AND PROACTIVO="REACTIVO" THEN APROXIMADO
        WHEN pais ="CR" AND PROACTIVO="REACTIVO" THEN APROXIMADO
        WHEN pais ="PA" AND PROACTIVO="REACTIVO" THEN APROXIMADO
        ELSE 0
            END REACTIVO_,
            CASE 
        WHEN pais ="GT" AND PROACTIVO="ACCESOS" THEN APROXIMADO
        WHEN pais ="SV" AND PROACTIVO="ACCESOS" THEN APROXIMADO
        WHEN pais ="HN" AND PROACTIVO="ACCESOS" THEN APROXIMADO
        WHEN pais ="NI" AND PROACTIVO="ACCESOS" THEN APROXIMADO
        WHEN pais ="CR" AND PROACTIVO="ACCESOS" THEN APROXIMADO
        WHEN pais ="PA" AND PROACTIVO="ACCESOS" THEN APROXIMADO
        ELSE 0
            END ACCESOS_
            
        FROM (
    """
    return sql

def pivot_procentaje_AS(): 
    # ) A ) b GROUP BY pais ORDER BY FIELD(pais,'GT','SV','HN','NI','CR','PA')
    sql="""
    
     ) A ) b GROUP BY pais ORDER BY FIELD(pais,'GT','SV','HN','NI','CR','PA')) C ) D )E
    """
    return sql

def pivot_reincidencia(d1,d2):
    sql="""  WITH
            tickets_formateados AS (
             SELECT *,
                                                                                                 CASE
                                                                                                    WHEN MONTH_CIERRE = MES_CIERRE and YEAR_APERTURA = YEAR_CIERRE then 'TICKET ABIERTO Y CERRADO EN MISMO PERIODO'
                                                                                                                else 'TICKET ABIERTO Y CERRADO EN DISTINTO PERIODO' END VALIDACION_FECHA2
                                                                                        FROM
                                                                                (
                                                                                        SELECT*,
                                                                                                                        CASE
                                                                                                                                WHEN T_RESOLUCION_AFECTACION_AND_SIN_AFECTACION_horas <=8 THEN 'T<=8 horas'
                                                                                                                                WHEN T_RESOLUCION_AFECTACION_AND_SIN_AFECTACION_horas >8 THEN 'T>8 horas'
                                                                                                                                ELSE NULL END T_8_HORAS_RESOLUCION_AFECTACION_AND_SIN_AFECTACION,
                                                                                                                        CASE
                                                                                                                                WHEN T_RESOLUCION_AFECTACION_AND_SIN_AFECTACION_horas <=12 THEN 'T<=12 horas'
                                                                                                                                WHEN T_RESOLUCION_AFECTACION_AND_SIN_AFECTACION_horas >12 THEN 'T>12 horas'
                                                                                                                                ELSE NULL END T_12_HORAS_RESOLUCION_AFECTACION_AND_SIN_AFECTACION,
                                                                                                                                -- VALIDACION SI LA ESCALACION A BO FUE CORRECTA
                                                                                                                        CASE
                                                                                                                            WHEN CATEGORÍA = 'DX - CLIENTE' then 'NO VALIDA'
                                                                                                                            WHEN CATEGORÍA = 'DX - AFECTACION MASIVA' then 'NO VALIDA'
                                                                                                                            WHEN CATEGORÍA = 'DX - BOLETA MAL ABIERTA' then 'NO VALIDA'
                                                                                                                            else 'VALIDA' END  VALIDACION_ESCALADO_A_BO,
                                                                                                                          -- VALIDACION DE CATEGORIA SE DESCARTA DX Y AFECTACION MASIVO
                                                                                                                        CASE
                                                                                                                        WHEN CATEGORÍA <> 'DX - AFECTACION MASIVA' then 'SIN DX AFECTACION MASIVA' else 'CON DX AFECTACION MASIVA'
                                                                                                                                END VALIDACION_CATEGORIA,
                                                                                                                        YEAR(FECHA_DE_CIERRE) YEAR_CIERRE,
                                                                                                                        MONTH(FECHA_DE_CIERRE) MONTH_CIERRE,
                                                                                                                        YEAR(FECHA_DE_APERTURA) YEAR_APERTURA,
                                                                                                                        -- VALIDACION DE FECHAS
                                                                                                                        CASE
                                                                                                                                WHEN MES_CIERRE <> NULL AND YEAR(FECHA_DE_CIERRE) <> NULL THEN 'FECHA INVALIDA'
                                                                                                                                ELSE 'FECHA VALIDA' END VALIDACION_FECHA

                                                                                                                 FROM (
                                                                                                                                SELECT *,     
                                                                                                                                             (T_RESOLUCION_AFECTACION_AND_SIN_AFECTACION_minutos/60) T_RESOLUCION_AFECTACION_AND_SIN_AFECTACION_horas
                                                                                                                                              
FROM (
                                                                                                                                SELECT *,     
                                                                                                                                             CASE
                                                                                                                                              
   WHEN T_RESOLUCION <= 30 then 't<=30 min'
                                                                                                                                              
   WHEN T_RESOLUCION > 30 then 't>30 min'
                                                                                                                                              
   else null END T_30_RESOLUCION,
                                                                                                                                             CASE
                                                                                                                                              
   WHEN T_RESOLUCION <= 60 then 't<=60 min'
                                                                                                                                              
   WHEN T_RESOLUCION > 60 then 't>60 min'
                                                                                                                                              
   else null END T_60_RESOLUCION,
                                                                                                                                             CASE
                                                                                                                                              
   WHEN T_RESOLUCION <= 120 then 't<=120 min'
                                                                                                                                              
   WHEN T_RESOLUCION > 120 then 't>120 min'
                                                                                                                                              
   else null END T_120_RESOLUCION,
                                                                                                                                             -- PENDIENTE EN VERIFICAR SI, ES MASIVO O NO. PREGUNTAR CUANDO CUMPLE Y CUANDO NO Y QUE CAMPOS SON A COMPARA
                                                                                                                                             
                                                                                                                                              
  CASE 
									WHEN ID_SERVICIO = '0'  AND  CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'
									WHEN ID_SERVICIO = ' 0'  AND  CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'
									WHEN ID_SERVICIO = ' '  AND  CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'
									WHEN ID_SERVICIO = 'None'  AND  CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'
									WHEN ID_SERVICIO LIKE '%F%' AND  FEMTOCELDA = 'FEMTOCELDA' AND  CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'
									WHEN ID_SERVICIO LIKE '%DEFAULT%' AND  CATEGORÍA <>'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'
									WHEN ID_SERVICIO LIKE '%MASIVO%'  AND  CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'
									WHEN ID_SERVICIO LIKE 'ESC_HN_DEF001'  AND  CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'
									WHEN ID_SERVICIO = 'XT - ACCESO EMPRESARIAL'  AND  CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'                                                                                                                
       							WHEN ID_SERVICIO = 'XT - ACCESO ACTIVOS'  AND  CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'                                                                                                                 
       							WHEN ID_SERVICIO = 'XT - ACCESO DATA_CENTER'  AND CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'                                                                                                                   
       							WHEN ID_SERVICIO = 'XT - DATOS'   AND  CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'                                                                                                                  
       							WHEN ID_SERVICIO = 'XT - INTERNET'  AND  CATEGORÍA <> 'DX - AFECTACION MASIVA' AND TIPO_SERVICIO NOT LIKE '%NO_CMDB%' THEN 'NO VALIDO'
									ELSE 'VALIDO'	END VALIDACION_REINCIDENCIA,
                                                                                                                                             -- PENDIENTE EN VERIFICAR SI, ES MASIVO O NO. PREGUNTAR CUANDO CUMPLE Y CUANDO NO Y QUE CAMPOS SON A COMPARA
                                                                                                                                              
       Open+Work_In_Progress+Pending_Vendor+Pending_Other+WO_Open+WO_Not_Assigned+WO_Pending_Supervisor+WO_Worker_Assigned+WO_Pending_Worker+WO_Work_In_Progress+WO_Pending_Vendor+WO_Pending_Other+WO_Resolved+Resolved T_RESOLUCION_AFECTACION_AND_SIN_AFECTACION_minutos

                                                                                                                                FROM (        
                                                                                                                                        SELECT *,
                                                                                                                                             T_RESOLUCION_DX_AFECTACION_MASIVA+T_RESOLUCION_WO_PENDING_VENDOR+T_RESOLUCION_WO_PENDING_OTHER T_RESOLUCION
                                                                                                                                             FROM(
                                                                                                                                             SELECT *,
                                                                                                                                             CASE
                                                                                                                                              
   WHEN  MASIVO='ASOCIADO A MASIVA' or MASIVO='MASIVA' then
                                                                                                                                              
       Open+Work_In_Progress+Pending_Vendor+Pending_Other+WO_Not_Assigned+WO_Resolved
                                                                                                                                              
   ELSE
                                                                                                                                              
       Open+Work_In_Progress+Pending_Vendor+Pending_Other+WO_Not_Assigned+WO_Resolved+Resolved
                                                                                                                                              
       END T_RESOLUCION_DX_AFECTACION_MASIVA,
                                                                                                                                             CASE
                                                                                                                                              
WHEN Upper(PROVEEDOR) ='UNKNOWN' and WO_Pending_Vendor>0 then WO_Pending_Vendor
                                                                                                                                              
else 0 END T_RESOLUCION_WO_PENDING_VENDOR,
                                                                                                                                             WO_Pending_Other T_RESOLUCION_WO_PENDING_OTHER
                                                                                                                                             FROM(
                                                                                                                                             SELECT *,
                                                                                                                                             CASE
                                                                                                                                             WHEN  (RESPONSABLE = 'MASIVO_REACTIVO'  or
                                                                                                                                             RESPONSABLE = 'MASIVO_PROACTIVO' OR
                                                                                                                                             CATEGORÍA = 'DX - MASIVO' or
                                                                                                                                             GRUPO_ASIGNADO= 'CNOC_MASIVO') AND
                                                                                                                                             (RESPONSABLE <> 'MASIVO_CORPORATIVO') then 'ASOCIADO A MASIVA'

                                                                                                                                             WHEN  (RESPONSABLE <> 'MASIVO_REACTIVO' and
                                                                                                                                             RESPONSABLE <> 'MASIVO_PROACTIVO' and
                                                                                                                                             RESPONSABLE <> 'MASIVO_CORPORATIVO' and
                                                                                                                                             CATEGORÍA <> 'DX - MASIVO') and
                                                                                                                                             (GRUPO_ASIGNADO <> 'CNOC_MASIVO' AND
                                                                                                                                             RESPONSABLE = 'ACCESO_EMPRESARIAL' or
                                                                                                                                             RESPONSABLE = 'PROACTIVO' or
                                                                                                                                             RESPONSABLE = 'REACTIVO' OR RESPONSABLE = 'REACTIVO_XT')  then 'NO ASOCIADO A MASIVA'
                                                                                                                                             WHEN  RESPONSABLE = 'MASIVO_CORPORATIVO' or ID_SERVICIO LIKE '%MASIVO%' THEN 'MASIVO' END MASIVO,
                                                                                                                                             CASE
                                                                                                                                             WHEN SUBCATEGORIA = "CLIENTE" then "CLIENTE" else "CLARO" END ATRIBUCION,
                                                                                                                                             CASE
                                                                                                                                             WHEN TIPO_SERVICIO LIKE '%F%' then 'FEMTOCELDA'
                                                                                                                                             WHEN TIPO_SERVICIO NOT LIKE '%F%' then 'NO FEMTOCELDA'
                                                                                                                                             else NULL END FEMTOCELDA,
                                                                                                                                             CASE
                                                                                                                                             WHEN GRUPO_WO = 'None' then 'RESUELTO POR CNOC'
                                                                                                                                             WHEN GRUPO_WO <> 'None' then 'RESUELTO POR OTRAS AREAS' else null
                                                                                                                                             END VALIDACION_RESOLUCION,
                                                                                                                                             CASE
                                                                                                                                              
   WHEN GRUPO_WO LIKE '%B.O%' then 'ESCALADO A BO'
                                                                                                                                              
   WHEN GRUPO_WO LIKE '%SEGURIDAD%' then 'ESCALADO A BO'
                                                                                                                                              
   WHEN GRUPO_WO LIKE '%GESTION DATOS SV%' then 'ESCALADO A BO'
                                                                                                                                              
   WHEN GRUPO_WO LIKE '%WIMAX%' then 'ESCALADO A BO'
                                                                                                                                              
   ELSE 'NO ESCALADO A BO' END ESCALADO_A_BO,
                                                                                                                                             CASE
                                                                                                                                             when Open>0 then 'OPEN VALIDO'
                                                                                                                                             ELSE 'OPEN INVALIDO' END VALIDACION_OPEN,
                                                                                                                                             CASE
                                                                                                                                              
        WHEN  Open <=10 then "t<=10 min"
                                                                                                                                             WHEN  Open > 10  then "t>10 min"
                                                                                                                                              
   ELSE '' END T_10_OPEN,
                                                                                                                                              
  CASE
                                                                                                                                              
        WHEN  OPEN <=15 then "t<=15 min"
                                                                                                                                             WHEN  OPEN > 15  then "t>15 min"
                                                                                                                                              
   ELSE '' END T_15_OPEN

                                                                                                                                             FROM fr_kpi_outsourcing1_ WHERE FECHA_DE_CIERRE  BETWEEN """+ str(d1)+""" AND """+ str(d2)+""")A
                                                                                                                                             )B
                                                                                                                                             )C
                                                                                                                                             )D
                                                                                                                                             )E
                                                                                                                                             )F
                ),


                TOTAL_AREAS AS (
                SELECT responsable,SUM(contar) SUMATODO FROM (
                SELECT pais_claro pais, responsable, COUNT(*) contar FROM fr_kpi_outsourcing1_
                GROUP BY pais_claro,responsable) A GROUP BY responsable
                ),
                
                
            
           LISTADO_REINCIDENCIA AS (
                SELECT 
					 TICKET,
					 VALIDACION_REINCIDENCIA,
					 ID_SERVICIO,
					 PAIS_CLARO PAIS,responsable  FROM tickets_formateados WHERE VALIDACION_REINCIDENCIA='VALIDO'
                 
                ),
                
                  
               REACTIVO_ AS (
               					 SELECT *,ROUND((CONTAR/T)*100) PORCENTAJE FROM (
                            	  SELECT PAIS,SUM(CONTAR) CONTAR,RESPONSABLE,
											(SELECT SUM(SUMATODO) FROM TOTAL_AREAS WHERE responsable  LIKE '%REACTIVO%') T FROM (
	                             SELECT ID_SERVICIO,COUNT(ID_SERVICIO) CONTAR,PAIS,responsable
                                    FROM LISTADO_REINCIDENCIA
                                GROUP BY PAIS,ID_SERVICIO,responsable)A WHERE CONTAR>=2 AND RESPONSABLE IN ('REACTIVO','REACTIVO_XT') GROUP BY PAIS )B

                ),
                ACCESOS AS (
					 				SELECT *,ROUND((CONTAR/T)*100) PORCENTAJE FROM (
                            	  SELECT PAIS,SUM(CONTAR) CONTAR,RESPONSABLE,
											(SELECT SUM(SUMATODO) FROM TOTAL_AREAS WHERE responsable  LIKE '%ACCESO_EMPRESARIALES%') T FROM (
	                             SELECT ID_SERVICIO,COUNT(ID_SERVICIO) CONTAR,PAIS,responsable
                                    FROM LISTADO_REINCIDENCIA
                                GROUP BY PAIS,ID_SERVICIO,responsable)A WHERE CONTAR>=2 AND RESPONSABLE IN ('ACCESO_EMPRESARIALES') GROUP BY PAIS )B
					 
					 )
			
				SELECT PAIS, SUM(REACTIVO) 'REACTIVO_APROXIMADO', SUM(ACCESOS) 'ACCESOS_APROXIMADO', SUM(REACTIVO_CONTAR) ENLACES_REACTIVO , SUM(ACCESOS_CONTAR) ENLACES_ACCESOS,
                                         (SELECT SUM(SUMATODO) FROM TOTAL_AREAS WHERE responsable IN ('REACTIVO','MASIVO_REACTIVO')) TT_REACTIVO,
                                         (SELECT SUM(SUMATODO) FROM TOTAL_AREAS WHERE responsable IN ('ACCESO_EMPRESARIALES')) TT_ACCESOS     
                                         FROM (
                SELECT
                PAIS,
                CASE
                    WHEN PAIS ="GT" AND AREA="REACTIVO" THEN PORCENTAJE
                    WHEN PAIS ="SV" AND AREA="REACTIVO" THEN PORCENTAJE
                    WHEN PAIS ="HN" AND AREA="REACTIVO" THEN PORCENTAJE
                    WHEN PAIS ="NI" AND AREA="REACTIVO" THEN PORCENTAJE
                    WHEN PAIS ="CR" AND AREA="REACTIVO" THEN PORCENTAJE
                    WHEN PAIS ="PA" AND AREA="REACTIVO" THEN PORCENTAJE
                    ELSE 0 END 'REACTIVO',
                CASE
                    WHEN PAIS ="GT" AND AREA="ACCESOS" THEN PORCENTAJE
                    WHEN PAIS ="SV" AND AREA="ACCESOS" THEN PORCENTAJE
                    WHEN PAIS ="HN" AND AREA="ACCESOS" THEN PORCENTAJE
                    WHEN PAIS ="NI" AND AREA="ACCESOS" THEN PORCENTAJE
                    WHEN pais ="CR" AND AREA="ACCESOS" THEN PORCENTAJE
                    WHEN PAIS ="PA" AND AREA="ACCESOS" THEN PORCENTAJE
                    ELSE 0 END 'ACCESOS',
                CASE
                    WHEN PAIS ="GT" AND AREA="REACTIVO" THEN CONTAR
                    WHEN PAIS ="SV" AND AREA="REACTIVO" THEN CONTAR
                    WHEN PAIS ="HN" AND AREA="REACTIVO" THEN CONTAR
                    WHEN PAIS ="NI" AND AREA="REACTIVO" THEN CONTAR
                    WHEN PAIS ="CR" AND AREA="REACTIVO" THEN CONTAR
                    WHEN PAIS ="PA" AND AREA="REACTIVO" THEN CONTAR
                    ELSE 0 END 'REACTIVO_CONTAR',
                CASE
                    WHEN PAIS ="GT" AND AREA="ACCESOS" THEN CONTAR
                    WHEN PAIS ="SV" AND AREA="ACCESOS" THEN CONTAR
                    WHEN PAIS ="HN" AND AREA="ACCESOS" THEN CONTAR
                    WHEN PAIS ="NI" AND AREA="ACCESOS" THEN CONTAR
                    WHEN pais ="CR" AND AREA="ACCESOS" THEN CONTAR
                    WHEN PAIS ="PA" AND AREA="ACCESOS" THEN CONTAR
                    ELSE 0 END 'ACCESOS_CONTAR'
                FROM(
                SELECT *,'ACCESOS' AREA FROM ACCESOS
                UNION
                SELECT *,'REACTIVO' AREA FROM REACTIVO_) A ) B GROUP BY PAIS  ORDER BY FIELD(PAIS,'GT','SV','HN','NI','CR','PA')
    
    """
    return sql


def pivot_acumulado(tickets_g,tickets_p,A,B,C):
    sql = """
            RESUMEN AS (
            
			SELECT *,'PROACTIVO' FROM  """+str(A)+"""
            UNION
            SELECT *,'REACTIVO' FROM """+str(B)+"""
            UNION
            SELECT *,'ACCESOS' FROM """+str(C)+""")
  
            SELECT PAIS, SUM(REACTIVO) 'REACTIVO_APROXIMADO', SUM(ACCESOS) 'ACCESOS_APROXIMADO', SUM(REACTIVO_CONTAR) ENLACES_REACTIVO , SUM(ACCESOS_CONTAR) ENLACES_ACCESOS,
					 (SELECT SUM(SUMATODO) FROM TOTAL_AREAS WHERE responsable2 IN ('REACTIVO','MASIVO_REACTIVO')) TT_REACTIVO,
					 (SELECT SUM(SUMATODO) FROM TOTAL_AREAS WHERE responsable2 IN ('ACCESO_EMPRESARIALES')) TT_ACCESOS 
					 FROM (      
                    SELECT 
                            CASE
                                WHEN PROACTIVO="REACTIVO" THEN SUMA_G
                                END REACTIVO_G,
                            CASE
                                WHEN PROACTIVO="REACTIVO" THEN SUMA_P
                                END REACTIVO_P,
                        CASE
                                WHEN PROACTIVO="REACTIVO" THEN PORCENTAJE
                                END REACTIVO_PP,
                        CASE
                                WHEN PROACTIVO="ACCESOS" THEN SUMA_G
                                END ACCESOS_G,
                        CASE
                                WHEN PROACTIVO="ACCESOS" THEN SUMA_P
                                END ACCESOS_P,
                        CASE
                                WHEN PROACTIVO="ACCESOS" THEN PORCENTAJE
                                END ACCESOS_PP,
                            CASE
                                WHEN PROACTIVO="PROACTIVO" THEN SUMA_G
                                END PROACTIVO_G,
                            CASE
                                WHEN PROACTIVO="PROACTIVO" THEN SUMA_P
                                END PROACTIVO_P,
                        CASE
                                WHEN PROACTIVO="PROACTIVO" THEN PORCENTAJE
                                END PROACTIVO_PP
                        
                        FROM (
                                SELECT SUMA_G,SUMA_P, (SUMA_G / TOTAL)*100 PORCENTAJE,PROACTIVO 
                                    FROM(
                                        SELECT
                                        SUM("""+str(tickets_g)+""") SUMA_G,SUM("""+str(tickets_p)+""")SUMA_P,PROACTIVO,(SUM("""+str(tickets_g)+""")  + SUM("""+str(tickets_p)+""")) TOTAL 
                        
                                            FROM RESUMEN GROUP BY PROACTIVO 
                                        ) 
                                A) 
                    B ) 
                    C
    
    """
    return sql


def sql_kpi_resolucion_70(date1,date2,area):
   
    sql="""
        WITH
            tickets_formateados AS ("""+str(data_trasformada(date1,date2))+"""),
            RESOLUCION_70_1 AS ("""+str(RESOLUCION_70(date1,date2,areas_cnoc('PROACTIVO',1)))+"""),
            RESOLUCION_70_REACTIVO AS ("""+str(RESOLUCION_70(date1,date2,areas_cnoc('REACTIVO',1)))+"""),
            RESOLUCION_70_ACCESOS AS ("""+str(RESOLUCION_70(date1,date2,areas_cnoc('ACCESOS',1)))+""")
            """+str(calculos('RESOLUCION_70_G', 'RESOLUCION_70_P',70))+"""
            SELECT *,'PROACTIVO' FROM  RESOLUCION_70_1  
            UNION
            SELECT *,'REACTIVO' FROM RESOLUCION_70_REACTIVO 
            UNION
            SELECT *,'ACCESOS' FROM RESOLUCION_70_ACCESOS """+str(pivot_procentaje_AS())
 
    return sql

def sql_kpi_escalado_bo(date1,date2,area):
    sql="""
        WITH
            tickets_formateados AS ("""+str(data_trasformada(date1,date2))+"""),
            ESCALADO_A_BO AS ("""+str(ESCALADO_A_BO(date1,date2,areas_cnoc('PROACTIVO',2)))+"""),
            ESCALADO_A_BO_R AS ("""+str(ESCALADO_A_BO(date1,date2,areas_cnoc('REACTIVO',2)))+"""),
            ESCALADO_A_BO_A AS ("""+str(ESCALADO_A_BO(date1,date2,areas_cnoc('ACCESOS',2)))+""")
            """+str(calculos('ESCALADO_G','ESCALADO_P',90))+"""
            
            SELECT *,'PROACTIVO' FROM  ESCALADO_A_BO 
            UNION 
            SELECT *,'REACTIVO' FROM ESCALADO_A_BO_R 
            UNION 
            SELECT *,'ACCESOS' FROM ESCALADO_A_BO_A """+str(pivot_procentaje_AS())
    return sql

def sql_kpi_open_10(date1,date2,area):
    sql="""
        WITH
            tickets_formateados AS ("""+str(data_trasformada(date1,date2))+"""),
            OPEN_10 AS ("""+str(OPEN_10(date1,date2,areas_cnoc('PROACTIVO',1)))+"""),
            OPEN_10_R AS ("""+str(OPEN_10(date1,date2,areas_cnoc('REACTIVO',1)))+"""),
            OPEN_10_A AS ("""+str(OPEN_10(date1,date2,areas_cnoc('ACCESOS',1)))+""")
             """+str(calculos('OPEN_10_G','OPEN_10_P',90))+"""
            SELECT *,'PROACTIVO' FROM  OPEN_10 
            UNION 
            SELECT *,'REACTIVO' FROM OPEN_10_R 
            UNION
            SELECT *,'ACCESOS' FROM OPEN_10_A """ +str(pivot_procentaje_AS())
    return sql

def sql_kpi_open_15(date1,date2,area):
    sql="""
        WITH
            tickets_formateados AS ("""+str(data_trasformada(date1,date2))+"""),
            OPEN_15 AS ("""+str(OPEN_15(date1,date2,areas_cnoc('PROACTIVO',1)))+"""),
            OPEN_15_R AS ("""+str(OPEN_15(date1,date2,areas_cnoc('REACTIVO',1)))+"""),
            OPEN_15_A AS ("""+str(OPEN_15(date1,date2,areas_cnoc('ACCESOS',1)))+""")
             """+str(calculos('OPEN_15_G','OPEN_15_P',98))+"""
            SELECT *,'PROACTIVO' FROM  OPEN_15 
            UNION
            SELECT *,'REACTIVO' FROM OPEN_15_R 
            UNION
            SELECT *,'ACCESOS' FROM OPEN_15_A """ +str(pivot_procentaje_AS())
    return sql

def sql_kpi_solucion_30(date1,date2,area):
    sql="""
        WITH
            tickets_formateados AS ("""+str(data_trasformada(date1,date2))+"""),
            SOLUCION_30 AS ("""+str(SOLUCION_30(date1,date2,areas_cnoc('PROACTIVO',2)))+"""),
            SOLUCION_30_R AS ("""+str(SOLUCION_30(date1,date2,areas_cnoc('REACTIVO',2)))+"""),
            SOLUCION_30_A AS ("""+str(SOLUCION_30(date1,date2,areas_cnoc('ACCESOS',2)))+""")
             """+str(calculos('T_30_RESOLUCION_G','T_30_RESOLUCION_P',60))+"""
            SELECT *,'PROACTIVO' FROM  SOLUCION_30 
            UNION
            SELECT *,'REACTIVO' FROM SOLUCION_30_R 
            UNION
            SELECT *,'ACCESOS' FROM SOLUCION_30_A """ +str(pivot_procentaje_AS())
    return sql

def sql_kpi_solucion_60(date1,date2,area):
    sql="""
        WITH
            tickets_formateados AS ("""+str(data_trasformada(date1,date2))+"""),
            SOLUCION_60 AS ("""+str(SOLUCION_60(date1,date2,areas_cnoc('PROACTIVO',2)))+"""),
            SOLUCION_60_R AS ("""+str(SOLUCION_60(date1,date2,areas_cnoc('REACTIVO',2)))+"""),
            SOLUCION_60_A AS ("""+str(SOLUCION_60(date1,date2,areas_cnoc('ACCESOS',2)))+""")
             """+str(calculos('T_60_RESOLUCION_G','T_60_RESOLUCION_P',90))+"""
            SELECT *,'PROACTIVO' FROM  SOLUCION_60 
            UNION
            SELECT *,'REACTIVO' FROM SOLUCION_60_R 
            UNION
            SELECT *,'ACCESOS' FROM SOLUCION_60_A """ +str(pivot_procentaje_AS())
    return sql

def sql_kpi_solucion_120(date1,date2,area):
    sql="""
        WITH
            tickets_formateados AS ("""+str(data_trasformada(date1,date2))+"""),
            SOLUCION_120 AS ("""+str(SOLUCION_120(date1,date2,areas_cnoc('PROACTIVO',2)))+"""),
            SOLUCION_120_R AS ("""+str(SOLUCION_120(date1,date2,areas_cnoc('REACTIVO',2)))+"""),
            SOLUCION_120_A AS ("""+str(SOLUCION_120(date1,date2,areas_cnoc('ACCESOS',2)))+""")
             """+str(calculos('T_120_RESOLUCION_G','T_120_RESOLUCION_P',98))+"""
            SELECT *,'PROACTIVO' FROM  SOLUCION_120 
            UNION
            SELECT *,'REACTIVO' FROM SOLUCION_120_R 
            UNION
            SELECT *,'ACCESOS' FROM SOLUCION_120_A """ +str(pivot_procentaje_AS())
    return sql

def indice_de_reincidencia(date1,date2,AREA):
    sql=pivot_reincidencia(date1,date2)
    return sql

def sql_kpi_solucion_8h(date1,date2,area):
    sql="""
        WITH
            tickets_formateados AS ("""+str(data_trasformada(date1,date2))+"""),
            SOLUCION_8 AS ("""+str(SOLUCION_8H(date1,date2,areas_cnoc('PROACTIVO',2)))+"""),
            SOLUCION_8_R AS ("""+str(SOLUCION_8H(date1,date2,areas_cnoc('REACTIVO',2)))+"""),
            SOLUCION_8_A AS ("""+str(SOLUCION_8H(date1,date2,areas_cnoc('ACCESOS',2)))+""")
             """+str(calculos('T_8_H_RESOLUCION_G','T_8_H_RESOLUCION_P',90))+"""
            SELECT *,'PROACTIVO' FROM  SOLUCION_8 
            UNION
            SELECT *,'REACTIVO' FROM SOLUCION_8_R 
            UNION
            SELECT *,'ACCESOS' FROM SOLUCION_8_A """ +str(pivot_procentaje_AS())
    return sql

def sql_kpi_solucion_12h(date1,date2,area):
    sql="""
        WITH
            tickets_formateados AS ("""+str(data_trasformada(date1,date2))+"""),
            SOLUCION_12H AS ("""+str(SOLUCION_12H(date1,date2,areas_cnoc('PROACTIVO',2)))+"""),
            SOLUCION_12H_R AS ("""+str(SOLUCION_12H(date1,date2,areas_cnoc('REACTIVO',2)))+"""),
            SOLUCION_12H_A AS ("""+str(SOLUCION_12H(date1,date2,areas_cnoc('ACCESOS',2)))+""")
             """+str(calculos('T_12_H_RESOLUCION_G','T_12_H_RESOLUCION_P',98))+"""
            SELECT *,'PROACTIVO' FROM  SOLUCION_12H 
            UNION
            SELECT *,'REACTIVO' FROM SOLUCION_12H_R 
            UNION
            SELECT *,'ACCESOS' FROM SOLUCION_12H_A """ +str(pivot_procentaje_AS())
    return sql


def acumulado_solucion_resolucion_70(date1,date2,area):
    sql="""
        WITH
            tickets_formateados AS ("""+str(data_trasformada(date1,date2))+"""),
            RESOLUCION_70_1 AS ("""+str(RESOLUCION_70(date1,date2,areas_cnoc('PROACTIVO',1)))+"""),
            RESOLUCION_70_REACTIVO AS ("""+str(RESOLUCION_70(date1,date2,areas_cnoc('REACTIVO',1)))+"""),
            RESOLUCION_70_ACCESOS AS ("""+str(RESOLUCION_70(date1,date2,areas_cnoc('ACCESOS',1)))+"""),
            """+str(pivot_acumulado('RESOLUCION_70_G', 'RESOLUCION_70_P','RESOLUCION_70_1','RESOLUCION_70_REACTIVO','RESOLUCION_70_ACCESOS'))
    return sql

def acumulado_solucion_escalado_bo(date1,date2,area):
    sql="""
        WITH
            tickets_formateados AS ("""+str(data_trasformada(date1,date2))+"""),
            ESCALADO_A_BO AS ("""+str(ESCALADO_A_BO(date1,date2,areas_cnoc('PROACTIVO',2)))+"""),
            ESCALADO_A_BO_R AS ("""+str(ESCALADO_A_BO(date1,date2,areas_cnoc('REACTIVO',2)))+"""),
            ESCALADO_A_BO_A AS ("""+str(ESCALADO_A_BO(date1,date2,areas_cnoc('ACCESOS',2)))+"""),
            """+str(pivot_acumulado('ESCALADO_G', 'ESCALADO_P','ESCALADO_A_BO','ESCALADO_A_BO_R','ESCALADO_A_BO_A'))
    return sql

def acumulado_solucion_open_10(date1,date2,area):
    sql="""
        WITH
            tickets_formateados AS ("""+str(data_trasformada(date1,date2))+"""),
            OPEN_10 AS ("""+str(OPEN_10(date1,date2,areas_cnoc('PROACTIVO',1)))+"""),
            OPEN_10_R AS ("""+str(OPEN_10(date1,date2,areas_cnoc('REACTIVO',1)))+"""),
            OPEN_10_A AS ("""+str(OPEN_10(date1,date2,areas_cnoc('ACCESOS',1)))+"""),
            """+str(pivot_acumulado('OPEN_10_G', 'OPEN_10_P','OPEN_10','OPEN_10_R','OPEN_10_A'))
    return sql

def acumulado_solucion_open_15(date1,date2,area):
    sql="""
        WITH
            tickets_formateados AS ("""+str(data_trasformada(date1,date2))+"""),
            OPEN_15 AS ("""+str(OPEN_15(date1,date2,areas_cnoc('PROACTIVO',1)))+"""),
            OPEN_15_R AS ("""+str(OPEN_15(date1,date2,areas_cnoc('REACTIVO',1)))+"""),
            OPEN_15_A AS ("""+str(OPEN_15(date1,date2,areas_cnoc('ACCESOS',1)))+"""),
            """+str(pivot_acumulado('OPEN_15_G', 'OPEN_15_P','OPEN_15','OPEN_15_R','OPEN_15_A'))
            
    return sql

def acumulado_solucion_solucion_30(date1,date2,area):
    sql="""
        WITH
            tickets_formateados AS ("""+str(data_trasformada(date1,date2))+"""),
            SOLUCION_30 AS ("""+str(SOLUCION_30(date1,date2,areas_cnoc('PROACTIVO',2)))+"""),
            SOLUCION_30_R AS ("""+str(SOLUCION_30(date1,date2,areas_cnoc('REACTIVO',2)))+"""),
            SOLUCION_30_A AS ("""+str(SOLUCION_30(date1,date2,areas_cnoc('ACCESOS',2)))+"""),
            """+str(pivot_acumulado('T_30_RESOLUCION_G', 'T_30_RESOLUCION_P','SOLUCION_30','SOLUCION_30_R','SOLUCION_30_A'))
             
    return sql

def acumulado_solucion_solucion_60(date1,date2,area):
    sql="""
        WITH
            tickets_formateados AS ("""+str(data_trasformada(date1,date2))+"""),
            SOLUCION_60 AS ("""+str(SOLUCION_60(date1,date2,areas_cnoc('PROACTIVO',2)))+"""),
            SOLUCION_60_R AS ("""+str(SOLUCION_60(date1,date2,areas_cnoc('REACTIVO',2)))+"""),
            SOLUCION_60_A AS ("""+str(SOLUCION_60(date1,date2,areas_cnoc('ACCESOS',2)))+"""),
            """+str(pivot_acumulado('T_60_RESOLUCION_G', 'T_60_RESOLUCION_P','SOLUCION_60','SOLUCION_60_R','SOLUCION_60_A'))
            
    return sql

def acumulado_solucion_solucion_120(date1,date2,area):
    sql="""
        WITH
            tickets_formateados AS ("""+str(data_trasformada(date1,date2))+"""),
            SOLUCION_120 AS ("""+str(SOLUCION_120(date1,date2,areas_cnoc('PROACTIVO',2)))+"""),
            SOLUCION_120_R AS ("""+str(SOLUCION_120(date1,date2,areas_cnoc('REACTIVO',2)))+"""),
            SOLUCION_120_A AS ("""+str(SOLUCION_120(date1,date2,areas_cnoc('ACCESOS',2)))+"""),
            """+str(pivot_acumulado('T_120_RESOLUCION_G', 'T_120_RESOLUCION_P','SOLUCION_120','SOLUCION_120_R','SOLUCION_120_A'))
            
    return sql



def acumulado_solucion_solucion_8h(date1,date2,area):
    sql="""
        WITH
            tickets_formateados AS ("""+str(data_trasformada(date1,date2))+"""),
            SOLUCION_8 AS ("""+str(SOLUCION_8H(date1,date2,areas_cnoc('PROACTIVO',2)))+"""),
            SOLUCION_8_R AS ("""+str(SOLUCION_8H(date1,date2,areas_cnoc('REACTIVO',2)))+"""),
            SOLUCION_8_A AS ("""+str(SOLUCION_8H(date1,date2,areas_cnoc('ACCESOS',2)))+"""),
            """+str(pivot_acumulado('T_8_H_RESOLUCION_G', 'T_8_H_RESOLUCION_P','SOLUCION_8','SOLUCION_8_R','SOLUCION_8_A'))
             
    return sql

def acumulado_solucion_solucion_12h(date1,date2,area):
    sql="""
        WITH
            tickets_formateados AS ("""+str(data_trasformada(date1,date2))+"""),
            SOLUCION_12H AS ("""+str(SOLUCION_12H(date1,date2,areas_cnoc('PROACTIVO',2)))+"""),
            SOLUCION_12H_R AS ("""+str(SOLUCION_12H(date1,date2,areas_cnoc('REACTIVO',2)))+"""),
            SOLUCION_12H_A AS ("""+str(SOLUCION_12H(date1,date2,areas_cnoc('ACCESOS',2)))+"""),
            """+str(pivot_acumulado('T_12_H_RESOLUCION_G', 'T_12_H_RESOLUCION_P','SOLUCION_12H','SOLUCION_12H_R','SOLUCION_12H_A'))
            
            
    return sql

def data_procesada_json(filtro):
    filtro_list=[]
    for i in filtro:
        store_details ={"PAIS":None,"PROACTIVO_G":None, "PROACTIVO_P":None, "PROACTIVO_APROXIMADO":None,"PROACTIVO_JUSTIFICAR_T":None,"PROACTIVO_JUSTIFICAR_PORCENTAJE":None,"SUMA_PROACTIVO":None,"REACTIVO_G":None, "REACTIVO_P":None, "REACTIVO_APROXIMADO":None,"REACTIVO_JUSTIFICAR_T":None,"REACTIVO_JUSTIFICAR_PORCENTAJE":None,"SUMA_REACTIVO":None,"ACCESOS_G":None, "ACCESOS_P":None, "ACCESOS_APROXIMADO":None,"ACCESOS_JUSTIFICAR_T":None,"ACCESOS_JUSTIFICAR_PORCENTAJE":None,"SUMA_ACCESOS":None}
        store_details['PAIS'] = i[0]
        store_details['PROACTIVO_G'] = i[1]
        store_details['PROACTIVO_P'] = i[2]
        store_details['PROACTIVO_APROXIMADO'] = i[3]
        store_details['SUMA_PROACTIVO'] = i[10]
        store_details['PROACTIVO_JUSTIFICAR_T'] = i[13]
        store_details['PROACTIVO_JUSTIFICAR_PORCENTAJE'] = i[17]
        
        store_details['REACTIVO_G'] = i[4]
        store_details['REACTIVO_P'] = i[5]
        store_details['REACTIVO_APROXIMADO'] = i[6]
        store_details['SUMA_REACTIVO'] = i[11]
        store_details['REACTIVO_JUSTIFICAR_T'] = i[14]
        store_details['REACTIVO_JUSTIFICAR_PORCENTAJE'] = i[18]
        
        store_details['ACCESOS_G'] = i[7]
        store_details['ACCESOS_P'] = i[8]
        store_details['ACCESOS_APROXIMADO'] = i[9]
        store_details['SUMA_ACCESOS'] = i[12]
        store_details['ACCESOS_JUSTIFICAR_T'] = i[15]
        store_details['ACCESOS_JUSTIFICAR_PORCENTAJE'] = i[19]
        
        filtro_list.append(store_details)
    
    return filtro_list

def data_procesada_json2(filtro):
    filtro_list=[]
    for i in filtro:
        store_details ={"PAIS":None, "PROACTIVO":None, "REACTIVO":None, "ACCESOS":None}
        store_details['PAIS'] = i[0]
        store_details['PROACTIVO'] = i[1]
        store_details['REACTIVO'] = i[2]
        store_details['ACCESOS'] = i[3]
        filtro_list.append(store_details)
    
    return filtro_list

def data_procesada_json3(filtro):
    filtro_list=[]
    for i in filtro:
        store_details ={"PAIS":None, "REACTIVO_APROXIMADO":None, "ACCESOS_APROXIMADO":None,"ENLACE_REACTIVO":None,"ENLACES_ACCESOS":None,"TT_REACTIVO":None,"TT_ACCESOS":None}
        store_details['PAIS'] = i[0]
        store_details['REACTIVO_APROXIMADO'] = i[1]
        store_details['ACCESOS_APROXIMADO'] = i[2]
        store_details['ENLACE_REACTIVO'] = i[3]
        store_details['ENLACES_ACCESOS'] = i[4]
        store_details['TT_REACTIVO'] = i[5]
        store_details['TT_ACCESOS'] = i[6]
        filtro_list.append(store_details)
    
    return filtro_list

def data_procesada_json4(filtro):
    filtro_list=[]
    for i in filtro:
        store_details ={"REACTIVO_G":None, "REACTIVO_P":None, "REACTIVOPP":None,"ACCESOS_G":None, "ACCESOS_P":None, "ACCESOSPP":None,"PROACTIVO_G":None, "PROACTIVO_P":None, "PROACTIVOPP":None}
        store_details['REACTIVO_G'] = i[0]
        store_details['REACTIVO_P'] = i[1]
        store_details['REACTIVOPP'] = i[2]
        store_details['ACCESOS_G'] = i[3]
        store_details['ACCESOS_P'] = i[4]
        store_details['ACCESOSPP'] = i[5]
        store_details['PROACTIVO_G'] = i[6]
        store_details['PROACTIVO_P'] = i[7]
        store_details['PROACTIVOPP'] = i[8]
        filtro_list.append(store_details)
    
    return filtro_list

def respuesta(data,nombre,area):
    if not data:
        msj="ERROR, NO HAY DATOS QUE MOSTRAR"
        cargar="no" 
    else:
        msj="SE GENERADO REPORTE, CORRECTAMENTE"
        cargar="si"
    respuesta={"code":200,
               "area":area,
               "nombre":nombre,
               "datos":len(data),
               "procesar":cargar,
               "data":data,
               "msj":msj}
    return respuesta

print(pivot_reincidencia('20220816','20220817'))