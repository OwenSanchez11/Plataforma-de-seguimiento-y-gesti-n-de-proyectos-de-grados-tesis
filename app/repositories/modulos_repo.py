from app.core.database import Database
from app.models.modulo import Modulo


class ModuloRepository:

    def __init__(self):
        self.db = Database()

    def obtenerModulos(self):
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

    def obtenerModuloId(self, id_modulo: int):
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

    def crearModulo(self, modulo: Modulo):
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

    def actualizarModulo(self, id_modulo: int, modulo: Modulo):
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

    def eliminarModulo(self, id_modulo: int):
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