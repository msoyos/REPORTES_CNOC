import datetime
from datetime import date, datetime
from doctest import Example
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import collections
from typing import Optional
from fastapi import FastAPI
from fastapi import Query, Path
from fastapi import status
from pydantic import Field
import re
import db
import helpers as h_
from reporte_semanal import consultas_varias as r_s
from login import index as lg
from kpi_diario_amd import funciones_kpi as kpi
app = FastAPI(title="API - REPORTES CNOC",
             description="Automatizacion de reportes CNOC",
             version="1.0")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5500",
    "http://portal.test",
    "http://portal.test:5500",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/",status_code=status.HTTP_200_OK,tags=["SESION"])
def getInformation(info :lg.Credenciales):
    r=lg.Inicio(info.name,info.password)
    return r

@app.get("/reporte_semanal/{item_id}",status_code=status.HTTP_200_OK,tags=["REPORTE SEMANAL"])
def read_item(item_id:Optional[int] = 0):
     week=r_s.procesar_week(db.dbmysql(r_s.sql_semana()))
     year=r_s.procesar_year(db.dbmysql(r_s.sql_year()))
     month=r_s.procesar_month(db.dbmysql(r_s.sql_mes()))
     r=r_s.respuesta(r_s.procesar_items(db.dbmysql(r_s.sql_semanal())),week,year,month)
     return r

@app.get("/reporte_enlace_default/{item_id}",status_code=status.HTTP_200_OK,tags=["REPORTE SEMANAL"])
def read_item(item_id:Optional[int]=0):
    if(item_id==0):
        r=r_s.respuesta2(r_s.procesar_enlaces_default(db.dbmysql(r_s.sql_enlace_default())))
    elif(item_id==2):
        r=r_s.respuesta2(r_s.procesar_item_masiva(db.dbmysql(r_s.sql_masivo())))
    else:
        r=r_s.respuesta2(r_s.procesar_item_default(db.dbmysql(r_s.sql_enlaces_default())))
    return r

@app.post("/kpi/DIPONIBILIDAD70/",status_code=status.HTTP_200_OK,tags=["REPORTE KPI AMD"])
def getInformation(info :kpi.KPI_model):
        date1=re.sub(r"[^0-9]","", str(info.fecha))
        r=kpi.respuesta(kpi.data_procesada_json(db.dbmysql(kpi.sql_kpi_resolucion_70(date1, re.sub(r"[^0-9]","", str(h_.sumar_dias(info.fecha2,1))),info.area))),"DIPONIBILIDAD 70",info.area)
        return r

@app.post("/kpi/BO",status_code=status.HTTP_200_OK,tags=["REPORTE KPI AMD"])
def getInformation(info :kpi.KPI_model):
        date1=re.sub(r"[^0-9]","", str(info.fecha))
        r=kpi.respuesta(kpi.data_procesada_json(db.dbmysql(kpi.sql_kpi_escalado_bo(date1, re.sub(r"[^0-9]","", str(h_.sumar_dias(info.fecha2,1))),info.area))),"ESCALADO BO",info.area)
        return r

@app.post("/kpi/OPEN10",status_code=status.HTTP_200_OK,tags=["REPORTE KPI AMD"])
def getInformation(info :kpi.KPI_model):
        date1=re.sub(r"[^0-9]","", str(info.fecha))
        r=kpi.respuesta(kpi.data_procesada_json(db.dbmysql(kpi.sql_kpi_open_10(date1, re.sub(r"[^0-9]","", str(h_.sumar_dias(info.fecha2,1))),info.area))),"OPEN 10",info.area)
        return r

@app.post("/kpi/OPEN15",status_code=status.HTTP_200_OK,tags=["REPORTE KPI AMD"])
def getInformation(info :kpi.KPI_model):
        date1=re.sub(r"[^0-9]","", str(info.fecha))
        r=kpi.respuesta(kpi.data_procesada_json(db.dbmysql(kpi.sql_kpi_open_15(date1, re.sub(r"[^0-9]","", str(h_.sumar_dias(info.fecha2,1))),info.area))),"OPEN 15",info.area)
        return r

@app.post("/kpi/SOLUCION30",status_code=status.HTTP_200_OK,tags=["REPORTE KPI AMD"])
def getInformation(info :kpi.KPI_model):
        date1=re.sub(r"[^0-9]","", str(info.fecha))
        r=kpi.respuesta(kpi.data_procesada_json(db.dbmysql(kpi.sql_kpi_solucion_30(date1, re.sub(r"[^0-9]","", str(h_.sumar_dias(info.fecha2,1))),info.area))),"SOLUCION 30",info.area)
        return r

@app.post("/kpi/SOLUCION60",status_code=status.HTTP_200_OK,tags=["REPORTE KPI AMD"])
def getInformation(info :kpi.KPI_model):
        date1=re.sub(r"[^0-9]","", str(info.fecha))
        r=kpi.respuesta(kpi.data_procesada_json(db.dbmysql(kpi.sql_kpi_solucion_60(date1, re.sub(r"[^0-9]","", str(h_.sumar_dias(info.fecha2,1))),info.area))),"SOLUCION 60",info.area)
        return r

@app.post("/kpi/SOLUCION120",status_code=status.HTTP_200_OK,tags=["REPORTE KPI AMD"])
def getInformation(info :kpi.KPI_model):
        date1=re.sub(r"[^0-9]","", str(info.fecha))
        r=kpi.respuesta(kpi.data_procesada_json(db.dbmysql(kpi.sql_kpi_solucion_120(date1, re.sub(r"[^0-9]","", str(h_.sumar_dias(info.fecha2,1))),info.area))),"SOLUCION 120",info.area)
        return r

@app.post("/kpi/REINCIDENCIA",status_code=status.HTTP_200_OK,tags=["REPORTE KPI AMD"])
def getInformation(info :kpi.KPI_model):
        date1=re.sub(r"[^0-9]","", str(info.fecha))
        r=kpi.respuesta(kpi.data_procesada_json3(db.dbmysql(kpi.indice_de_reincidencia(date1, re.sub(r"[^0-9]","", str(h_.sumar_dias(info.fecha2,1))),info.area))),"REINCIDENCIA",info.area)
        return r

@app.post("/kpi/SOLUCION8H",status_code=status.HTTP_200_OK,tags=["REPORTE KPI AMD"])
def getInformation(info :kpi.KPI_model):
        date1=re.sub(r"[^0-9]","", str(info.fecha))
        r=kpi.respuesta(kpi.data_procesada_json(db.dbmysql(kpi.sql_kpi_solucion_8h(date1, re.sub(r"[^0-9]","", str(h_.sumar_dias(info.fecha2,1))),info.area))),"SOLUCION 8H",info.area)
        return r

@app.post("/kpi/SOLUCION12H",status_code=status.HTTP_200_OK,tags=["REPORTE KPI AMD"])
def getInformation(info :kpi.KPI_model):
        date1=re.sub(r"[^0-9]","", str(info.fecha))
        r=kpi.respuesta(kpi.data_procesada_json(db.dbmysql(kpi.sql_kpi_solucion_12h(date1, re.sub(r"[^0-9]","", str(h_.sumar_dias(info.fecha2,1))),info.area))),"SOLUCION 12H",info.area)
        return r 
    
@app.post("/global/DIPONIBILIDAD70/",status_code=status.HTTP_200_OK,tags=["ACUMULADO REPORTE KPI AMD"])
def getInformation(info :kpi.KPI_model):
        date1=re.sub(r"[^0-9]","", str(info.fecha))
        r=kpi.respuesta(kpi.data_procesada_json4(db.dbmysql(kpi.acumulado_solucion_resolucion_70(date1, re.sub(r"[^0-9]","", str(h_.sumar_dias(info.fecha2,1))),info.area))),"DIPONIBILIDAD 70",info.area)
        return r

@app.post("/global/BO",status_code=status.HTTP_200_OK,tags=["ACUMULADO REPORTE KPI AMD"])
def getInformation(info :kpi.KPI_model):
        date1=re.sub(r"[^0-9]","", str(info.fecha))
        r=kpi.respuesta(kpi.data_procesada_json4(db.dbmysql(kpi.acumulado_solucion_escalado_bo(date1, re.sub(r"[^0-9]","", str(h_.sumar_dias(info.fecha2,1))),info.area))),"ESCALADO BO",info.area)
        return r

@app.post("/global/OPEN10",status_code=status.HTTP_200_OK,tags=["ACUMULADO REPORTE KPI AMD"])
def getInformation(info :kpi.KPI_model):
        date1=re.sub(r"[^0-9]","", str(info.fecha))
        r=kpi.respuesta(kpi.data_procesada_json4(db.dbmysql(kpi.acumulado_solucion_open_10(date1, re.sub(r"[^0-9]","", str(h_.sumar_dias(info.fecha2,1))),info.area))),"OPEN 10",info.area)
        return r

@app.post("/global/OPEN15",status_code=status.HTTP_200_OK,tags=["ACUMULADO REPORTE KPI AMD"])
def getInformation(info :kpi.KPI_model):
        date1=re.sub(r"[^0-9]","", str(info.fecha))
        r=kpi.respuesta(kpi.data_procesada_json4(db.dbmysql(kpi.acumulado_solucion_open_15(date1, re.sub(r"[^0-9]","", str(h_.sumar_dias(info.fecha2,1))),info.area))),"OPEN 15",info.area)
        return r

@app.post("/global/SOLUCION30",status_code=status.HTTP_200_OK,tags=["ACUMULADO REPORTE KPI AMD"])
def getInformation(info :kpi.KPI_model):
        date1=re.sub(r"[^0-9]","", str(info.fecha))
        r=kpi.respuesta(kpi.data_procesada_json4(db.dbmysql(kpi.acumulado_solucion_solucion_30(date1, re.sub(r"[^0-9]","", str(h_.sumar_dias(info.fecha2,1))),info.area))),"SOLUCION 30",info.area)
        return r

@app.post("/global/SOLUCION60",status_code=status.HTTP_200_OK,tags=["ACUMULADO REPORTE KPI AMD"])
def getInformation(info :kpi.KPI_model):
        date1=re.sub(r"[^0-9]","", str(info.fecha))
        r=kpi.respuesta(kpi.data_procesada_json4(db.dbmysql(kpi.acumulado_solucion_solucion_60(date1, re.sub(r"[^0-9]","", str(h_.sumar_dias(info.fecha2,1))),info.area))),"SOLUCION 60",info.area)
        return r

@app.post("/global/SOLUCION120",status_code=status.HTTP_200_OK,tags=["ACUMULADO REPORTE KPI AMD"])
def getInformation(info :kpi.KPI_model):
        date1=re.sub(r"[^0-9]","", str(info.fecha))
        r=kpi.respuesta(kpi.data_procesada_json4(db.dbmysql(kpi.acumulado_solucion_solucion_120(date1, re.sub(r"[^0-9]","", str(h_.sumar_dias(info.fecha2,1))),info.area))),"SOLUCION 120",info.area)
        return r


@app.post("/global/SOLUCION8H",status_code=status.HTTP_200_OK,tags=["ACUMULADO REPORTE KPI AMD"])
def getInformation(info :kpi.KPI_model):
        date1=re.sub(r"[^0-9]","", str(info.fecha))
        r=kpi.respuesta(kpi.data_procesada_json4(db.dbmysql(kpi.acumulado_solucion_solucion_8h(date1, re.sub(r"[^0-9]","", str(h_.sumar_dias(info.fecha2,1))),info.area))),"SOLUCION 8H",info.area)
        return r

@app.post("/global/SOLUCION12H",status_code=status.HTTP_200_OK,tags=["ACUMULADO REPORTE KPI AMD"])
def getInformation(info :kpi.KPI_model):
        date1=re.sub(r"[^0-9]","", str(info.fecha))
        r=kpi.respuesta(kpi.data_procesada_json4(db.dbmysql(kpi.acumulado_solucion_solucion_12h(date1, re.sub(r"[^0-9]","", str(h_.sumar_dias(info.fecha2,1))),info.area))),"SOLUCION 12H",info.area)
        return r 
    
