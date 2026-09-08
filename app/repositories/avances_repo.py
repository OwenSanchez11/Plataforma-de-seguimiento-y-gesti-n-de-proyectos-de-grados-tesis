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
            ORDER BY id_avance ASC
        """)

        avances = cursor.fetchall()

        conn.close()

        return avances


    def obtenerAvancesPorId(self, id_avance: int):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM avances
            WHERE id_avance = %s;
        """, (id_avance,))

        avance = cursor.fetchone()

        conn.close()

        return avance


    def crearAvances(self, avance: Avances):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        query = """
            INSERT INTO avances (
                id_trabajo_grado,
                titulo,
                subido_por,
                descripcion,
                numero_version,
                nombre_archivo,
                ruta_archivo,
                tamano_bytes,
                fecha_inicio,
                fecha_entrega,
                fecha_limite,
                estado
            )
            VALUES (
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
            )
            RETURNING id_avance;
        """

        cursor.execute(
            query,
            (
                avance.id_trabajo_grado,
                avance.titulo,
                avance.subido_por,
                avance.descripcion,
                avance.numero_version,
                avance.nombre_archivo,
                avance.ruta_archivo,
                avance.tamano_bytes,
                avance.fecha_inicio,
                avance.fecha_entrega,
                avance.fecha_limite,
                avance.estado
            )
        )

        id_avance = cursor.fetchone()["id_avance"]

        conn.commit()

        conn.close()

        return id_avance


    def actualizarAvances(
        self,
        id_avance: int,
        avance: Avances
    ):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        query = """
            UPDATE avances
            SET
                id_trabajo_grado = %s,
                titulo = %s,
                subido_por = %s,
                descripcion = %s,
                numero_version = %s,
                nombre_archivo = %s,
                ruta_archivo = %s,
                tamano_bytes = %s,
                fecha_inicio = %s,
                fecha_entrega = %s,
                fecha_limite = %s,
                estado = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id_avance = %s
            RETURNING id_avance;
        """

        cursor.execute(
            query,
            (
                avance.id_trabajo_grado,
                avance.titulo,
                avance.subido_por,
                avance.descripcion,
                avance.numero_version,
                avance.nombre_archivo,
                avance.ruta_archivo,
                avance.tamano_bytes,
                avance.fecha_inicio,
                avance.fecha_entrega,
                avance.fecha_limite,
                avance.estado,
                id_avance
            )
        )

        avance_actualizado = cursor.fetchone()

        conn.commit()

        conn.close()

        return avance_actualizado is not None


    def eliminarAvances(self, id_avance: int):

        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM avances
            WHERE id_avance = %s
            RETURNING id_avance;
        """, (id_avance,))

        eliminado = cursor.fetchone()

        conn.commit()

        conn.close()

        return eliminado is not None