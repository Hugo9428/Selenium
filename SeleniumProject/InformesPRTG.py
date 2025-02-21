from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuración
PRTG_URL = ""  # Reemplazar con la URL de PRTG
USERNAME = ""
PASSWORD = ""
CHROME_DRIVER_PATH = "chromedriver"  # Cambia esto si es necesario

# Inicializar el navegador
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Maximiza la ventana
driver = webdriver.Chrome(options=options)

try:
    # 1️⃣ Ir a la página de login
    driver.get(PRTG_URL)
    
    # 2️⃣ Iniciar sesión
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login_user"))).send_keys(USERNAME)
    driver.find_element(By.ID, "login_password").send_keys(PASSWORD, Keys.RETURN)
    
    # 3️⃣ Esperar a que cargue el dashboard
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mainpage")))

    # 4️⃣ Ir a la sección de informes (Ajusta la ruta según tu interfaz de PRTG)
    driver.get(f"{PRTG_URL}/reports.htm")

    # 5️⃣ Esperar a que cargue la página de informes
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "table")))

    # 6️⃣ Seleccionar el informe deseado (ajusta el índice según el informe específico)
    informes = driver.find_elements(By.CLASS_NAME, "reportitem")
    if informes:
        informes[0].click()  # Selecciona el primer informe (ajusta según sea necesario)

    # 7️⃣ Elegir rango de fechas
    time.sleep(3)
    fecha_inicio = driver.find_element(By.ID, "sdate")
    fecha_fin = driver.find_element(By.ID, "edate")

    # Limpiar y escribir fechas
    fecha_inicio.clear()
    fecha_inicio.send_keys("2024-01-01")  # Modifica según necesites
    fecha_fin.clear()
    fecha_fin.send_keys("2024-01-31")

    # 8️⃣ Descargar informe
    driver.find_element(By.ID, "downloadReportButton").click()
    
    print("✅ Informe generado correctamente")

    # Esperar unos segundos antes de cerrar
    time.sleep(10)

finally:
    driver.quit()  # Cerrar el navegador
