from time import sleep
#Unittest
import unittest, allure
#Selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
#Services
from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.firefox.service import Service
#Drivers
from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.firefox import GeckoDriverManager
#Otros
import sys, os, pytest, subprocess
#Page
from ..PopeyesPage.LoginPage import Login

@allure.feature(u'Log in') 
class LoginAccount(unittest.TestCase):
    @classmethod
    def setUp(inst):
        with allure.step(u"Iniciar el controlador de Chrome"):
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            #inst.driver = webdriver.Chrome(service=Service("D:\\PROYECTOS CICLO IX\\SELENIUM\\Drivers\\chromedriver.exe"),options=options)
            inst.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
            #inst.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
            inst.driver.maximize_window()
            inst.driver.implicitly_wait(15)
            inst.loginPage = Login(inst.driver)
    
    @allure.title(u"Navegación inicial")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description(u"Se requiere ingresar a la página de Popeyes en la sección de home")
    @allure.story(u'Navegación')
    def test_01_nav_ppys(self):
        with allure.step("Abrir página inicial de Popeyes"):
            self.driver.get("https://ppys-dev.jnq.io/")
            self.assertIn("Popeyes", self.driver.title)
            assert "No se encontro el elemento" not in self.driver.page_source
    
    @allure.title(u"Login cuenta nativa")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description(u"Se requiere iniciar sesión con cuenta nativa")
    @allure.story(u'Inicio de sesión')
    def test_02_login(self):
        with allure.step(u"Accedemos a la página de inicio de sesión"):
            self.loginPage.navToLogin()
        
        with allure.step(u"Ingresamos las credenciales de inicio de sesión con cuenta nativa"):
            self.loginPage.loginNative()
        
        with allure.step(u"Validamos el inicio de sesión"):
            self.loginPage.loginValidate("native")    
    
    @allure.title(u"Login cuenta Facebook")
    @allure.story(u'Inicio de sesión')    
    @allure.description(u"Se requiere iniciar sesión con cuenta Facebook")
    def test_02_login_facebook(self):
        with allure.step(u"Ingresamos a la página de inicio de sesión"):
            self.loginPage.navToLogin()
        
        with allure.step(u"Abrimos ventana de facebook"):
            self.loginPage.openWindow("facebook")
            self.loginPage.switchPage(1) #switch Facebook        
        
        with allure.step(u"Ingresamos las credenciales de la cuenta de Facebook"):
            self.loginPage.loginFacebook()      
            self.loginPage.switchPage(0) #switch Popeyes 
                 
        with allure.step(u"Validamos el ingreso correcto"):        
            self.loginPage.loginValidate("facebook")    
           
    @allure.title(u"Login cuenta Google")
    @allure.story(u'Inicio de sesión')
    @allure.description(u"Se requiere iniciar sesión con cuenta Google")
    def test_02_login_google(self):
        with allure.step(u"Ingresamos a la página de inicio de sesión"):        
            self.loginPage.navToLogin()
            
        with allure.step(u"Abrimos ventana de google"):
            self.loginPage.openWindow("google")
            self.loginPage.switchPage(1) #switch Google 
            
        with allure.step(u"Ingresamos las credenciales de la cuenta de Google"):            
            self.loginPage.loginGoogle()
            self.loginPage.switchPage(0) #switch Popeyes   
              
        with allure.step(u"Validamos el ingreso correcto"):                    
            self.loginPage.loginValidate("google")            
    
    @allure.title(u"Confirmar dirección") 
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description(u"Se requiere confirmar la primera dirección registrada")
    @allure.story(u'Dirección')
    def test_03_login_confirm(self):        
        self.test_02_login()
        with allure.step(u"Seleccionamos la primera dirección"):        
            self.loginPage.selectAddress(1) #Seleccionar primera dirección
        with allure.step(u"Confirmamos la selección"): 
            self.loginPage.confirmAddress()
        with allure.step(u"Validamos la configuración de dirección"):        
            self.loginPage.validateAddress()
    
    @allure.title(u"Agregar nueva dirección")
    @allure.description(u"Se requiere agregar una nueva dirección")
    @allure.story(u'Dirección')
    def test_04_login_add(self):
        self.test_02_login()
        with allure.step(u"Seleccionamos nueva dirección"):  
            self.loginPage.clickAddAddress()                           
        with allure.step(u"Ingresamos la dirección de prueba"):  
            self.loginPage.searchAddress("Av. Inca Garcilaso de la Vega 1698, Cercado de Lima, Perú") #Dirección
        with allure.step(u"Ingresamos los datos restantes"):  
            self.loginPage.searchAddress("Casa","998753545","Referencia", "Casa", False, False, False) #Tipo, Telefono, Referencia, Guardar como, Promociones, Predeterminada, Manzana y Lote            
        with allure.step(u"Validamos la configuración de la dirección"):  
            self.loginPage.validateAddress()
    
    @allure.title(u"Seleccionar local")    
    @allure.description(u"Se requiere seleccionar un local, en este caso en CENTRO CIVICO")
    @allure.story(u'Dirección')
    def test_05_login_select(self):
        self.test_02_login()     
        with allure.step(u"Seleccionamos recojo en local"):  
            self.loginPage.selectPickUp()
        with allure.step(u"Seleccionamos recojo el local"):  
            self.loginPage.selectStore("Cercado de Lima") #Local Titulo
        with allure.step(u"Confirmamos la selección"):   
            self.loginPage.confirmStore()            
        with allure.step(u"Validamos el local seleccionado"):              
            self.loginPage.validateStore()                       
       
    @classmethod
    def tearDown(inst):
        inst.driver.quit()
    
if __name__ == '__main__':
    unittest.main(verbosity=2)
    #Run allure report of this file, export report to PJ/Reports
    #pytest.main(['-s', '-q','--alluredir','D://','Unittest.py'])
    #Open allue report via browser
    #subprocess.run([r'powershell.exe', r'allure ' + 'serve ' + 'C://'])
    #unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='C:/Users/artur/Desktop/Python/Python/PopeyesPruebas/UnitTest'))
    #unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='UnitTest'))
