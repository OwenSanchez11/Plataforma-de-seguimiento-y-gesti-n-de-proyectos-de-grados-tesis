from app.core.database import Database
from app.models.facultad import FacultadCrear, ActualizarFacultad


class FacultadRepository:

    def __init__(self):
        self.db = Database()

    def obtenerFacultades(self):
        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id_facultad, nombre_facultad, codigo_facultad
            FROM facultad
            ORDER BY id_facultad ASC;
        """)

        facultades = cursor.fetchall()

        cursor.close()
        conn.close()

        return facultades

    def obtenerFacultadPorId(self, id_facultad: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id_facultad, nombre_facultad, codigo_facultad
            FROM facultad
            WHERE id_facultad = %s;
        """, (id_facultad,))

        facultad = cursor.fetchone()

        cursor.close()
        conn.close()

        return facultad

    def crearFacultad(self, facultad: FacultadCrear):
        conn = self.db.getConnection()
        cursor = conn.cursor()

        query = """
            INSERT INTO facultad (
                nombre_facultad,
                codigo_facultad
            )
            VALUES (%s, %s)
            RETURNING id_facultad;
        """

        cursor.execute(
            query,
            (
                facultad.nombre_facultad,
                facultad.codigo_facultad
            )
        )

        id_facultad = cursor.fetchone()["id_facultad"]

        conn.commit()

        cursor.close()
        conn.close()

        return {
            "mensaje": "Facultad creada correctamente",
            "id_facultad": id_facultad
        }

    def actualizarFacultad(
        self,
        id_facultad: int,
        facultad: ActualizarFacultad
    ):
        conn = self.db.getConnection()
        cursor = conn.cursor()

        query = """
            UPDATE facultad
            SET nombre_facultad = %s,
                codigo_facultad = %s
            WHERE id_facultad = %s
            RETURNING id_facultad;
        """

        cursor.execute(
            query,
            (
                facultad.nombre_facultad,
                facultad.codigo_facultad,
                id_facultad
            )
        )

        actualizado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return actualizado is not None

    def eliminarFacultad(self, id_facultad: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM facultad
            WHERE id_facultad = %s
            RETURNING id_facultad;
        """, (id_facultad,))

        eliminado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return eliminado is not None