from app.core.database import Database
from app.models.retroalimentaciones import Retroalimentacion




class RetroalimentacionesRepository:
    def __init__(self):
        self.db = Database()
        
    def obtenerRetroalimentacion(self):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT *
            FROM retroalimentaciones
            ORDER BY id_retroalimentacion ASC
        """)
        
        retroalimentacion = cursor.fetchall()
        conn.close()
        
        return retroalimentacion
    
    def obtenerRetroalimentacionPorId(self, id_retroalimentacion: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT *
            FROM retroalimentaciones
            WHERE id_retroalimentacion = %s;
        """, (id_retroalimentacion,))
        
        retroalimentacion = cursor.fetchone()
        
        conn.close()
        
        return retroalimentacion
    
    def crearRetroalimentacion(self, retroalimentacion: Retroalimentacion):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO retroalimentaciones (
            id_entrega,
            id_usuario,
            comentario,
            estado,
            fecha_creacion
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_retroalimentacion;
        """
        cursor.execute(
            query,
            (
                retroalimentacion.id_entrega,
                retroalimentacion.id_usuario,
                retroalimentacion.comentario,
                retroalimentacion.estado,
                retroalimentacion.fecha_creacion
            )
        )

        id_retroalimentacion = cursor.fetchone()["id_retroalimentacion"]

        conn.commit()
        conn.close()

        return id_retroalimentacion
    
    
    def actualizarRetroalimentacion(self, id_retroalimentacion: int, retroalimentacion: Retroalimentacion):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        
        query = """
            UPDATE retroalimentaciones
            SET
            comentario = %s,
            estado = %s,
            fecha_creacion = %s
            WHERE id_retroalimentacion = %s
            RETURNING id_retroalimentacion;
        """
        cursor.execute(
                query,
                    (
                        retroalimentacion.comentario, retroalimentacion.estado, retroalimentacion.fecha_creacion,
                        id_retroalimentacion
                    )
                )
        
        retroalimentacionActualizada = cursor.fetchone()
        
        conn.commit()
        conn.close()
        
        return retroalimentacionActualizada is not None
    
    def eliminarRetroalimentacion(self, id_retroalimentacion: int): 
        conn = self.db.getConnection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM retroalimentaciones
            WHERE id_retroalimentacion = %s
            RETURNING id_retroalimentacion;
        """, (id_retroalimentacion,))

        eliminado = cursor.fetchone()

        conn.commit()
        conn.close()

        return eliminado is not None