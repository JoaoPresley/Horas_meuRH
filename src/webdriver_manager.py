from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time

class WebDriverManager:
    def __init__(self, config):
        self.config = config
        self.driver = None
        self.wait = None
        self.action = None

    def initialize_driver(self):
        # Assuming chromedriver is in PATH or specify service=Service('/path/to/chromedriver')
        self.driver = webdriver.Chrome()
        self.driver.get(self.config.rh_online_url)
        self.wait = WebDriverWait(self.driver, 10)
        self.action = ActionChains(self.driver)

    def login(self):
        try:
            txt_user = self.wait.until(EC.element_to_be_clickable((By.NAME, "user")))
            txt_password = self.wait.until(EC.element_to_be_clickable((By.NAME, "password")))
            btn_entrar = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "button")))

            self.action.move_to_element(txt_user).click().send_keys(self.config.user_name).perform()
            self.action.move_to_element(txt_password).click().send_keys(self.config.user_password).perform()
            btn_entrar.click()
        except Exception as e:
            print(f"Erro durante o login: {e}")
            self.quit_driver()
            raise

    def navigate_to_time_sheet(self):
        try:
            ponto_menu = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@aria-label, 'Ponto')]")))
            ponto_menu.click()

            espelho_ponto = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), 'Espelho de ponto')]")))
            espelho_ponto.click()

            # Select the previous month's data (this part might need adjustment based on actual HTML structure)
            # The original notebook had a hardcoded date, which is not ideal. 
            # For now, I'll keep a placeholder for selecting a period.
            # A more robust solution would involve dynamically finding the correct option.
            # For demonstration, let's assume we want the first available option that is not the current period.
            # This is a simplification and might need refinement based on the actual website's behavior.
            #time.sleep(self.config.t_wait) # Wait for the page to load periods
            
            # Attempt to select a period. This is highly dependent on the website's structure.
            # The original code selected '16/03/2026'. I'll try to find a similar element.
            # If this fails, it might require manual inspection of the website's HTML.
            try:
                # This XPath is a guess based on the original notebook's intent.
                # It might need to be more generic or specific depending on the actual site.
                data_analisada = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//option[contains(text(), '16/03/2026')]" )))
                data_analisada.click()
            except Exception:
                print("Could not find specific date option '16/03/2026'. Attempting to proceed without explicit selection.")
                # If the specific date is not found, proceed, assuming the default or current period is loaded.

            time.sleep(self.config.t_wait) # Wait for the selected period to load

        except Exception as e:
            print(f"Erro durante a navegação para a página de ponto: {e}")
            self.quit_driver()
            raise

    def get_page_source(self):
        if self.driver:
            return self.driver.page_source
        return None

    def quit_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.wait = None
            self.action = None
