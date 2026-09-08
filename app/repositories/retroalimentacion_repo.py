from app.core.database import Database
from app.models.retroalimentaciones import Retroalimentacion


class RetroalimentacionesRepository:

    def __init__(self):
        self.db = Database()

    def obtenerRetroalimentacion(self):
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

    def obtenerRetroalimentacionPorId(self, id_retroalimentacion: int):
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

    def crearRetroalimentacion(
        self,
        retroalimentacion: Retroalimentacion
    ):
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

    def actualizarRetroalimentacion(
        self,
        id_retroalimentacion: int,
        retroalimentacion: Retroalimentacion
    ):
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

    def eliminarRetroalimentacion(self, id_retroalimentacion: int):
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