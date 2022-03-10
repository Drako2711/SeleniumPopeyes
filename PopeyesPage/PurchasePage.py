import unittest, allure, math
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PurchasePg(unittest.TestCase):
    def __init__(self, driver):
        self.driver = driver    
    #Navs
    def navHome(self):
        self.driver.get("https://ppys-dev.jnq.io/")
    
    def navPersonales(self):
        btnPersonales = self.driver.find_element(By.XPATH,'//h4[contains(text(),"Personales y para compartir")]')
        self.driver.execute_script("arguments[0].click();", btnPersonales)
    
    #Cajun Full
    def selectCajunFull(self):
        btnCajunFull = self.driver.find_element(By.CSS_SELECTOR,'.product-card:nth-child(2) .btn')
        self.driver.execute_script("arguments[0].click();", btnCajunFull)
    
    def selectPieces(self):
        # (1) Elige tus piezas (Obligatorio)       
        #1 Tradicional
        btnTradicional = self.driver.find_element(By.CSS_SELECTOR, ".isMinMaxOption:nth-child(3) > div:nth-child(1) .quantity-operator:nth-child(3)")
        self.driver.execute_script("arguments[0].click();", btnTradicional)
        #1 Picantito
        btnPicantito = self.driver.find_element(By.CSS_SELECTOR, ".isMinMaxOption:nth-child(3) > div:nth-child(2) .quantity-operator:nth-child(3)")
        self.driver.execute_script("arguments[0].click();", btnPicantito)
        #1 Tender
        btnTender = self.driver.find_element(By.CSS_SELECTOR, ".isMinMaxOption:nth-child(3) > div:nth-child(3) .quantity-operator:nth-child(3)")
        self.driver.execute_script("arguments[0].click();", btnTender)  
    
    def selectSize(self):
        # (2) Elige el tamaño de la papa cajún
        #Elegimos la Papa Cajún Familiar + S/5.00
        btnSize = self.driver.find_element(By.CSS_SELECTOR, ".selection-block-area:nth-child(2) .radio-selecction-w:nth-child(3) .fkcbxcircle")
        self.driver.execute_script("arguments[0].click();", btnSize)
    
    def selectDrink(self):
        # (3) Elige el sabor de tu bebida (Obligatorio)
        #Selecionamos Inca Kola Sin Azúcar 500ml        
        btnDrink = self.driver.find_element(By.CSS_SELECTOR, ".selection-block-area:nth-child(3) .radio-selecction-w:nth-child(4) .fkcbxcircle")
        self.driver.execute_script("arguments[0].click();", btnDrink)          
        
    def selectSauces(self):
        # (4) ¿Deseas salsas extras? (Opcional)
        #Seleccionamos 1 de cada una
        #Ají + S/0.30 
        btnAji = self.driver.find_element(By.CSS_SELECTOR, ".selection-block-area:nth-child(4) .isMinMaxOption > div:nth-child(1) .quantity-operator:nth-child(3)")
        self.driver.execute_script("arguments[0].click();", btnAji)
        #Ketchup + S/0.30 
        btnKetchup = self.driver.find_element(By.CSS_SELECTOR, ".selection-block-area:nth-child(4) .isMinMaxOption > div:nth-child(2) .quantity-operator:nth-child(3)")
        self.driver.execute_script("arguments[0].click();", btnKetchup)
        #Mayonesa + S/0.30 
        btnMayonesa = self.driver.find_element(By.CSS_SELECTOR, ".selection-block-area:nth-child(4) .isMinMaxOption > div:nth-child(3) .quantity-operator:nth-child(3)")
        self.driver.execute_script("arguments[0].click();", btnMayonesa)
        #Mostaza + S/0.30 
        btnMostaza = self.driver.find_element(By.CSS_SELECTOR, ".selection-block-area:nth-child(4) .isMinMaxOption > div:nth-child(4) .quantity-operator:nth-child(3)")
        self.driver.execute_script("arguments[0].click();", btnMostaza)
    
    def validateAmount(self):
        #Validar monto
        inputAmount = self.driver.find_element(By.CSS_SELECTOR, ".button-price > p")
        self.assertTrue(inputAmount.text == "S/ 24.10","El monto total del producto no corresponde, debería ser S/ 24.10")
    
    def addToCart(self):
        #Agregar al carrito button 
        btnAdd = self.driver.find_element(By.XPATH, "//button[contains(text(),'AGREGAR AL CARRITO')]")
        self.driver.execute_script("arguments[0].click();", btnAdd)      
    
    def validateMsgAdd(self):
        #Validar mensaje
        try:
            element_present = EC.element_to_be_clickable((By.CSS_SELECTOR, ".section-img-information > div.information > h4:nth-child(1)"))
            WebDriverWait(self.driver, 25).until(element_present)
            txtAdd = self.driver.find_element(By.CSS_SELECTOR,'.section-img-information > div.information > h4:nth-child(1)')  
            self.screenshot("Producto Agregado")
            self.assertTrue(txtAdd.text=="Acabas de agregar","Ocurrió un problema al agregar el producto al carrito")
        except TimeoutException:        
            assert False, "Ocurrió un problema al confirmar el mensaje de producto agregado"
    
    #Purchase Common
    def btnFinishPurchase(self):
        #Click en Finalizar tu compra 
        btnFinish = self.driver.find_element(By.CSS_SELECTOR, ".btn.line-orange")
        btnFinish.click()
        
    def clickBtnPay(self):
        #Click en ir a Pagar
        try:
            element_present = EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-pay"))
            WebDriverWait(self.driver, 15).until(element_present)
            btnPay = self.driver.find_element(By.CSS_SELECTOR,'.btn-pay')  
            btnPay.click()
        except TimeoutException:        
            assert False, 'Ocurrió un problema al dar click en ir a pagar'
    
    def acceptTerms(self):
        #Seleccionar Acepto terminos y condiciones
        btnTerms = self.driver.find_element(By.ID, "terminosCondiciones")
        self.driver.execute_script("arguments[0].click();", btnTerms)
    
    #Purchase with cash
    def insertAmount(self):
        txtAmount = self.driver.find_element(By.CSS_SELECTOR,".price-total td:nth-child(2) h3") 
        monto = txtAmount.text[3:]       
        inputAmount = self.driver.find_element(By.CSS_SELECTOR,".icon-pay > input") 
        inputAmount.send_keys(math.ceil(float(monto)))       
    
    def finishPurchase(self):
        try:
            element_present = EC.element_to_be_clickable((By.CSS_SELECTOR, ".onestepcheckout-button"))
            WebDriverWait(self.driver, 15).until(element_present)
            btnFinishPurchase = self.driver.find_element(By.CSS_SELECTOR,'.onestepcheckout-button')  
            btnFinishPurchase.click()
        except TimeoutException:        
            assert False, 'Ocurrió un problema al dar click en finalizar compra'
    
    def validatePaySuccess(self,method):       
        selector = ""
        txtCompare = ""        
        if method == "cash":
            selector = ".content-main > h1:nth-child(1)"
            txtCompare = "¡FELICIDADES !"
        else:
            selector = ".failure-resumen-visa > h3"
            txtCompare = "Resumen:"
            
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, ".content-main > h1:nth-child(1)"))
            WebDriverWait(self.driver, 15).until(element_present)
            self.screenshot("Compra exitosa")
            txtResult = self.driver.find_element(By.CSS_SELECTOR,selector)  
            self.assertTrue(txtResult.text==txtCompare,"No se encontró el texto que verifica la compra")
        except TimeoutException:        
            assert False, 'Ocurrió un problema al finalizar la compra' 
    
    #Purchase with credit card
    def selectMethodCard(self):
        btnChange = self.driver.find_element(By.CSS_SELECTOR,".input-buy > .btn")
        btnChange.click()
        btnMethod = self.driver.find_element(By.CSS_SELECTOR,".list-methods .method-item:nth-child(2)")
        btnMethod.click()
    
    def selectCreditCard(self):
        try:
            element_present = EC.element_located_to_be_selected((By.XPATH, "/html/body/div[3]/iframe"))
            WebDriverWait(self.driver, 25).until(element_present)
            elem = self.driver.find_element(By.CSS_SELECTOR,'.visaNetWrapper > iframe#visaNetJS')
            self.driver.switch_to.frame(elem)
        except TimeoutException:        
            self.assertTrue(self.is_element_present(By.XPATH,'/html/body/div[3]/iframe'),'Ocurrió un problema al cargar el iframe')
        self.driver.switch_to.frame(2)
        radioCard = self.driver.find_element(By.ID,'pm001')  
        radioCard.click()
        btnContinue = self.driver.find_element(By.ID,"payment-continue")
        btnContinue.click()
    
    def insertCardData(self):
        inputNumber = self.driver.find_element(By.ID,"number")
        self.driver.execute_script("arguments[1].value = arguments[0]; ", "4474-1183-5563-2240", inputNumber); 
        inputDate = self.driver.find_element(By.ID,"expiry")            
        self.driver.execute_script("arguments[1].value = arguments[0]; ", "03 / 2022", inputDate); 
        inputCVC = self.driver.find_element(By.ID,"cvc")
        inputCVC.send_keys("111")
        inputEmail = self.driver.find_element(By.ID,"email")
        inputEmail.send_keys("janaq.test22@yopmail.com")
        inputEmail.send_keys(Keys.ENTER)
        ''' elem = self.driver.find_element(By.ID,"city")
        elem.send_keys("Peru")
        elem = self.driver.find_element(By.ID,"country")
        elem.send_keys("Lima") '''
        self.driver.switch_to.default_content()
    
    def is_element_present(self, how, what):
        """
        Metodo auxiliar para confirmar la presencia de un elemento en la página
        : param how: por tipo de localizador
        : params what: valor del localizador
        """
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException: return False
        return True
    
    def scrollDown(self):
        #Scroll Down 
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        
    def screenshot(self,description):
        allure.attach(self.driver.get_screenshot_as_png(), description, attachment_type=allure.attachment_type.PNG)