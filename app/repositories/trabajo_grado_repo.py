from app.core.database import Database
from app.models.trabajo_grado import Trabajo_grado



class TrabajoGradoRepository: 
    def __init__(self):
        self.db = Database()
        
    def obtenerTrabajosGrados(self): 
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trabajo_grado ORDER BY id_trabajo_grado ASC")
        trabajos_grado = cursor.fetchall()
        conn.close()
        return trabajos_grado
    
    def obtenerTrabajoGradoPorId(self, id_trabajo_grado: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT * from trabajo_grado WHERE id_trabajo_grado = %s
                       """, (id_trabajo_grado,))
        trabajo_grado = cursor.fetchone()
        return trabajo_grado
    
    def crearTrabajoGrado(self, trabajo_grado: Trabajo_grado):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        query = """
            INSERT INTO trabajo_grado (id_carrera,titulo, resumen, linea_investigacion, fecha_inicio, fecha_fin, estado, fecha_sustentacion, observaciones_finales)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_trabajo_grado;
        """
        cursor.execute(query, (trabajo_grado.id_carrera,trabajo_grado.titulo, trabajo_grado.resumen, trabajo_grado.linea_investigacion,trabajo_grado.fecha_inicio, trabajo_grado.fecha_fin, trabajo_grado.estado, trabajo_grado.fecha_sustentacion, trabajo_grado.observaciones_finales))
        id_trabajo_grado_nuevo = cursor.fetchone()["id_trabajo_grado"]
        
        conn.commit()
        conn.close()
        
        return id_trabajo_grado_nuevo
    
    
    def actualizarTrabajoGrado(self, id_trabajo_grado: int, trabajo_grado: Trabajo_grado):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        query = """
            UPDATE trabajo_grado SET titulo =%s, fecha_fin = %s, estado = %s, fecha_sustentacion = %s, observaciones_finales = %s WHERE id_trabajo_grado = %s RETURNING id_trabajo_grado;
        """
        
        cursor.execute(query, (trabajo_grado.titulo, trabajo_grado.fecha_fin, trabajo_grado.estado,trabajo_grado.fecha_sustentacion, trabajo_grado.observaciones_finales,id_trabajo_grado))
        
        trabajoGradoActualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        
        return trabajoGradoActualizado
    
    
    def eliminarTrabajoGrado(self, id_trabajo_grado: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM trabajo_grado WHERE id_trabajo_grado = %s RETURNING id_trabajo_grado;", (id_trabajo_grado,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None   
        