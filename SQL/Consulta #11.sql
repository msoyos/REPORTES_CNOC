  WITH
            tickets_formateados AS (
            SELECT *,
CASE
        WHEN date_format(PRO7.FECHA_APERTURA, "%d-%m-%Y")=date_format(PRO7.FECHA_CIERRE, "%d-%m-%Y") then "TNH"
        WHEN date_format(PRO7.FECHA_APERTURA, "%d-%m-%Y") < date_format(PRO7.FECHA_CIERRE, "%d-%m-%Y") then "TH"
        WHEN date_format(PRO7.FECHA_APERTURA, "%d-%m-%Y") > date_format(PRO7.FECHA_CIERRE, "%d-%m-%Y") then "REVISAR"
        else null
        END  VALIDACION_TICKET_HEREDADO,
CASE
-- VALIDACION TIPO ENLACE EN TICKET
WHEN PRO7.ID_SERVICIO = 0  then "TICKET SIN ENLACE"
WHEN PRO7.ID_SERVICIO = "None" OR PRO7.ID_SERVICIO = NULL then "TICKET SIN ENLACE"
WHEN PRO7.ID_SERVICIO LIKE '%MASIV%'  then "MASIVA"
WHEN PRO7.ID_SERVICIO LIKE '%CC_%' then "TICKET CON ID DE CPE"
else "TICKET CON ENLACE"
END VALIDACION_TIPO_ENLACE_EN_TICKET
FROM (
SELECT *,
CASE
        WHEN PRO6.MES_CIERRE = NULL  AND PRO6.ANO_CIERRE = NULL  then "FECHA_INVALIDA"
        else "FECHA_VALIDA"
        END VALIDACION_FECHA,
CASE
-- VALIDACION DE TIKETS SI CORRESPONDE AL PERIODO.
        WHEN PRO6.MES_APERTURA=PRO6.MES_CIERRE AND PRO6.ANO_APERTURA=PRO6.ANO_CIERRE then "TICKET ABIERTO Y CERRADO EN MISMO PERIODO"
                else "TICKET ABIERTO Y CERRADO EN DISTINTO PERIODO"
   END VALIDACION_FECHA_2
FROM(
SELECT *,
CASE
        WHEN PRO5.T_RESOLUCION_AFECTACION_SIN_AFECTACION_HORAS <= 8 then "t<=8 horas"
        WHEN PRO5.T_RESOLUCION_AFECTACION_SIN_AFECTACION_HORAS > 8 then "t>8 horas"
END T_8_HORAS_RESOLUCION_AFECTACION_SIN_AFECTACION,
-- T 8 HORAS RESOLUCION AFECTACION / SIN AFECTACION
CASE
        WHEN PRO5.T_RESOLUCION_AFECTACION_SIN_AFECTACION_HORAS <= 12 then "t<=12 horas"
        WHEN PRO5.T_RESOLUCION_AFECTACION_SIN_AFECTACION_HORAS > 12 then "t>12 horas"
END T_12_HORAS_RESOLUCION_AFECTACION_SIN_AFECTACION,
-- T 12 HORAS RESOLUCION AFECTACION / SIN AFECTACION
-- VALIDACION DE CATEGORIA ESCALADO A BO
CASE
        WHEN PRO5.CATEGORIA ="DX - AFECTACION MASIVA" then "NO VALIDA"
        WHEN PRO5.CATEGORIA = "DX - BOLETA MAL ABIERTA" then "NO VALIDA"
        ELSE "VALIDA"
        END VALIDACION_CATEGORIA_ESCALADO_A_BO,
-- VALIDACION CATEGORIA DESCARTAR DX - AFECTACION MASIVA
CASE
        WHEN PRO5.CATEGORIA  <> "DX - AFECTACION MASIVA" then "SIN DX AFECTACION MASIVA"
        else "CON DX AFECTACION MASIVA"
        END VALIDACION_CATEGORIA_DESCARTAR_DX_AFECTACION_MASIVA,
YEAR(PRO5.FECHA_CIERRE) ANO_CIERRE,
MONTH(PRO5.FECHA_APERTURA) MES_APERTURA,
YEAR(PRO5.FECHA_APERTURA) ANO_APERTURA
FROM (
SELECT *,
(PRO4.T_RESOLUCION_AFECTACION_SIN_AFECTACION_minutos/60) T_RESOLUCION_AFECTACION_SIN_AFECTACION_HORAS

FROM (
                SELECT *,
                        CASE
                                WHEN PRO3.T_RESOLUCION <= 30 then "t<=30 min"
                                WHEN PRO3.T_RESOLUCION > 30 then "t>30 min"
                        END T_30_RESOLUCION,
                        CASE
                                WHEN PRO3.T_RESOLUCION <= 60 then "t<=60 min"
                                WHEN PRO3.T_RESOLUCION > 60 then "t>60 min"
                        END T_60_RESOLUCION,
                        CASE
                                WHEN PRO3.T_RESOLUCION <= 120 then "t<=120 min"
                                WHEN PRO3.T_RESOLUCION > 120 then "t>120 min"
                        END T_120_RESOLUCION,
                        CASE
                                WHEN PRO3.ID_SERVICIO LIKE '%DEFAULT%'
                                        OR  PRO3.ID_SERVICIO LIKE '%MASIVO%'
                                        OR  PRO3.ID_SERVICIO LIKE '%ESC_HN_DEF001%'
                                        OR PRO3.ID_SERVICIO <> "XT - ACCESO EMPRESARIAL"
                                        OR PRO3.ID_SERVICIO <> "XT - ACCESO ACTIVOS"
                                        OR PRO3.ID_SERVICIO <> "XT - ACCESO DATA_CENTER"
                                        OR PRO3.ID_SERVICIO <> "XT - DATOS"
                                        OR PRO3.ID_SERVICIO <> "0"
                                        OR PRO3.ID_SERVICIO <> 0
                                        OR PRO3.ID_SERVICIO  <> ""
                                        OR PRO3.FEMTOCELDA= "NO FEMTOCELDA"
                                        OR PRO3.CATEGORIA <> "DX - AFECTACION MASIVA"
                                        OR PRO3.TIPO_SERVICIO <> "NO_CMDB" then "VALIDO"
                                        else "NO VALIDO" END VALIDACION_REINCIDENCIA,
                        -- RESOLUCION DE AFECTACION EN MINUTOS
                        (PRO3.Open+Work_In_Progress+PRO3.Pending_Vendor+PRO3.Pending_Other+WO_Open+PRO3.WO_Not_Assigned+PRO3.WO_Pending_Supervisor+PRO3.WO_Worker_Assigned+WO_Pending_Worker+WO_Work_In_Progress+PRO3.WO_Pending_Vendor+PRO3.WO_Pending_Other+PRO3.
WO_Resolved+PRO3.Resolved) T_RESOLUCION_AFECTACION_SIN_AFECTACION_minutos
 FROM (
                SELECT *,
                (T_RESOLUCION_DX_AFECTACION_MASIVA+T_RESOLUCION_WO_PENDING_VENDOR+T_RESOLUCION_WO_PENDING_OTHER) T_RESOLUCION
 FROM (
        SELECT *,
                CASE
                        WHEN PRO1.MASIVO="ASOCIADO A MASIVA" or PRO1.MASIVO="MASIVA" then
                        PRO1.Open+PRO1.Work_In_Progress+PRO1.Pending_Vendor+PRO1.Pending_Other+PRO1.WO_Not_Assigned+PRO1.WO_Resolved
                        ELSE
                        PRO1.Open+PRO1.Work_In_Progress+PRO1.Pending_Vendor+PRO1.Pending_Other+PRO1.WO_Not_Assigned+PRO1.WO_Resolved+Resolved
                        END T_RESOLUCION_DX_AFECTACION_MASIVA,
                CASE
                        WHEN UPPER(PRO1.PROVEEDOR) ='UNKNOWN' AND PRO1.Pending_Vendor>0 THEN WO_Pending_Vendor ELSE 0
                        END T_RESOLUCION_WO_PENDING_VENDOR,
                        PRO1.WO_Pending_Other T_RESOLUCION_WO_PENDING_OTHER

FROM (
SELECT *,
CASE
        WHEN RESPONSABLE = 'MASIVO_REACTIVO' OR  RESPONSABLE = 'MASIVO_PROACTIVO' THEN 'MASIVO_CORPORATIVO'
        WHEN RESPONSABLE = 'MASIVO_CORPORATIVO' THEN 'MASIVO'
        ELSE 'NO ASOCIADO A MASIVA'
END MASIVO,
CASE
        WHEN SUBCATEGORY = "CLIENTE" THEN "CLIENTE" else "CLARO" END ATRIBUCION,
CASE
        WHEN TIPO_SERVICIO LIKE '%F%' THEN "FENTOCELDA" ELSE "NO FENTOCELDA" END FEMTOCELDA,
CASE
        WHEN GRUPO_WO ='None' OR GRUPO_WO ='' OR GRUPO_WO =NULL THEN "RESUELTO POR CNOC"
ELSE "RESUELTO POR OTRAS AREAS" END  VALIDACION_RESOLUCION,
CASE
        WHEN GRUPO_WO = 'None' THEN  'NO ESCALADO A BO'
        WHEN GRUPO_WO LIKE '%B.O%'  then "ESCALADO A BO"
        WHEN GRUPO_WO LIKE '%SEGURIDAD%' then "ESCALADO A BO"
        WHEN GRUPO_WO LIKE '%GESTION DATOS SV%' then "ESCALADO A BO"
        WHEN GRUPO_WO LIKE '%WIMAX%' then "ESCALADO A BO"
        ELSE "NO ESCALADO A BO"
END ESCALADO_A_BO, -- VALIDACION DE RESOLUCION
CASE
        WHEN Open > 0 then "OPEN VALIDO" else "OPEN INVALIDO"
END VALIDACION_OPEN,
CASE
        WHEN Open <> "" and Open <=10 then "t<=10 min"
        WHEN Open <> "" and Open > 10  then "t>10 min"
END T_10_OPEN,
CASE
        WHEN Open <> "" and OPEN <=15 then "t<=15 min"
        WHEN Open <> "" and OPEN > 15  then "t>15 min"
END T_15_OPEN
FROM fr_kpi_outsourcing1
) AS PRO1
) AS PRO2
) AS PRO3
) AS PRO4
) AS PRO5
) AS PRO6
) AS PRO7
INNER JOIN catalogo_areas_cnoc ON catalogo_areas_cnoc.nombre_area_claro = pro7.RESPONSABLE
WHERE PRO7.VALIDACION_FECHA="FECHA_VALIDA"
    ),
            RESOLUCION_70_1 AS (
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
                                                                SELECT tickets_formateados.pais,tickets_formateados.VALIDACION_RESOLUCION,COUNT(*) AS CONTAR
                                                                FROM tickets_formateados
                                                                WHERE
                                                                tickets_formateados.FECHA_CIERRE BETWEEN 20220628 AND 20220629
                                                                AND tickets_formateados.TIPO_SERVICIO   NOT IN ('FENTOCELDA','NO_CMDB','SERVICIO INTERNO')
                                                                AND  tickets_formateados.responsable2 IN ('PROACTIVO')
                                                                AND  tickets_formateados.FEMTOCELDA    IN ('NO FENTOCELDA')
                                                                AND  tickets_formateados.MASIVO IN ('MASIVO_CORPORATIVO','NO ASOCIADO A MASIVA')
                                                                GROUP BY tickets_formateados.VALIDACION_RESOLUCION,tickets_formateados.pais
                                                                ) A
                                                ) B  GROUP BY B.pais
                                ) C
                ) D
    ),
            RESOLUCION_70_REACTIVO AS (
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
                                                                SELECT tickets_formateados.pais,tickets_formateados.VALIDACION_RESOLUCION,COUNT(*) AS CONTAR
                                                                FROM tickets_formateados
                                                                WHERE
                                                                tickets_formateados.FECHA_CIERRE BETWEEN 20220628 AND 20220629
                                                                AND tickets_formateados.TIPO_SERVICIO   NOT IN ('FENTOCELDA','NO_CMDB','SERVICIO INTERNO')
                                                                AND  tickets_formateados.responsable2 IN ('REACTIVO','MASIVO_REACTIVO')
                                                                AND  tickets_formateados.FEMTOCELDA    IN ('NO FENTOCELDA')
                                                                AND  tickets_formateados.MASIVO IN ('MASIVO_CORPORATIVO','NO ASOCIADO A MASIVA')
                                                                GROUP BY tickets_formateados.VALIDACION_RESOLUCION,tickets_formateados.pais
                                                                ) A
                                                ) B  GROUP BY B.pais
                                ) C
                ) D
    ),
            RESOLUCION_70_ACCESOS AS (
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
                                                                SELECT tickets_formateados.pais,tickets_formateados.VALIDACION_RESOLUCION,COUNT(*) AS CONTAR
                                                                FROM tickets_formateados
                                                                WHERE
                                                                tickets_formateados.FECHA_CIERRE BETWEEN 20220628 AND 20220629
                                                                AND tickets_formateados.TIPO_SERVICIO   NOT IN ('FENTOCELDA','NO_CMDB','SERVICIO INTERNO')
                                                                AND  tickets_formateados.responsable2 IN ('ACCESO_EMPRESARIALES')
                                                                AND  tickets_formateados.FEMTOCELDA    IN ('NO FENTOCELDA')
                                                                AND  tickets_formateados.MASIVO IN ('MASIVO_CORPORATIVO','NO ASOCIADO A MASIVA')
                                                                GROUP BY tickets_formateados.VALIDACION_RESOLUCION,tickets_formateados.pais
                                                                ) A
                                                ) B  GROUP BY B.pais
                                ) C
                ) D
    )

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
                                 WHEN P_APROXIMADO <70 THEN ROUND((((SUMA_PROACTIVO*70)/100)/1)-PROACTIVO_G)
                                                ELSE '' END JUSTIFICAR_P,
                        CASE
                                 WHEN R_APROXIMADO <70 THEN ROUND((((SUMA_REACTIVO*70)/100)/1)-REACTIVO_G)
                                                ELSE '' END JUSTIFICAR_R,
                        CASE
                                 WHEN A_APROXIMADO <70 THEN ROUND((((SUMA_ACCEOSO*70)/100)/1)-ACCESOS_G)
                                                ELSE '' END JUSTIFICAR_A,
                        70 PORCENTAJE_GANAR

                        FROM (
                   SELECT
                        *,PROACTIVO_G+PROACTIVO_P SUMA_PROACTIVO,REACTIVO_G+REACTIVO_P SUMA_REACTIVO,ACCESOS_G+ACCESOS_P SUMA_ACCEOSO

                        FROM (
                        SELECT
                pais,
                                         sum(RESOLUCION_70_G_PROACTIVO) PROACTIVO_G , sum(RESOLUCION_70_P_PROACTIVO) PROACTIVO_P , SUM(APROXIMADO_PROACTIVO) P_APROXIMADO,
                sum(RESOLUCION_70_G_REACTIVO) REACTIVO_G , sum(RESOLUCION_70_P_REACTIVO) REACTIVO_P, SUM(APROXIMADO_REACTIVO) R_APROXIMADO,
                sum(RESOLUCION_70_G_ACCESOS) ACCESOS_G , sum(RESOLUCION_70_P_ACCESOS) ACCESOS_P,SUM(APROXIMADO_ACCESOS) A_APROXIMADO
        FROM (
                  SELECT
        pais,
        CASE
        WHEN pais ="GT" AND PROACTIVO="PROACTIVO" THEN RESOLUCION_70_G
        WHEN pais ="SV" AND PROACTIVO="PROACTIVO" THEN RESOLUCION_70_G
        WHEN pais ="HN" AND PROACTIVO="PROACTIVO" THEN RESOLUCION_70_G
        WHEN pais ="NI" AND PROACTIVO="PROACTIVO" THEN RESOLUCION_70_G
        WHEN pais ="CR" AND PROACTIVO="PROACTIVO" THEN RESOLUCION_70_G
        WHEN pais ="PA" AND PROACTIVO="PROACTIVO" THEN RESOLUCION_70_G
        ELSE 0 END RESOLUCION_70_G_PROACTIVO,
        CASE
        WHEN pais ="GT" AND PROACTIVO="PROACTIVO" THEN RESOLUCION_70_P
        WHEN pais ="SV" AND PROACTIVO="PROACTIVO" THEN RESOLUCION_70_P
        WHEN pais ="HN" AND PROACTIVO="PROACTIVO" THEN RESOLUCION_70_P
        WHEN pais ="NI" AND PROACTIVO="PROACTIVO" THEN RESOLUCION_70_P
        WHEN pais ="CR" AND PROACTIVO="PROACTIVO" THEN RESOLUCION_70_P
        WHEN pais ="PA" AND PROACTIVO="PROACTIVO" THEN RESOLUCION_70_P
        ELSE 0 END RESOLUCION_70_P_PROACTIVO,
        CASE
        WHEN pais ="GT" AND PROACTIVO="PROACTIVO" THEN APROXIMADO
        WHEN pais ="SV" AND PROACTIVO="PROACTIVO" THEN APROXIMADO
        WHEN pais ="HN" AND PROACTIVO="PROACTIVO" THEN APROXIMADO
        WHEN pais ="NI" AND PROACTIVO="PROACTIVO" THEN APROXIMADO
        WHEN pais ="CR" AND PROACTIVO="PROACTIVO" THEN APROXIMADO
        WHEN pais ="PA" AND PROACTIVO="PROACTIVO" THEN APROXIMADO
        ELSE 0 END APROXIMADO_PROACTIVO,
        CASE
        WHEN pais ="GT" AND PROACTIVO="REACTIVO" THEN RESOLUCION_70_G
        WHEN pais ="SV" AND PROACTIVO="REACTIVO" THEN RESOLUCION_70_G
        WHEN pais ="HN" AND PROACTIVO="REACTIVO" THEN RESOLUCION_70_G
        WHEN pais ="NI" AND PROACTIVO="REACTIVO" THEN RESOLUCION_70_G
        WHEN pais ="CR" AND PROACTIVO="REACTIVO" THEN RESOLUCION_70_G
        WHEN pais ="PA" AND PROACTIVO="REACTIVO" THEN RESOLUCION_70_G
        ELSE 0
        END RESOLUCION_70_G_REACTIVO,
        CASE
        WHEN pais ="GT" AND PROACTIVO="REACTIVO" THEN RESOLUCION_70_P
        WHEN pais ="SV" AND PROACTIVO="REACTIVO" THEN RESOLUCION_70_P
        WHEN pais ="HN" AND PROACTIVO="REACTIVO" THEN RESOLUCION_70_P
        WHEN pais ="NI" AND PROACTIVO="REACTIVO" THEN RESOLUCION_70_P
        WHEN pais ="CR" AND PROACTIVO="REACTIVO" THEN RESOLUCION_70_P
        WHEN pais ="PA" AND PROACTIVO="REACTIVO" THEN RESOLUCION_70_P
        ELSE 0
        END RESOLUCION_70_P_REACTIVO,
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
        WHEN pais ="GT" AND PROACTIVO="ACCESOS" THEN RESOLUCION_70_G
        WHEN pais ="SV" AND PROACTIVO="ACCESOS" THEN RESOLUCION_70_G
        WHEN pais ="HN" AND PROACTIVO="ACCESOS" THEN RESOLUCION_70_G
        WHEN pais ="NI" AND PROACTIVO="ACCESOS" THEN RESOLUCION_70_G
        WHEN pais ="CR" AND PROACTIVO="ACCESOS" THEN RESOLUCION_70_G
        WHEN pais ="PA" AND PROACTIVO="ACCESOS" THEN RESOLUCION_70_G
        ELSE 0
                END RESOLUCION_70_G_ACCESOS,
        CASE
        WHEN pais ="GT" AND PROACTIVO="ACCESOS" THEN RESOLUCION_70_P
        WHEN pais ="SV" AND PROACTIVO="ACCESOS" THEN RESOLUCION_70_P
        WHEN pais ="HN" AND PROACTIVO="ACCESOS" THEN RESOLUCION_70_P
        WHEN pais ="NI" AND PROACTIVO="ACCESOS" THEN RESOLUCION_70_P
        WHEN pais ="CR" AND PROACTIVO="ACCESOS" THEN RESOLUCION_70_P
        WHEN pais ="PA" AND PROACTIVO="ACCESOS" THEN RESOLUCION_70_P
        ELSE 0
        END RESOLUCION_70_P_ACCESOS,
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


            SELECT *,'PROACTIVO' FROM  RESOLUCION_70_1
            UNION
            SELECT *,'REACTIVO' FROM RESOLUCION_70_REACTIVO
            UNION
            SELECT *,'ACCESOS' FROM RESOLUCION_70_ACCESOS

     ) A ) b GROUP BY pais ORDER BY FIELD(pais,'GT','SV','HN','NI','CR','PA')) C ) D )E