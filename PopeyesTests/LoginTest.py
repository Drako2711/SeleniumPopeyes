from time import sleep
#Unittest
import unittest, allure, pytest
#Selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
#Page
from ..PopeyesPage.BasePage import BasePg
from ..PopeyesPage.LoginPage import LoginPg
import sys
@allure.feature(u'Log in') 
class LoginAccount(unittest.TestCase):
    @classmethod
    def setUp(inst):
        with allure.step(u"Iniciar el controlador"):            
            inst.browser = BasePg.get_option("browser")
            inst.host = BasePg.get_option("host")
            inst.display = BasePg.get_option("display")
            print("Browser: "+inst.browser)
            print("Host: "+str(inst.host))
            print("Display: "+inst.display)
            #inst.driver = BasePg.__init__(inst, inst.browser,"desktop","a") #browser,platform,display
            inst.driver = BasePg.__init__(inst,inst.browser,inst.display) #browser,platform,display
            inst.driver.implicitly_wait(20)
            inst.loginPage = LoginPg(inst.driver)     

    @allure.title(u"Navegación inicial")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description(u"Se requiere ingresar a la página de Popeyes en la sección de home")
    @allure.story(u'Navegación')
    def test_01_nav_ppys(self):
        with allure.step("Abrir página inicial de Popeyes"):
            self.driver.get(self.host)
            self.assertIn("Popeyes", self.driver.title)
            self.loginPage.acceptCookies()
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
            #Carga de página  
            sleep(2)
            
        with allure.step(u"Abrimos ventana de google"):
            self.loginPage.openWindow("google")
            self.loginPage.switchPage(1) #switch Google 
            
        with allure.step(u"Ingresamos las credenciales de la cuenta de Google"):            
            if self.browser == "Chrome" or self.browser == "chrome" or self.browser == "CHROME" or self.browser == "ch" or self.browser == "Opera" or self.browser == "opera" or self.browser == "op" or self.browser == "default":
                self.loginPage.loginGoogle("serve") #serve o local
            else:
                self.loginPage.loginGoogle("local") #serve o local                
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
            self.loginPage.validateAddress("confirm")
    
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
            self.loginPage.addDataAddress("Casa","998753545","Referencia", "Casa", False, False, False) #Tipo, Telefono, Referencia, Guardar como, Promociones, Predeterminada, Manzana y Lote            
        with allure.step(u"Validamos la configuración de la dirección"):  
            self.loginPage.validateAddress("add")
    
    @allure.title(u"Seleccionar local")    
    @allure.description(u"Se requiere seleccionar un local, en este caso en CENTRO CIVICO")
    @allure.story(u'Dirección')
    def test_05_login_select(self):
        self.test_02_login()     
        with allure.step(u"Seleccionamos recojo en local"):  
            self.loginPage.selectPickUp()
        with allure.step(u"Seleccionamos el local"):  
            self.loginPage.selectStore("Cercado de Lima") #Local Titulo
        with allure.step(u"Confirmamos la selección"):   
            self.loginPage.confirmStore()            
        with allure.step(u"Validamos el local seleccionado"):              
            self.loginPage.validateStore()                       
    
    def test_06_address_clean(self):
        self.test_02_login()     
        with allure.step(u"Ingresamos a la cuenta"):  
            self.loginPage.navToLogin()
        with allure.step(u"Ingresamos a las direcciones"):  
            self.loginPage.navToAddress()
        with allure.step(u"Borramos las direcciones guardadas"):  
            self.loginPage.cleanAddress()
        
       
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
