from app.core.database import Database
from app.models.trabajo_grado_estudiante import Trabajo_grado_estudiante
from app.models.trabajo_grado_estudiante import CrearTrabajoGradoPorEstudiante
from app.models.trabajo_grado_estudiante import ActualizarTrabajoGradoPorEstudiante

class TrabajoGradoEstudianteRepository:
    def __init__(self):
        self.db = Database()
        
    def obtenerTrabajosPorEstudiante(self):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trabajo_grado_estudiante ORDER BY id_trabajo_grado_estudiante ASC")
        trabajoGrado = cursor.fetchall()
        conn.close()
        return trabajoGrado
    
    def obtenerTrabajoGradoPorEstudiantePorId(self, id_trabajo_grado_estudiante: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("""
                SELECT *
                FROM trabajo_grado_estudiante
                WHERE id_trabajo_grado_estudiante = %s
            """, (id_trabajo_grado_estudiante,))
        trabajoGradoEstudiante = cursor.fetchone()
        return trabajoGradoEstudiante
    
    def crearRelacionTrabajoGradoPorEstudiante(self, trabajo_grado_estudiante: CrearTrabajoGradoPorEstudiante):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        query = """
            INSERT INTO trabajo_grado_estudiante (id_trabajo_grado, id_estudiante) 
            VALUES (%s, %s) RETURNING id_trabajo_grado_estudiante;
        """
        
        cursor.execute(query, (trabajo_grado_estudiante.id_trabajo_grado, trabajo_grado_estudiante.id_estudiante))
        id_trabajo_grado_estudiante = cursor.fetchone()["id_trabajo_grado_estudiante"]
                
        conn.commit()
        conn.close()
                
        return id_trabajo_grado_estudiante
    
    
    def actualizarTrabajoGradoPorEstudiante(self, id_trabajo_grado_estudiante: int, trabajo_grado_estudiante: ActualizarTrabajoGradoPorEstudiante):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        query= """
            UPDATE trabajo_grado_estudiante SET id_trabajo_grado = %s, id_estudiante = %s WHERE id_trabajo_grado_estudiante = %s RETURNING id_trabajo_grado_estudiante;
        """
        
        cursor.execute(query, (trabajo_grado_estudiante.id_trabajo_grado, trabajo_grado_estudiante.id_estudiante, id_trabajo_grado_estudiante))
        
        trabajoGradoPorEstudianteActualizado = cursor.fetchone()
        conn.commit()
        conn.close()
                
        return trabajoGradoPorEstudianteActualizado is not None
    
    def eliminarTrabajoGradoPorEstudiante(self, id_trabajo_grado_estudiante: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM trabajo_grado_estudiante WHERE id_trabajo_grado_estudiante = %s RETURNING id_trabajo_grado_estudiante;", (id_trabajo_grado_estudiante,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None 