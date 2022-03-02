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
#Credenciales
from credenciales import PopeyeAccounts
#Otros
import sys, os, pytest, subprocess

@allure.feature(u'Log in') 
class LoginAccount(unittest.TestCase):
    @classmethod
    def setUp(inst):
        with allure.step(u"Iniciar el controlador de Chrome"):
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            inst.driver = webdriver.Chrome(service=Service("D:\\PROYECTOS CICLO IX\\SELENIUM\\Drivers\\chromedriver.exe"),options=options)
            #inst.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
            inst.driver.maximize_window()
            inst.driver.implicitly_wait(15)
    
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
        account = PopeyeAccounts.default_account()
        with allure.step(u"Accedemos a la página de inicio de sesión"):
            self.driver.get("https://ppys-dev.jnq.io/customer/account/login")
        with allure.step(u"Ingresamos las credenciales de inicio de sesión con cuenta nativa"):
            elem = self.driver.find_element(By.CSS_SELECTOR,"#__layout > div > div.page-wrapper > div.page-content-wrapper > div > div > div > form > div > div:nth-child(1) > input[type=email]")
            elem.send_keys(account["user"])
            elem = self.driver.find_element(By.ID,"input-password")
            elem.send_keys(account["password"])
            elem.send_keys(Keys.ENTER)    
        with allure.step(u"Validamos el inicio de sesión"):
            self.assertTrue(self.is_element_present(By.CSS_SELECTOR,".alert-content.success"))       
            #Aceptar cookies y seleccionar later en suscribir
            try: 
                self.driver.find_element(By.CSS_SELECTOR,".btn.btn-acepta").click()
                self.driver.find_element(By.CSS_SELECTOR,"#onesignal-slidedown-cancel-button").click()
            except:
                print("No se encontraron los botones de cookies ni de suscripción")    
    
    @allure.title(u"Login cuenta Facebook")
    @allure.story(u'Inicio de sesión')    
    @allure.description(u"Se requiere iniciar sesión con cuenta Facebook")
    def test_02_login_facebook(self):
        account = PopeyeAccounts.facebook_account()
        with allure.step(u"Ingresamos a la página de inicio de sesión"):
            self.driver.get("https://ppys-dev.jnq.io/customer/account/login")
        with allure.step(u"Abrimos ventana de facebook"):
            elem = self.driver.find_element(By.CSS_SELECTOR,"div.btn-fb")
            elem.click()
            #Esperamos a que cargue Facebook
            try:
                WebDriverWait(self.driver, 30).until(EC.number_of_windows_to_be(2))
            except TimeoutException:
                print ("No se logró cargar la página de facebook")
            #Cambiamos a la pestaña de Facebook
            self.driver.switch_to.window(self.driver.window_handles[1])
        with allure.step(u"Ingresamos las credenciales de la cuenta de Facebook"):
            elem = self.driver.find_element(By.ID, "email")
            elem.send_keys(account["user"])
            try:
                element_present = EC.presence_of_element_located((By.ID, "pass"))
                WebDriverWait(self.driver, 30).until(element_present)
            except TimeoutException:
                print ("No se logró cargar el input de contraseña de Facebook")            
            #Escribir contraseña y correo de facebook / Si se ingresa en otro orden hay error
            elem = self.driver.find_element(By.ID, "pass")
            elem.send_keys(account["password"])     
            elem.send_keys(Keys.ENTER)     
            #Volver a la pagina de ppys
            self.driver.switch_to.window(self.driver.window_handles[0])
        with allure.step(u"Validamos el ingreso correcto"):        
            #Verificamos si el logeo es correcto
            self.assertTrue(self.is_element_present(By.XPATH,'//p[contains(text(),"¡Bienvenido! Gracias por iniciar sesión con tu cuenta de Facebook en Popeyes.")]'),"Ocurrió un error al intentar ingresar con la cuenta de Facebook")  
            #Aceptar cookies y seleccionar later en suscribir
            try: 
                self.driver.find_element(By.CSS_SELECTOR,".btn.btn-acepta").click()
                self.driver.find_element(By.CSS_SELECTOR,"#onesignal-slidedown-cancel-button").click()
            except:
                print("No se encontraron los botones de cookies ni de suscripción")    
           
    @allure.title(u"Login cuenta Google")
    @allure.story(u'Inicio de sesión')
    @allure.description(u"Se requiere iniciar sesión con cuenta Google")
    def test_02_login_google(self):
        account = PopeyeAccounts.google_account()
        with allure.step(u"Ingresamos a la página de inicio de sesión"):        
            self.driver.get("https://ppys-dev.jnq.io/customer/account/login")
        with allure.step(u"Abrimos ventana de google"):
            #Seleccionar Google
            elem = self.driver.find_element(By.ID,"google-signin-btn-0")
            elem.click()
            #Esperamos a que cargue Google
            try:
                WebDriverWait(self.driver, 30).until(EC.number_of_windows_to_be(2))
            except TimeoutException:
                print ("No se logró cargar la página de google") 
            #Cambiar a la pestaña de Google        
            self.driver.switch_to.window(self.driver.window_handles[1])
        with allure.step(u"Ingresamos las credenciales de la cuenta de Google"):
            #Esperamos a que cargue el botón de iniciar sesión
            try:
                element_present = EC.presence_of_element_located((By.ID, "identifierId"))
                WebDriverWait(self.driver, 30).until(element_present)
            except TimeoutException:
                print ("Se agotó el tiempo de espera para cargar la página")            
            elem = self.driver.find_element(By.ID, "identifierId")
            elem.send_keys(account["user"])  
            elem.send_keys(Keys.ENTER)  
            try:
                element_present = EC.presence_of_element_located((By.NAME, "password"))
                WebDriverWait(self.driver, 30).until(element_present)
            except TimeoutException:
                print ("Se agotó el tiempo de espera para cargar la página")            
            elem = self.driver.find_element(By.NAME, "password")
            elem.send_keys(account["password"])  
            elem.send_keys(Keys.ENTER)
            #Volver a la pagina de ppys
            self.driver.switch_to.window(self.driver.window_handles[0])        
        with allure.step(u"Validamos el ingreso correcto"):                    
            #Verificamos si el logeo es correcto
            self.assertTrue(self.is_element_present(By.XPATH,'//p[contains(text(),"¡Bienvenido! Gracias por iniciar sesión con tu cuenta de Google en Popeyes.")]'))  
            #Aceptar cookies y seleccionar later en suscribir
            try: 
                self.driver.find_element(By.CSS_SELECTOR,".btn.btn-acepta").click()
                self.driver.find_element(By.CSS_SELECTOR,"#onesignal-slidedown-cancel-button").click()
            except:
                print("No se encontraron los botones de cookies ni de suscripción")    
    
    @allure.title(u"Confirmar dirección") 
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description(u"Se requiere confirmar la primera dirección registrada")
    @allure.story(u'Dirección')
    def test_03_login_confirm(self):        
        self.test_02_login()
        with allure.step(u"Seleccionamos la primera dirección"):        
            #Delivery, Confirmar Primera dirección    
            try:
                element_present = EC.presence_of_element_located((By.CSS_SELECTOR, "div.input-box-old.address-item"))
                WebDriverWait(self.driver, 30).until(element_present)
            except TimeoutException:
                print ("No se encontró ninguna dirección registrada")
            elem = self.driver.find_element(By.CSS_SELECTOR,'div.input-box-old.address-item')
            elem.click()
        with allure.step(u"Confirmamos la selección"): 
            elem = self.driver.find_element(By.XPATH,'//button[contains(text(),"CONFIRMAR")]') 
            elem.click() 
        with allure.step(u"Validamos la configuración de dirección"):        
            #self.assertTrue(self.is_element_present(By.CSS_SELECTOR,".alert-content.success")) 
            try:
                element_present = EC.presence_of_element_located((By.XPATH, '//p[contains(text(),"Tu dirección ha sido configurada correctamente.")]'))
                WebDriverWait(self.driver, 20).until(element_present) 
                self.assertTrue(self.is_element_present(By.XPATH,'//p[contains(text(),"Tu dirección ha sido configurada correctamente.")]'))  
            except TimeoutException:        
                self.assertTrue(self.is_element_present(By.XPATH,'//p[contains(text(),"Tu dirección ha sido configurada correctamente.")]'),'Ocurrió un problema al confirmar el mensaje dirección correctamente configurada')
    
    @allure.title(u"Agregar nueva dirección")
    @allure.description(u"Se requiere agregar una nueva dirección")
    @allure.story(u'Dirección')
    def test_04_login_add(self):
        self.test_02_login()
        #Opcion 2: Delivery, Nueva dirección        
        with allure.step(u"Seleccionamos nueva dirección"):  
            elem = self.driver.find_element(By.XPATH,'//button[contains(text(),"NUEVA DIRECCIÓN")]') 
            elem.click()                
        with allure.step(u"Ingresamos la dirección de prueba"):  
            #Entrar al input de dirección 
            elem = self.driver.find_element(By.ID,'mi_ubicacion') 
            elem.send_keys("Av. Inca Garcilaso de la Vega 1698, Cercado de Lima, Perú")        
            #Dar click en la lupa para buscar
            elem = self.driver.find_element(By.XPATH,'//*[@id="__layout"]/div/div[1]/div[2]/div/div[2]/div/div[2]/div/div/div[1]/button')
            elem.click()            
            #selecciona el primer item de la busqueda   
            elem = self.driver.find_element(By.CLASS_NAME,'pac-item') 
            elem.click()    
        with allure.step(u"Ingresamos los datos restantes"):  
            #Seleccionar Tipo de vivienda
            try:
                element_present = EC.presence_of_element_located((By.CSS_SELECTOR, "select"))
                WebDriverWait(self.driver, 30).until(element_present)
            except TimeoutException:
                print ("Se agotó el tiempo de espera para cargar la página")
            
            elem = Select(self.driver.find_element(By.CSS_SELECTOR,'select'))
            #elem.find_element(By.XPATH, "//option[. = 'Casa']").click()      
            elem.select_by_visible_text("Casa")
            #Ingresar celular
            elem = self.driver.find_element(By.CSS_SELECTOR, ".phone > input")
            elem.send_keys("998218812")
            #Ingresar Referencia
            elem = self.driver.find_element(By.CSS_SELECTOR, ".reference > input")
            elem.send_keys("Referencia")
            #Seleccionar Casa
            elem = self.driver.find_element(By.ID,'home')
            elem.click()
            #Dar click en Confirmar
            elem = self.driver.find_element(By.CSS_SELECTOR,'div.content-btn > button')         
            elem.click()        
        with allure.step(u"Validamos la configuración de la dirección"):  
            self.assertTrue(self.is_element_present(By.XPATH,'//p[contains(text(),"Tu dirección ha sido guardada correctamente.")]'))  
    
    @allure.title(u"Seleccionar local")    
    @allure.description(u"Se requiere seleccionar un local, en este caso en CENTRO CIVICO")
    @allure.story(u'Dirección')
    def test_05_login_select(self):
        self.test_02_login()
        #Opcion 3: Recojo en local, Seleccionar local        
        with allure.step(u"Seleccionamos recojo en local"):  
            elem = self.driver.find_elements(By.CSS_SELECTOR,'div.button-delivery')[1]
            elem.click()
            #Seleccionar el item del local de Cercado de Lima
            elem = self.driver.find_element(By.XPATH,'//h4[contains(text(),"Cercado de Lima")]')
        with allure.step(u"Confirmamos la selección"):  
            self.driver.execute_script("arguments[0].click();", elem)
            #elem = self.driver.find_element(By.CSS_SELECTOR,'div.buttons-store.btn')  
            elem = self.driver.find_element(By.XPATH,'//button[contains(text(),"CONFIRMAR")]') 
            elem.click()
        with allure.step(u"Validamos el local seleccionada"):              
            try:
                element_present = EC.presence_of_element_located((By.CSS_SELECTOR, "div.store-name > p"))
                WebDriverWait(self.driver, 5).until(element_present)
                elem = self.driver.find_element(By.CSS_SELECTOR,'div.store-name > p')  
                self.screenshot("Seleccionar local")
                self.assertEqual(elem.text,"CENTRO CIVICO","No se seleccionó el local esperada")
            except TimeoutException:        
                self.screenshot("Error en la selección de local")
                self.assertTrue(self.is_element_present(By.CSS_SELECTOR,'div.store-name > p'),'Ocurrió un error al confirmar el local, posiblemente no esté disponible')
       
    def explicit_wait_click(self,tipo,selector,time,error):
        try:
            element_present = EC.element_to_be_clickable((tipo, selector))
            WebDriverWait(self.driver, time).until(element_present)
            elem = self.driver.find_element(tipo,selector)  
            elem.click()
        except TimeoutException:        
            self.assertTrue(self.is_element_present(tipo,selector), error)
            
    def explicit_wait_equal(self,tipo,selector,time,text,error):
        try:
            element_present = EC.element_to_be_clickable((tipo, selector))
            WebDriverWait(self.driver, time).until(element_present)
            elem = self.driver.find_element(tipo,selector)  
            self.assertEqual(elem.text,text,error)
        except TimeoutException:        
            self.assertTrue(self.is_element_present(tipo,selector), error)
    
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
    def screenshot(self,description):
        allure.attach(self.driver.get_screenshot_as_png(), description, attachment_type=allure.attachment_type.PNG)
    
if __name__ == '__main__':
    unittest.main(verbosity=2)
    #Run allure report of this file, export report to PJ/Reports
    #pytest.main(['-s', '-q','--alluredir','D://','Unittest.py'])
    #Open allue report via browser
    #subprocess.run([r'powershell.exe', r'allure ' + 'serve ' + 'C://'])
    #unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='C:/Users/artur/Desktop/Python/Python/PopeyesPruebas/UnitTest'))
    #unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='UnitTest'))
