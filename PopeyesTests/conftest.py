# content of conftest.py
import pytest, os

def pytest_addoption(parser):
    parser.addoption("--br", action="store", default="Chrome", help = "Nombre del Navegador: Chrome, Firefox, Edge, Opera, IE")
    parser.addoption("--hs", action="store", default="https://ppys-dev.jnq.io/", help = "URL del host: default => https://ppys-dev.jnq.io/") 
    parser.addoption("--ds", action="store", default="1920x1080", help = "Algunas resoluciones son: \n Mobile: 412x915, 360x640, 393x851, 360x780, 412x892, 393x873 \n\
        Desktop: 1366x768, 1920x1080, 1536x864, 1600x900, 1440x900, 1280x720")

def pytest_configure(config):
    os.environ["V_Browser"]=config.getoption("br")
    os.environ["V_Host"]=config.getoption("hs")
    os.environ["V_Display"]=config.getoption("ds")
