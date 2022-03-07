from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from ..credenciales import PopeyeAccounts
import unittest
class Login(unittest.TestCase):
    def __init__(self, driver):
        self.driver = driver

    def navToLogin(self):
        self.driver.get("https://ppys-dev.jnq.io/customer/account/login")
    
    def switchPage(self, window):
        self.driver.switch_to.window(self.driver.window_handles[window])
        
    def loginNative(self):
        account = PopeyeAccounts.default_account()
        
        user = self.driver.find_element(By.CSS_SELECTOR,"#__layout > div > div.page-wrapper > div.page-content-wrapper > div > div > div > form > div > div:nth-child(1) > input[type=email]")
        if user is not None:
            user.send_keys(account["user"])
        password = self.driver.find_element(By.ID,"input-password")
        if password is not None:
            password.send_keys(account["password"])
            password.send_keys(Keys.ENTER)  
            
    def loginValidate(self,type):
        #Verificamos si el logeo es correcto
        if (type == "native"):   
            self.assertTrue(self.is_element_present(By.XPATH,'//p[contains(text(),"¡Bienvenido! Gracias por iniciar sesión en Popeyes.")]'),"Ocurrió un error al intentar ingresar con la cuenta Nativa")          
        elif(type == "facebook"):
            self.assertTrue(self.is_element_present(By.XPATH,'//p[contains(text(),"¡Bienvenido! Gracias por iniciar sesión con tu cuenta de Facebook en Popeyes.")]'),"Ocurrió un error al intentar ingresar con la cuenta de Facebook")          
        else:
            self.assertTrue(self.is_element_present(By.XPATH,'//p[contains(text(),"¡Bienvenido! Gracias por iniciar sesión con tu cuenta de Google en Popeyes.")]'),"Ocurrió un error al intentar ingresar con la cuenta de Google")   
        
        self.acceptCookies()                
    
    def acceptCookies(self):
        #Aceptar cookies y seleccionar later en suscribir
        try: 
            self.driver.find_element(By.CSS_SELECTOR,".btn.btn-acepta").click()
            self.driver.find_element(By.CSS_SELECTOR,"#onesignal-slidedown-cancel-button").click()
        except:
            print("No se encontraron los botones de cookies ni de suscripción")
        
    def loginFacebook(self):
        account = PopeyeAccounts.facebook_account()
        
        user = self.driver.find_element(By.ID, "email")
        if user is not None:
            user.send_keys(account["user"])
        try:
            element_present = EC.presence_of_element_located((By.ID, "pass"))
            WebDriverWait(self.driver, 30).until(element_present)
        except TimeoutException:
            print ("No se logró cargar el input de contraseña de Facebook")
        password = self.driver.find_element(By.ID, "pass")
        if password is not None:
            password.send_keys(account["password"])     
            password.send_keys(Keys.ENTER)    
         
    def openWindow(self,window):
        if(window == "facebook"):
            elem = self.driver.find_element(By.CSS_SELECTOR,"div.btn-fb")
            elem.click()
        else:
            elem = self.driver.find_element(By.ID,"google-signin-btn-0")
            elem.click()
        try:
            WebDriverWait(self.driver, 30).until(EC.number_of_windows_to_be(2))
        except TimeoutException:
            assert False, f"No se logró cargar la página de {window}"            
    
    def loginGoogle(self):
        account = PopeyeAccounts.google_account()        
        #Esperamos a que cargue el botón de iniciar sesión
        try:
            element_present = EC.presence_of_element_located((By.ID, "identifierId"))
            WebDriverWait(self.driver, 30).until(element_present)
        except TimeoutException:
            print ("Se agotó el tiempo de espera para cargar la página")            
        user = self.driver.find_element(By.ID, "identifierId")
        if user is not None:
            user.send_keys(account["user"])  
            user.send_keys(Keys.ENTER)  
        try:
            element_present = EC.presence_of_element_located((By.NAME, "password"))
            WebDriverWait(self.driver, 30).until(element_present)
        except TimeoutException:
            print ("Se agotó el tiempo de espera para cargar la página")            
        password = self.driver.find_element(By.NAME, "password")
        if password is not None:
            password.send_keys(account["password"])  
            password.send_keys(Keys.ENTER)
    
    def is_element_present(self, how, what):
        """
        Metodo auxiliar para confirmar la presencia de un elemento en la página
        : param how: por tipo de localizador
        : params what: valor del localizador
        """
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException: return False
        return True
