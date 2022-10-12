from sqlite3 import register_converter
import db
sql="""SELECT * FROM FR_KPI_OUTSOURCING1"""
r=db.select(sql)
print(r) 
for item in r:

    #verificar si existe en base de datos, si existe eliminar he insetar de nuevo
    sql_verificar = """TRUNCATE `fr_kpi_outsourcing1`"""
    res_verificar = db.dbmysql(sql_verificar)
    sql=f"""INSERT INTO FR_KPI_OUTSOURCING1 VALUES ('"""+str(item[0])+"','"+str(item[1])+"','"+str(item[2])+"','"+str(item[3])+"','"+str(item[4])+"','"+str(item[5])+"','"+str(item[6])+"','"+str(item[7])+"','"+str(item[8])+"','"+str(item[9])+"','"+str(item[10])+"','"+str(item[11])+"','"+str(item[12])+"','"+str(item[13])+"','"+str(item[14])+"','"+str(item[15])+"','"+str(item[16])+"','"+str(item[17])+"','"+str(item[18])+"','"+str(item[19])+"','"+str(item[20])+"','"+str(item[21])+"','"+str(item[22])+"','"+str(item[23])+"','"+str(item[24])+"','"+str(item[25])+"','"+str(item[26])+"','"+str(item[27])+"','"+str(item[28])+"','"+str(item[29])+"','"+str(item[30])+"','"+str(item[31])+"','"+str(item[32])+"','"+str(item[33])+"')" 
    
    if not res_verificar:
        res=db.dbmysql(sql,1)
    else :
        sql_delete="""DELETE FROM FR_KPI_OUTSOURCING1 WHERE TICKET='"""+str(item[0])+"'"
        res_delete=db.dbmysql(sql_delete,3)
        res=db.dbmysql(sql,1)
    print(res)    

