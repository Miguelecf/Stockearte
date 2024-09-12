# infrastructure/user_repository.py
import mysql.connector
from domain.entities import User
from domain.interfaces import UserRepositoryInterface
from config.db_config import DB_CONFIG

class MySQLUserRepository(UserRepositoryInterface):
    def get_user_by_username(self, username: str) -> User:
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor(dictionary=True)

            query = "SELECT username, password, enabled FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            print(result)

            cursor.close()
            connection.close()

            if result:
                return User(username=result['username'], password=result['password'], enabled=result['enabled'])
            return None
        except mysql.connector.Error as err:
            print(f"Error de base de datos: {err}")
            return None

    def create_user(self, username: str, password: str) -> bool:
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor()

            # Consulta para insertar un nuevo usuario en la base de datos
            query = """
                INSERT INTO users (username, password, enabled,role,first_name,last_name)
                VALUES (%s, %s, %s,%s,%s,%s)
            """
            values = (username, password, True,2, "aaaa","aaa")
            cursor.execute(query, values)

            # Confirma la transacción
            connection.commit()

            cursor.close()
            connection.close()

            return cursor.rowcount > 0  # Retorna True si la inserción fue exitosa

        except mysql.connector.Error as err:
            print(f"Error de base de datos: {err}")
            return False
