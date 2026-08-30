from app.core.database import Database
from app.models.asignacion import Asignacion


class AsignacionRepository:

    def __init__(self):
        self.db = Database()


    def obtenerAsignaciones(self):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM asignacion
            ORDER BY id_asignacion ASC
        """)

        asignaciones = cursor.fetchall()

        conn.close()

        return asignaciones


    def obtenerAsignacionPorId(self, id_asignacion: int):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM asignacion
            WHERE id_asignacion = %s;
        """, (id_asignacion,))

        asignacion = cursor.fetchone()

        conn.close()

        return asignacion


    def crearAsignacion(self, asignacion: Asignacion):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        query = """
            INSERT INTO asignacion (
                id_trabajo_grado,
                id_usuario,
                id_rol,
                fecha_asignacion,
                estado
            )
            VALUES (
                %s,
                %s,
                %s,
                COALESCE(%s, CURRENT_DATE),
                %s
            )
            RETURNING id_asignacion;
        """

        cursor.execute(
            query,
            (
                asignacion.id_trabajo_grado,
                asignacion.id_usuario,
                asignacion.id_rol,
                asignacion.fecha_asignacion,
                asignacion.estado
            )
        )

        id_asignacion = cursor.fetchone()["id_asignacion"]

        conn.commit()

        conn.close()

        return {
            "mensaje": "Asignación creada correctamente",
            "id_asignacion": id_asignacion
        }


    def actualizarAsignacion(
        self,
        id_asignacion: int,
        asignacion: Asignacion
    ):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        query = """
            UPDATE asignacion
            SET
                id_trabajo_grado = %s,
                id_usuario = %s,
                id_rol = %s,
                fecha_asignacion = %s,
                estado = %s
            WHERE id_asignacion = %s
            RETURNING id_asignacion;
        """

        cursor.execute(
            query,
            (
                asignacion.id_trabajo_grado,
                asignacion.id_usuario,
                asignacion.id_rol,
                asignacion.fecha_asignacion,
                asignacion.estado,
                id_asignacion
            )
        )

        asignacion_actualizada = cursor.fetchone()

        conn.commit()

        conn.close()

        if asignacion_actualizada is None:

            return {
                "mensaje": "Asignación no encontrada"
            }

        return {
            "mensaje": "Asignación actualizada correctamente"
        }


    def eliminarAsignacion(self, id_asignacion: int):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM asignacion
            WHERE id_asignacion = %s
            RETURNING id_asignacion;
        """, (id_asignacion,))

        eliminada = cursor.fetchone()

        conn.commit()

        conn.close()

        if eliminada is None:

            return {
                "mensaje": "Asignación no encontrada"
            }

        return {
            "mensaje": "Asignación eliminada correctamente"
        }