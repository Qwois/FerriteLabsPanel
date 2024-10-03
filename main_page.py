import flet as ft
import paramiko
import os

class MainPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Main Panel"
        self.page.theme_mode = "dark"
        self.page.bgcolor = ft.colors.BLACK87

        self.ssh_client = None
        self.ssh_key_path = None

        # AppBar для навигации
        self.page.appbar = ft.AppBar(
            title=ft.Text("Server Control Panel"),
            bgcolor=ft.colors.BLACK12,
            actions=[
                ft.IconButton(ft.icons.HOME, on_click=self.go_home),
                ft.IconButton(ft.icons.SETTINGS, on_click=self.go_settings),
                ft.IconButton(ft.icons.LOGOUT, on_click=self.handle_logout)
            ],
        )

        # FilePicker
        self.file_picker = ft.FilePicker(on_result=self.file_picked)
        self.page.overlay.append(self.file_picker)

        # Строим главную страницу
        self.build_main_page()

    def build_main_page(self):
        self.server_ip_field = ft.TextField(label="Server IP", width=300)

        self.ssh_key_button = ft.ElevatedButton("Select SSH Key", on_click=self.pick_ssh_key)
        self.ssh_key_label = ft.Text("No SSH key selected", color="white")

        self.connect_button = ft.ElevatedButton("Connect to SSH", on_click=self.handle_connect)

        self.connection_status = ft.Text("", color="white")

        self.page.add(
            ft.Column(
                [
                    ft.Text("SSH Connection Panel", size=30, weight="bold", color="white"),
                    self.server_ip_field,
                    self.ssh_key_button,
                    self.ssh_key_label,
                    self.connect_button,
                    self.connection_status
                ],
                alignment="center",
                horizontal_alignment="center",
                spacing=20
            )
        )

    def pick_ssh_key(self, e):
        self.file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=None  # Разрешаем выбрать любой тип файла
        )

    def file_picked(self, e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            self.ssh_key_path = e.files[0].path
            self.ssh_key_label.value = f"Selected SSH Key: {self.ssh_key_path}"
            print(f"Selected file: {self.ssh_key_path}")  # Отладочная информация
        else:
            self.ssh_key_label.value = "No SSH key selected"
            print("No file selected.")
        self.page.update()

    def handle_connect(self, e):
        if not self.ssh_key_path:
            self.connection_status.value = "Please select an SSH key first."
            self.page.update()
            return

        server_ip = self.server_ip_field.value

        if not server_ip:
            self.connection_status.value = "Please enter the Server IP."
            self.page.update()
            return

        try:
            if not os.path.exists(self.ssh_key_path):
                raise FileNotFoundError(f"No such file: {self.ssh_key_path}")

            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(server_ip, username="root", key_filename=self.ssh_key_path)

            self.connection_status.value = "Successfully connected to the server!"
            self.connection_status.color = "green"
            print("SSH connection successful.")

        except Exception as ex:
            self.connection_status.value = f"Failed to connect: {ex}"
            self.connection_status.color = "red"
            print(f"Failed to connect: {ex}")

        self.page.update()

    def go_home(self, e):
        self.connection_status.value = "Home button clicked"
        self.page.update()

    def go_settings(self, e):
        self.connection_status.value = "Settings button clicked"
        self.page.update()

    def handle_logout(self, e):
        self.page.controls.clear()
        self.page.appbar = None
        self.page.bgcolor = None
        from login_page import LoginPage
        LoginPage(self.page)
        self.page.update()