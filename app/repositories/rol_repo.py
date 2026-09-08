from app.core.database import Database
from app.models.rol import Rol


class RolRepository:

    def __init__(self):
        self.db = Database()

    def obtenerRoles(self):
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

    def obtenerRolPorId(self, id_rol: int):
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

    def crearRol(self, rol: Rol):
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

    def actualizarRol(self, id_rol: int, rol: Rol):
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

    def eliminarRol(self, id_rol: int):
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