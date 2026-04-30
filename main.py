from fastapi import FastAPI, Body, Path, Query

app = FastAPI()
@app.get("/")
async def home():
    return {"mensaje": "Bienvenido a la Gestión de Biblioteca Digital", "ver_libros": "/libros", "documentacion": "/docs"}


# Simulación de Base de Datos
libros = [
    {"id": 1, "titulo": "Cien años de soledad", "autor": "Gabriel García Márquez", "paginas": 471, "disponible": True},
    {"id": 2, "titulo": "1984", "autor": "George Orwell", "paginas": 328, "disponible": True},
    {"id": 3, "titulo": "El Aleph", "autor": "Jorge Luis Borges", "paginas": 146, "disponible": True},
]

# 1. GET - Obtener todos los libros
@app.get("/libros")
async def listar_libros():
    return libros

# 2. GET - Obtener un libro por ID (usando Path)
@app.get("/libros/{id}")
async def obtener_libro(
    id: int = Path(gt=0, description="El ID del libro debe ser mayor a 0")
):
    for libro in libros:
        if libro["id"] == id:
            return libro
    return {"error": "Libro no encontrado"}

# 3. POST - Crear un nuevo libro (usando Body)
@app.post("/libros")
async def crear_libro(
    id: int = Body(gt=0),
    titulo: str = Body(min_length=1, max_length=100),
    autor: str = Body(min_length=3),
    paginas: int = Body(gt=0)
):
    nuevo_libro = {
        "id": id,
        "titulo": titulo,
        "autor": autor,
        "paginas": paginas,
        "disponible": True
    }
    libros.append(nuevo_libro)
    return {"message": "Libro agregado con éxito", "libro": nuevo_libro}

# 4. PUT - Actualizar datos de un libro (Path + Body)
@app.put("/libros/{id}")
async def actualizar_libro(
    id: int = Path(gt=0),
    titulo: str = Body(min_length=1),
    disponible: bool = Body()
):
    for libro in libros:
        if libro["id"] == id:
            libro["titulo"] = titulo
            libro["disponible"] = disponible
            return {"message": "Libro actualizado", "libro": libro}
    return {"error": "No se encontró el libro para actualizar"}

# 5. DELETE - Borrar un libro (Query para borrado lógico)
@app.delete("/libros/{id}")
async def borrar_libro(
    id: int = Path(gt=0),
    fisico: bool = Query(default=True, description="Si es False, solo marca como no disponible")
):
    for libro in libros:
        if libro["id"] == id:
            if fisico:
                libros.remove(libro)
                return {"detail": "Eliminado de la base de datos"}
            else:
                libro["disponible"] = False
                return {"detail": "Marcado como no disponible (borrado lógico)"}
    return {"error": "ID no encontrado"}