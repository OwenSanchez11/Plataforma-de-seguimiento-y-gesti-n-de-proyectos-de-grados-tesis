import psycopg2
from app.core.database import Database
from app.models.facultad import Facultad


class FacultadRepository:

    def __init__(self):
        self.db = Database()

    def obtenerFacultades(self):

        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM facultad
                ORDER BY id_facultad ASC
            """)

            facultades = cursor.fetchall()

            conn.close()

            return facultades

        except psycopg2.Error as e:
            print("Error al obtener facultades:", e)
            return []

    def obtenerFacultadPorId(self, id_facultad: int):

        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM facultad
                WHERE id_facultad = %s;
            """, (id_facultad,))

            facultad = cursor.fetchone()

            conn.close()

            return facultad

        except psycopg2.Error as e:
            print("Error al obtener facultad:", e)
            return None

    def crearFacultad(self, facultad: Facultad):

        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            query = """
                INSERT INTO facultad (
                    nombre_facultad,
                    codigo_facultad,
                    estado
                )
                VALUES (%s, %s, %s)
                RETURNING id_facultad;
            """

            cursor.execute(
                query,
                (
                    facultad.nombre_facultad,
                    facultad.codigo_facultad,
                    facultad.estado
                )
            )

            id_facultad = cursor.fetchone()["id_facultad"]

            conn.commit()

            conn.close()

            return {
                "mensaje": "Facultad creada correctamente",
                "id_facultad": id_facultad
            }

        except psycopg2.Error as e:
            print("Error al crear facultad:", e)
            return {
                "error": "No se pudo crear la facultad"
            }

    def actualizarFacultad(
        self,
        id_facultad: int,
        facultad: Facultad
    ):

        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            query = """
                UPDATE facultad
                SET
                    nombre_facultad = %s,
                    codigo_facultad = %s,
                    estado = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_facultad = %s
                RETURNING id_facultad;
            """

            cursor.execute(
                query,
                (
                    facultad.nombre_facultad,
                    facultad.codigo_facultad,
                    facultad.estado,
                    id_facultad
                )
            )

            facultad_actualizada = cursor.fetchone()

            conn.commit()

            conn.close()

            return facultad_actualizada is not None

        except psycopg2.Error as e:
            print("Error al actualizar facultad:", e)
            return False

    def eliminarFacultad(self, id_facultad: int):

        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM facultad
                WHERE id_facultad = %s
                RETURNING id_facultad;
            """, (id_facultad,))

            eliminada = cursor.fetchone()

            conn.commit()

            conn.close()

            return eliminada is not None

        except psycopg2.Error as e:
            print("Error al eliminar facultad:", e)
            return False