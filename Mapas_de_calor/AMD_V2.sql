WITH
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
																												RESPONSABLE = 'PROACTIVO'  or 
																												RESPONSABLE = 'REACTIVO' OR RESPONSABLE = 'REACTIVO_XT')  then 'NO ASOCIADO A MASIVA'
																										WHEN  RESPONSABLE = 'MASIVO_CORPORATIVO' or ID_SERVICIO LIKE '%MASIVO%' THEN 'MASIVO' END MASIVO
																										
																										
																										,
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
																										
									 													FROM fr_kpi_outsourcing1_ WHERE FECHA_DE_CIERRE BETWEEN 20220816 AND 20220817)A 
																					)B
																					)C 
																		)D
																		)E 
																		)F 
											),
											FILTRAR_TICKETS_REAC_PROACTIVO AS (
													SELECT * FROM tickets_formateados 
													WHERE 
													(MASIVO <> 'MASIVO') and (MASIVO = 'NO ASOCIADO A MASIVA') and (TIPO_SERVICIO = 'CPE' or TIPO_SERVICIO = 'ENLACE DE DATOS' or TIPO_SERVICIO = 'INTERNET CORPORATIVO') 
											),	
											FILTRAR_TICKETS_ACCESOS AS (
													SELECT * FROM (
													SELECT * FROM tickets_formateados
													WHERE (MASIVO <> 'MASIVO') AND (MASIVO = 'NO ASOCIADO A MASIVA') and (TIPO_SERVICIO <> 'NO_CMDB'))A WHERE
													 (MASIVO <> 'MASIVO') and (MASIVO = 'NO ASOCIADO A MASIVA') and (TIPO_SERVICIO = 'ACCESO EMPRESARIAL') and (RESPONSABLE = 'ACCESO_EMPRESARIAL')
											),
											TOTAL_REACTIVO AS ( -- TOTAL DE TICKETS REACTIVOS.
											SELECT RESPONSABLE,COUNT(*) CONTAR,pais_claro 
											FROM FILTRAR_TICKETS_REAC_PROACTIVO WHERE RESPONSABLE IN('REACTIVO','REACTIVO_XT') GROUP BY pais_claro),
											
											TOTAL_T_ACCESOS AS(
											SELECT RESPONSABLE,COUNT(*) RECUENTO,pais_claro FROM FILTRAR_TICKETS_ACCESOS
											GROUP BY RESPONSABLE,pais_claro)
											
											SELECT * FROM TOTAL_REACTIVO;
											
											/*ACCESOS AS ( -- TOTAL DE TICKETS RECIBIDOS ACCESOS EMPRESARIALES
											SELECT RESPONSABLE,COUNT(*) CONTAR 
											FROM FILTRAR_TICKETS_ACCESOS WHERE RESPONSABLE IN('ACCESO_EMPRESARIAL')),
											
											VAL_REINCIDENCIA_REACTIVO AS (
											SELECT * FROM (
											SELECT W,COUNT(*) RECUENTO,pais_claro PAIS  FROM FILTRAR_TICKETS_REAC_PROACTIVO 
											WHERE RESPONSABLE IN('REACTIVO','REACTIVO_XT') AND ATRIBUCION='CLIENTE' 
											GROUP BY ID_SERVICIO,pais_claro)AS A WHERE A.RECUENTO >=2 GROUP BY A.ID_SERVICIO,A.PAIS) ,
											
											VAL_REINCIDENCIA_ACCESO AS (
											SELECT * FROM(
											SELECT ID_SERVICIO, COUNT(*) RECUENTO,pais_claro PAIS FROM FILTRAR_TICKETS_ACCESOS WHERE SUBCATEGORIA ='CLIENTE'
											GROUP BY ID_SERVICIO,pais_claro) A WHERE A.RECUENTO >=2
											
											) ,TOTAL_T_REACTIVO AS(
											SELECT SUM(RECUENTO) RECUENTO,pais_claro,SUBSTR(RESPONSABLE,1,8) RESPONSABLE_ FROM  (
											SELECT RESPONSABLE,COUNT(*) RECUENTO,pais_claro FROM FILTRAR_TICKETS_REAC_PROACTIVO 
											WHERE RESPONSABLE IN('REACTIVO','REACTIVO_XT') 
											GROUP BY RESPONSABLE,pais_claro)A GROUP BY pais_claro,RESPONSABLE_),
											
											REINCIDENCIA_REACTIVO AS (
											SELECT PAIS,(RECUENTO/(SELECT RECUENTO FROM TOTAL_T_REACTIVO WHERE pais_claro=PAIS ))*100 PORCENTAJE FROM VAL_REINCIDENCIA_REACTIVO GROUP BY PAIS
											),
											TOTAL_T_ACCESOS AS(
											SELECT RESPONSABLE,COUNT(*) RECUENTO,pais_claro FROM FILTRAR_TICKETS_ACCESOS
											GROUP BY RESPONSABLE,pais_claro)
											
											SELECT * FROM  VAL_REINCIDENCIA_REACTIVO 
											
										/*	
											UNION_ALL AS (
											SELECT *,(SELECT COUNT(*) FROM FILTRAR_TICKETS_REAC_PROACTIVO WHERE RESPONSABLE IN ('REACTIVO','REACTIVO_XT'))TT,'REACTIVO' AREA FROM VAL_REINCIDENCIA_ACCESO
											UNION
											SELECT *,(SELECT COUNT(*) FROM FILTRAR_TICKETS_ACCESOS) TT,'ACCESOS' AREA FROM VAL_REINCIDENCIA_REACTIVO)
											
											SELECT *,
												CASE 
													WHEN AREA='REACTIVO' THEN (RECUENTO/TT)*100
													END REACTIVO,
												CASE 
													WHEN AREA='ACCESOS' THEN (RECUENTO/TT)*100
													END ACCESOS
											 FROM UNION_ALL
											;
											 -- WHERE RESPONSABLE IN('REACTIVO','REACTIVO_XT')
																						
											/*SELECT * FROM(
											SELECT
											
											     RESPONSABLE,COUNT(*) CONTAR,ID_SERVICIO 
											FROM FILTRAR_TICKETS_REAC_PROACTIVO 
											 WHERE CATEGORÍA='DX - INDIVIDUAL' AND ID_SERVICIO NOT IN ('0') AND RESPONSABLE NOT IN ('REACTIVO','REACTIVO_XT') GROUP BY RESPONSABLE,ID_SERVICIO) A WHERE A.CONTAR >=2
											*/
											
										
/*
SELECT *, (SELECT  CONTAR FROM suma ) FROM(
SELECT RESPONSABLE, COUNT(ID_SERVICIO) CONTAR,ID_SERVICIO FROM tickets_formateados  WHERE VALIDACION_REINCIDENCIA='VALIDO'	AND MASIVO='NO ASOCIADO A MASIVA' GROUP BY RESPONSABLE	,ID_SERVICIO )A 
WHERE A.CONTAR >=2  AND A.RESPONSABLE LIKE '%REACTIVO%'  */                       