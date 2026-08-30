from app.core.database import get_connection
from app.models.facultad import Facultad


class FacultadRepository:

    def obtenerFacultades(self):

        cn = get_connection()
        cursor = cn.cursor(dictionary=True)

        sql = "SELECT * FROM facultad"

        cursor.execute(sql)

        facultades = cursor.fetchall()

        cursor.close()
        cn.close()

        return facultades


    def obtenerFacultadPorId(self, id_facultad: int):

        cn = get_connection()
        cursor = cn.cursor(dictionary=True)

        sql = """
            SELECT *
            FROM facultad
            WHERE id_facultad = %s
        """

        cursor.execute(sql, (id_facultad,))

        facultad = cursor.fetchone()

        cursor.close()
        cn.close()

        return facultad


    def crearFacultad(self, facultad: Facultad):

        cn = get_connection()
        cursor = cn.cursor()

        sql = """
            INSERT INTO facultad
            (nombre_facultad, codigo_facultad)
            VALUES (%s, %s)
        """

        valores = (
            facultad.nombre_facultad,
            facultad.codigo_facultad
        )

        cursor.execute(sql, valores)

        cn.commit()

        id_facultad = cursor.lastrowid

        cursor.close()
        cn.close()

        return {
            "mensaje": "Facultad creada correctamente",
            "id_facultad": id_facultad
        }


    def actualizarFacultad(self, id_facultad: int, facultad: Facultad):

        cn = get_connection()
        cursor = cn.cursor()

        sql = """
            UPDATE facultad
            SET nombre_facultad = %s,
                codigo_facultad = %s
            WHERE id_facultad = %s
        """

        valores = (
            facultad.nombre_facultad,
            facultad.codigo_facultad,
            id_facultad
        )

        cursor.execute(sql, valores)

        cn.commit()

        filas_afectadas = cursor.rowcount

        cursor.close()
        cn.close()

        return filas_afectadas


    def eliminarFacultad(self, id_facultad: int):

        cn = get_connection()
        cursor = cn.cursor()

        sql = """
            DELETE FROM facultad
            WHERE id_facultad = %s
        """

        cursor.execute(sql, (id_facultad,))

        cn.commit()

        filas_afectadas = cursor.rowcount

        cursor.close()
        cn.close()

        return filas_afectadas