import mysql.connector

def conectar():
    connection = mysql.connector.connect(host='34.123.1.37',
                                        database='db_quadros',
                                        user='root',
                                        password='123456')
    return connection

# if connection.is_connected():
#     print("Conectado")
#     cursor = connection.cursor()

# conectar.close()
# cursor.close()

#crud
def create(title, url, views, likes, comments, duration):
    conexao = conectar()
    cursor = conexao.cursor()
    comando = 'INSERT INTO querido_diario (title, url, views, likes, comments, duration) VALUES (%s, %s, %s, %s, %s, %s)'
    valores = (title, url, views, likes, comments, duration)
    cursor.execute(comando, valores)
    conexao.commit()
    cursor.close()
    conexao.close()



# def read():
#     comando = 'SELECT * FROM querido_diario'
#     cursor.execute(comando)
#     resultado = cursor.fetchall()
#     return resultado

# def update():
#     comando = 'UPDATE querido_diario SET DATAFRAME'
#     cursor.execute(comando)
#     connection.commit()

# def delete():
#     comando = 'DELETE FROM querido_diario DATAFRAME'
#     cursor.execute(comando)
#     connection.commit()