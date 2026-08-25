from app.core.database import Database
from app.models.trabajo_grado_jurado import Crear_trabajo_grado_jurado
from app.models.trabajo_grado_jurado import Actualizar_trabajo_grado_jurado

class TrabajoGradoJuradoRepository:
    def __init__(self):
        self.db = Database()
        
    def obtenerTrabajosPorJurado(self):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trabajo_grado_jurado ORDER BY id_trabajo_grado_jurado ASC")
        trabajoGrado = cursor.fetchall()
        conn.close()
        return trabajoGrado
    
    def obtenerTrabajoGradoPorJuradoPorId(self, id_trabajo_grado_jurado: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("""
                SELECT *
                FROM trabajo_grado_jurado
                WHERE id_trabajo_grado_jurado = %s
            """, (id_trabajo_grado_jurado,))
        trabajoGradoJurado = cursor.fetchone()
        return trabajoGradoJurado
    
    def crearRelacionTrabajoGradoPorJurado(self, trabajo_grado_jurado: Crear_trabajo_grado_jurado):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        query = """
            INSERT INTO trabajo_grado_jurado (id_trabajo_grado, id_profesor) 
            VALUES (%s, %s) RETURNING id_trabajo_grado_jurado;
        """
        
        cursor.execute(query, (trabajo_grado_jurado.id_trabajo_grado, trabajo_grado_jurado.id_profesor))
        id_trabajo_grado_jurado = cursor.fetchone()["id_trabajo_grado_jurado"]
                
        conn.commit()
        conn.close()
                
        return id_trabajo_grado_jurado
    
    def actualizarTrabajoGradoPorJurado(self, id_trabajo_grado_jurado: int, trabajo_grado_jurado: Actualizar_trabajo_grado_jurado):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        query= """
            UPDATE trabajo_grado_jurado SET id_trabajo_grado = %s, id_profesor = %s WHERE id_trabajo_grado_jurado = %s RETURNING id_trabajo_grado_jurado;
        """
        
        cursor.execute(query, (trabajo_grado_jurado.id_trabajo_grado, trabajo_grado_jurado.id_profesor, id_trabajo_grado_jurado))
        
        trabajoGradoPorJuradoActualizado = cursor.fetchone()
        conn.commit()
        conn.close()
                
        return trabajoGradoPorJuradoActualizado is not None
    
    def eliminarTrabajoGradoPorJurado(self, id_trabajo_grado_jurado: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM trabajo_grado_jurado WHERE id_trabajo_grado_jurado = %s RETURNING id_trabajo_grado_jurado;", (id_trabajo_grado_jurado,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None 
    