import psycopg2
from app.core.database import Database
from app.models.carrera import Carrera


class CarreraRepository:

    def __init__(self):
        self.db = Database()

    def obtenerCarreras(self):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM carrera
                ORDER BY id_carrera ASC
            """)

            carreras = cursor.fetchall()

            conn.close()

            return carreras

        except psycopg2.Error as e:
            print("Error al obtener carreras:", e)
            return []

    def obtenerCarreraPorId(self, id_carrera: int):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM carrera
                WHERE id_carrera = %s;
            """, (id_carrera,))

            carrera = cursor.fetchone()

            conn.close()

            return carrera

        except psycopg2.Error as e:
            print("Error al obtener carrera:", e)
            return None

    def crearCarrera(self, carrera: Carrera):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            query = """
                INSERT INTO carrera (
                    id_facultad,
                    nombre_carrera,
                    codigo_carrera,
                    estado
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id_carrera;
            """

            cursor.execute(
                query,
                (
                    carrera.id_facultad,
                    carrera.nombre_carrera,
                    carrera.codigo_carrera,
                    carrera.estado
                )
            )

            id_carrera = cursor.fetchone()["id_carrera"]

            conn.commit()
            conn.close()

            return {
                "mensaje": "Carrera creada correctamente",
                "id_carrera": id_carrera
            }

        except psycopg2.Error as e:
            print("Error al crear carrera:", e)
            return {
                "error": "No se pudo crear la carrera"
            }

    def actualizarCarrera(
        self,
        id_carrera: int,
        carrera: Carrera
    ):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            query = """
                UPDATE carrera
                SET
                    id_facultad = %s,
                    nombre_carrera = %s,
                    codigo_carrera = %s,
                    estado = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_carrera = %s
                RETURNING id_carrera;
            """

            cursor.execute(
                query,
                (
                    carrera.id_facultad,
                    carrera.nombre_carrera,
                    carrera.codigo_carrera,
                    carrera.estado,
                    id_carrera
                )
            )

            carrera_actualizada = cursor.fetchone()

            conn.commit()
            conn.close()

            return carrera_actualizada is not None

        except psycopg2.Error as e:
            print("Error al actualizar carrera:", e)
            return False

    def eliminarCarrera(self, id_carrera: int):
        try:
            conn = self.db.getConnection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM carrera
                WHERE id_carrera = %s
                RETURNING id_carrera;
            """, (id_carrera,))

            eliminada = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminada is not None

        except psycopg2.Error as e:
            print("Error al eliminar carrera:", e)
            return False