from app.core.database import Database
from app.models.entrega import Entrega
from app.models.entrega import CrearEntrega
from app.models.entrega import ActualizarEntrega


class EntregaRepository:
    def __init__(self):
        self.db = Database()

    def obtenerEntregas(self):
        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM entregas
            ORDER BY id_entrega ASC
        """)

        entregas = cursor.fetchall()

        conn.close()

        return entregas

    def obtenerEntregaPorId(self, id_entrega: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM entregas
            WHERE id_entrega = %s;
        """, (id_entrega,))

        entrega = cursor.fetchone()

        conn.close()

        return entrega

    def crearEntrega(self, entrega: CrearEntrega):
        conn = self.db.getConnection()
        cursor = conn.cursor()

        query = """
            INSERT INTO entregas (
                id_hito,
                numero_version,
                nombre_archivo,
                ruta_archivo,
                comentarios,
                estado,
                fecha_entrega
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_entrega;
        """

        cursor.execute(
            query,
            (
                entrega.id_hito,
                entrega.numero_version,
                entrega.nombre_archivo,
                entrega.ruta_archivo,
                entrega.comentarios,
                entrega.estado,
                entrega.fecha_entrega
            )
        )

        id_entrega = cursor.fetchone()["id_entrega"]

        conn.commit()
        conn.close()

        return id_entrega

    def actualizarEntrega(
        self,
        id_entrega: int,
        entrega: ActualizarEntrega
    ):
        conn = self.db.getConnection()
        cursor = conn.cursor()

        query = """
            UPDATE entregas
            SET
                id_hito = %s,
                numero_version = %s,
                nombre_archivo = %s,
                ruta_archivo = %s,
                comentarios = %s,
                estado = %s,
                fecha_entrega = %s
            WHERE id_entrega = %s
            RETURNING id_entrega;
        """

        cursor.execute(
            query,
            (
                entrega.id_hito,
                entrega.numero_version,
                entrega.nombre_archivo,
                entrega.ruta_archivo,
                entrega.comentarios,
                entrega.estado,
                entrega.fecha_entrega,
                id_entrega
            )
        )

        entregaActualizada = cursor.fetchone()

        conn.commit()
        conn.close()

        return entregaActualizada is not None

    def eliminarEntrega(self, id_entrega: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM entregas
            WHERE id_entrega = %s
            RETURNING id_entrega;
        """, (id_entrega,))

        eliminada = cursor.fetchone()

        conn.commit()
        conn.close()

        return eliminada is not None