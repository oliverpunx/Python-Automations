#creado por mlopez 22/05/2024
#copiar fuentes de desarrollo NAF
import os
import logging
#import shutil
from distutils.dir_util import copy_tree

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
       result=fecha.day
       
       if len(str(result))==1:
          result='0'+str(result)    
    
    return result

#obtengo nombre de carpeta anio/mes segun fecha actual
now = datetime.now()
dia=str(current_date_format(now,'dia'))
anio=str(current_date_format(now,'anio'))
mes=str(current_date_format(now,'nummes'))
nomMes=current_date_format(now,'mes')    
ruta='//192.168.2.122/e$/respaldos/desarrollo/'+anio+'/'
origen='c:/naf47/'

nomarchivoLog='backupFuentes'+dia+mes+anio+'.log'

try:
    #ruta donde se grabará el respaldo
    print('ruta destino: '+ruta)    
    print('ruta origen: '+origen)      
    
    #iniciando archivo de log
    registraLog=create_log('C:/scripts_python/logs/backupFuentes_'+ dia + mes + anio +'.log')
    registraLog.debug('Log iniciado....')
    subruta=ruta+mes+dia+'/naf47'
    
    try:
        if os.path.exists(ruta):
           os.makedirs(subruta)
        else:
            print('No se pudo crear subruta, no existe la ruta principal: '+ruta)
    
    except Exception as error:
       registraLog.info('Cerrando Log....')
       registraLog.error('Ocurrió el error al crear subruta: '+str(error.args))
       print('Ocurrió el error al crear subruta: '+str(error.args))

except Exception as error:
       registraLog.info('Cerrando Log....')
       registraLog.error('Ocurrió el error al iniciar archivo de log: '+str(error.args))
       print('Ocurrió el error al iniciar archivo de log: '+str(error.args))

try:
    # copia backup de fuentes
    registraLog.info('Iniciando copia de backup de fuentes NAF.....')
    print('DESTINO FINAL: '+subruta)
    
    if not os.path.isdir(subruta):
       print(subruta+' no existe')
    elif not os.path.isdir(origen):
        print(origen+' no existe')
    else:
        contenidos=os.listdir(origen)
        
        for elemento in contenidos:
            registraLog.info('copiando: '+elemento)
            shutil.copy(origen+elemento, subruta)
            registraLog.info('Copiado')
            
        registraLog.info('copiando: '+elemento)
        copy_tree(origen, subruta)
      
    registraLog.info('Respaldo copiado con éxito.')
    
except Exception as error:
       registraLog.info('Cerrando conexion al intentar copiar el archivo....')
       registraLog.error('Ocurrio un error al copiar backup de fuentes NAF '+str(error.args))
       print('Ocurrio un error al copiar backup de fuentes NAF: '+str(error.args))
    
