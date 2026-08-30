from app.core.database import Database
from app.models.avances import Avances


class AvancesRepository:

    def __init__(self):
        self.db = Database()


    def obtenerAvances(self):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM avances
            ORDER BY id_avances ASC
        """)

        avances = cursor.fetchall()

        conn.close()

        return avances


    def obtenerAvancesPorId(self, id_avances: int):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM avances
            WHERE id_avances = %s;
        """, (id_avances,))

        avances = cursor.fetchone()

        conn.close()

        return avances


    def crearAvances(self, avances: Avances):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        query = """
            INSERT INTO avances (
                id_trabajo_grado,
                titulo,
                descripcion,
                fecha_inicio,
                fecha_limite,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_avances;
        """

        cursor.execute(
            query,
            (
                avances.id_trabajo_grado,
                avances.titulo,
                avances.descripcion,
                avances.fecha_inicio,
                avances.fecha_limite,
                avances.estado
            )
        )

        id_avances = cursor.fetchone()["id_avances"]

        conn.commit()

        conn.close()

        return id_avances


    def actualizarAvances(
        self,
        id_avances: int,
        avances: Avances
    ):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        query = """
            UPDATE avances
            SET
                id_trabajo_grado = %s,
                titulo = %s,
                descripcion = %s,
                fecha_inicio = %s,
                fecha_limite = %s,
                estado = %s
            WHERE id_avances = %s
            RETURNING id_avances;
        """

        cursor.execute(
            query,
            (
                avances.id_trabajo_grado,
                avances.titulo,
                avances.descripcion,
                avances.fecha_inicio,
                avances.fecha_limite,
                avances.estado,
                id_avances
            )
        )

        avances_actualizado = cursor.fetchone()

        conn.commit()

        conn.close()

        return avances_actualizado is not None


    def eliminarAvances(self, id_avances: int):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM avances
            WHERE id_avances = %s
            RETURNING id_avances;
        """, (id_avances,))

        eliminado = cursor.fetchone()

        conn.commit()

        conn.close()

        return eliminado is not None