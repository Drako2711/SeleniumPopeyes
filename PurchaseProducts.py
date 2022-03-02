from time import sleep
#Unittest
import unittest, allure, math
#Selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
#Service
from selenium.webdriver.chrome.service import Service
#Driver
from webdriver_manager.chrome import ChromeDriverManager
#Credenciales
from credenciales import PopeyeAccounts
#Otros
import sys, os, pytest, subprocess

@allure.feature(u'Purchase') 
class Purchase(unittest.TestCase):
    skip = True
    @classmethod
    def setUp(inst):
        with allure.step(u"Iniciar el controlador de Chrome"):
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            #inst.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
            inst.driver = webdriver.Chrome(service=Service("D:\\PROYECTOS CICLO IX\\SELENIUM\\Drivers\\chromedriver.exe"),options=options)
            inst.driver.maximize_window()
            inst.driver.implicitly_wait(15)
        
    def test_01_login(self):        
        if self.skip: self.skipTest("Ya realizado en test login")    
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
    
    def test_02_login_confirm(self):
        if self.skip: self.skipTest("Ya realizado en test login")    
        self.test_01_login()
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
            try:
                element_present = EC.presence_of_element_located((By.XPATH, '//p[contains(text(),"Tu dirección ha sido configurada correctamente.")]'))
                WebDriverWait(self.driver, 25).until(element_present) 
                self.assertTrue(self.is_element_present(By.XPATH,'//p[contains(text(),"Tu dirección ha sido configurada correctamente.")]'))  
            except TimeoutException:        
                self.assertTrue(self.is_element_present(By.XPATH,'//p[contains(text(),"Tu dirección ha sido configurada correctamente.")]'),'Ocurrió un problema al confirmar el mensaje dirección correctamente configurada')
    
    @allure.title(u"Agregar un producto al carrito")    
    @allure.description(u"Se requiere agregar un producto a un carrito en este caso el Cajun Full")
    @allure.story(u'Compra de un producto')
    def test_03_purchase_product(self):
        #Login   
        self.skip = False
        self.test_02_login_confirm()
        self.skip = True
        with allure.step(u"Nos dirigimos al home"):
            self.driver.get("https://ppys-dev.jnq.io/")
        with allure.step(u"Seleccionamos personales y para compartir"):        
            elem = self.driver.find_element(By.XPATH,'//h4[contains(text(),"Personales y para compartir")]')
            self.driver.execute_script("arguments[0].click();", elem)
        with allure.step(u"Seleccionamos el segundo producto (Cajun Full)"):        
            elem = self.driver.find_element(By.CSS_SELECTOR,'.product-card:nth-child(2) .btn')
            self.driver.execute_script("arguments[0].click();", elem)
        with allure.step(u"Eligimos las piezas"):  
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
        with allure.step(u"Elegimos el tamaño"):      
            # (2) Elige el tamaño de la papa cajún
            #Elegimos la Papa Cajún Familiar + S/5.00
            elem = self.driver.find_element(By.CSS_SELECTOR, ".selection-block-area:nth-child(2) .radio-selecction-w:nth-child(3) .fkcbxcircle")
            self.driver.execute_script("arguments[0].click();", elem)  
        with allure.step(u"Eligimos el sabor de bebida"):  
            # (3) Elige el sabor de tu bebida (Obligatorio)
            #Selecionamos Inca Kola Sin Azúcar 500ml        
            elem = self.driver.find_element(By.CSS_SELECTOR, ".selection-block-area:nth-child(3) .radio-selecction-w:nth-child(4) .fkcbxcircle")
            self.driver.execute_script("arguments[0].click();", elem)          
            #Scroll Down 
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        with allure.step(u"Eligimos las salsas"):  
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
        with allure.step(u"Validamos el monto"):  
            #Validar monto
            elem = self.driver.find_element(By.CSS_SELECTOR, ".button-price > p")
            self.assertEqual(elem.text,"S/ 24.10","El monto total del producto no corresponde, debería ser S/ 24.10")
        with allure.step(u"Agregamos al carrito"):  
            #Agregar al carrito button 
            elem = self.driver.find_element(By.XPATH, "//button[contains(text(),'AGREGAR AL CARRITO')]")
            self.driver.execute_script("arguments[0].click();", elem)        
        with allure.step(u"Validamos que se agregó correctamente"):  
            #Validar mensaje
            try:
                element_present = EC.element_to_be_clickable((By.CSS_SELECTOR, ".section-img-information > div.information > h4:nth-child(1)"))
                WebDriverWait(self.driver, 25).until(element_present)
                elem = self.driver.find_element(By.CSS_SELECTOR,'.section-img-information > div.information > h4:nth-child(1)')  
                self.assertEqual(elem.text,"Acabas de agregar","Ocurrió un problema al agregar el producto al carrito")
            except TimeoutException:        
                self.assertTrue(self.is_element_present(By.CSS_SELECTOR,'.section-img-information > div.information > h4:nth-child(1)'),'Ocurrió un problema al confirmar el mensaje de producto agregado')
    
    @allure.title(u"Pagar el producto del carrito con efectivo")
    @allure.description(u"Se requiere pagar el producto que está en el carrito con un monto de 25 en efectivo")
    @allure.story(u'Compra de un producto')
    def test_04_purchase_bag_cash(self):
        self.test_03_purchase_product()
        with allure.step(u"Finalizamos la compra"):  
            #Click en Finalizar tu compra 
            elem = self.driver.find_element(By.CSS_SELECTOR, ".btn.line-orange")
            elem.click()
        with allure.step(u"Elegimos el botón de pagar"):  
            #Click en ir a Pagar
            try:
                element_present = EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-pay"))
                WebDriverWait(self.driver, 15).until(element_present)
                elem = self.driver.find_element(By.CSS_SELECTOR,'.btn-pay')  
                elem.click()
            except TimeoutException:        
                self.assertTrue(self.is_element_present(By.CSS_SELECTOR,'.btn-pay'),'Ocurrió un problema al dar click en ir a pagar')
        with allure.step(u"Ingresamos el monto"):  
            elem = self.driver.find_element(By.CSS_SELECTOR,".price-total td:nth-child(2) h3") 
            monto = elem.text[3:]       
            elem = self.driver.find_element(By.CSS_SELECTOR,".icon-pay > input") 
            elem.send_keys(math.ceil(float(monto)))       
        with allure.step(u"Aceptamos los términos y condiciones"): 
            #Seleccionar Acepto terminos y condiciones
            elem = self.driver.find_element(By.ID, "terminosCondiciones")
            elem.click()
        with allure.step(u"Finalizamos la compra"):  
            try:
                element_present = EC.element_to_be_clickable((By.CSS_SELECTOR, ".onestepcheckout-button"))
                WebDriverWait(self.driver, 15).until(element_present)
                elem = self.driver.find_element(By.CSS_SELECTOR,'.onestepcheckout-button')  
                elem.click()
            except TimeoutException:        
                self.assertTrue(self.is_element_present(By.CSS_SELECTOR,'.onestepcheckout-button'),'Ocurrió un problema al dar click en finalizar compra')
        with allure.step(u"Validamos la compra exitosa"):  
            #Validar mensaje
            try:
                element_present = EC.element_to_be_clickable((By.CSS_SELECTOR, ".content-main > h1:nth-child(1)"))
                WebDriverWait(self.driver, 15).until(element_present)
                self.screenshot("Compra exitosa")
                elem = self.driver.find_element(By.CSS_SELECTOR,'.content-main > h1:nth-child(1)')  
                self.assertEqual(elem.text,"¡FELICIDADES !","No se encontró el texto")
            except TimeoutException:        
                self.assertTrue(self.is_element_present(By.CSS_SELECTOR,'.content-main > h1:nth-child(1)'),'Ocurrió un problema al dar click en finalizar compra')        

    def test_05_purchase_bag_online(self):
        self.test_03_purchase_product()
        with allure.step(u"Finalizamos la compra"):  
            elem = self.driver.find_element(By.CSS_SELECTOR, ".btn.line-orange")
            elem.click()
        with allure.step(u"Elegimos el botón de pagar"):  
            try:
                element_present = EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-pay"))
                WebDriverWait(self.driver, 15).until(element_present)
                elem = self.driver.find_element(By.CSS_SELECTOR,'.btn-pay')  
                elem.click()
            except TimeoutException:        
                self.assertTrue(self.is_element_present(By.CSS_SELECTOR,'.btn-pay'),'Ocurrió un problema al dar click en ir a pagar')
        with allure.step(u"Seleccionamos el método de pago online"):  
            elem = self.driver.find_element(By.CSS_SELECTOR,".input-buy > .btn")
            elem.click()
            elem = self.driver.find_element(By.CSS_SELECTOR,".list-methods .method-item:nth-child(2)")
            elem.click()
        with allure.step(u"Aceptamos los términos y condiciones"): 
            elem = self.driver.find_element(By.ID, "terminosCondiciones")
            self.driver.execute_script("arguments[0].click();", elem) 
        with allure.step(u"Confirmamos con el botón de finalizar compra"):  
            try:
                element_present = EC.element_to_be_clickable((By.CSS_SELECTOR, ".onestepcheckout-button"))
                WebDriverWait(self.driver, 15).until(element_present)
                elem = self.driver.find_element(By.CSS_SELECTOR,'.onestepcheckout-button')  
                elem.click()
            except TimeoutException:        
                self.assertTrue(self.is_element_present(By.CSS_SELECTOR,'.onestepcheckout-button'),'Ocurrió un problema al dar click en finalizar compra')
        with allure.step(u"Seleccionamos tarjeta de crédito"):  
            self.driver.switch_to.frame(0)
            self.driver.find_element(By.CSS_SELECTOR, ".radio:nth-child(2)")
            elem.click()
            #elem = self.driver.find_element(By.ID,"pm001")
            #elem.click()
            elem = self.driver.find_element(By.ID,"payment-continue")
            elem.click()
        with allure.step(u"Ingresamos los datos de la tarjeta de prueba"):  
            elem = self.driver.find_element(By.ID,"number")
            elem.send_keys("4474118355632240")
            elem = self.driver.find_element(By.ID,"expiry")
            elem.send_keys("03/2022	")
            elem = self.driver.find_element(By.ID,"cvc")
            elem.send_keys("111")
            elem = self.driver.find_element(By.ID,"email")
            elem.send_keys("janaq.test22@yopmail.com")
            elem = self.driver.find_element(By.ID,"city")
            elem.send_keys("Lima")
            elem = self.driver.find_element(By.ID,"country")
            elem.send_keys("Peru")
            elem.send_keys(Keys.ENTER)
        with allure.step(u"Validamos la compra exitosa"):  
            try:
                element_present = EC.element_to_be_clickable((By.CSS_SELECTOR, ".content-main > h1:nth-child(1)"))
                WebDriverWait(self.driver, 15).until(element_present)
                self.screenshot("Compra exitosa")
                elem = self.driver.find_element(By.CSS_SELECTOR,'.content-main > h1:nth-child(1)')  
                self.assertEqual(elem.text,"¡FELICIDADES !","No se encontró el texto")
            except TimeoutException:        
                self.assertTrue(self.is_element_present(By.CSS_SELECTOR,'.content-main > h1:nth-child(1)'),'Ocurrió un problema al dar click en finalizar compra')        
        
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
    #unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='C:/Users/artur/Desktop/Python/Python/PopeyesPruebas/UnitTest'))
    #unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='UnitTest'))