import reflex as rx  # type: ignore
import aiohttp  # type: ignore
import asyncio

# Función para obtener los datos del usuario de manera asincrónica
async def fetch_user_data(user_id: str):
    url = f"http://localhost:8000/api/users/{user_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                user_data = await response.json()
                return user_data
            else:
                return None

# Función para leer el user_id desde el archivo
def get_user_id():
    try:
        with open("user_id.txt", "r") as file:
            user_id = file.read().strip().replace("Usuario ID: ", "")
            return user_id
    except FileNotFoundError:
        return "Desconocido"  # Si no se encuentra el archivo

# Página principal donde mostraremos la información
@rx.page(route="/inicio", title="Inicio")
def index() -> rx.Component:

    print("Función index de inicio.py ejecutada")  # Agrega esta línea para depuración
    # Register Page
    # Leer el user_id de forma síncrona
    user_id = get_user_id()

    # Ejecutar la obtención de datos de usuario de forma asincrónica
    user_data = asyncio.run(fetch_user_data(user_id))

    # Si se obtienen los datos del usuario, los mostramos en la página
    if user_data:
        user_info = f"""
        ID: {user_data['id']}
        Nombre completo: {user_data['full_name']}
        Teléfono: {user_data['phone']}
        """
    else:
        user_info = "No se pudo obtener los datos del usuario."

    # Mostrar la página con la información
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading(rx.text("Bienvenido", size="9")),
            rx.text(user_info, size="5"),  # Mostrar la información del usuario
            rx.hstack(
                rx.link(rx.button("Editar perfil personal", size="4"), href="/editar_perfil"),
                rx.link(rx.button("Salir de perfil", size="4"), href="/"),
                spacing="5",
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
    )

# Configuración de la app
app = rx.App()
app.add_page(index, route="/inicio")
