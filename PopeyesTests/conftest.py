# content of conftest.py
import pytest, os

def pytest_addoption(parser):
    parser.addoption("--br", action="store", default="Chrome", help = "Nombre del Navegador: Chrome, Firefox, Edge, Opera, IE")
    parser.addoption("--pl", action="store", default="desktop", help = "Nombre de la plataforma 'Desktop' or 'Mobile'") 
    parser.addoption("--ds", action="store", default="a", help = "Resoluciones disponibles: \n Mobile: a=412x915, b=360x640, c=393x851, d=360x780, e=412x892, f=393x873 \n\
        Desktop: a=1366x768, b=1920x1080, c=1536x864, d=1600x900, e=1440x900, f=1280x720")

def pytest_configure(config):
    os.environ["V_Browser"]=config.getoption("br")
    os.environ["V_Platform"]=config.getoption("pl")
    os.environ["V_Display"]=config.getoption("ds")
