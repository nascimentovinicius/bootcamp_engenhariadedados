#%%
from selenium import webdriver

# %%
driver = webdriver.Chrome('.\src\chromedriver.exe')

#%%
driver.get("https://howedu.com.br")
driver.find_element_by_xpath('//*[@id="PopupSignupForm_0"]/div[2]/div[1]').click()
driver.find_element_by_xpath('/html/body/section[4]/div/div/div[2]/a').click()

#%%
driver.get('https://buscacepinter.correios.com.br/app/endereco/index.php')

#%%
e_cep = driver.find_element_by_name('endereco')
e_cep.clear()
e_cep.send_keys('Rua Juripiranga')

# %%
e_cmb = driver.find_element_by_name('tipoCEP')
e_cmb.click()
driver.find_element_by_xpath('//*[@id="formulario"]/div[2]/div/div[2]/select/option[6]').click()

# %%
driver.find_element_by_id('btn_pesquisar').click()

# %%
logradouro = driver.find_element_by_xpath('//*[@id="resultado-DNEC"]/tbody/tr[7]/td[1]').text
bairro = driver.find_element_by_xpath('//*[@id="resultado-DNEC"]/tbody/tr[7]/td[2]').text
localidade = driver.find_element_by_xpath('//*[@id="resultado-DNEC"]/tbody/tr[7]/td[3]').text
cep = driver.find_element_by_xpath('//*[@id="resultado-DNEC"]/tbody/tr[7]/td[4]').text

# %%
print(f"Endereço: {logradouro} - Bairro: {bairro} - Cidade/Estado: {localidade} - CEP: {cep}")

# %%
driver.close()