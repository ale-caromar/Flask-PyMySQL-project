# Importar pymysql y el módulo cursors que se usa para ejecutar consultas SQL (SELECT, INSERT, UPDATE, DELETE)
import pymysql.cursors

# Se define la clase MySQLConnection
class MySQLConnection:
    # El __init__ inicializa una conexión a la base de datos MySQL.
    def __init__(self, db):
        # Se establece la conexión con los parámetros necesarios como el host, usuario, contraseña y base de datos.
        connection = pymysql.connect(host = 'localhost',  
                                    user = 'root',       
                                    password = 'root',   
                                    db = db,              
                                    charset = 'utf8mb4', #para manejar caracteres especiales
                                    cursorclass = pymysql.cursors.DictCursor, #'DictCursor' para recibir resultados como diccionarios
                                    autocommit = True, # Permite que las operaciones hacia la DB se confirmen automáticamente
                                    )
        # Se asigna la conexión a un atributo de la instancia para usarla en otros métodos
        self.connection = connection

    # Ejecuta la consulta SQL, maneja las operaciones y devuelve resultados según el tipo de consulta.
    def query_db(self, query, data=None):
        # Usa un cursor para ejecutar la consulta SQL.
        with self.connection.cursor() as cursor:
            try:
                #Prepara la consulta SQL (incluyendo datos si se proporcionan)
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                
                #Ejecuta la consulta SQL con los datos proporcionados
                executable = cursor.execute(query, data) 

                #Si la consulta es un insert, devuelve el id de la última fila, ya que esa es la fila que acabamos de agregar
                if query.lower().find("insert") >= 0:
                    self.connection.commit() # Realiza los cambios en la base de datos
                    return cursor.lastrowid  # Devuelve el ID del último registro insertado
                
                #Si la consulta es un SELECT, devuelve todos los resultados obtenidos.
                elif query.lower().find("select") >= 0:
                    # Si la consulta es un select, devuelve todo lo que se obtiene de la base de datos
                    # El resultado será una lista de diccionarios
                    result = cursor.fetchall() # Recupera todos los resultados para consultas SELECT
                    return result
                
                #Si la consulta es una actualización o eliminación, realiza un commit para confirmar los cambios.
                else:
                    self.connection.commit()
            except Exception as e:
                # En caso de error durante la consulta, imprime el mensaje de error y retorna False.
                print("Algo salió mal", e)
                return False
            finally:
                # Cierra la conexión a la base de datos después de ejecutar la consulta.
                self.connection.close() 

# Función para crear una instancia de MySQLConnection con la base de datos.
def connectToMySQL(db):
    return MySQLConnection(db)