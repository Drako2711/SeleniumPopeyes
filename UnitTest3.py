from time import sleep
import unittest, HtmlTestRunner
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


class PurchaseProduct(unittest.TestCase):
    @classmethod
    def setUp(inst):
        options = webdriver.ChromeOptions()        
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver_path = Service("D:\\PROYECTOS CICLO IX\\SELENIUM\\Drivers\\chromedriver.exe")
        inst.driver = webdriver.Chrome(service=driver_path,options=options)
        inst.driver.maximize_window()
        inst.driver.implicitly_wait(30)
        
    def test_01_purchase(self):
        #Opcion 1: Redirigir a un producto  
        #self.driver.get("https://ppys-dev.jnq.io/")
        self.driver.get("https://ppys-dev.jnq.io/menu/promociones/cyber-popeyes-compartir-old")
        print("purchase")
       
    @classmethod
    def tearDown(inst):
        inst.driver.quit()
        
    def is_element_present(self, how, what):
        """
        Metodo auxiliar para confirmar la presencia de un elemento en la página
        : param how: por tipo de localizador
        : params what: valor del localizador
        """
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException: return False
        return True
    
if __name__ == '__main__':
    unittest.main(verbosity=2)
    #unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='C:/Users/artur/Desktop/Python/Python/PopeyesPruebas/UnitTest'))
    #unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='UnitTest'))