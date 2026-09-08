import psycopg2
from app.core.database import Database
from app.models.usuario import Usuario


class UsuarioRepository:

    def __init__(self):
        self.db = Database()

    def obtenerUsuarios(self):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM usuario
                ORDER BY id_user ASC
            """)

            usuarios = cursor.fetchall()

            conn.close()

            return usuarios

        except Exception as e:
            print("Error al obtener usuarios:", e)
            return []

    def obtenerPorId(self, id_user: int):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM usuario
                WHERE id_user = %s;
            """, (id_user,))

            usuario = cursor.fetchone()

            conn.close()

            return usuario

        except psycopg2.Error as e:
            print("Error al obtener usuario:", e)
            return None

    def crearUsuario(self, usuario: Usuario):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            query = """
                INSERT INTO usuario (
                    id_carrera,
                    id_rol,
                    username,
                    nombre,
                    apellido,
                    email,
                    documento,
                    contrasena,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_user;
            """

            cursor.execute(
                query,
                (
                    usuario.id_carrera,
                    usuario.id_rol,
                    usuario.username,
                    usuario.nombre,
                    usuario.apellido,
                    usuario.email,
                    usuario.documento,
                    usuario.contrasena,
                    usuario.estado
                )
            )

            id_user = cursor.fetchone()["id_user"]

            conn.commit()
            conn.close()

            return {
                "mensaje": "Usuario creado correctamente",
                "id_user": id_user
            }

        except Exception as e:
            print("Error al crear usuario:", e)
            return {
                "error": "No se pudo crear el usuario"
            }

    def actualizarUsuario(self, id_user: int, usuario: Usuario):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            query = """
                UPDATE usuario
                SET
                    id_carrera = %s,
                    id_rol = %s,
                    username = %s,
                    nombre = %s,
                    apellido = %s,
                    email = %s,
                    documento = %s,
                    contrasena = %s,
                    estado = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_user = %s
                RETURNING id_user;
            """

            cursor.execute(
                query,
                (
                    usuario.id_carrera,
                    usuario.id_rol,
                    usuario.username,
                    usuario.nombre,
                    usuario.apellido,
                    usuario.email,
                    usuario.documento,
                    usuario.contrasena,
                    usuario.estado,
                    id_user
                )
            )

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None

        except psycopg2.Error as e:
            print("Error al actualizar usuario:", e)
            return False

    def eliminarUsuario(self, id_user: int):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM usuario
                WHERE id_user = %s
                RETURNING id_user;
            """, (id_user,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None

        except psycopg2.Error as e:
            print("Error al eliminar usuario:", e)
            return False