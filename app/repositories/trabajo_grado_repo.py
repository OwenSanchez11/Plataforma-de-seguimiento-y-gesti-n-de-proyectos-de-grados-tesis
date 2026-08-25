from app.core.database import Database
from app.models.trabajo_grado import Trabajo_grado
from app.models.trabajo_grado import ActualizarTrabajoGrado
from app.models.trabajo_grado import CrearTrabajoGrado


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
    
    def crearTrabajoGrado(self, trabajo_grado: CrearTrabajoGrado):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        query = """
            INSERT INTO trabajo_grado (titulo, descripcion, estado, fecha_inicio, fecha_estimada_finalizacion)
            VALUES (%s, %s, %s, %s, %s) RETURNING id_trabajo_grado;
        """
        cursor.execute(query, (trabajo_grado.titulo, trabajo_grado.descripcion, trabajo_grado.estado, trabajo_grado.fecha_inicio, trabajo_grado.fecha_estimada_finalizacion))
        id_trabajo_grado_nuevo = cursor.fetchone()["id_trabajo_grado"]
        
        conn.commit()
        conn.close()
        
        return id_trabajo_grado_nuevo
    
    
    def actualizarTrabajoGrado(self, id_trabajo_grado: int, trabajo_grado: ActualizarTrabajoGrado):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        query = """
            UPDATE trabajo_grado SET titulo =%s, estado = %s, fecha_estimada_finalizacion = %s WHERE id_trabajo_grado = %s RETURNING id_trabajo_grado;
        """
        
        cursor.execute(query, (trabajo_grado.titulo, trabajo_grado.estado, trabajo_grado.fecha_estimada_finalizacion, id_trabajo_grado))
        
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
        