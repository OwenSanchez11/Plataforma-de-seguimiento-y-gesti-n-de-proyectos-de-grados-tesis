import psycopg2
from app.core.database import Database
from app.models.equipo_trabajo import (
    EquipoTrabajo
)


class EquipoTrabajoRepository:

    def __init__(self):
        self.db = Database()

    def obtenerEquiposTrabajo(self):

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

            equipos = cursor.fetchall()

            conn.close()

            return equipos

        except psycopg2.Error as e:
            print("Error al obtener equipos de trabajo:", e)
            return []

    def obtenerEquipoTrabajoPorId(
        self,
        id_equipo: int,
    ):
        conn = None
        cursor = None

        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM equipo_trabajo
                WHERE id_equipo = %s
            """, (
                id_equipo,
            ))

            equipo = cursor.fetchone()

            return equipo

        except psycopg2.Error as e:
            print("Error al obtener equipo de trabajo:", e)
            return None

    def crearEquipoTrabajo(
        self,
        equipo: EquipoTrabajo
    ):

        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
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
                RETURNING id_equipo;
            """, (
                equipo.id_trabajo_grado,
                equipo.id_usuario,
                equipo.id_rol_proyecto,
                equipo.observaciones,
                equipo.fecha_asignacion,
                equipo.fecha_finalizacion,
                equipo.estado
            ))

            resultado = cursor.fetchone()["id_equipo"]

            conn.commit()
            conn.close()

            return resultado

        except psycopg2.Error as e:
            print("Error al crear equipo de trabajo:", e)
            return None

    def actualizarEquipoTrabajo(
        self,
        id_equipo: int,
        equipo: EquipoTrabajo
    ):
        conn = None
        cursor = None

        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE equipo_trabajo
                SET
                    id_trabajo_grado = COALESCE(%s, id_trabajo_grado),
                    id_usuario = COALESCE(%s, id_usuario),
                    id_rol_proyecto = COALESCE(%s, id_rol_proyecto),
                    observaciones = COALESCE(%s, observaciones),
                    fecha_asignacion = COALESCE(%s, fecha_asignacion),
                    fecha_finalizacion = COALESCE(%s, fecha_finalizacion),
                    estado = COALESCE(%s, estado)
                WHERE id_equipo = %s
                RETURNING
                    id_equipo,
                    id_trabajo_grado,
                    id_usuario,
                    id_rol_proyecto,
                    observaciones,
                    fecha_asignacion,
                    fecha_finalizacion,
                    estado
            """, (
                equipo.id_trabajo_grado,
                equipo.id_usuario,
                equipo.id_rol_proyecto,
                equipo.observaciones,
                equipo.fecha_asignacion,
                equipo.fecha_finalizacion,
                equipo.estado,
                id_equipo
            ))

            actualizado = cursor.fetchone()

            conn.commit()

            return actualizado

        except psycopg2.Error as e:
            if conn:
                conn.rollback()

            print("Error al actualizar equipo de trabajo:", e)
            return None


    def eliminarEquipoTrabajo(
        self,
        id_equipo: int
    ):
        conn = None
        cursor = None

        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM equipo_trabajo
                WHERE id_equipo = %s
                RETURNING id_equipo
            """, (
                id_equipo,
            ))

            eliminado = cursor.fetchone()

            conn.commit()

            return eliminado

        except psycopg2.Error as e:
            if conn:
                conn.rollback()

            print("Error al eliminar equipo de trabajo:", e)
            return None

        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()