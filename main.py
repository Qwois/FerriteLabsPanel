import flet as ft
import os
from login_page import LoginPage
import uvicorn
import time
from multiprocessing import Process

def main(page: ft.Page):
    LoginPage(page)

if __name__ == "__main__":
    os.environ["FLET_APP_DEBUG"] = "1"
    api_process = Process(target=uvicorn.run, args=("api:app",), kwargs={"host": "0.0.0.0", "port": 8000})
    api_process.start()
    
    time.sleep(2)
    
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)