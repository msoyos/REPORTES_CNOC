from sqlite3 import register_converter
import db
sql=""" WITH T AS
  (SELECT ADD_MONTHS(SYSDATE,-1) INI, SYSDATE FIN, SYSDATE HOY FROM DUAL
  ) ,
  TK AS
  (SELECT 
  M1."NUMBER" ,
 dev.company,
 
     M2.TG_ENLACE ,
    DEV.TG_ID_CLASE_SERVICIO ,
    M2.TG_SEVERIDAD ,
    M2.TG_ESTADOSERVICIO ,
    M2.INITIAL_IMPACT ,
    M1.SEVERITY ,
    M1.PRIORITY_CODE,
     M1.CATEGORY ,
     m1.subcategory,
     m1.product_type,
     m1.problem_type,
     m2.res_anal_code,
     m1.resolution_code,
     m2.TG_TTAREARESP, 
    m2.TG_TTSERVESPECIFICO,
    m2.TG_TTRESOLUCION,
    CASE
      WHEN TG_ENLACE LIKE '%_GT_%'
      THEN 'GT'
      WHEN TG_ENLACE LIKE '%_SV_%'
      THEN 'SV'
      WHEN TG_ENLACE LIKE '%_HN_%'
      THEN 'HN'
      WHEN TG_ENLACE LIKE '%_NI_%'
      THEN 'NI'
      WHEN TG_ENLACE LIKE '%_CR_%'
      THEN 'CR'
      WHEN TG_ENLACE LIKE '%T'
      THEN 'GT'
      WHEN TG_ENLACE LIKE '%SV'
      THEN 'SV'
      WHEN TG_ENLACE LIKE '%OH'
      THEN 'HN'
      WHEN TG_ENLACE LIKE '%ON%'
      THEN 'NI'
      WHEN TG_ENLACE LIKE '%OC'
      THEN 'CR'
      ELSE DEV.TG_COUNTRY_CODE
    END PAIS ,
    CASE
      WHEN M1.PROBLEM_TYPE LIKE '%CAIDA TOTAL%'
      THEN 'AFECTACION'
      ELSE 'SIN AFECTACION'
    END AFECTACION ,
    CASE
      WHEN M1.ASSIGNMENT = 'CNOC_MASIVO' AND M2.TG_ENLACE LIKE 'MASIVO%' THEN 'TK_MASIVO'
      WHEN M1.ASSIGNMENT = 'CNOC_MASIVO'  THEN 'TK_REL_MASIVO'
      WHEN M1.ASSIGNMENT IN ('GESTION DE DATOS N1','GESTION N1_CBO','CNOC_CBO_PROACTIVO','CNOC_CBO_REACTIVO','CNOC','GT - ACC. EMPRESARIAL - NOC')
      THEN 'CNOC'

      WHEN M1.ASSIGNMENT IN ('SOPORTE_N1_XT','SOPORTE_N2_XT','SOPORTE_N3_XT','CYBER_SOC_XT')
      THEN 'CNOC_XT'
      WHEN M1.ASSIGNMENT IN ('CNOC_NICARAGUA')
      THEN 'CNOC_NICARAGUA'
      ELSE 'PENDIENTE'
    END RESP_TK ,
    CASE
      WHEN M1.ASSIGNMENT IN ('CNOC_CBO_PROACTIVO','CNOC_CBO_REACTIVO','CNOC')
      THEN 'PROACTIVO'
      ELSE 'REACTIVO'
    END TIPO_TK ,
    OPENED_BY,
    CASE
      WHEN OPENED_BY= 'tmipuser'
      THEN 'AUTOMATICO'
      ELSE 'MANUAL'
    END APERTURA ,
    CASE
      WHEN M2.TG_WORKORDER ='t'
      THEN 'CON_WO'
      ELSE 'SIN_WO'
    END WO ,
    CASE
      WHEN M1.CATEGORY = 'DX - CLIENTE'
      THEN 'CLIENTE'
      WHEN M1.CATEGORY IN ('DX - MASIVO' , 'DX - RED CLARO','DX - AFECTACION MASIVA')
      THEN 'MASIVA'
      ELSE 'NORMAL'
    END ATRIBUCION,

    CASE
      WHEN M2.TG_ENLACE LIKE '%MASIVO%'
      THEN 'MASIVO_CORPORATIVOS'
      ELSE 'TICKET'
    END CLASIFICACION,

    CASE
      WHEN CL.NAME IN ('WO - CNOC_GT - WO Open','WO - CNOC_GT - WO Pending Supervisor','WO - CNOC_GT - WO Pending Worker','WO - CNOC_GT - WO Worker Assigned','WO - CNOC_GT - WO Work In Progress')
      THEN 'Work In Progress'
      WHEN CL.NAME LIKE 'WO - %'
      AND CL.NAME LIKE '%- Open'
      THEN 'WO Open'
      WHEN CL.NAME LIKE 'WO - %'
      AND CL.NAME LIKE '%- Work In Progress'
      THEN 'WO Work In Progress'
      WHEN CL.NAME LIKE '%WO Pendiente de Tecnico%'
      THEN 'WO Pending Worker'
      WHEN CL.NAME LIKE '%WO Resuelta%'
      THEN 'WO Resolved'
      WHEN CL.NAME = 'Resuelto'
      THEN 'Resolved'
      ELSE trim(SUBSTR(cl.name,(INSTR(CL.NAME,'- WO ')+1)))
    END ESTADO
    ,
    CL.NAME ,
    ((TO_DATE(TO_CHAR(CL.TOTAL,'DD/MM/YYY HH24:MI:SS'),'DD/MM/YYY HH24:MI:SS') -TO_DATE('01/01/2000 00:00:00','DD/MM/YY HH24:MI:SS'))*24) AS TIEMPO_RELOJ ,
    (m1.close_time                                                             - m1.open_time)*24 TT ,
    M1.VENDOR ,
    TO_CHAR(M1.close_time,'HH') HORA,
    TO_CHAR(M1.close_time,'DD') DIA,
    TO_CHAR(M1.close_time,'WW') SEMANA,
   TO_CHAR(M1.close_time,'MM') MES,
    TO_CHAR(M1.close_time,'YYYY') AÑO,
    m1.close_time ,
    m1.open_time,
    m1.sysmoduser u_cierre_tk,
    cl.sysmoduser as usuario_cl
  FROM PROBSUMMARYM1 M1
  INNER JOIN PROBSUMMARYM2 M2
  ON M1."NUMBER" = M2."NUMBER"
  INNER JOIN CLOCKSM1 CL
  ON M2."NUMBER" = CL.KEY_CHAR
  INNER JOIN DEVICE2M1 DEV
  ON M2.TG_ENLACE = DEV.LOGICAL_NAME
  INNER JOIN BIZSERVICEM1 BIZ
  ON DEV.LOGICAL_NAME  = BIZ.LOGICAL_NAME
  WHERE M1.ASSIGNMENT IN ('GESTION DE DATOS N1','GESTION N1_CBO','CNOC_CBO_PROACTIVO','CNOC_CBO_REACTIVO','CNOC','GT - ACC. EMPRESARIAL - NOC','SOPORTE_N1_XT','SOPORTE_N2_XT','SOPORTE_N3_XT','CYBER_SOC_XT','CNOC_NICARAGUA','CNOC_MASIVO')
  
  AND NAME NOT LIKE 'Time locked by%'
  AND M1.CLOSE_TIME BETWEEN
    (SELECT INI FROM T
    )
  AND (SELECT FIN+1 FROM T)
  AND CL.NAME NOT LIKE 'F - %'
  AND CL.NAME NOT LIKE 'Tiempo%'
  AND CL.NAME NOT   IN ('WorkInProgress','WorkOrder','Review')
  AND M1.CLOSE_TIME IS NOT NULL
  
  AND CL.RUNNING = 'f'
  ) SELECT "NUMBER","COMPANY","TG_ENLACE","TG_ID_CLASE_SERVICIO","TG_SEVERIDAD","TG_ESTADOSERVICIO","INITIAL_IMPACT","SEVERITY","PRIORITY_CODE","CATEGORY","SUBCATEGORY","PRODUCT_TYPE","PROBLEM_TYPE","RES_ANAL_CODE","RESOLUTION_CODE","TG_TTAREARESP","TG_TTSERVESPECIFICO","TG_TTRESOLUCION","PAIS","AFECTACION","RESP_TK","TIPO_TK","OPENED_BY","APERTURA","WO","ATRIBUCION","CLASIFICACION","ESTADO","NAME","TIEMPO_RELOJ","TT","VENDOR","HORA","DIA","SEMANA","MES","AÑO","CLOSE_TIME","OPEN_TIME","U_CIERRE_TK","USUARIO_CL" FROM TK """
r=db.select(sql)
print(r) 