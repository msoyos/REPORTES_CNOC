# API - REPORTES CNOC
>## INSTALAR DEPENCIAS PARA PARA PONER EN MARCHA CODIGO

 Tener instalado, PYTHON > 3.10.
 # CREAR ENTORNO VIRTUAL UBUNTU
1. sudo apt-get install python3-venv
2. virtualenv nombre_del_entorno -p python3
3. source nombre_del_entorno/bin/activate
    * source nombre_del_entorno/bin/deactivate

# CREAR ENTORNO VIRTUAL  WINDOWS
1.  py -m venv analisis 
2.  .\analisis\Scripts\activate

# INSTALACION PARA WINDOWS ORANCLE 
1. Entrar carpeta instaladores
    * Crear Carpeta Orancle en Disco C
    * Descomprimir archivo instantclient-basiclite-windows.x64-21.6.0.0.0dbru en carpeta creada
    * Intalar VC_redist.x64.exe 
2. CONFIGURAR VARIABLES DE ENTORNO VIRTUAL EN WINDOWS
    *Path -> agregar la acceso a carpeta orancle.
    *crear variable SQL_PATH -> ruta carpeta creada en C (C:\orancle)
3. Realizar paso si da problema de conexion a base de datos.
    * Crear variable de entorno tns_admin -> ruta carpeta creada en C (C:\orancle)
    * crear variable de entorno NLS_LANG -> LATIN AMERICAN SPANISH_GUATEMALA.WE8ISO8859P15
    

### Oracle
-------------------------------
1. pip install cx_Oracle
### 1. MySQL
Crear Base Datos: Escalaciones.
-------------------------------- 

1. python -m pip install mysql-connector-python
2. show variables like 'max_connections';
    * Si esta en 151 aumentar 500;
    ** SET GLOBAL max_connections = 500;

### 2. FAST API
--------------------------------
1. pip install fastapi uvicorn   
2. pip install numpy

### 3. EJECUTAR JOBS
---------------------------------
1. pip install schedule
#### PONER EN MARCHA EL CODIGO, CON FAST API. EJECUTADO DENTRO DEL ENTORNO VIRTUAL
 
 1. uvicorn main:app --reload  // modo developer
 2. uvicorn main:app --host 172.17.222.105 --port 8000   // modo produccion

 ##
 #
 >
 *https://oracle.github.io/python-cx_Oracle/samples/tutorial/Python-and-Oracle-Database-Scripting-for-the-Future.html

