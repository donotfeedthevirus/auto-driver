from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time, random

class AutoDriverRobot():
    def __init__(self, username, password):
        # service = Service(GeckoDriverManager().install())
        # self.driver = webdriver.Firefox(service=service)
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 100)
        self.username = username
        self.password = password

    def login(self):
        self.driver.get("https://dataclose.pro")
        self.wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(self.username)
        time.sleep(5)
        self.driver.find_element(By.NAME, "password").send_keys(self.password)
        time.sleep(5)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(20)

    def wait_popup(self, retries=3):
        status_element = self.driver.find_elements(By.CSS_SELECTOR, "div[role='status']")
        if status_element:
            popup_text = status_element[0].text
            if "Nenhum resultado recebido do provedor." in popup_text:
                if retries > 0:
                    print(f"Aviso detectado. Esperando 100 segundos para tentar novamente. {retries} tentativas restantes.")
                    time.sleep(100)
                    return True
                else: 
                    raise Exception("Máximo de tentativas alcançado.")
        return False

    def search_by_cnh(self, cnh, retries=3):
        self.driver.get("https://dataclose.pro/modules/100")
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-key='register']"))).click()
        self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Digite o REGISTRO do condutor que deseja consultar!']").send_keys(cnh)
        time.sleep(5)
        self.driver.find_element(By.XPATH, "//button[normalize-space()='Consultar']").click()
        time.sleep(2)
        if self.wait_popup(retries):
            return self.search_by_cnh(cnh, retries - 1)
        name = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "(//div[contains(@class, 'border-foreground-200')])[4]"))).text.removeprefix("NOME\n")
        cpf = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "(//div[contains(@class, 'border-foreground-200')])[11]"))).text.removeprefix("CPF\n").replace(".", "").replace("-", "")
        return name, cpf

    def search_by_cpf(self, cpf, retries=3):
        self.driver.get("https://dataclose.pro/modules/108")
        cpf_input = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[placeholder='Insira o CPF que deseja consultar!']")))
        cpf_input.click()
        cpf_input.send_keys(cpf)
        time.sleep(5)
        self.driver.find_element(By.XPATH, "//button[normalize-space()='Consultar']").click()
        time.sleep(2)
        if self.wait_popup(retries):
            return self.search_by_cpf(cpf, retries - 1)
        numbers = self.wait.until(EC.presence_of_element_located((
            By.XPATH, "//div[div[p[normalize-space()='TELEFONES']]]//table//tbody/tr[1]/td[1]//span"
        ))).text
        return numbers

    def close(self):
        self.driver.close()