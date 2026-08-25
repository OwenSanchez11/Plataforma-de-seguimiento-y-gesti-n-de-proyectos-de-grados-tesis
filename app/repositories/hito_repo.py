from app.core.database import Database
from app.models.hito import CrearHito
from app.models.hito import ActualizarHito


class HitoRepository:

    def __init__(self):
        self.db = Database()

    def obtenerHitos(self):
        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM hitos
            ORDER BY id_hito ASC
        """)

        hitos = cursor.fetchall()

        conn.close()

        return hitos

    def obtenerHitoPorId(self, id_hito: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM hitos
            WHERE id_hito = %s;
        """, (id_hito,))

        hito = cursor.fetchone()

        conn.close()

        return hito

    def crearHito(self, hito: CrearHito):
        conn = self.db.getConnection()
        cursor = conn.cursor()

        query = """
            INSERT INTO hitos (
                id_trabajo_grado,
                titulo,
                descripcion,
                fecha_inicio,
                fecha_limite,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_hito;
        """

        cursor.execute(
            query,
            (
                hito.id_trabajo_grado,
                hito.titulo,
                hito.descripcion,
                hito.fecha_inicio,
                hito.fecha_limite,
                hito.estado
            )
        )

        id_hito = cursor.fetchone()["id_hito"]

        conn.commit()
        conn.close()

        return id_hito

    def actualizarHito(
        self,
        id_hito: int,
        hito: ActualizarHito
    ):
        conn = self.db.getConnection()
        cursor = conn.cursor()

        query = """
            UPDATE hitos
            SET
                id_trabajo_grado = %s,
                titulo = %s,
                descripcion = %s,
                fecha_inicio = %s,
                fecha_limite = %s,
                estado = %s
            WHERE id_hito = %s
            RETURNING id_hito;
        """

        cursor.execute(
            query,
            (
                hito.id_trabajo_grado,
                hito.titulo,
                hito.descripcion,
                hito.fecha_inicio,
                hito.fecha_limite,
                hito.estado,
                id_hito
            )
        )

        hitoActualizado = cursor.fetchone()

        conn.commit()
        conn.close()

        return hitoActualizado is not None

    def eliminarHito(self, id_hito: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM hitos
            WHERE id_hito = %s
            RETURNING id_hito;
        """, (id_hito,))

        eliminado = cursor.fetchone()

        conn.commit()
        conn.close()

        return eliminado is not None