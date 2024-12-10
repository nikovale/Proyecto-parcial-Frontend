import reflex as rx # type: ignore
import requests as rq # type: ignore
import re


class loginState(rx.State):
    loader: bool = False
    username: str = "ejemplo@gmail.com"
    password: str
    error = False
    response: dict = {}

    @rx.background
    async def loginService(self, data: dict):
        async with self:
            self.loader = True
            self.error = False
            # Ajustar los nombres de los campos para que coincidan con el esquema del backend
            payload = {
                "correo": self.username,
                "password": self.password
            }
            response = rq.post("http://localhost:8000/api/login", json=payload, headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                self.loader = False
                self.response = response.json()  # Almacenar la respuesta en el estado
                user_id = self.response.get("user", {}).get("id", "")
                handle_user_id(user_id)  # Imprimir el ID del usuario
                return rx.redirect("/inicio")  # Redirigir a la página principal
            else:
                self.loader = False
                self.error = True

    @rx.var
    def user_invalid(self) -> bool:
        return not re.match(r"[^@]+@[^@]+\.[^@]+", self.username)
    
    @rx.var
    def user_empty(self) -> bool:
        return not self.username.strip()
    
    @rx.var
    def password_empty(self) -> bool:
        return not self.password.strip()
    
    @rx.var
    def validate_fields(self) -> bool:
        return (
            self.user_empty
            or self.user_invalid
            or self.password_empty
        )

# Función para manejar el ID del usuario y mostrar los datos
def handle_user_id(user_id):
    # Guardar el user_id en un archivo
    with open("user_id.txt", "w") as file:
        file.write(f"Usuario ID: {user_id}")


@rx.page(route="/login", title="Login")
def login() -> rx.Component:
    # Login Page
    return rx.section(
        rx.flex(
            rx.image(src='/login.ico', width="300px", border_radius="15px 10px"),
            rx.heading("Inicio de sesion"),
            rx.form.root(
                rx.flex(
                    field_form_component_general("Usuario", "Ingrese su correo", "Ingrese un correo valido", "username",
                                                 loginState.set_username, loginState.user_invalid),
                    field_form_component("Contraseña", "Ingrese su contraseña", "password",
                                         loginState.set_password, "password"),
                    rx.form.submit(
                        rx.cond(
                            loginState.loader,
                            rx.chakra.spinner(color="red", size="xs"),
                            rx.button(
                                "Iniciar sesion",
                                disabled=loginState.validate_fields,
                                width="30vw",
                            ),
                        ),
                        as_child=True,
                    ),
                    rx.link(
                        "Registrar usuario",
                        href="/registro",
                    ),
                    rx.link(
                        "Inicio",
                        href="/",
                    ),
                    direction="column",
                    justify="center",
                    align="center",
                    spacing="2",
                ),
                rx.cond(
                    loginState.error,
                    rx.callout(
                        "creadenciales incorrectas",
                        icon="alarm_clock",
                        color_scheme="red",
                        role="alert",
                        style={"margin_top": "10px"}
                    ),
                ),
                on_submit=loginState.loginService,
                reset_on_submit=True,
                width="80%",
            ),
            width="100%",
            direction="column",
            align="center",
            justify="center",
        ),
        
    )


def field_form_component(label: str, placeholder: str, name_var: str, on_change_funtion, type_field: str) -> rx.Component:
    return rx.form.field(
        rx.flex(
            rx.form.label(label),
            rx.form.control(
                rx.input(
                    placeholder=placeholder,
                    on_change=on_change_funtion,
                    name=name_var,
                    type=type_field,
                    required=True
                ),
                as_child=True,
            ),
            rx.form.message(
                "el campo no puede ser nulo",
                match="valueMissing",
                color="red",
            ),
            direction="column",
            spacing="2",
            align="stretch",
        ),
        name=name_var,
        width="30vw",
    )


def field_form_component_general(label: str, placeholder: str, message_validate: str, name: str, on_change_funtion, show) -> rx.Component:
    return rx.form.field(
        rx.flex(
            rx.form.label(label),
            rx.form.control(
                rx.input(
                    placeholder=placeholder,
                    on_change=on_change_funtion,
                    name=name,
                    required=True
                ),
                as_child=True,
            ),
            rx.form.message(
                message_validate,
                name=name,
                match="valueMissing",
                force_match=show,
                color="red",
            ),
            direction="column",
            spacing="2",
            align="stretch",
        ),
        name=name,
        width="30vw",
    )


style_section = {
    "height": "90vh",
    "width": "80%",
    "margin": "auto",
}