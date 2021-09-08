#%%
from selenium import webdriver
import time
import pandas as pd

# %%
driver = webdriver.Chrome('.\src\chromedriver.exe')
driver.implicitly_wait(10)
driver.get('https://pt.wikipedia.org/wiki/Nicolas_Cage')

#%%
def has_item(xpath, driver=driver):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False

def wait_for_item(xpath, driver=driver, num_tries = 5, wait_time=10):
    while num_tries > 0:
        if has_item(xpath, driver):
            return driver.find_element_by_xpath(xpath)
        else:
            time.sleep(wait_time)
        num_tries -= 1
    return None

#%%
tabela = wait_for_item(xpath='/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[2]')
#tabela = driver.find_element_by_xpath('/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[2]')

#%%
with open('print_screen.png', 'wb') as f:
    f.write(driver.find_element_by_xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[2]/td/div/div/div/a/img').screenshot_as_png)

#%%
df = pd.read_html('<table>' + tabela.get_attribute('innerHTML') + '</table>')[0]
driver.close()

# %%
df.to_csv('filmes_nicolas_cage.csv', sep=';', index=False)
