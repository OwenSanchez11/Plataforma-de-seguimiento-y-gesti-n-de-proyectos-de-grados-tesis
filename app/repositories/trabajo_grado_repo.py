from app.core.database import Database
from app.models.trabajo_grado import Trabajo_grado


class TrabajoGradoRepository:

    def __init__(self):
        self.db = Database()

    def obtenerTrabajosGrados(self):
        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM trabajo_grado
            ORDER BY id_trabajo_grado ASC
        """)

        trabajos_grado = cursor.fetchall()

        conn.close()

        return trabajos_grado

    def obtenerTrabajoGradoPorId(self, id_trabajo_grado: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM trabajo_grado
            WHERE id_trabajo_grado = %s;
        """, (id_trabajo_grado,))

        trabajo_grado = cursor.fetchone()

        conn.close()

        return trabajo_grado

    def crearTrabajoGrado(self, trabajo_grado: Trabajo_grado):
        conn = self.db.getConnection()
        cursor = conn.cursor()

        query = """
            INSERT INTO trabajo_grado (
                id_carrera,
                titulo,
                resumen,
                linea_investigacion,
                estado_tramite,
                fecha_inicio,
                fecha_fin,
                fecha_sustentacion,
                observaciones_finales,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_trabajo_grado;
        """

        cursor.execute(
            query,
            (
                trabajo_grado.id_carrera,
                trabajo_grado.titulo,
                trabajo_grado.resumen,
                trabajo_grado.linea_investigacion,
                trabajo_grado.estado_tramite,
                trabajo_grado.fecha_inicio,
                trabajo_grado.fecha_fin,
                trabajo_grado.fecha_sustentacion,
                trabajo_grado.observaciones_finales,
                trabajo_grado.estado
            )
        )

        id_trabajo_grado = cursor.fetchone()["id_trabajo_grado"]

        conn.commit()
        conn.close()

        return {
            "mensaje": "Trabajo de grado creado correctamente",
            "id_trabajo_grado": id_trabajo_grado
        }

    def actualizarTrabajoGrado(
        self,
        id_trabajo_grado: int,
        trabajo_grado: Trabajo_grado
    ):
        conn = self.db.getConnection()
        cursor = conn.cursor()

        query = """
            UPDATE trabajo_grado
            SET
                id_carrera = %s,
                titulo = %s,
                resumen = %s,
                linea_investigacion = %s,
                estado_tramite = %s,
                fecha_inicio = %s,
                fecha_fin = %s,
                fecha_sustentacion = %s,
                observaciones_finales = %s,
                estado = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id_trabajo_grado = %s
            RETURNING id_trabajo_grado;
        """

        cursor.execute(
            query,
            (
                trabajo_grado.id_carrera,
                trabajo_grado.titulo,
                trabajo_grado.resumen,
                trabajo_grado.linea_investigacion,
                trabajo_grado.estado_tramite,
                trabajo_grado.fecha_inicio,
                trabajo_grado.fecha_fin,
                trabajo_grado.fecha_sustentacion,
                trabajo_grado.observaciones_finales,
                trabajo_grado.estado,
                id_trabajo_grado
            )
        )

        trabajo_grado_actualizado = cursor.fetchone()

        conn.commit()
        conn.close()

        return trabajo_grado_actualizado is not None

    def eliminarTrabajoGrado(self, id_trabajo_grado: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM trabajo_grado
            WHERE id_trabajo_grado = %s
            RETURNING id_trabajo_grado;
        """, (id_trabajo_grado,))

        eliminado = cursor.fetchone()

        conn.commit()
        conn.close()

        return eliminado is not None