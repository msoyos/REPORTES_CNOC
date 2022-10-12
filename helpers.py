import datetime
from datetime import timedelta

def sumar_dias(date_,dias):
    date_time_str = date_
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
    date_fin=date_time_obj + timedelta(days=dias)
   
    return date_fin.date()
