

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException


class SocialShare:
    def __init__(self,page_url):
        # Set up the browser (in this example, we're using Chrome)

        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # self.driver = webdriver.Chrome(options=chrome_options)

        self.driver = webdriver.Chrome()
        # Open the webpage
        self.webpage_url = page_url
        self.driver.get(self.webpage_url)
        self.share_score_class = 'st-label'
        self.facebook_share_url_element_css_selector = 'img[src="https://platform-cdn.sharethis.com/img/facebook.svg"]'

    def getLiveTotalShare(self):
        get_score = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, self.share_score_class)))
        print(get_score.text," total number of share")
        return get_score.text
    
    def getFacebookShareElement(self):
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.facebook_share_url_element_css_selector)))
        return element

    def IncreaseCountShare(self, number):
        i=0
        while i<number:
            try:
                facebook_element = self.getFacebookShareElement()
                facebook_element.click()
                print(f"Clicked {i + 1} times")
                i+=1
            except ElementClickInterceptedException:
                print(f"Element is not clickable, waiting and retrying... ({i + 1}/{number})")
                self.driver.implicitly_wait(2)  # Adjust the wait time as needed
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Additional details:", str(e))
                break
        print("Operation completed")

    
    def exit(self):
        pass
        #self.driver.quit()

