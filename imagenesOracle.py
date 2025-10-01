import cx_Oracle
import os

# Configuración de conexión
username = "libra"
password = "aRkkL9a0QWVQ"
dsn = "10.1.2.3/libra"  # Cambia por tu cadena de conexión Oracle

# Carpeta destino
output_dir = "imagenes_activos"
os.makedirs(output_dir, exist_ok=True)

try:
    # Conexión a Oracle
    connection = cx_Oracle.connect(username, password, dsn)
    cursor = connection.cursor()

    # Consulta de imágenes
    sql = '''select a.codigo ID,rpad(rtrim(ltrim(substr(a.descripcion,1,5))),5,'Z') NOMBRE,'png' tipo,b.imagen IMAGEN_BLOB
  from inmovilizado a,IMA_INMOVILIZADO b
 where a.empresa=b.empresa and a.codigo=b.codigo 
  and b.imagen is not null'''
    cursor.execute(sql)

    for row in cursor:
        id_imagen, nombre, tipo, blob_data = row

        # Si no tiene extensión en la BD, intentamos inferirla
        extension = ""
        if tipo:
            if "jpeg" in tipo:
                extension = ".jpg"
            elif "png" in tipo:
                extension = ".png"
            elif "gif" in tipo:
                extension = ".gif"

        # Nombre de archivo
        filename = f"{id_imagen}_{nombre}{extension}"
        filepath = os.path.join(output_dir, filename)

        # Guardar BLOB en archivo
        with open(filepath, "wb") as f:
            f.write(blob_data.read())

        print(f"✅ Imagen guardada: {filepath}")

except cx_Oracle.DatabaseError as e:
    print("❌ Error de base de datos:", e)

finally:
    # Cerrar recursos
    try:
        cursor.close()
        connection.close()
    except:
        pass
