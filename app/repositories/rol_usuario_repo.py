from app.core.database import Database
from app.models.rol_usuario import RolUsuario
from app.models.rol_usuario import CrearRelacionUsuarioRol
from app.models.rol_usuario import ActualizarRelacionRolYUsuario

class RolUsuarioRepository:
    def __init__(self):
        self.db = Database()
        
    def obtenerRolesYUsuario(self):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rol_usuario ORDER BY id_rol_usuario ASC")
        rolYUsuario = cursor.fetchall()
        conn.close()
        return rolYUsuario 
    
    def obtenerRolYUsuarioPorId(self, id_rol_usuario: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("""
                SELECT id_rol_usuario, id_rol, id_usuario
                FROM rol_usuario
                WHERE id_rol_usuario = %s
            """, (id_rol_usuario,))
        rolUsuario = cursor.fetchone()
        return rolUsuario
    
    def crearRelacionUsuarioRol(self, rol_usuario: CrearRelacionUsuarioRol):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        query = """
            INSERT INTO rol_usuario (id_rol, id_usuario) 
            VALUES (%s, %s) RETURNING id_rol_usuario;
        """
        
        cursor.execute(query, (rol_usuario.id_rol, rol_usuario.id_usuario))
        id_rol_usuario = cursor.fetchone()["id_rol_usuario"]
        
        conn.commit()
        conn.close()
        
        return id_rol_usuario
    
    def actualizarRelacionUsuarioRol(self, id_rol_usuario: int, rol_usuario: ActualizarRelacionRolYUsuario):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        query= """
            UPDATE rol_usuario SET id_rol = %s WHERE id_rol_usuario = %s RETURNING id_rol_usuario;
        """
        
        cursor.execute(query, (rol_usuario.id_rol, id_rol_usuario))
        
        rolUsuarioActualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        
        return rolUsuarioActualizado is not None
    
    def eliminarRelacionRolUsuario(self, id_rol_usuario: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM rol_usuario WHERE id_rol_usuario = %s RETURNING id_rol;", (id_rol_usuario,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None      
        
        
    
        