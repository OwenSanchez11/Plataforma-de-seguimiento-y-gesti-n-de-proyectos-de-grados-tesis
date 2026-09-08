from app.core.database import Database
from app.models.modulo_rol import ModuloRol, ActualizarModuloRol


class ModuloRolRepository:

    def __init__(self):
        self.db = Database()

    def obtenerModulosRol(self):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM modulo_rol
            ORDER BY id_modulo_rol ASC
        """)

        modulos_rol = cursor.fetchall()

        conn.close()

        return modulos_rol

    def obtenerModuloRolPorId(self, id_modulo_rol: int):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM modulo_rol
            WHERE id_modulo_rol = %s
        """, (id_modulo_rol,))

        modulo_rol = cursor.fetchone()

        conn.close()

        return modulo_rol

    def crearModuloRol(self, modulo_rol: ModuloRol):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO modulo_rol (
                id_rol,
                id_modulo,
                puede_leer,
                puede_crear,
                puede_editar,
                puede_eliminar,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_modulo_rol
        """, (
            modulo_rol.id_rol,
            modulo_rol.id_modulo,
            modulo_rol.puede_leer,
            modulo_rol.puede_crear,
            modulo_rol.puede_editar,
            modulo_rol.puede_eliminar,
            modulo_rol.estado
        ))

        resultado = cursor.fetchone()

        conn.commit()
        conn.close()

        return resultado

    def actualizarModuloRol(
        self,
        id_modulo_rol: int,
        modulo_rol: ActualizarModuloRol
    ):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE modulo_rol
            SET
                id_rol = COALESCE(%s, id_rol),
                id_modulo = COALESCE(%s, id_modulo),
                puede_leer = COALESCE(%s, puede_leer),
                puede_crear = COALESCE(%s, puede_crear),
                puede_editar = COALESCE(%s, puede_editar),
                puede_eliminar = COALESCE(%s, puede_eliminar),
                estado = COALESCE(%s, estado),
                updated_at = CURRENT_TIMESTAMP
            WHERE id_modulo_rol = %s
            RETURNING id_modulo_rol
        """, (
            modulo_rol.id_rol,
            modulo_rol.id_modulo,
            modulo_rol.puede_leer,
            modulo_rol.puede_crear,
            modulo_rol.puede_editar,
            modulo_rol.puede_eliminar,
            modulo_rol.estado,
            id_modulo_rol
        ))

        actualizado = cursor.fetchone()

        conn.commit()
        conn.close()

        return actualizado

    def eliminarModuloRol(self, id_modulo_rol: int):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM modulo_rol
            WHERE id_modulo_rol = %s
            RETURNING id_modulo_rol
        """, (id_modulo_rol,))

        eliminado = cursor.fetchone()

        conn.commit()
        conn.close()

        return eliminado