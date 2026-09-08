from app.core.database import Database
from app.models.asignacion import Asignacion


class AsignacionRepository:

    def __init__(self):
        self.db = Database()

    def obtenerAsignaciones(self):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM equipo_trabajo
                ORDER BY id_trabajo_grado ASC,
                         id_usuario ASC,
                         id_rol_proyecto ASC
            """)

            asignaciones = cursor.fetchall()
            conn.close()

            return asignaciones

        except Exception as e:
            print(f"Error al obtener asignaciones: {e}")
            return []

    def obtenerAsignacionPorId(
        self,
        id_trabajo_grado: int,
        id_usuario: int,
        id_rol_proyecto: int
    ):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM equipo_trabajo
                WHERE id_trabajo_grado = %s
                  AND id_usuario = %s
                  AND id_rol_proyecto = %s;
            """, (
                id_trabajo_grado,
                id_usuario,
                id_rol_proyecto
            ))

            asignacion = cursor.fetchone()
            conn.close()

            return asignacion

        except Exception as e:
            print(f"Error al obtener la asignación: {e}")
            return None

    def crearAsignacion(self, asignacion: Asignacion):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            query = """
                INSERT INTO equipo_trabajo (
                    id_trabajo_grado,
                    id_usuario,
                    id_rol_proyecto,
                    observaciones,
                    fecha_asignacion,
                    fecha_finalizacion,
                    estado
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    COALESCE(%s, CURRENT_DATE),
                    %s,
                    %s
                )
                RETURNING
                    id_trabajo_grado,
                    id_usuario,
                    id_rol_proyecto;
            """

            cursor.execute(
                query,
                (
                    asignacion.id_trabajo_grado,
                    asignacion.id_usuario,
                    asignacion.id_rol_proyecto,
                    asignacion.observaciones,
                    asignacion.fecha_asignacion,
                    asignacion.fecha_finalizacion,
                    asignacion.estado
                )
            )

            resultado = cursor.fetchone()

            conn.commit()
            conn.close()

            return {
                "mensaje": "Asignación creada correctamente",
                "id_trabajo_grado": resultado["id_trabajo_grado"],
                "id_usuario": resultado["id_usuario"],
                "id_rol_proyecto": resultado["id_rol_proyecto"]
            }

        except Exception as e:
            print(f"Error al crear la asignación: {e}")
            return {
                "mensaje": "Error al crear la asignación",
                "error": str(e)
            }

    def actualizarAsignacion(
        self,
        id_trabajo_grado: int,
        id_usuario: int,
        id_rol_proyecto: int,
        asignacion: Asignacion
    ):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            query = """
                UPDATE equipo_trabajo
                SET
                    observaciones = %s,
                    fecha_asignacion = %s,
                    fecha_finalizacion = %s,
                    estado = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_trabajo_grado = %s
                  AND id_usuario = %s
                  AND id_rol_proyecto = %s
                RETURNING
                    id_trabajo_grado,
                    id_usuario,
                    id_rol_proyecto;
            """

            cursor.execute(
                query,
                (
                    asignacion.observaciones,
                    asignacion.fecha_asignacion,
                    asignacion.fecha_finalizacion,
                    asignacion.estado,
                    id_trabajo_grado,
                    id_usuario,
                    id_rol_proyecto
                )
            )

            asignacion_actualizada = cursor.fetchone()

            conn.commit()
            conn.close()

            return asignacion_actualizada is not None

        except Exception as e:
            print(f"Error al actualizar la asignación: {e}")
            return False

    def eliminarAsignacion(
        self,
        id_trabajo_grado: int,
        id_usuario: int,
        id_rol_proyecto: int
    ):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM equipo_trabajo
                WHERE id_trabajo_grado = %s
                  AND id_usuario = %s
                  AND id_rol_proyecto = %s
                RETURNING
                    id_trabajo_grado,
                    id_usuario,
                    id_rol_proyecto;
            """, (
                id_trabajo_grado,
                id_usuario,
                id_rol_proyecto
            ))

            eliminada = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminada is not None

        except Exception as e:
            print(f"Error al eliminar la asignación: {e}")
            return False