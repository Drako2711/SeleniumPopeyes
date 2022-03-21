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
#Page
from ..PopeyesPage.BasePage import BasePg
from ..PopeyesPage.PurchasePage import PurchasePg
from ..PopeyesPage.LoginPage import LoginPg

@allure.feature(u'Purchase') 
class Purchase(unittest.TestCase):
    skip = True
    @classmethod
    def setUp(inst):
        with allure.step(u"Iniciar el controlador"):
            inst.browser = BasePg.get_option("browser")
            inst.platform = BasePg.get_option("platform")
            inst.display = BasePg.get_option("display")
            print("Browser: "+inst.browser)
            print("Platform: "+inst.platform)
            print("Display: "+inst.display)
            #inst.driver = BasePg.__init__(inst, inst.browser,"desktop","a") #browser,platform,display
            inst.driver = BasePg.__init__(inst, inst.browser,inst.platform,inst.display) #browser,platform,display
            inst.driver.implicitly_wait(20)
            inst.loginPage = LoginPg(inst.driver)
            inst.purchasePage = PurchasePg(inst.driver)
        
    @allure.title(u"Login cuenta nativa")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description(u"Se requiere iniciar sesión con cuenta nativa")
    @allure.story(u'Inicio de sesión')
    def test_01_login(self):        
        if self.skip: self.skipTest("Ya realizado en test login")    
        with allure.step(u"Accedemos a la página de inicio de sesión"):
            self.loginPage.navToLogin()
        
        with allure.step(u"Ingresamos las credenciales de inicio de sesión con cuenta nativa"):
            self.loginPage.loginNative()
        
        with allure.step(u"Validamos el inicio de sesión"):
            self.loginPage.loginValidate("native")  
    
    @allure.title(u"Confirmar dirección") 
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description(u"Se requiere confirmar la primera dirección registrada")
    @allure.story(u'Inicio de sesión')
    def test_02_login_confirm(self):
        if self.skip: self.skipTest("Ya realizado en test login")    
        self.test_01_login()
        sleep(1) #Para que se borre el mensaje de logeo
        with allure.step(u"Seleccionamos la primera dirección"):        
            self.loginPage.selectAddress(1) #Seleccionar primera dirección
        with allure.step(u"Confirmamos la selección"): 
            self.loginPage.confirmAddress()
        with allure.step(u"Validamos la configuración de dirección"):        
            self.loginPage.validateAddress("confirm")
            
    @allure.title(u"Agregar un producto al carrito")    
    @allure.description(u"Se requiere agregar un producto a un carrito en este caso el Cajun Full")
    @allure.story(u'Compra de un producto')
    def test_03_purchase_product(self):
        self.skip = False
        self.test_02_login_confirm()
        self.skip = True
        with allure.step(u"Nos dirigimos al home"):
            self.purchasePage.navHome()
            
        with allure.step(u"Seleccionamos personales y para compartir"):        
            self.purchasePage.navPersonales()
            
        with allure.step(u"Seleccionamos el segundo producto (Cajun Full)"):        
            self.purchasePage.selectCajunFull()  
                                  
        with allure.step(u"Eligimos las piezas"):  
            self.purchasePage.selectPieces()
            
        with allure.step(u"Elegimos el tamaño"):      
            self.purchasePage.selectSize()
            
        with allure.step(u"Eligimos el sabor de bebida"):  
            self.purchasePage.selectDrink()
            self.purchasePage.scrollDown()
            
        with allure.step(u"Eligimos las salsas"):  
            self.purchasePage.selectSauces()            
            
        with allure.step(u"Validamos el monto"):  
            self.purchasePage.validateAmount()
            
        with allure.step(u"Agregamos al carrito"):  
            self.purchasePage.addToCart()            
              
        with allure.step(u"Validamos que se agregó correctamente"):  
            self.purchasePage.validateMsgAdd()            
                   
    @allure.title(u"Pagar el producto del carrito con efectivo")
    @allure.description(u"Se requiere pagar el producto que está en el carrito con un monto de 25 en efectivo")
    @allure.story(u'Compra de un producto')
    def test_04_purchase_bag_cash(self):
        self.test_03_purchase_product()
        with allure.step(u"Finalizamos la compra"):
            self.purchasePage.btnFinishPurchase()
            
        with allure.step(u"Seleccionamos el botón de pagar"):  
            self.purchasePage.clickBtnPay()
            
        with allure.step(u"Ingresamos el monto"):  
            self.purchasePage.insertAmount()            
            
        with allure.step(u"Aceptamos los términos y condiciones"): 
            self.purchasePage.acceptTerms()           
            
        with allure.step(u"Finalizamos la compra"):  
            self.purchasePage.finishPurchase()            
            
        with allure.step(u"Validamos la compra exitosa"):  
            self.purchasePage.validatePaySuccess("cash")            
              
    @allure.title(u"Pagar el producto del carrito con tarjeta")
    @allure.description(u"Se requiere pagar el producto que está en el carrito con una tarjeta")
    @allure.story(u'Compra de un producto')
    def test_05_purchase_bag_online(self):
        self.test_03_purchase_product()
        with allure.step(u"Finalizamos la compra"):  
            self.purchasePage.btnFinishPurchase()
            
        with allure.step(u"Elegimos el botón de pagar"):  
            self.purchasePage.clickBtnPay()
            
        with allure.step(u"Seleccionamos el método de pago online"):  
            self.purchasePage.selectMethodCard()
                        
        with allure.step(u"Aceptamos los términos y condiciones"): 
            self.purchasePage.acceptTerms()
            
        with allure.step(u"Confirmamos con el botón de finalizar compra"):  
            self.purchasePage.finishPurchase()
            
        with allure.step(u"Seleccionamos tarjeta de crédito"):
            self.purchasePage.selectCreditCard()            
            
        with allure.step(u"Ingresamos los datos de la tarjeta de prueba"):  
            self.purchasePage.insertCardData()
            
        with allure.step(u"Validamos la compra exitosa"):  
            self.purchasePage.validatePaySuccess("cc")
                    
        
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