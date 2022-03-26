import unittest, allure
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
#Services
from selenium.webdriver.chrome.service import Service as ServiceChrome
from selenium.webdriver.firefox.service import Service as ServiceFirefox
from selenium.webdriver.edge.service import Service as ServiceEdge
from selenium.webdriver.ie.service import Service as ServiceIE
#Drivers
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.microsoft import IEDriverManager
#Options 
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.ie.options import Options as IeOptions
#Otros
import sys, os

class BasePg(object):
    def __init__(self,browser,display):
        br = ""
        if browser == "Chrome" or browser == "chrome" or browser == "CHROME" or browser == "ch":
            br = "Google Chrome"
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument ('disable-infobars')
            options.add_argument('--headless')
            options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(service=ServiceChrome(ChromeDriverManager().install()),options=options)
        elif browser == "Firefox" or browser == "firefox" or browser == "FIREFOX" or browser == "ff":
            br = "Firefox"
            options = FirefoxOptions()
            options.add_argument('--headless')
            options.add_argument("--no-sandbox")
            #Para carga de locales
            options.set_preference("geo.prompt.testing", True)
            options.set_preference("geo.prompt.testing.allow", False)    
            driver = webdriver.Firefox(service=ServiceFirefox(GeckoDriverManager().install()),options=options)
        elif browser == "Edge" or browser == "edge" or browser == "EDGE" or browser == "ed":
            br = "Edge"
            options = EdgeOptions()
            options.add_argument('--headless')
            options.add_argument("--no-sandbox")
            driver = webdriver.Edge(service=ServiceEdge(EdgeChromiumDriverManager().install()),options=options)
        elif browser == "Opera" or browser == "opera" or browser == "OPERA" or browser == "op":
            br = "Opera"
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument("--no-sandbox")
            options.add_experimental_option('w3c', True) 
            driver = webdriver.Opera(executable_path=OperaDriverManager().install(),options=options)
        elif browser == "IE" or browser == "ie" or browser == "IEXPLORER" or browser == "iex":
            br = "Internet Explorer"
            options = IeOptions()
            options.add_argument('--headless')
            options.add_argument("--no-sandbox")
            #options.add_argument ('window-size = 1920x1080')
            driver = webdriver.Ie(service=ServiceIE(IEDriverManager().install()),options=options)
        
        dis = display.split("x")
        if (len(dis) == 2):
            driver.set_window_size(int(dis[0]),int(dis[1]))
        else:                
            raise NameError("Ingrese un tamaño de pantalla valida")
        
        try:            
            self.driver = driver
            BasePg.set_environment(br,display,driver.capabilities['browserVersion'])
        except Exception:
            raise NameError("Not found %s browser,You can enter 'ie', 'ff' or 'chrome'." % browser + " error: "+browser)
        return self.driver
                
    def get_option(option):
        if (option == "browser"):
            return os.environ["V_Browser"]    
        elif (option == "host"):
            return os.environ["V_Host"]
        elif (option == "display"):
            return os.environ["V_Display"]
            
    def set_environment(br,dis,ver):
        f = open("../allure-results/environment.properties","w+")
        f.write("Navegador = " + br + " " + ver + "\n")
        f.write("Pantalla = " + dis + "\n")
        f.close()

    #Commmon 
    def is_element_present(self, how, what):
        """
        Metodo auxiliar para confirmar la presencia de un elemento en la página
        : param how: por tipo de localizador
        : params what: valor del localizador
        """
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException: return False
        return True

    def screenshot(self,description):
        allure.attach(self.driver.get_screenshot_as_png(), description, attachment_type=allure.attachment_type.PNG)
