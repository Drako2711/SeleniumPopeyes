import unittest
import HtmlTestRunner
import os
from Login import LoginAccount
from PurchaseProducts import Purchase
  
# obtener la ruta del directorio al archivo de informe de salida
dir = os.getcwd()
 
# se obtienen los test desde SearchText y la clase HomePageTest 
login = unittest.TestLoader().loadTestsFromTestCase(LoginAccount)
purchase = unittest.TestLoader().loadTestsFromTestCase(Purchase)
 
# se crea el pack de test combinando con search_text and home_page_test
test_suite = unittest.TestSuite([login,purchase])
 
# abre el archivo de reporte
outfile = open(dir + "\SeleniumPythonTestSummary.html", "w")
 
# configura las opciones de HTMLTestRunner 
#runner = HtmlTestRunner.HtmlTestRunner(stream=outfile,title='Test Report', description='Acceptance Tests')
runner = HtmlTestRunner.HTMLTestRunner(output='Testplan')
 
# ejecuta la suite usando HTMLTestRunner
runner.run(test_suite)