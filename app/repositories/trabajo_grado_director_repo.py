from app.core.database import Database
from app.models.trabajo_grado_director import Trabajo_grado_director
from app.models.trabajo_grado_director import Crear_trabajo_grado_director
from app.models.trabajo_grado_director import Actualizar_trabajo_grado_director

class TrabajoGradoDirectorRepository:
    def __init__(self):
        self.db = Database()
        
    def obtenerTrabajosDeGradoPorDirector(self):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trabajo_grado_director ORDER BY id_trabajo_grado_director ASC")
        trabajoGrado = cursor.fetchall()
        conn.close()
        return trabajoGrado
    
    def obtenerTrabajoDeGradoDirectorPorId(self, id_trabajo_grado_director: int): 
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("""
                SELECT *
                FROM trabajo_grado_director
                WHERE id_trabajo_grado_director = %s
            """, (id_trabajo_grado_director,))
        trabajoGradoDirector = cursor.fetchone()
        return trabajoGradoDirector
    
    def crearRelacionTrabajoGradoPorDirector(self, trabajo_grado_director: Crear_trabajo_grado_director):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        query = """
            INSERT INTO trabajo_grado_director (id_trabajo_grado, id_profesor) 
            VALUES (%s, %s) RETURNING id_trabajo_grado_director;
        """
        
        cursor.execute(query, (trabajo_grado_director.id_trabajo_grado, trabajo_grado_director.id_profesor))
        id_trabajo_grado_director = cursor.fetchone()["id_trabajo_grado_director"]
                
        conn.commit()
        conn.close()
                
        return id_trabajo_grado_director
    
    def actualizarTrabajoGradoPorDirector(self, id_trabajo_grado_director: int, trabajo_grado_director: Actualizar_trabajo_grado_director):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        query= """
            UPDATE trabajo_grado_director SET id_trabajo_grado = %s, id_profesor = %s WHERE id_trabajo_grado_director = %s RETURNING id_trabajo_grado_director;
        """
                
        cursor.execute(query, (trabajo_grado_director.id_trabajo_grado, trabajo_grado_director.id_profesor, id_trabajo_grado_director))
                
        trabajoGradoPorDirectorActualizado = cursor.fetchone()
        conn.commit()
        conn.close()
                        
        return trabajoGradoPorDirectorActualizado is not None
    
    def eliminarTrabajoDeGradoPorDirector(self, id_trabajo_grado_director: int): 
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM trabajo_grado_director WHERE id_trabajo_grado_director = %s RETURNING id_trabajo_grado_director;", (id_trabajo_grado_director,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None 