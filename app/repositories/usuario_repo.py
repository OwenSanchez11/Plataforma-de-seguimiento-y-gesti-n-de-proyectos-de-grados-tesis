from app.core.database import Database
from app.models.usuario import Usuario


class UsuarioRepository: 
    def __init__(self):
        self.db = Database()
        
    def obtenerUsuarios(self):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario ORDER BY id_user ASC")
        usuario = cursor.fetchall()
        conn.close()
        return usuario
    
    
    def obtenerPorId(self, id_user: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE id_user = %s;", (id_user,))
        usuario = cursor.fetchone()
        return usuario
    
    def crearUsuario(self, usuario: Usuario):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        query = """
            INSERT INTO usuario (id_carrera, username, nombre, apellido, email, documento, contraseña) 
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_user;
        """
        cursor.execute(query, (usuario.id_carrera,usuario.username, usuario.nombre, usuario.apellido, usuario.email, usuario.documento, usuario.contraseña))
        id_user = cursor.fetchone()["id_user"]
        
        conn.commit()
        conn.close()
        
        return id_user
    
    def actualizarUsuario(self, id_user: int, usuario: Usuario):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        query = """
            UPDATE usuario SET username = %s, email = %s, contraseña = %s WHERE id_user = %s RETURNING id_user;
        """
        
        cursor.execute(query, (usuario.username, usuario.email, usuario.contraseña, id_user))
        
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        
        return actualizado is not None
    
    
    def eliminarUsuario(self, id_user: int):
        conn = self.db.getConnection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuario WHERE id_user = %s RETURNING id_user;", (id_user,))
        eliminaado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminaado is not None