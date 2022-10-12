import schedule
import time
from datetime import datetime
import vista1

def Job1():
    vista1.Actualizar_vista_fr_kpi_outsourcing1(1)
    print("Job Ejecutado con Exito. JOB 1...")

def Job2():
    vista1.Actualizar_vista_fr_kpi_outsourcing1(2)
    print("Job Ejecutado con Exito. JOB 2...")

def Job3():
    vista1.Actualizar_vista_fr_kpi_outsourcing1(3)
    print("Job Ejecutado con Exito. JOB 3...")

schedule.every().day.at("23:50").do(Job1) 
schedule.every().day.at("15:00").do(Job2) 
schedule.every(10).minutes.do(Job3)
while True:
    schedule.run_pending()
    time.sleep(1)
