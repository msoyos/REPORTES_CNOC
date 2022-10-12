import mysql.connector
def dbmysql(SQL_,c=0):
    try:
        connection = mysql.connector.connect(host='localhost',
                                         database='reportes',
                                         user='root',
                                         password='')
        cursor = connection.cursor()
        if(c==0):
                q=SQL_
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
            print("MySQL, CONEXION CERRADA")