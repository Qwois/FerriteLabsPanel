import flet as ft
import requests
from main_page import MainPage
import time

class LoginPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Login Page"
        self.page.theme_mode = "dark"
        self.build_login_page()

    def build_login_page(self):
        self.username_field = ft.TextField(label="Username", width=300)
        self.password_field = ft.TextField(label="Password", password=True, width=300)

        self.login_status = ft.Text("", color="red")

        login_button = ft.ElevatedButton("Login", on_click=self.handle_login)

        self.login_container = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Login to Server Control Panel", size=30, weight="bold", color="white"),
                    self.username_field,
                    self.password_field,
                    login_button,
                    self.login_status
                ],
                alignment="center",
                horizontal_alignment="center",
                spacing=20
            ),
            alignment=ft.alignment.center,
            padding=50,
        )

        self.page.add(self.login_container)

    def handle_login(self, e):
        username = self.username_field.value
        password = self.password_field.value

        if not username or not password:
            self.login_status.value = "Please enter both username and password."
            self.page.update()
            return

        try:
            response = requests.post(
                "http://localhost:8000/token", 
                data={"username": username, "password": password},  
                headers={"Content-Type": "application/x-www-form-urlencoded"}  
            )
            if response.status_code == 200:
                token = response.json().get("access_token")
                self.login_status.value = "Login successful"

                self.page.controls.remove(self.login_container)

                MainPage(self.page)
                self.page.update()
            else:
                self.login_status.value = "Invalid username or password"
        except Exception as ex:
            self.login_status.value = f"Error: {ex}"

        self.page.update()