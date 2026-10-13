
import psycopg2

from app.core.database import Database
from app.models.equipo_trabajo import EquipoTrabajo


class EquipoTrabajoRepository:

    def __init__(self):
        self.db = Database()

    def obtenerEquiposTrabajo(self):
        conn = None
        cursor = None

        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM equipo_trabajo
                ORDER BY
                    id_trabajo_grado ASC,
                    id_usuario ASC,
                    id_rol_proyecto ASC
            """)

            return cursor.fetchall()

        except psycopg2.Error as e:
            print("Error al obtener equipos de trabajo:", e)
            return []

        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()

    def obtenerTrabajoPorEstudiante(self, id_user):
        conn = None
        cursor = None

        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            # Buscar el trabajo de grado del usuario.
            cursor.execute("""
                SELECT tg.*
                FROM trabajo_grado tg
                JOIN equipo_trabajo et
                    ON et.id_trabajo_grado = tg.id_trabajo_grado
                WHERE et.id_usuario = %s
                  AND et.estado = TRUE
                  AND et.id_rol_proyecto = 2
                ORDER BY et.fecha_asignacion DESC
                LIMIT 1
            """, (id_user,))

            trabajo = cursor.fetchone()

            if trabajo is None:
                return None

            # Obtener los integrantes activos del trabajo.
            cursor.execute("""
                SELECT
                    u.id_user,
                    u.nombre,
                    u.apellido,
                    u.email AS correo,
                    rp.nombre AS rol_proyecto,
                    et.fecha_asignacion
                FROM equipo_trabajo et
                JOIN usuario u
                    ON u.id_user = et.id_usuario
                LEFT JOIN rol_proyecto rp
                    ON rp.id_rol_proyecto = et.id_rol_proyecto
                WHERE et.id_trabajo_grado = %s
                  AND et.estado = TRUE
                ORDER BY et.id_rol_proyecto ASC, u.nombre ASC
            """, (trabajo["id_trabajo_grado"],))

            equipo = cursor.fetchall()

            return {
                "trabajo": trabajo,
                "equipo": equipo
            }

        except psycopg2.Error as e:
            print("Error al obtener el trabajo del estudiante:", e)
            return None

        finally:
            if cursor:
                cursor.close()


    def obtenerTrabajoPorDocente(self, id_user): 
        conn = self.db.getConnection()
        cursor = conn.cursor()
        
        try:
            # 1) Todos los trabajos donde participa el docente
            cursor.execute(
                """
                    SELECT tg.*,
                        rp.nombre AS rol_docente,
                        c.nombre_carrera AS carrera,
                        ult.nombre_archivo AS ultimo_avance,
                        ult.fecha_entrega AS fecha_ultimo_avance,
                        (ev.id_evaluacion IS NOT NULL) AS evaluado
                    FROM trabajo_grado tg
                    JOIN equipo_trabajo et ON et.id_trabajo_grado = tg.id_trabajo_grado
                    LEFT JOIN rol_proyecto rp ON rp.id_rol_proyecto = et.id_rol_proyecto
                    LEFT JOIN carrera c ON c.id_carrera = tg.id_carrera
                    LEFT JOIN LATERAL (
                        SELECT a.nombre_archivo, a.fecha_entrega
                        FROM avances a
                        WHERE a.id_trabajo_grado = tg.id_trabajo_grado
                            AND a.estado = TRUE
                        ORDER BY a.fecha_entrega DESC NULLS LAST
                        LIMIT 1
                    ) ult ON TRUE
                    LEFT JOIN evaluacion_final ev
                        ON ev.id_trabajo_grado = tg.id_trabajo_grado
                        AND ev.id_usuario = et.id_usuario
                        AND ev.estado = TRUE
                    WHERE et.id_usuario = %s
                        AND et.estado = TRUE
                """, (id_user,))
            trabajos = cursor.fetchall()
            
            if not trabajos:
                return []
            
            ##2) equipos de todos los trabajos en una sola consulta
            
            ids = [t["id_trabajo_grado"] for t in trabajos]
            cursor.execute(
                """
                    SELECT et.id_trabajo_grado,
                            u.id_user, u.nombre, u.apellido, u.email AS correo,
                            rp.nombre AS rol_proyecto,
                            et.fecha_asignacion
                    FROM equipo_trabajo et
                    JOIN usuario u ON u.id_user = et.id_usuario
                    LEFT JOIN rol_proyecto rp ON rp.id_rol_proyecto = et.id_rol_proyecto
                    WHERE et.id_trabajo_Grado = ANY(%s)
                        AND et.estado = TRUE
                """, (ids,)) 
            equipo = cursor.fetchall()
            
            for t in trabajos:
                t["equipo"] = [e for e in equipo if e["id_trabajo_grado"] == t["id_trabajo_grado"]]
                
            return trabajos
        finally:
            cursor.close()
            conn.close()
        
    def obtenerEquipoTrabajoPorId(self, id_equipo):
        conn = None
        cursor = None

        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM equipo_trabajo
                WHERE id_equipo = %s
            """, (id_equipo,))

            return cursor.fetchone()

        except psycopg2.Error as e:
            print("Error al obtener equipo de trabajo:", e)
            return None

        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()

    def crearEquipoTrabajo(self, equipo: EquipoTrabajo):
        conn = None
        cursor = None

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
                RETURNING id_equipo
            """, (
                equipo.id_trabajo_grado,
                equipo.id_usuario,
                equipo.id_rol_proyecto,
                equipo.observaciones,
                equipo.fecha_asignacion,
                equipo.fecha_finalizacion,
                equipo.estado
            ))

            resultado = cursor.fetchone()

            conn.commit()

            return resultado["id_equipo"]

        except psycopg2.Error as e:
            if conn:
                conn.rollback()

            print("Error al crear equipo de trabajo:", e)
            return None

        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()

    def actualizarEquipoTrabajo(self, id_equipo: int, equipo: EquipoTrabajo):
        conn = None
        cursor = None

        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE equipo_trabajo
                SET
                    id_trabajo_grado = COALESCE(
                        %s, id_trabajo_grado
                    ),
                    id_usuario = COALESCE(
                        %s, id_usuario
                    ),
                    id_rol_proyecto = COALESCE(
                        %s, id_rol_proyecto
                    ),
                    observaciones = COALESCE(
                        %s, observaciones
                    ),
                    fecha_asignacion = COALESCE(
                        %s, fecha_asignacion
                    ),
                    fecha_finalizacion = COALESCE(
                        %s, fecha_finalizacion
                    ),
                    estado = COALESCE(
                        %s, estado
                    ),
                    updated_at = CURRENT_TIMESTAMP
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

            if actualizado is None:
                conn.rollback()
                return None

            conn.commit()

            return actualizado

        except psycopg2.Error as e:
            if conn:
                conn.rollback()

            print("Error al actualizar equipo de trabajo:", e)
            return None

        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()

    def eliminarEquipoTrabajo(self, id_equipo: int):
        conn = None
        cursor = None

        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM equipo_trabajo
                WHERE id_equipo = %s
                RETURNING id_equipo
            """, (id_equipo,))

            eliminado = cursor.fetchone()

            if eliminado is None:
                conn.rollback()
                return None

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
