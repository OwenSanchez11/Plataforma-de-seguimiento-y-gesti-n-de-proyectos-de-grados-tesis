import psycopg2
from app.core.database import Database
from app.models.rol import Rol


class RolRepository:

    def __init__(self):
        self.db = Database()

    def obtenerRoles(self):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM rol
                ORDER BY id_rol ASC
            """)

            roles = cursor.fetchall()

            conn.close()

            return roles

        except psycopg2.Error as e:
            print("Error al obtener roles:", e)
            return []

    def obtenerRolPorId(self, id_rol: int):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM rol
                WHERE id_rol = %s;
            """, (id_rol,))

            rol = cursor.fetchone()

            conn.close()

            return rol

        except psycopg2.Error as e:
            print("Error al obtener rol:", e)
            return None

    def crearRol(self, rol: Rol):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            query = """
                INSERT INTO rol (
                    rol_nombre,
                    estado
                )
                VALUES (%s, %s)
                RETURNING id_rol;
            """

            cursor.execute(
                query,
                (
                    rol.rol_nombre,
                    rol.estado
                )
            )

            id_rol = cursor.fetchone()["id_rol"]

            conn.commit()
            conn.close()

            return {
                "mensaje": "Rol creado correctamente",
                "id_rol": id_rol
            }

        except psycopg2.Error as e:
            print("Error al crear rol:", e)
            return {
                "error": "No se pudo crear el rol"
            }

    def actualizarRol(self, id_rol: int, rol: Rol):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            query = """
                UPDATE rol
                SET
                    rol_nombre = %s,
                    estado = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_rol = %s
                RETURNING id_rol;
            """

            cursor.execute(
                query,
                (
                    rol.rol_nombre,
                    rol.estado,
                    id_rol
                )
            )

            rol_actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return rol_actualizado is not None

        except psycopg2.Error as e:
            print("Error al actualizar rol:", e)
            return False

    def eliminarRol(self, id_rol: int):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM rol
                WHERE id_rol = %s
                RETURNING id_rol;
            """, (id_rol,))

            rol_eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return rol_eliminado is not None

        except psycopg2.Error as e:
            print("Error al eliminar rol:", e)
            return False