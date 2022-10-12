
from time import sleep
import db
from datetime import datetime


def sql_script(r=1):
    if(r==1):
        #se actualiza todo a media noche de cada dia 
        sql=""" SELECT F. *, PM1.ASSIGNMENT 
FROM fr_kpi_outsourcing1 F, PROBSUMMARYM1 PM1
                                        WHERE 
                                            PM1."NUMBER"=F.TICKET ORDER BY "MES CIERRE" DESC """
    elif(r==2):
        # se actualiza lo del mes cada 12 horas 
        sql=""" SELECT * FROM FR_KPI_OUTSOURCING1 WHERE "FECHA CIERRE" >= TO_DATE(TO_CHAR(ADD_MONTHS(SYSDATE, -1), 'DD/MM/YYYY' ), 'DD/MM/YYYY' )
		AND  "FECHA CIERRE" <= TO_DATE(TO_CHAR(SYSDATE, 'DD/MM/YYYY' ), 'DD/MM/YYYY' )"""
    elif(r==3):
        # se actualiza lo del mes cada 20 minutos 
        sql=""" SELECT * FROM FR_KPI_OUTSOURCING1 
        WHERE "FECHA CIERRE" >= TO_DATE(TO_CHAR(SYSDATE, 'DD/MM/YYYY' ), 'DD/MM/YYYY' )-1
		AND  "FECHA CIERRE" <= TO_DATE(TO_CHAR(SYSDATE, 'DD/MM/YYYY' ), 'DD/MM/YYYY' )+1 
        order by "FECHA CIERRE" desc"""
    return sql
        

def Actualizar_vista_fr_kpi_outsourcing1(sqltxt,job):
    print(datetime.now())
    r=db.select(sql_script(sqltxt))
    print(r) 
    """ sql_verificar = TRUNCATE `fr_kpi_outsourcing1` 
    res_verificar = db.dbmysql(sql_verificar) ORDER """
    vueltas=0
    lineas_update=0
    lineas_insert=0
    for item in r:

        #verificar si existe en base de datos, si existe eliminar he insetar de nuevo
        vueltas+=1
        print("-..."+str(vueltas))
        # validamos cambio fecha de cierre si cambia se actuliza la data , si no existe lo insertameos
        sql_validar=""" SELECT TICKET,FECHA_CIERRE FROM `fr_kpi_outsourcing1` WHERE TICKET='"""+str(item[0])+"""' AND FECHA_APERTURA='"""+str(item[6])+"""'"""
        res_validar = db.dbmysql(sql_validar)
        if not res_validar:
            lineas_insert+=1 
            sql=f"""INSERT INTO FR_KPI_OUTSOURCING1 VALUES ('"""+str(item[0])+"','"+str(item[1])+"','"+str(item[2])+"','"+str(item[3])+"','"+str(item[4])+"','"+str(item[5])+"','"+str(item[6])+"','"+str(item[7])+"','"+str(item[8])+"','"+str(item[9])+"','"+str(item[10])+"','"+str(item[11])+"','"+str(item[12])+"','"+str(item[13])+"','"+str(item[14])+"','"+str(item[15])+"','"+str(item[16])+"','"+str(item[17])+"','"+str(item[18])+"','"+str(item[19])+"','"+str(item[20])+"','"+str(item[21])+"','"+str(item[22])+"','"+str(item[23])+"','"+str(item[24])+"','"+str(item[25])+"','"+str(item[26])+"','"+str(item[27])+"','"+str(item[28])+"','"+str(item[29])+"','"+str(item[30])+"','"+str(item[31])+"','"+str(item[32])+"','"+str(item[33])+"','"+str(item[34])+"')"
            res=db.dbmysql(sql,1)
        else:
            lineas_update+=1
            sql=""" UPDATE fr_kpi_outsourcing1 SET `TICKET`='"""+str(item[0])+"""',`CATEGORIA`='"""+str(item[1])+"""',`SUBCATEGORY`='"""+str(item[2])+"""',`ID_SERVICIO`='"""+str(item[3])+"""',`GRUPO_WO`='"""+str(item[4])+"""',`PROVEEDOR`='"""+str(item[5])+"""',`FECHA_APERTURA`='"""+str(item[6])+"""',`FECHA_CIERRE`='"""+str(item[7])+"""',`MES_CIERRE`='"""+str(item[8])+"""',`AFECTACION`='"""+str(item[9])+"""',`RESPONSABLE`='"""+str(item[10])+"""',`INICIADOR`='"""+str(item[11])+"""',`TT_TK_MIN`='"""+str(item[12])+"""',`Open`='"""+str(item[13])+"""',`Work_In_Progress`='"""+str(item[14])+"""',`Pending_Vendor`='"""+str(item[15])+"""',`Pending_Other`='"""+str(item[16])+"""',`Pending_Customer`='"""+str(item[17])+"""',`WO_Not_Assigned`='"""+str(item[18])+"""',`WO_Open`='"""+str(item[19])+"""',`WO_Pending_Supervisor`='"""+str(item[20])+"""',`WO_Worker_Assigned`='"""+str(item[21])+"""',`WO_Pending_Worker`='"""+str(item[22])+"""',`WO_Work_In_Progress`='"""+str(item[23])+"""',`WO_Pending_Vendor`='"""+str(item[24])+"""',`WO_Pending_Other`='"""+str(item[25])+"""',`WO_Resolved`='"""+str(item[26])+"""',`Resolved`='"""+str(item[27])+"""',`WO_Pending_Customer`='"""+str(item[28])+"""',`Monitoreo`='"""+str(item[29])+"""',`Otros`='"""+str(item[30])+"""',`Dictamen`='"""+str(item[31])+"""',`PAIS`='"""+str(item[32])+"""',`TIPO_SERVICIO`='"""+str(item[33])+"""',`ASSIGNMENT`='"""+str(item[34])+"""'  WHERE TICKET='"""+str(item[0])+"""' AND FECHA_CIERRE='"""+str(item[7])+"""'"""
            res=db.dbmysql(sql,2)
         
        print(res)
    sql_log=""" INSERT INTO `log_actualizaciones`( `name_job`, `lineas_actualizadas`, `lineas_nuevas`) VALUES ('"""+str(job)+"""',"""+str(lineas_update)+""","""+str(lineas_insert)+""")""" 
    db.dbmysql(sql_log,1)   
    print(datetime.now())

Actualizar_vista_fr_kpi_outsourcing1(1,'job2')