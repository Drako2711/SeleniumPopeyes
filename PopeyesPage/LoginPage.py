import unittest, allure
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from ..credenciales import PopeyeAccounts
class LoginPg(unittest.TestCase):
    def __init__(self, driver):
        self.driver = driver
    #Login
    def loginNative(self):
        account = PopeyeAccounts.default_account()
        
        user = self.driver.find_element(By.CSS_SELECTOR,"#__layout > div > div.page-wrapper > div.page-content-wrapper > div > div > div > form > div > div:nth-child(1) > input[type=email]")
        if user is not None:
            user.send_keys(account["user"])
        password = self.driver.find_element(By.ID,"input-password")
        if password is not None:
            password.send_keys(account["password"])
            password.send_keys(Keys.ENTER)  
            
    def loginFacebook(self):
        account = PopeyeAccounts.facebook_account()
        
        user = self.driver.find_element(By.ID, "email")
        if user is not None:
            self.screenshot("SS_window_Facebook")
            user.send_keys(account["user"])
        try:
            element_present = EC.presence_of_element_located((By.ID, "pass"))
            WebDriverWait(self.driver, 30).until(element_present)
        except TimeoutException:
            print ("No se logró cargar el input de contraseña de Facebook")
        password = self.driver.find_element(By.ID, "pass")
        if password is not None:
            password.send_keys(account["password"])     
            self.screenshot("SS_creedenciales_Facebook")
            password.send_keys(Keys.ENTER)    
         
    def loginGoogle(self,type):
        selectorEmail = ""
        selectorPassword = ""
        if type == "serve":
            selectorEmail = "#Email"
            selectorPassword = "input[type=password]"
        else:
            selectorEmail = "#identifierId"
            selectorPassword = "input[name=password]"
            
        account = PopeyeAccounts.google_account()        
        self.screenshot("SS_abrir google") 
        #Esperamos a que cargue el botón de iniciar sesión
        try:
            element_present = EC.element_to_be_clickable((By.CSS_SELECTOR, selectorEmail))
            WebDriverWait(self.driver, 30).until(element_present)
        except TimeoutException:
            print ("Se agotó el tiempo de espera para cargar la página")            
        user = self.driver.find_element(By.CSS_SELECTOR, selectorEmail)
        if user is not None:
            user.send_keys(account["user"])
            self.screenshot("SS_creedenciales_Google_01")
            sleep(1)
            user.send_keys(Keys.ENTER)
        try:
            element_present = EC.element_to_be_clickable((By.CSS_SELECTOR, selectorPassword))
            WebDriverWait(self.driver, 30).until(element_present)
        except TimeoutException:
            print ("Se agotó el tiempo de espera para cargar la página")            
        password = self.driver.find_element(By.CSS_SELECTOR, selectorPassword)
        if password is not None:
            password.send_keys(account["password"])
            self.screenshot("SS_creedenciales_Google_02")  
            sleep(1)
            password.send_keys(Keys.ENTER)
    
    #Commom Login
    def navToLogin(self):
        self.driver.get("https://ppys-dev.jnq.io/customer/account/login")
    
    def loginValidate(self,type):
        self.screenshot("SS_login_validate_"+type)
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
            elem = self.driver.find_element(By.CSS_SELECTOR,".btn.btn-acepta")
            self.driver.execute_script("arguments[0].click();", elem)
            self.screenshot("cookies nias")
        except:
            print("No se encontró el botón de cookies")
        try:     
            elem = self.driver.find_element(By.CSS_SELECTOR,"button.align-right.primary.slidedown-button")
            self.driver.execute_script("arguments[0].click();", elem)
        except:
            print("No se encontró el botón de suscripción")
        
    def openWindow(self,window):
        if(window == "facebook"):
            element_present = EC.element_to_be_clickable((By.CSS_SELECTOR, "div.btn-fb"))
            WebDriverWait(self.driver, 30).until(element_present)
            elem = self.driver.find_element(By.CSS_SELECTOR,"div.btn-fb")
            self.driver.execute_script("arguments[0].click();", elem)
        else:
            element_present = EC.element_to_be_clickable((By.ID, "google-signin-btn-0"))
            WebDriverWait(self.driver, 30).until(element_present)
            elem = self.driver.find_element(By.ID,"google-signin-btn-0")
            self.driver.execute_script("arguments[0].click();", elem)
        try:
            WebDriverWait(self.driver, 30).until(EC.number_of_windows_to_be(2))
        except TimeoutException:
            assert False, f"No se logró cargar la página de {window}"            
    
    def switchPage(self, window):
        self.driver.switch_to.window(self.driver.window_handles[window])
    
    #Confirm Address
    def selectAddress(self,order):
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, "div.input-box-old.address-item"))
            WebDriverWait(self.driver, 30).until(element_present)
        except TimeoutException:
            assert False, f"No se encontró la dirección número {order-1}"   
        address = self.driver.find_elements(By.CSS_SELECTOR,'div.input-box-old.address-item')
        if address is not None:
            address[order-1].click()
            
    def confirmAddress(self):
        confirmButton = self.driver.find_element(By.XPATH,'//button[contains(text(),"CONFIRMAR")]') 
        if confirmButton is not None:
            self.driver.execute_script("arguments[0].click();", confirmButton)
        
    #New Address
    def clickAddAddress(self):
        btnAddAddress = self.driver.find_element(By.XPATH,'//button[contains(text(),"NUEVA DIRECCIÓN")]') 
        if btnAddAddress is not None:
            self.driver.execute_script("arguments[0].click();", btnAddAddress)
    
    def searchAddress(self,address):
        inputNewAddress = self.driver.find_element(By.ID,'mi_ubicacion') 
        if inputNewAddress is not None:            
            inputNewAddress.send_keys(address)       
            sleep(1.5)
            inputNewAddress.send_keys(Keys.ENTER)      
        #selecciona el primer item de la busqueda   
        elemAddress = self.driver.find_element(By.CLASS_NAME,'pac-item') 
        elemAddress.click()          
    
    def addDataAddress(self,type,phone,reference,savehow,promo,default,mznlt):        
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, "select"))
            WebDriverWait(self.driver, 30).until(element_present)
        except TimeoutException:
            print ("Se agotó el tiempo de espera para cargar la página")
        
        inputType = Select(self.driver.find_element(By.CSS_SELECTOR,'select'))
        inputType.select_by_visible_text(type) #Casa, Condominio, Departamento, Empresa, Hotel, Hospital
        
        inputPhone = self.driver.find_element(By.CSS_SELECTOR, ".phone > input")
        inputPhone.send_keys(phone)
        
        inputReference = self.driver.find_element(By.CSS_SELECTOR, ".reference > input")
        inputReference.send_keys(reference)
        
        if mznlt:             
            btnMznLt = self.driver.find_element(By.ID, "mz-ipt")
            btnMznLt.click()    
            inputMzn = self.driver.find_element(By.CSS_SELECTOR, ".info-item:nth-child(1) input")
            inputMzn.send_keys("1")
            inputLt = self.driver.find_element(By.CSS_SELECTOR, ".info-item:nth-child(2) input")
            inputLt.send_keys("2")
        
        if savehow == "Casa":
            inputSaveHow = self.driver.find_element(By.ID,'home')
            inputSaveHow.click()
        elif savehow == "Oficina":
            inputSaveHow = self.driver.find_element(By.ID,'oficina')
            inputSaveHow.click()
        elif savehow == "Novios":
            inputSaveHow = self.driver.find_element(By.ID,'novios')
            inputSaveHow.click()
        else:
            btnOtro = self.driver.find_element(By.CSS_SELECTOR, "#otro > img")
            btnOtro.click()  
            inputOtro = self.driver.find_element(By.CSS_SELECTOR, ".input-wrapper:nth-child(3) > input")
            inputOtro.send_keys(savehow)  
                    
        if promo:
            checkPromo = self.driver.find_element(By.CSS_SELECTOR, "label:nth-child(1) > input")
            checkPromo.click()
        if default:
            checkDefault = self.driver.find_element(By.CSS_SELECTOR, "label:nth-child(2) > input")
            checkDefault.click()
        
        btnConfirm = self.driver.find_element(By.CSS_SELECTOR,'div.content-btn > button')         
        btnConfirm.click()
        
    #Pick Up Address
    def selectPickUp(self):
        btnPickUp = self.driver.find_elements(By.CSS_SELECTOR,'div.button-delivery')[1]
        btnPickUp.click()
    
    def selectStore(self,store):
        #Seleccionar el item del local 
        self.screenshot("SS_locales")
        try:
            element_present = EC.visibility_of_element_located((By.XPATH,f'//h4[contains(text(),"{store}")]'))
            WebDriverWait(self.driver, 30).until(element_present)
        except TimeoutException:
            self.screenshot("SS_error_locales")
            assert False, f"No se lograron cargar los locales"   
        store = self.driver.find_element(By.XPATH,f'//h4[contains(text(),"{store}")]')
        self.driver.execute_script("arguments[0].click();", store)
    
    def confirmStore(self):
        btnConfirmStore = self.driver.find_element(By.XPATH,'//button[contains(text(),"CONFIRMAR")]') 
        btnConfirmStore.click()
        
    def validateStore(self):
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, "div.store-name > p"))
            WebDriverWait(self.driver, 5).until(element_present)
            elem = self.driver.find_element(By.CSS_SELECTOR,'div.store-name > p')  
            self.screenshot("Seleccionar local")
            self.assertTrue(elem.text == "CENTRO CIVICO","No se seleccionó el local esperado")
        except TimeoutException:        
            self.screenshot("Error en la selección de local")
            assert False, "Ocurrió un error al confirmar el local, posiblemente no esté disponible"
        
    #Commmon Address
    def validateAddress(self,msg):
        if(msg == "confirm"):
            msgError = 'Ocurrió un problema al confirmar el mensaje dirección correctamente configurada'
            selectorPath = '//p[contains(text(),"Tu dirección ha sido configurada correctamente.")]'
            try:
                element_present = EC.presence_of_element_located((By.XPATH, selectorPath))
                WebDriverWait(self.driver, 20).until(element_present) 
                self.assertTrue(self.is_element_present(By.XPATH, selectorPath),msgError)  
            except TimeoutException:        
                assert False, msgError
        else:
            msgError = 'Ocurrió un problema al confirmar el mensaje dirección guardada correctamente'
            selectorPath = '//p[contains(text(),"Tu dirección ha sido guardada correctamente.")]'
            try:
                element_present = EC.presence_of_element_located((By.XPATH, selectorPath))
                WebDriverWait(self.driver, 20).until(element_present) 
                self.assertTrue(self.is_element_present(By.XPATH, selectorPath),msgError)  
            except TimeoutException:        
                assert False, msgError          
    
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
    
    