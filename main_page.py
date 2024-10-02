import flet as ft

class MainPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Main Panel"
        self.page.theme_mode = "dark"
        self.page.bgcolor = ft.colors.BLUE_300

        self.build_main_page()

    def build_main_page(self):
        pass