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

class Login(unittest.TestCase):
    @classmethod
    def setUp(inst):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        inst.driver = webdriver.Chrome(service=ChromeDriverManager().install(),options=options)
        #inst.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        inst.driver.maximize_window()
        inst.driver.implicitly_wait(15)
    
    def test_01_nav_ppys(self):
        with allure.step("Open application"):
            self.driver.get("https://ppys-dev.jnq.io/")
            self.assertIn("Popeyes", self.driver.title)
            assert "No se encontro el elemento" not in self.driver.page_source
    
    def test_02_login(self):
        #Credenciales
        account = PopeyeAccounts.default_account()
        #Ingreso a la sección de login
        self.driver.get("https://ppys-dev.jnq.io/customer/account/login")
        #Busqueda del elemento de correo y su ingreso
        elem = self.driver.find_element(By.CSS_SELECTOR,"#__layout > div > div.page-wrapper > div.page-content-wrapper > div > div > div > form > div > div:nth-child(1) > input[type=email]")
        elem.send_keys(account["user"])
        #Busqueda del elemento de contraseña y su ingreso
        elem = self.driver.find_element(By.ID,"input-password")
        elem.send_keys(account["password"])
        elem.send_keys(Keys.ENTER)    
        #Verificamos si el logeo es correcto
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR,".alert-content.success"))       
        #Aceptar cookies y seleccionar later en suscribir
        try: 
            self.driver.find_element(By.CSS_SELECTOR,".btn.btn-acepta").click()
            self.driver.find_element(By.CSS_SELECTOR,"#onesignal-slidedown-cancel-button").click()
        except:
            print("No se encontraron los botones de cookies ni de suscripción")    
        
    def test_02_login_facebook(self):
        #Credenciales
        account = PopeyeAccounts.facebook_account()
        #Ingreso a la sección de login
        self.driver.get("https://ppys-dev.jnq.io/customer/account/login")
        #Seleccionar Facebook
        elem = self.driver.find_element(By.CSS_SELECTOR,"div.btn-fb")
        elem.click()
        #Esperamos a que cargue Facebook
        try:
            WebDriverWait(self.driver, 30).until(EC.number_of_windows_to_be(2))
        except TimeoutException:
            print ("No se logró cargar la página de facebook")
        #Cambiamos a la pestaña de Facebook
        self.driver.switch_to.window(self.driver.window_handles[1])
        #Esperamos a que cargue el inicio de sesión de facebook          
        elem = self.driver.find_element(By.ID, "email")
        elem.send_keys(account["user"])
        try:
            element_present = EC.presence_of_element_located((By.ID, "pass"))
            WebDriverWait(self.driver, 30).until(element_present)
        except TimeoutException:
            print ("No se logró cargar el input de contraseña de facebook")            
        #Escribir contraseña y correo de facebook / Si se ingresa en otro orden hay error
        elem = self.driver.find_element(By.ID, "pass")
        elem.send_keys(account["password"])     
        elem.send_keys(Keys.ENTER)     
        #Volver a la pagina de ppys
        self.driver.switch_to.window(self.driver.window_handles[0])
                
        #Verificamos si el logeo es correcto
        self.assertTrue(self.is_element_present(By.XPATH,'//p[contains(text(),"¡Bienvenido! Gracias por iniciar sesión con tu cuenta de Facebook en Popeyes.")]'))  
        #Aceptar cookies y seleccionar later en suscribir
        try: 
            self.driver.find_element(By.CSS_SELECTOR,".btn.btn-acepta").click()
            self.driver.find_element(By.CSS_SELECTOR,"#onesignal-slidedown-cancel-button").click()
        except:
            print("No se encontraron los botones de cookies ni de suscripción")    
           
    def test_02_login_google(self):
        #Credenciales
        account = PopeyeAccounts.google_account()
        #Ingreso a la sección de login
        self.driver.get("https://ppys-dev.jnq.io/customer/account/login")
        #self.driver.execute_cdp_cmd("Browser.grantPermissions",{"origin": "https://ppys-dev.jnq.io/","permissions": ["geolocation"]},)
        #Obteniendo el ID del sitio
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
        #Esperamos a que cargue el botón de iniciar sesión
        try:
            element_present = EC.presence_of_element_located((By.ID, "identifierId"))
            WebDriverWait(self.driver, 30).until(element_present)
        except TimeoutException:
            print ("Se agotó el tiempo de espera para cargar la página")            
        #Escribir contraseña y correo de facebook / Si se ingresa en otro orden hay error
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
                
        #Verificamos si el logeo es correcto
        self.assertTrue(self.is_element_present(By.XPATH,'//p[contains(text(),"¡Bienvenido! Gracias por iniciar sesión con tu cuenta de Google en Popeyes.")]'))  
        #Aceptar cookies y seleccionar later en suscribir
        try: 
            self.driver.find_element(By.CSS_SELECTOR,".btn.btn-acepta").click()
            self.driver.find_element(By.CSS_SELECTOR,"#onesignal-slidedown-cancel-button").click()
        except:
            print("No se encontraron los botones de cookies ni de suscripción")    
     
    def test_03_login_confirm(self):
        self.test_02_login()
        #Opcion 1: Delivery, Confirmar Primera dirección    
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, "div.input-box-old.address-item"))
            WebDriverWait(self.driver, 30).until(element_present)
        except TimeoutException:
            print ("No se encontró ninguna dirección registrada")
        #Confirmar dirección, seleccionando la primera
        elem = self.driver.find_element(By.CSS_SELECTOR,'div.input-box-old.address-item')
        elem.click()
        #Dar click en Confirmar   
        elem = self.driver.find_element(By.XPATH,'//button[contains(text(),"CONFIRMAR")]') 
        elem.click()        
        #self.assertTrue(self.is_element_present(By.CSS_SELECTOR,".alert-content.success")) 
        try:
            element_present = EC.presence_of_element_located((By.XPATH, '//p[contains(text(),"Tu dirección ha sido configurada correctamente.")]'))
            WebDriverWait(self.driver, 20).until(element_present) 
            self.assertTrue(self.is_element_present(By.XPATH,'//p[contains(text(),"Tu dirección ha sido configurada correctamente.")]'))  
        except TimeoutException:        
            self.assertTrue(self.is_element_present(By.XPATH,'//p[contains(text(),"Tu dirección ha sido configurada correctamente.")]'),'Ocurrió un problema al confirmar el mensaje dirección correctamente configurada')
    
    def test_04_login_add(self):
        self.test_02_login()
        #Opcion 2: Delivery, Nueva dirección
        
        #Dar click en Nueva dirección   
        elem = self.driver.find_element(By.XPATH,'//button[contains(text(),"NUEVA DIRECCIÓN")]') 
        elem.click()        
        #Entrar al input de dirección 
        elem = self.driver.find_element(By.ID,'mi_ubicacion') 
        elem.send_keys("Av. Inca Garcilaso de la Vega 1698, Cercado de Lima, Perú")        
        #Dar click en la lupa para buscar
        elem = self.driver.find_element(By.XPATH,'//*[@id="__layout"]/div/div[1]/div[2]/div/div[2]/div/div[2]/div/div/div[1]/button')
        elem.click()
        #selecciona el primer item de la busqueda   
        elem = self.driver.find_element(By.CLASS_NAME,'pac-item') 
        elem.click()    
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
        #Verificar que se guardo la dirección
        self.assertTrue(self.is_element_present(By.XPATH,'//p[contains(text(),"Tu dirección ha sido guardada correctamente.")]'))  
    
    def test_05_login_select(self):
        self.test_02_login_google()
        #Opcion 3: Recojo en tienda, Seleccionar tienda
        #Seleccionar botón Recojo en tienda
        #elem = self.driver.find_element(By.XPATH,'//label[contains(text(),"RECOJO EN TIENDA")]')
        elem = self.driver.find_elements(By.CSS_SELECTOR,'div.button-delivery')[1]
        elem.click()
        #Seleccionar cuarto item de tiendas (Cercado de Lima)
        #elem = self.driver.find_element(By.CSS_SELECTOR,'#list_recojo > div:nth-child(3)')
        elem = self.driver.find_element(By.CSS_SELECTOR,'.store-card:nth-child(4) button')
        self.driver.execute_script("arguments[0].click();", elem)
        #Confirmar cuarto item de tiendas (Surco)
        #elem = self.driver.find_element(By.CSS_SELECTOR,'div.buttons-store.btn')  
        elem = self.driver.find_element(By.XPATH,'//button[contains(text(),"CONFIRMAR")]') 
        elem.click()
        #Verificar que se seleccionó la tienda
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, "div.store-name > p"))
            WebDriverWait(self.driver, 5).until(element_present)
            elem = self.driver.find_element(By.CSS_SELECTOR,'div.store-name > p')  
            self.assertEqual(elem.text,"CENTRO CIVICO")
        except TimeoutException:        
            self.assertTrue(self.is_element_present(By.CSS_SELECTOR,'div.store-name > p'),'Ocurrió un error al confirmar la tienda, posiblemente no esté disponible')
    
    def test_06_purchase_product(self):
        #Login
        self.test_03_login_confirm()
        
        self.driver.get("https://ppys-dev.jnq.io/")
        #Seleccionar personales y para compartir
        elem = self.driver.find_element(By.XPATH,'//h4[contains(text(),"Personales y para compartir")]')
        self.driver.execute_script("arguments[0].click();", elem)
        #Seleccionar el segundo producto (Cajun Full)
        elem = self.driver.find_element(By.CSS_SELECTOR,'.product-card:nth-child(2) .btn')
        self.driver.execute_script("arguments[0].click();", elem)
        
        # (1) Elige tus piezas (Obligatorio)       
        #1 Tradicional
        elem = self.driver.find_element(By.CSS_SELECTOR, ".isMinMaxOption:nth-child(3) > div:nth-child(1) .quantity-operator:nth-child(3)")
        self.driver.execute_script("arguments[0].click();", elem)
        #1 Picantito
        elem = self.driver.find_element(By.CSS_SELECTOR, ".isMinMaxOption:nth-child(3) > div:nth-child(2) .quantity-operator:nth-child(3)")
        self.driver.execute_script("arguments[0].click();", elem)
        #1 Tender
        elem = self.driver.find_element(By.CSS_SELECTOR, ".isMinMaxOption:nth-child(3) > div:nth-child(3) .quantity-operator:nth-child(3)")
        self.driver.execute_script("arguments[0].click();", elem)  
        
        # (2) Elige el tamaño de la papa cajún
        #Elegimos la Papa Cajún Familiar + S/5.00
        elem = self.driver.find_element(By.CSS_SELECTOR, ".selection-block-area:nth-child(2) .radio-selecction-w:nth-child(3) .fkcbxcircle")
        self.driver.execute_script("arguments[0].click();", elem)  
       
        # (3) Elige el sabor de tu bebida (Obligatorio)
        #Selecionamos Inca Kola Sin Azúcar 500ml        
        elem = self.driver.find_element(By.CSS_SELECTOR, ".selection-block-area:nth-child(3) .radio-selecction-w:nth-child(4) .fkcbxcircle")
        self.driver.execute_script("arguments[0].click();", elem)  
        
        #Scroll Down 
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        
        # (4) ¿Deseas salsas extras? (Opcional)
        #Seleccionamos 1 de cada una
        #Ají + S/0.30 
        elem = self.driver.find_element(By.CSS_SELECTOR, ".selection-block-area:nth-child(4) .isMinMaxOption > div:nth-child(1) .quantity-operator:nth-child(3)")
        self.driver.execute_script("arguments[0].click();", elem)
        #Ketchup + S/0.30 
        elem = self.driver.find_element(By.CSS_SELECTOR, ".selection-block-area:nth-child(4) .isMinMaxOption > div:nth-child(2) .quantity-operator:nth-child(3)")
        self.driver.execute_script("arguments[0].click();", elem)
        #Mayonesa + S/0.30 
        elem = self.driver.find_element(By.CSS_SELECTOR, ".selection-block-area:nth-child(4) .isMinMaxOption > div:nth-child(3) .quantity-operator:nth-child(3)")
        self.driver.execute_script("arguments[0].click();", elem)
        #Mostaza + S/0.30 
        elem = self.driver.find_element(By.CSS_SELECTOR, ".selection-block-area:nth-child(4) .isMinMaxOption > div:nth-child(4) .quantity-operator:nth-child(3)")
        self.driver.execute_script("arguments[0].click();", elem)
        
        #Validar monto
        elem = self.driver.find_element(By.CSS_SELECTOR, ".button-price > p")
        self.assertEqual(elem.text,"S/ 24.10","El monto total del producto no corresponde, debería ser S/ 24.10")
        
        #Agregar al carrito button 
        elem = self.driver.find_element(By.XPATH, "//button[contains(text(),'AGREGAR AL CARRITO')]")
        self.driver.execute_script("arguments[0].click();", elem)
        
        #Validar mensaje
        #Acabas de agregar
        #sleep(6)
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, ".section-img-information > div.information > h4:nth-child(1)"))
            WebDriverWait(self.driver, 20).until(element_present)
            elem = self.driver.find_element(By.CSS_SELECTOR,'.section-img-information > div.information > h4:nth-child(1)')  
            self.assertEqual(elem.text,"Acabas de agregar","Ocurrió un problema al agregar el producto al carrito")
        except TimeoutException:        
            self.assertTrue(self.is_element_present(By.CSS_SELECTOR,'.section-img-information > div.information > h4:nth-child(1)'),'Ocurrió un problema al confirmar el mensaje de producto agregado')
        
        sleep(2)
    
    def test_07_purchase_bag_cash(self):
        self.test_06_purchase_product()
        #Click en Finalizar tu compra 
        #elem = self.driver.find_element(By.XPATH, "//button[contains(text(),'FINALIZAR TU COMPRA')]")
        #self.driver.execute_script("arguments[0].click();", elem)
        elem = self.driver.find_element(By.CSS_SELECTOR, ".btn.line-orange")
        elem.click()
        #Click en ir a Pagar
        try:
            element_present = EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-pay"))
            WebDriverWait(self.driver, 10).until(element_present)
            elem = self.driver.find_element(By.CSS_SELECTOR,'.btn-pay')  
            elem.click()
        except TimeoutException:        
            self.assertTrue(self.is_element_present(By.CSS_SELECTOR,'.btn-pay'),'Ocurrió un problema al dar click en ir a pagar')
        
        #elem = self.driver.find_element(By.CSS_SELECTOR, ".btn-pay")
        #elem.click()
        #Ingreso de monto para pago en efectivo 
        sleep(2)
        elem = self.driver.find_element(By.CSS_SELECTOR,".icon-pay > input") 
        elem.send_keys("25")       
        #Seleccionar Acepto terminos y condiciones
        elem = self.driver.find_element(By.ID, "terminosCondiciones")
        elem.click()
        #Finalizar compra
        elem = self.driver.find_element(By.CSS_SELECTOR, ".large.orange.onestepcheckout-button")
        elem.click()
        #Validar mensaje
        elem = self.driver.find_element(By.CSS_SELECTOR, ".content-main > h1:nth-child(1)")
        self.assertEqual(elem.text,"Acabas de agregar","¡FELICIDADES ARTURO!")
        sleep(5)
    
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
    #Run allure report of this file, export report to PJ/Reports
    #pytest.main(['-s', '-q','--alluredir','D://','Unittest.py'])
    #Open allue report via browser
    #subprocess.run([r'powershell.exe', r'allure ' + 'serve ' + 'C://'])
    #unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='C:/Users/artur/Desktop/Python/Python/PopeyesPruebas/UnitTest'))
    #unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='UnitTest'))
