import reflex as rx  # type: ignore
import requests as rq  # type: ignore
import re

class RegisterState(rx.State):
    loader: bool = False
    username: str = ""
    email: str = ""
    password: str = ""
    error: bool = False
    response: dict = {}

    @rx.background
    async def registerService(self, data: dict):
        async with self:
            self.loader = True
            self.error = False
            # Ajustar los nombres de los campos para que coincidan con el esquema del backend
            payload = {
                "full_name": self.username,
                "password": self.password,
                "correo": self.email  # Asegúrate de que el campo sea "email" y no "correo"
            }
            response = rq.post("http://localhost:8000/api/insert_users", json=payload, headers={"Content-Type": "application/json"})
            if response.status_code == 201:
                self.loader = False
                return rx.redirect("/login")  # Redirigir a la página de inicio de sesión
            else:
                self.loader = False
                self.error = True
    
    @rx.var
    def username_empty(self) -> bool:
        return not self.username.strip()
    
    @rx.var
    def email_empty(self) -> bool:
        return not self.email.strip()
    
    @rx.var
    def email_invalid(self) -> bool:
        return not re.match(r"[^@]+@[^@]+\.[^@]+", self.email)
    
    @rx.var
    def password_empty(self) -> bool:
        return not self.password.strip()
    
    @rx.var
    def validate_fields(self) -> bool:
        return (
            self.username_empty
            or self.email_empty
            or self.email_invalid
            or self.password_empty
        )


@rx.page(route="/registro", title="Registro")
def register() -> rx.Component:
    print("Función index de registro.py ejecutada")  # Agrega esta línea para depuración
    # Register Page
    return rx.section(
        rx.flex(
            rx.image(src='/registro.ico', width="300px", border_radius="15px 10px"),
            rx.heading("Crear cuenta"),
            rx.form.root(
                rx.flex(
                    field_form_component("Nombre completo", "Escribe tu nombre completo", "username",
                                         RegisterState.set_username, "text"),
                    field_form_component_general("Correo electrónico", "Escribe un correo válido", "Escribe un correo válido", "email",
                                                 RegisterState.set_email, RegisterState.email_invalid),
                    field_form_component("Contraseña", "Elige una contraseña segura", "password",
                                         RegisterState.set_password, "password"),
                    rx.form.submit(
                        rx.cond(
                            RegisterState.loader,
                            rx.chakra.spinner(color="red", size="xs"),
                            rx.button(
                                "Registrarme",
                                disabled=RegisterState.validate_fields,
                                width="30vw",
                            ),
                        ),
                        as_child=True,
                    ),
                    rx.link(
                        "¿Ya tienes cuenta? Inicia sesión",
                        href="/login",
                    ),
                    rx.link(
                        "Volver al inicio",
                        href="/",
                    ),
                    direction="column",
                    justify="center",
                    align="center",
                    spacing="2",
                ),
                rx.cond(
                    RegisterState.error,
                    rx.callout(
                        "Hubo un error al registrar tu cuenta",
                        icon="alarm_clock",
                        color_scheme="red",
                        role="alert",
                        style={"margin_top": "10px"}
                    ),
                ),
                on_submit=RegisterState.registerService,
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
                "Este campo es obligatorio",
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
