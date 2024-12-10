import reflex as rx  # type: ignore
import requests

# Función para obtener los datos del usuario
def fetch_user_data(user_id: str):
    url = f"http://localhost:8000/api/users/{user_id}"
    response = requests.get(url)
    if response.status_code == 200:
        user_data = response.json()
        return user_data  # Devolver los datos del usuario para usarlos más adelante
    else:
        return None  # En caso de error, retornar None

# Página para editar el perfil
@rx.page(route="/editar_perfil", title="Editar Perfil")
def editar_perfil() -> rx.Component:
    # Obtener el ID del usuario desde el archivo solo cuando se acceda a esta página
    try:
        with open("user_id.txt", "r") as file:
            user_id = file.read().strip().replace("Usuario ID: ", "")
    except FileNotFoundError:
        user_id = "Desconocido"

    # Obtener los datos del usuario solo si se tiene un ID válido
    user_data = None
    if user_id != "Desconocido":
        user_data = fetch_user_data(user_id)

    # Si se obtienen los datos del usuario, los mostramos en la página
    if user_data:
        user_info = f"""
        ID: {user_data['id']}
        Nombre completo: {user_data['full_name']}
        Teléfono: {user_data['phone']}
        """
    else:
        user_info = "No se pudo obtener los datos del usuario."

    # Mostrar la página de edición de perfil
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading(rx.text("Editar Perfil", size="9")),
            rx.text(user_info, size="5"),  # Mostrar la información del usuario
            rx.hstack(
                # Botón para ir al inicio
                rx.link(rx.button("Inicio", size="4"), href="/inicio"),
                # Botón para eliminar el perfil en rojo
                rx.link(
                    rx.button("Eliminar Perfil", size="4", color_scheme="red"), 
                    href="/eliminar_perfil "
                ),
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
app.add_page(editar_perfil, route="/editar_perfil")