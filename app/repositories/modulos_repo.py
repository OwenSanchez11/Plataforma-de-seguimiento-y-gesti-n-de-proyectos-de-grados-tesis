import psycopg2
from app.core.database import Database
from app.models.modulo import Modulo


class ModuloRepository:

    def __init__(self):
        self.db = Database()

    def obtenerModulos(self):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM modulos
                ORDER BY id_modulo ASC
            """)

            modulos = cursor.fetchall()

            conn.close()

            return modulos

        except psycopg2.Error as e:
            print("Error al obtener módulos:", e)
            return []

    def obtenerModuloId(self, id_modulo: int):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM modulos
                WHERE id_modulo = %s;
            """, (id_modulo,))

            modulo = cursor.fetchone()

            conn.close()

            return modulo

        except psycopg2.Error as e:
            print("Error al obtener módulo:", e)
            return None

    def crearModulo(self, modulo: Modulo):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            query = """
                INSERT INTO modulos (
                    nombre_modulo,
                    estado
                )
                VALUES (%s, %s)
                RETURNING id_modulo;
            """

            cursor.execute(
                query,
                (
                    modulo.nombre_modulo,
                    modulo.estado
                )
            )

            id_modulo = cursor.fetchone()["id_modulo"]

            conn.commit()
            conn.close()

            return {
                "mensaje": "Módulo creado correctamente",
                "id_modulo": id_modulo
            }

        except psycopg2.Error as e:
            print("Error al crear módulo:", e)
            return {
                "error": "No se pudo crear el módulo"
            }

    def actualizarModulo(self, id_modulo: int, modulo: Modulo):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            query = """
                UPDATE modulos
                SET
                    nombre_modulo = %s,
                    estado = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_modulo = %s
                RETURNING id_modulo;
            """

            cursor.execute(
                query,
                (
                    modulo.nombre_modulo,
                    modulo.estado,
                    id_modulo
                )
            )

            modulo_actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return modulo_actualizado is not None

        except psycopg2.Error as e:
            print("Error al actualizar módulo:", e)
            return False

    def eliminarModulo(self, id_modulo: int):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM modulos
                WHERE id_modulo = %s
                RETURNING id_modulo;
            """, (id_modulo,))

            modulo_eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return modulo_eliminado is not None

        except psycopg2.Error as e:
            print("Error al eliminar módulo:", e)
            return False