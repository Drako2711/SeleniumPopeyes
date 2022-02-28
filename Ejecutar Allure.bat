echo. ################################# PRUEBAS #################################

python -m pytest UnitTest.py --alluredir ./results
allure serve ./results/

pause