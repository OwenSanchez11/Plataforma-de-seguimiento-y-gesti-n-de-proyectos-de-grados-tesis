from app.core.database import Database
from app.models.permiso import Permiso


class PermisoRepository:

    def __init__(self):
        self.db = Database()

    def obtenerPermisos(self):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM permisos
            ORDER BY id_permiso ASC
        """)

        permisos = cursor.fetchall()

        conn.close()

        return permisos

    def obtenerPermisoPorId(self, id_permiso: int):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM permisos
            WHERE id_permiso = %s;
        """, (id_permiso,))

        permiso = cursor.fetchone()

        conn.close()

        return permiso

    def crearPermiso(self, permiso: Permiso):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        query = """
            INSERT INTO permisos (
                nombre_permiso
            )
            VALUES (%s)
            RETURNING id_permiso;
        """

        cursor.execute(
            query,
            (
                permiso.nombre_permiso,
            )
        )

        id_permiso = cursor.fetchone()["id_permiso"]

        conn.commit()
        conn.close()

        return {
            "mensaje": "Permiso creado correctamente",
            "id_permiso": id_permiso
        }

    def actualizarPermiso(
        self,
        id_permiso: int,
        permiso: Permiso
    ):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        query = """
            UPDATE permisos
            SET
                nombre_permiso = %s
            WHERE id_permiso = %s
            RETURNING id_permiso;
        """

        cursor.execute(
            query,
            (
                permiso.nombre_permiso,
                id_permiso
            )
        )

        permiso_actualizado = cursor.fetchone()

        conn.commit()
        conn.close()

        if permiso_actualizado is None:
            return {
                "mensaje": "Permiso no encontrado"
            }

        return {
            "mensaje": "Permiso actualizado correctamente"
        }

    def eliminarPermiso(self, id_permiso: int):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM permisos
            WHERE id_permiso = %s
            RETURNING id_permiso;
        """, (id_permiso,))

        eliminado = cursor.fetchone()

        conn.commit()
        conn.close()

        if eliminado is None:
            return {
                "mensaje": "Permiso no encontrado"
            }

        return {
            "mensaje": "Permiso eliminado correctamente"
        }