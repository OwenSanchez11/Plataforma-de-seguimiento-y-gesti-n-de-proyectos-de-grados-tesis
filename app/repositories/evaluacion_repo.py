import psycopg2
from app.core.database import Database
from app.models.evaluacion import Evaluacion
from fastapi import HTTPException

class EvaluacionRepository:

    def __init__(self):
        self.db = Database()

    def obtenerEvaluaciones(self, id_carrera=None, id_facultad=None):

        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            query = """
                SELECT e.*
                FROM evaluacion_final e 
                LEFT JOIN trabajo_grado t ON e.id_trabajo_grado = t.id_trabajo_grado
                LEFT JOIN carrera c ON t.id_carrera = c.id_carrera            
            """
            
            condiciones = []
            valores = []


            if id_carrera is not None:
                condiciones.append("c.id_carrera = %s")
                valores.append(id_carrera)
                
            if id_facultad is not None:
                condiciones.append("c.id_facultad = %s")
                valores.append(id_facultad)
                
            if condiciones:
                query += " WHERE " + " AND ".join(condiciones)                

            cursor.execute(query, valores)
            evaluaciones = cursor.fetchall()
            conn.close()
            
            return evaluaciones

        except psycopg2.Error as e:
            print("Error al obtener evaluaciones:", e)
            return []

    def obtenerEvaluacionPorId(self, id_evaluacion: int):

        try:
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

        except psycopg2.Error as e:
            print("Error al obtener evaluación:", e)
            return None

    def crearEvaluacion(self, evaluacion: Evaluacion):
        conn = None
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            query = """
                INSERT INTO evaluacion_final (
                    id_trabajo_grado,
                    id_usuario,
                    nota,
                    veredicto,
                    observaciones,
                    fecha_evaluacion,
                    estado
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    COALESCE(%s, CURRENT_DATE),
                    %s
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
                    evaluacion.fecha_evaluacion,
                    evaluacion.estado
                )
            )

            id_evaluacion = cursor.fetchone()["id_evaluacion"]

            conn.commit()

            conn.close()

            return {
                "mensaje": "Evaluación creada correctamente",
                "id_evaluacion": id_evaluacion
            }

        except psycopg2.errors.ForeignKeyViolation:
            conn.rollback()
            raise HTTPException(status_code=400, detail="El trabajo de grado o el usuario no existe")
        except psycopg2.Error as e:
            conn.rollback()
            print("Error al crear evaluación:", e)
            raise HTTPException(status_code=500, detail="No se pudo crear la evaluación")
        finally:
            if conn:
                conn.close()

    def actualizarEvaluacion(self, id_evaluacion: int, evaluacion: Evaluacion):
        conn = None
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            query = """
                UPDATE evaluacion_final
                SET id_trabajo_grado = %s,
                    id_usuario = %s,
                    nota = %s,
                    veredicto = %s,
                    observaciones = %s,
                    fecha_evaluacion = COALESCE(%s, fecha_evaluacion),
                    estado = %s
                WHERE id_evaluacion = %s
                RETURNING id_evaluacion;
            """

            cursor.execute(query, (
                evaluacion.id_trabajo_grado,
                evaluacion.id_usuario,
                evaluacion.nota,
                evaluacion.veredicto,
                evaluacion.observaciones,
                evaluacion.fecha_evaluacion,
                evaluacion.estado,
                id_evaluacion
            ))

            fila = cursor.fetchone()
            if fila is None:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Evaluación no encontrada")

            conn.commit()
            return {"mensaje": "Evaluación actualizada correctamente", "id_evaluacion": fila["id_evaluacion"]}

        except psycopg2.errors.ForeignKeyViolation:
            conn.rollback()
            raise HTTPException(status_code=400, detail="El trabajo de grado o el usuario no existe")
        except psycopg2.Error as e:
            conn.rollback()
            print("Error al actualizar evaluación:", e)
            raise HTTPException(status_code=500, detail="No se pudo actualizar la evaluación")
        finally:
            if conn:
                conn.close()

    def eliminarEvaluacion(self, id_evaluacion: int):

        try:
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

            return eliminada is not None

        except psycopg2.Error as e:
            print("Error al eliminar evaluación:", e)
            return False