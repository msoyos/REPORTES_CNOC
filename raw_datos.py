
import db
sql="""SELECT TICKET,"ID SERVICIO","FECHA CIERRE" FROM FR_KPI_OUTSOURCING1"""
r=db.select(sql)
print(r) 
#TO_NUMBER(TO_CHAR(TO_TIMESTAMP('2021-01-01'), 'WW')) OBTENER SEMANA SOBRE FECHA DE CIERRE
#[0] TICKET
#[1] CATEGORIA
#[2] ID SERVICIO
#[3] GRUPO WO
#[4] PROVEEDOR
#[5] FECHA APERTURA
#[6] FECHA CIERRE 
#[7] MES CIERRE
#[8] AFECTACION
#[9] RESPONSABLE
#[10] INICIADOR 
#[11] TT_TK_MIN
#[12] OPEN 
#[13] WORK IN PROGRESS  
#[14] PENDING VENDOR
#[15] PENDING OTHER
#[16] PENDING CUSTOMER
#[17] WO NOT ASSIGNED
#[18] WO OPEN
#[19] WO PENDING SUPERVISOR
#[20] WO Worker Assigned	
#[21] WO Pending Worker	
#[22] WO Work In Progress	
#[23] WO Pending Vendor	
#[24] WO Pending Other	
#[25] WO Resolved	
#[26] Resolved	
#[27] WO Pending Customer	
#[28] WO PendingMonitoreo	
#[29] Otros	
#[30] Dictamen	
#[31] PAIS	
#[32] TIPO_SERVICIO
"""
TICKET,	
CATEGORIA,	
ID_SERVICIO,	
GRUPO_WO
PROVEEDOR,	
FECHA_APERTURA,	
FECHA_CIERRE,	
MES_CIERRE,	
AFECTACION,	
RESPONSABLE,	
INICIADOR,	
TT_TK_MIN,	
Open,	
Work_In_Progress,	
Pending_Vendor,	
Pending_Other,	
Pending_Customer,	
WO_Not_Assigned,	
WO_Open,	
WO_Pending_Supervisor,	
WO_Worker_Assigned,	
WO_Pending_Worker",	
WO_Work_In_Progress,	
WO_Pending_Vendor",	
WO_Pending_Other",	
WO_Resolved,	
Resolved,	
WO_Pending_Customer",	
Monitoreo,	
Otros,	
Dictamen,	
PAIS,	
TIPO_SERVICIO

TICKET,"ID SERVICIO",to_char("FECHA CIERRE" , 'yyyy-mm-dd hh24:mi:ss')
"""