## Backend del sistema de seguimiento de los trabajos de grados de la Universidad

### Problema a resolver
- Actualmente, la gestión de tesis y trabajos de grado suele dispersarse entre diversos canales de comunicación, como correos electrónicos y reuniones informales. Esta falta de centralización dificulta mantener un registro formal y estructurado del seguimiento y los avances realizados entre estudiantes y directores

### Solución:
- la solución que se ha diseñado para esto, es desarrollar una plataforma virtual en la cual se le hará el seguimiento correcto; marcado por hitos definidos, enregas de avances, retroalimentaciones por parte del director y seguimiento del cronograma de graduación


### Diagrama Entidad-Relación — Seguimiento de Trabajos de Grado

```mermaid
erDiagram

    USUARIO {
        int id_user PK
        varchar username
        varchar nombre
        varchar apellido
        varchar email
        varchar documento
        varchar contrasena
    }

    ROL {
        int id_rol PK
        varchar rol_nombre
    }

    ROL_USUARIO {
        int id_rol_usuario PK
        int id_usuario FK
        int id_rol FK
    }

    TRABAJO_GRADO {
        int id_trabajo_grado PK
        varchar titulo
        varchar descripcion
        varchar estado
        date fecha_inicio
        date fecha_estimada_finalizacion
    }

    TRABAJO_GRADO_ESTUDIANTE {
        int id_trabajo_grado_estudiante PK
        int id_trabajo_grado FK
        int id_estudiante FK
    }

    TRABAJO_GRADO_DIRECTOR {
        int id_trabajo_grado_director PK
        int id_trabajo_grado FK
        int id_profesor FK
        varchar tipo_director
    }

    HITOS {
        int id_hito PK
        int id_trabajo_grado FK
        varchar titulo
        text descripcion
        date fecha_inicio
        date fecha_limite
        varchar estado
    }

    ENTREGAS {
        int id_entrega PK
        int id_hito FK
        int numero_version
        varchar nombre_archivo
        varchar ruta_archivo
        text comentarios
        varchar estado
        date fecha_entrega
    }

    RETROALIMENTACIONES {
        int id_retroalimentacion PK
        int id_entrega FK
        int id_profesor FK
        text comentario
        varchar estado
        date fecha_creacion
    }

    TRABAJO_GRADO_JURADO {
        int id_trabajo_grado_jurado PK
        int id_trabajo_grado FK
        int id_profesor FK
    }

    USUARIO ||--o{ ROL_USUARIO : "tiene"
    ROL ||--o{ ROL_USUARIO : "asignado a"

    TRABAJO_GRADO ||--o{ TRABAJO_GRADO_ESTUDIANTE : "tiene"
    USUARIO ||--o{ TRABAJO_GRADO_ESTUDIANTE : "participa como estudiante"

    TRABAJO_GRADO ||--o{ TRABAJO_GRADO_DIRECTOR : "tiene"
    USUARIO ||--o{ TRABAJO_GRADO_DIRECTOR : "dirige"

    TRABAJO_GRADO ||--o{ TRABAJO_GRADO_JURADO : "tiene"
    USUARIO ||--o{ TRABAJO_GRADO_JURADO : "participa como jurado"

    TRABAJO_GRADO ||--o{ HITOS : "contiene"
    USUARIO ||--o{ HITOS : "responsable de"

    HITOS ||--o{ ENTREGAS : "recibe"
    USUARIO ||--o{ ENTREGAS : "realiza"

    ENTREGAS ||--o{ RETROALIMENTACIONES : "recibe"
    USUARIO ||--o{ RETROALIMENTACIONES : "realiza"

```

### Arquitectura del proyecto
- por indicaciones se ha decidido utilizar una arquitectura por capas o arquitectura modular por responsabilidades, en donde cada directorio posee una responsabilidad. permitiendo separar la lógica de la aplicación, fecilitar el mantenimiento y evittar que el codigo esté concentrado en un mismo lugar y hacerlo demasiado denso.

```text
app/
├── api/           # Endpoints y rutas de la API
├── core/          # Configuración y componentes centrales
├── models/        # Modelos y esquemas de datos
├── repositories/  # Acceso y operaciones con la base de datos
└── main.py        # Punto de entrada de la aplicación

```

#### Autores
- Owen Sanchez
- Jair Joven
- Jenifer Camacho

#### Corporación universitaria Latinoamericana - CUL