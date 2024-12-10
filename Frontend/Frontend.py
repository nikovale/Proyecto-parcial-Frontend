import reflex as rx  # type: ignore
from rxconfig import config

class State(rx.State):
    """The app state."""

    ...

def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Bienvenido a mi página", size="9"),
            rx.text(
                "Nombre del creador: Nicolas Arturo Valencia",
                size="5",
            ),
            rx.text(
                "Código: 202067802",
                size="5",
            ),
            rx.hstack(
                rx.link(
                    rx.button("Registro"),
                    href="/registro",
                ),
                rx.link(
                    rx.button("Login"),
                    href="/login",
                ),
                spacing="5",
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
    )

app = rx.App()
app.add_page(index)