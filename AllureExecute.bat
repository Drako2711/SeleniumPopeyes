echo. ################################# PRUEBAS #################################

python -m pytest Login.py PurchaseProducts.py --alluredir ./results

allure serve ./results/

pause