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
class PS(unittest.TestCase):
    @classmethod
    def setUp(inst):
        with allure.step(u"Iniciar el controlador de Chrome"):
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            inst.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
            inst.driver.maximize_window()
            inst.driver.implicitly_wait(15)

    @allure.title(u"PageSpeed cuenta nativa")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description(u"Se requiere fotos de page speed")
    @allure.story(u'Page speed')
    def test_01_speed(self):
        with allure.step(u"Accedemos a la página de pagespeed"):
            sleep(2)
            self.driver.get("https://pagespeed.web.dev/")
        with allure.step(u"Ingresamos la pagina a probar"):
            sleep(2)
            elem = self.driver.find_element(By.ID,"i2")
            elem.send_keys("https://www.popeyes.com.pe/customer/account/login")
            elem.send_keys(Keys.ENTER)    
        with allure.step(u"Mobile"):
            selector = "lh-score__gauge .lh-gauge__wrapper"
            try:
                element_present = EC.visibility_of_element_located((By.CSS_SELECTOR, "a.lh-calclink"))
                WebDriverWait(self.driver, 100).until(element_present)
                sleep(2)
                self.driver.execute_script("window.scrollTo(0,1000)")
                self.screenshot("Mobile")
                elem = self.driver.find_element(By.CSS_SELECTOR, selector+" .lh-gauge__percentage")
                print("Mobile: "+elem.text)
            except TimeoutException:
                print ("No se logró cargar el Mobile") 
        
        with allure.step(u"Desktop"):
            selector = ".google-material-icons.VfPpkd-cfyjzb"
            selector2 = ".lh-gauge__wrapper.lh-gauge__wrapper--pass"
            #Button
            elem = self.driver.find_elements(By.CSS_SELECTOR, selector)[1]
            elem.click()
            try:
                element_present = EC.presence_of_element_located((By.CSS_SELECTOR, selector2))
                WebDriverWait(self.driver, 100).until(element_present)
                self.screenshot("Desktop")
                elem = self.driver.find_element(By.CSS_SELECTOR, selector2+".lh-gauge__percentage")
                print("Desktop: "+elem.text)
            except TimeoutException:
                print ("No se logró cargar el Desktop") 
     
    @classmethod
    def tearDown(inst):
        inst.driver.quit()
    
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
