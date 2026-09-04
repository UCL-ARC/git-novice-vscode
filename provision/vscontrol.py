from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By

options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)
### Start VS Code
### code serve-web --host 0.0.0.0 --port 8000 --without-connection-token --accept-server-license-terms


## send keys https://www.selenium.dev/documentation/webdriver/actions_api/keyboard/


driver.get("http://127.0.0.1:8000")

driver.implicitly_wait(15)

ActionChains(driver).send_keys(Keys.F1).perform()
## ✅ Opening a folder and entering the name doesn't work
ActionChains(driver).key_down(Keys.CONTROL).send_keys("ko").key_up(Keys.CONTROL).perform()
# text_input = driver.find_element(By.CLASS_NAME, "ibwrapper")
# ActionChains(driver).send_keys_to_element(text_input, "test_repo").perform()
ActionChains(driver).send_keys("test_repo").send_keys(Keys.ENTER).send_keys(Keys.ENTER).perform()
ActionChains(driver).send_keys(Keys.ENTER).perform()

## ✅ Initialising repository
ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys("g").key_up(Keys.CONTROL).key_up(Keys.SHIFT).perform()
buttons_input = driver.find_element(By.CLASS_NAME, "button-container")
ActionChains(driver).click(buttons_input).perform()

## Create a new file
ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys("e").key_up(Keys.CONTROL).key_up(Keys.SHIFT).perform()
buttons_input = driver.find_element(By.CLASS_NAME, "codicon-new-file")
ActionChains(driver).click(buttons_input).perform()
ActionChains(driver).send_keys("guacamole.md").send_keys(Keys.ENTER).perform()

## Write content on new file
ActionChains(driver).send_keys("# Guacamole").send_keys(Keys.ENTER).send_keys("## Ingredients").send_keys(Keys.ENTER).send_keys("## Instructions").send_keys(Keys.ENTER).perform()
## and save
ActionChains(driver).key_down(Keys.CONTROL).send_keys("s").key_up(Keys.CONTROL).perform()

# Commit to git
ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys("g").key_up(Keys.CONTROL).key_up(Keys.SHIFT).perform()

#buttons_input = driver.find_element(By.CLASS_NAME, "codicon-add") # (not sure where's finding the add)
#ActionChains(driver).click(buttons_input).perform()

buttons_input = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div/div[2]/div[1]/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div/div[1]/div[4]/div/div[3]/div/div[1]/div/div[2]/div/div/ul/li[3]/a")
ActionChains(driver).click(buttons_input).perform()
## and commit message
ActionChains(driver).send_keys_to_element(text_input, "# Guacamole").send_keys(Keys.ENTER)
ActionChains(driver).send_keys_to_element(text_input, "Defines template").key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()

# Open a new terminal
ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys("c").key_up(Keys.CONTROL).key_up(Keys.SHIFT).perform()
driver.implicitly_wait(5)
ActionChains(driver).send_keys("ls").send_keys(Keys.ENTER).perform()

ActionChains(driver).send_keys("git config --list").send_keys(Keys.ENTER).perform()
ActionChains(driver).send_keys("q").perform()

# Show and hide terminal
ActionChains(driver).key_down(Keys.CONTROL).send_keys("j").key_up(Keys.CONTROL).key_up(Keys.SHIFT).perform()
driver.implicitly_wait(5)
ActionChains(driver).send_keys("ls").send_keys(Keys.ENTER).perform()
driver.implicitly_wait(5)
ActionChains(driver).key_down(Keys.CONTROL).send_keys("j").key_up(Keys.CONTROL).key_up(Keys.SHIFT).perform()




# text_input = driver.find_element(By.CLASS_NAME, "terminal-widget-container")
# ActionChains(driver).send_keys_to_element(text_input, "ls").send_keys(Keys.ENTER).perform()


driver.save_full_page_screenshot("full_page_screenshot.png")
