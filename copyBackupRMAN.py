
import os
import logging
from datetime import datetime

#funcion para crear archivo de log
def create_log(name):
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename=name,filemode='w', encoding='utf-8', level=logging.DEBUG)
    logging.basicConfig(format='%(asctime)s %(message)s')
    
    return logger

#funcion para obtener las partes de una fecha
# dia, mes, mes en letras, año
def current_date_format(fecha,tipo):
    months = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    result=''

    if tipo=='mes':
       result = months[fecha.month - 1]

    if tipo=='nummes':
       result = fecha.month

       if len(str(result))==1:
          result='0'+str(result)
    
    if tipo=='anio':
       result = fecha.year

    if tipo=='dia':
       result = fecha.day

       if len(str(result))==1:
          result='0'+str(result)

    if tipo=='diaFolder':
       result = fecha.day
    
    return result

#obtengo nombre de carpeta anio/mes segun fecha actual
now = datetime.now()
#print(str(now))
dia=str(current_date_format(now,'dia'))
diaFolder=str(current_date_format(now,'diaFolder'))
anio=str(current_date_format(now,'anio'))
mes=str(current_date_format(now,'nummes'))
nomMes=current_date_format(now,'mes')    

nomarchivoLog='copyRMAN_'+ dia + mes + anio + '.log'

origen=r"/respaldos/respaldos_RMAN/"
destino=r"//192.168.2.122/e$/respaldos/"
destino=destino + anio + '/Oracle/RMAN/' + nomMes + '/' + diaFolder +'/'
