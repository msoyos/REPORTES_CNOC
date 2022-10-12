import cx_Oracle
import mysql.connector
cx_Oracle.init_oracle_client(lib_dir="C:\oracle")
## cx_Oracle.init_oracle_client(lib_dir="/Users/your_username/Downloads/instantclient_19_8")
cx_Oracle.clientversion()

# Connect as user "hr" with password "welcome" to the "orclpdb1" service running on this computer.
def select(sql):
    print("INICIANDO CONEXION DB")
    connection = cx_Oracle.connect(user="frt_msoyos", password="Heh-pBH8Mt5u",
                               dsn="172.17.114.223/sm9",encoding="UTF-8")
    print("INICIANDO SQL")
    cursor = connection.cursor()
    print("EJECUTANDO SQL "+sql)
    r =cursor.execute(sql)
    res = r.fetchall()
    print(r)
    print("CONSULTA EJECUTADA ")
    
    return res


def dbmysql(SQL_,c=0):
    try:
        connection = mysql.connector.connect(host='localhost',
                                         database='reportes',
                                         user='root',
                                         password='')
        cursor = connection.cursor()
        if(c==0):
                q=SQL_
                print(q)
                cursor.execute(q)
                myresult =  cursor.fetchall()    
                print("SELECT")
        elif(c==1):
                mySql_insert_query = SQL_     
                cursor.execute(mySql_insert_query)
                connection.commit()
                myresult=cursor.lastrowid
                print("INSERT")
        else:
                mySql_insert_query = SQL_     
                cursor.execute(mySql_insert_query)
                connection.commit()
                myresult=cursor.rowcount
                print("UPDATE O DELETE")
        
        cursor.close()
        print(myresult)
        return myresult
    
    except mysql.connector.Error as error:
        
        print("ERROR{}".format(error))
        return "ERROR{}".format(error)
    finally:
        if connection.is_connected():
            connection.close()
        else:
            pass
        print("MySQL, CONEXION CERRADA")
