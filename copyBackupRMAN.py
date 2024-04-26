import os
import shutil
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
    
    return result

#obtengo nombre de carpeta anio/mes segun fecha actual
now = datetime.now()
dia=str(current_date_format(now,'dia'))
anio=str(current_date_format(now,'anio'))
mes=str(current_date_format(now,'nummes'))
nomMes=current_date_format(now,'mes')    

nomarchivoLog='copyRMAN_'+dia+mes+anio+'.log'

origen='//pc-origen/respaldos/'
destino='//pc-destino/e$/respaldos/'+anio+'/'+ nomMes +'/'+ dia+'/'

#lista los archivos a copiar de la carpeta origen
contenidos=os.listdir(origen)
registraLog=create_log('C:/backups/logs/copiaDMP'+ dia + mes + anio +'.log')
registraLog.debug('Iniciando copia de archivos backup RMAN....')

for elemento in contenidos:
    try:
        #iniciando archivo de log
        registraLog.info(f"Copiando {elemento} --> {destino} ... ", end="")

        src = os.path.join(origen, elemento) # origen
        dst = os.path.join(destino, elemento) # destino

        shutil.copy(src, dst)
        registraLog.debug('Copia exitosa....')

    except Exception as error:
           registraLog.info('Cerrando conexion....')
           registraLog.error('Ocurrió un error al copiar backup RMAN: '+str(error.args))
           print('Ocurrió un error al copiar backup RMAN: '+str(error.args)+' : '+f"Copiando {elemento} --> {destino} ... ", end="")
