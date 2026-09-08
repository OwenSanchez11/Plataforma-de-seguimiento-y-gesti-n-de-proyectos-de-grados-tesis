import psycopg2
from app.core.database import Database
from app.models.retroalimentaciones import Retroalimentacion


class RetroalimentacionesRepository:

    def __init__(self):
        self.db = Database()

    def obtenerRetroalimentacion(self):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM retroalimentaciones
                ORDER BY id_retroalimentacion ASC
            """)

            retroalimentaciones = cursor.fetchall()

            conn.close()

            return retroalimentaciones

        except psycopg2.Error as e:
            print("Error al obtener retroalimentaciones:", e)
            return []

    def obtenerRetroalimentacionPorId(self, id_retroalimentacion: int):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM retroalimentaciones
                WHERE id_retroalimentacion = %s;
            """, (id_retroalimentacion,))

            retroalimentacion = cursor.fetchone()

            conn.close()

            return retroalimentacion

        except psycopg2.Error as e:
            print("Error al obtener retroalimentación:", e)
            return None

    def crearRetroalimentacion(
        self,
        retroalimentacion: Retroalimentacion
    ):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            query = """
                INSERT INTO retroalimentaciones (
                    id_avance,
                    id_usuario,
                    comentario,
                    estado
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id_retroalimentacion;
            """

            cursor.execute(
                query,
                (
                    retroalimentacion.id_avance,
                    retroalimentacion.id_usuario,
                    retroalimentacion.comentario,
                    retroalimentacion.estado
                )
            )

            id_retroalimentacion = cursor.fetchone()["id_retroalimentacion"]

            conn.commit()
            conn.close()

            return {
                "mensaje": "Retroalimentación creada correctamente",
                "id_retroalimentacion": id_retroalimentacion
            }

        except psycopg2.Error as e:
            print("Error al crear retroalimentación:", e)
            return {
                "error": "No se pudo crear la retroalimentación"
            }

    def actualizarRetroalimentacion(
        self,
        id_retroalimentacion: int,
        retroalimentacion: Retroalimentacion
    ):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            query = """
                UPDATE retroalimentaciones
                SET
                    id_avance = %s,
                    id_usuario = %s,
                    comentario = %s,
                    estado = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_retroalimentacion = %s
                RETURNING id_retroalimentacion;
            """

            cursor.execute(
                query,
                (
                    retroalimentacion.id_avance,
                    retroalimentacion.id_usuario,
                    retroalimentacion.comentario,
                    retroalimentacion.estado,
                    id_retroalimentacion
                )
            )

            retroalimentacion_actualizada = cursor.fetchone()

            conn.commit()
            conn.close()

            return retroalimentacion_actualizada is not None

        except psycopg2.Error as e:
            print("Error al actualizar retroalimentación:", e)
            return False

    def eliminarRetroalimentacion(self, id_retroalimentacion: int):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM retroalimentaciones
                WHERE id_retroalimentacion = %s
                RETURNING id_retroalimentacion;
            """, (id_retroalimentacion,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None

        except psycopg2.Error as e:
            print("Error al eliminar retroalimentación:", e)
            return False