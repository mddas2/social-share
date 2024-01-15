

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the browser (in this example, we're using Chrome)
driver = webdriver.Chrome()

# Open the webpage
webpage_url = 'https://newspolar.com/archives/225646'
driver.get(webpage_url)

# Locate the button by its class name
get_score_class = 'st-label'  # Replace with the actual class name of the button
get_score = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, get_score_class)))
get_score = get_score.text
# Click the button
print(get_score)
print(get_score)
print(get_score)

webpage_url = 'https://newspolar.com/archives/225646'
driver.get(webpage_url)

# Locate the element by its data-network attribute
element_css_selector = 'img[src="https://platform-cdn.sharethis.com/img/facebook.svg"]'

# Click the element
for i in range(20):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, element_css_selector)))
    try:
        element.click()
        print("clicked ")
    except:
        print(" error ")



# Close the browser
# driver.quit()

input("Press Enter to close the browser.")

# if __name__ == "__main__":
#     #initialize a gui box
#     print("this is initializing gui")
#     pass