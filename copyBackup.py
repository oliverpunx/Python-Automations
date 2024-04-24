#creado por mlopez 24/04/2024
#copiar respaldo de bd de servidor linux a 
#disco duro conectado en otro equipo (servidor de fuentes de desarrollo)

import paramiko
import os
import logging
from datetime import datetime
from paramiko import SSHClient
from scp import SCPClient

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
raiz='//192.168.2.122/e$/respaldos/'+anio+'/'
nomarchivo='fullexport_'+dia+mes+anio+'013000.dmp'

try:
    ruta='Oracle/DUMP/'
    #ruta donde se grabará el respaldo
    print(raiz+ruta+nomMes)    
    #nombre del archivo que se copiará
    print(nomarchivo)
    
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    #iniciando archivo de log
    registraLog=create_log('C:/resources_mlopez/logs/copiaDMP'+ dia + mes + anio +'.log')
    registraLog.debug('Conectando al servidor....')

    #conexion al servidor donde está el respaldo
    ssh.connect(hostname='192.168.2.126',username='root',password='ToqhSA*eJc')
    registraLog.info('Conexion exitosa....')

except Exception as error:
       registraLog.info('Cerrando conexion....')
       ssh.close()
       registraLog.error('Ocurrió el error CONNECT: '+str(error.args))
       print('Ocurrió el error CONNECT: '+str(error.args))

try:
    # copia archivo DMP a disco de backup
    registraLog.info('Iniciando copia.....')
    scp = SCPClient(ssh.get_transport())

    try:
        scp.get('/respaldos/respaldos_dmp/'+nomarchivo, raiz + ruta + nomMes)
        registraLog.info('copiado exitoso')

        #elimina archivo DMP en origen
        try:
            registraLog.info('Iniciando eliminación de archivo DMP en origen.....')

            if os.path.exists(archivo):
               os.remove('/respaldos/respaldos_dmp/'+nomarchivo)
               registraLog.info("El archivo "+ nomarchivo +" ha sido eliminado")
            else:
               registraLog.error('Ocurrió un error al eliminar archivo en el origen: Archivo no existe.')

        except Exception as error:
            registraLog.info('Cerrando conexion durante eliminación de archivo en origen....')
            scp.close()
            registraLog.error('Ocurrio un error al eliminar archivo '+ nomarchivo +' en el origen: '+str(error.args))
            print('Ocurrio un error al eliminar archivo '+ nomarchivo +' en el origen: '+str(error.args))         
    
    except Exception as error:
           registraLog.info('Cerrando conexion durante el copiado....')
           scp.close()
           registraLog.error('Ocurrió un error al copiar archivo: '+ nomarchivo + str(error.args))
           print('Ocurrio un error al copiar archivo '+nomarchivo+': '+str(error.args))
 
except Exception as error:
       registraLog.info('Cerrando conexion al intentar copiar el archivo....')
       scp.close()
       registraLog.error('Ocurrio un error en get_transport '+str(error.args))
       print('Ocurrió un error en get_transport: '+str(error.args))

scp.close()       