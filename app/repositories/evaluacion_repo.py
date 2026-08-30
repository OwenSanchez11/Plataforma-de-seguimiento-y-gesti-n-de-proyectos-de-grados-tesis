from app.core.database import Database
from app.models.evaluacion import Evaluacion


class EvaluacionRepository:

    def __init__(self):
        self.db = Database()

    def obtenerEvaluaciones(self):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM evaluacion_final
            ORDER BY id_evaluacion ASC
        """)

        evaluaciones = cursor.fetchall()

        conn.close()

        return evaluaciones

    def obtenerEvaluacionPorId(self, id_evaluacion: int):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM evaluacion_final
            WHERE id_evaluacion = %s;
        """, (id_evaluacion,))

        evaluacion = cursor.fetchone()

        conn.close()

        return evaluacion

    def crearEvaluacion(self, evaluacion: Evaluacion):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        query = """
            INSERT INTO evaluacion_final (
                id_trabajo_grado,
                id_usuario,
                nota,
                veredicto,
                observaciones,
                fecha_evaluacion
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                COALESCE(%s, CURRENT_DATE)
            )
            RETURNING id_evaluacion;
        """

        cursor.execute(
            query,
            (
                evaluacion.id_trabajo_grado,
                evaluacion.id_usuario,
                evaluacion.nota,
                evaluacion.veredicto,
                evaluacion.observaciones,
                evaluacion.fecha_evaluacion
            )
        )

        id_evaluacion = cursor.fetchone()["id_evaluacion"]

        conn.commit()
        conn.close()

        return {
            "mensaje": "Evaluación creada correctamente",
            "id_evaluacion": id_evaluacion
        }

    def actualizarEvaluacion(
        self,
        id_evaluacion: int,
        evaluacion: Evaluacion
    ):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        query = """
            UPDATE evaluacion_final
            SET
                id_trabajo_grado = %s,
                id_usuario = %s,
                nota = %s,
                veredicto = %s,
                observaciones = %s,
                fecha_evaluacion = %s
            WHERE id_evaluacion = %s
            RETURNING id_evaluacion;
        """

        cursor.execute(
            query,
            (
                evaluacion.id_trabajo_grado,
                evaluacion.id_usuario,
                evaluacion.nota,
                evaluacion.veredicto,
                evaluacion.observaciones,
                evaluacion.fecha_evaluacion,
                id_evaluacion
            )
        )

        evaluacion_actualizada = cursor.fetchone()

        conn.commit()
        conn.close()

        if evaluacion_actualizada is None:
            return {
                "mensaje": "Evaluación no encontrada"
            }

        return {
            "mensaje": "Evaluación actualizada correctamente"
        }

    def eliminarEvaluacion(self, id_evaluacion: int):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM evaluacion_final
            WHERE id_evaluacion = %s
            RETURNING id_evaluacion;
        """, (id_evaluacion,))

        eliminada = cursor.fetchone()

        conn.commit()
        conn.close()

        if eliminada is None:
            return {
                "mensaje": "Evaluación no encontrada"
            }

        return {
            "mensaje": "Evaluación eliminada correctamente"
        }