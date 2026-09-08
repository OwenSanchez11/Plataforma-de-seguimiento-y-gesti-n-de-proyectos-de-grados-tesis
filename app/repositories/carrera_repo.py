from app.core.database import Database
from app.models.carrera import Carrera


class CarreraRepository:

    def __init__(self):
        self.db = Database()

    def obtenerCarreras(self):
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

    def obtenerCarreraPorId(self, id_carrera: int):
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

    def crearCarrera(self, carrera: Carrera):
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

    def actualizarCarrera(
        self,
        id_carrera: int,
        carrera: Carrera
    ):
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

    def eliminarCarrera(self, id_carrera: int):
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