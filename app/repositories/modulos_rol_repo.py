from app.core.database import Database
from app.models.usuario import Usuario
from app.models.modulos_por_rol import Modulo_rol


class ModuloPorRolRepository:
    def __init__(self):
        self.db = Database()
        
    def obtenerModuloRol(self):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM modulo_rol ORDER BY id_modulo_rol ASC")
        modulo_rol = cursor.fetchall()
        conn.close()
        return modulo_rol
    
    def obtenerModuloRolPorId(self, id_modulo_rol: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM modulo_rol WHERE id_modulo_rol = %s;", (id_modulo_rol,))
        modulo_rol = cursor.fetchone()
        return modulo_rol
    
    def crearModuloPorRol(self, modulo: Modulo_rol):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        query = """
            INSERT INTO modulo_rol (id_rol, id_modulo, id_permiso) 
            VALUES (%s, %s, %s) RETURNING id_modulo_rol;
        """
        
        cursor.execute(query, (modulo.id_rol,modulo.id_modulo, modulo.id_permiso))
        id_modulo_rol = cursor.fetchone()["id_modulo_rol"] 
        
        conn.commit()
        conn.close()
        
        return id_modulo_rol
    
    
    def actualizarModuloRol(self, id_modulo_rol: int, modulo_rol: Modulo_rol):
        conn = self.db.getConnection()
        cursor = conn.cursor()

        query = """
            UPDATE modulo_rol SET id_rol = %s, id_modulo = %s, id_permiso = %s WHERE id_modulo_rol = %s RETURNING id_modulo_rol;
        """
        
        cursor.execute(query, (modulo_rol.id_rol, modulo_rol.id_modulo, modulo_rol.id_permiso, id_modulo_rol))
        
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        
        return actualizado is not None
    
    
    
    def eliminarModuloRol(self, id_modulo_rol: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM modulo_rol WHERE id_modulo_rol = %s RETURNING id_modulo_rol;", (id_modulo_rol,))
        eliminaado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminaado is not None
    
        