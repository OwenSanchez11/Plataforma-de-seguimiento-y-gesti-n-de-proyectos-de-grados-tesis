from app.core.database import Database
from app.models.rol import Rol


class RolRepository:
    def __init__(self):
        self.db = Database()
        
        
    def obtenerRoles(self):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Rol ORDER BY id_rol ASC")
        rol = cursor.fetchall()
        conn.close()
        return rol
    
    def obtenerRolPorId(self, id_rol: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Rol WHERE id_rol = %s;", (id_rol,))
        rol = cursor.fetchone()
        return rol
    
    def crearRol(self, rol: Rol):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        query = """
            INSERT INTO Rol (rol_nombre) 
            VALUES (%s) RETURNING id_rol;
        """
        cursor.execute(query, (rol.rol_nombre,))
        id_rol = cursor.fetchone()["id_rol"]
        
        conn.commit()
        conn.close()
        
        return id_rol 
    
    def actualizarRol(self, id_rol: int, rol: Rol):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        query = """
            UPDATE Rol SET rol_nombre = %s WHERE id_rol = %s RETURNING id_rol;
        """
        
        cursor.execute(query, (rol.rol_nombre, id_rol))
        
        rolActualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        
        return rolActualizado is not None
        
        
        
    def eliminarRol(self, id_rol: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Rol WHERE id_rol = %s RETURNING id_rol;", (id_rol,))
        eliminaado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminaado is not None