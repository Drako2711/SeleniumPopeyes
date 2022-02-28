import unittest
import HtmlTestRunner
import os
from UnitTest import Login
from UnitTest2 import Login2
from UnitTest3 import PurchaseProduct
  
# obtener la ruta del directorio al archivo de informe de salida
dir = os.getcwd()
 
# se obtienen los test desde SearchText y la clase HomePageTest 
login1 = unittest.TestLoader().loadTestsFromTestCase(Login)
login2 = unittest.TestLoader().loadTestsFromTestCase(Login2)
purchase = unittest.TestLoader().loadTestsFromTestCase(PurchaseProduct)
 
# se crea el pack de test combinando con search_text and home_page_test
test_suite = unittest.TestSuite([login1,login2,purchase])
 
# abre el archivo de reporte
outfile = open(dir + "\SeleniumPythonTestSummary.html", "w")
 
# configura las opciones de HTMLTestRunner 
#runner = HtmlTestRunner.HtmlTestRunner(stream=outfile,title='Test Report', description='Acceptance Tests')
runner = HtmlTestRunner.HTMLTestRunner(output='Testplan')
 
# ejecuta la suite usando HTMLTestRunner
runner.run(test_suite)