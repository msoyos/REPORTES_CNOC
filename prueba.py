import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir="C:\oracle")
## cx_Oracle.init_oracle_client(lib_dir="/Users/your_username/Downloads/instantclient_19_8")
cx_Oracle.clientversion()
# Connect as user "hr" with password "welcome" to the "orclpdb1" service running on this computer.
connection = cx_Oracle.connect(user="frt_msoyos", password="Heh-pBH8Mt5u",
                               dsn="172.17.114.223/sm9",encoding="UTF-8")

cursor = connection.cursor()
cursor.execute("""
        SELECT 'PRUEBA DE CONEXION EXITOSA' as fname FROM dual""")
for fname in cursor:
    print("Values:", fname)
    
connection.close()