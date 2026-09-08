import psycopg2
from app.core.database import Database
from app.models.rol_proyecto import Rol_proyecto


class RolProyectoRepository:

    def __init__(self):
        self.db = Database()

    def obtenerRolesProyecto(self):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM rol_proyecto
                ORDER BY id_rol_proyecto ASC
            """)

            roles = cursor.fetchall()

            conn.close()

            return roles

        except Exception as e:
            print("Error al obtener roles de proyecto:", e)
            return []

    def obtenerPorId(self, id_rol_proyecto: int):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM rol_proyecto
                WHERE id_rol_proyecto = %s;
            """, (id_rol_proyecto,))

            rol = cursor.fetchone()

            conn.close()

            return rol

        except psycopg2.Error as e:
            print("Error al obtener rol de proyecto:", e)
            return None

    def crearRolProyecto(self, rol_proyecto: Rol_proyecto):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            query = """
                INSERT INTO rol_proyecto (
                    nombre,
                    estado
                )
                VALUES (%s, %s)
                RETURNING id_rol_proyecto;
            """

            cursor.execute(
                query,
                (
                    rol_proyecto.nombre,
                    rol_proyecto.estado
                )
            )

            id_rol_proyecto = cursor.fetchone()["id_rol_proyecto"]

            conn.commit()
            conn.close()

            return {
                "mensaje": "Rol de proyecto creado correctamente",
                "id_rol_proyecto": id_rol_proyecto
            }

        except Exception as e:
            print("Error al crear rol de proyecto:", e)
            return {
                "error": "No se pudo crear el rol de proyecto"
            }

    def actualizarRolProyecto(self, id_rol_proyecto: int, rol_proyecto: Rol_proyecto):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            query = """
                UPDATE rol_proyecto
                SET
                    nombre = %s,
                    estado = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_rol_proyecto = %s
                RETURNING id_rol_proyecto;
            """

            cursor.execute(
                query,
                (
                    rol_proyecto.nombre,
                    rol_proyecto.estado,
                    id_rol_proyecto
                )
            )

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None

        except psycopg2.Error as e:
            print("Error al actualizar rol de proyecto:", e)
            return False

    def eliminarRolProyecto(self, id_rol_proyecto: int):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM rol_proyecto
                WHERE id_rol_proyecto = %s
                RETURNING id_rol_proyecto;
            """, (id_rol_proyecto,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None

        except psycopg2.Error as e:
            print("Error al eliminar rol de proyecto:", e)
            return False