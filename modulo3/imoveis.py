#%%
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# %%
import logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)

# %%
url = 'https://www.vivareal.com.br/venda/parana/curitiba/apartamento_residencial/?pagina={}'

# %%
i = 1
ret = requests.get(url.format(i))
soup = bs(ret.text)

# %%
houses = soup.find_all('a', {'class':'property-card__content-link js-card-title'})
qtde_imoveis = float(soup.find('strong', {'class':'results-summary__count'}).text.replace('.',''))

# %%
len(houses)

# %%
qtde_imoveis

# %%
house = houses[0]

# %%
house

#%%
df = pd.DataFrame(columns = [
     'descricao'
    ,'endereco'
    ,'area'
    ,'quartos'
    ,'wc'
    ,'vagas'
    ,'valor'
    ,'condominio'
    ,'wlink'
])
i = 0

#%%
while qtde_imoveis > df.shape[0]:
    i += 1
    print(f"Valor i: {i} \t\t qtde_imoveis: {df.shape[0]}")
    ret = requests.get(url.format(i))
    soup = bs(ret.text)
    houses = soup.find_all('a', {'class':'property-card__content-link js-card-title'})
    for house in houses:
        #print(house)
        try:
            descricao = house.find('span', {'class': 'property-card__title'}).text.strip()
        except:
            descricao = None
        try:
            endereco = house.find('span', {'class': 'property-card__address'}).text.strip()
        except:
            endereco = None
        try:
            area = house.find('span', {'class': 'js-property-card-detail-area'}).text.strip()
        except:
            area = None
        try:
            quartos = house.find('li', {'class': 'property-card__detail-room'}).span.text.strip()
        except:
            quartos = None
        try:
            wc = house.find('li', {'class': 'property-card__detail-bathroom'}).span.text.strip()
        except:
            wc = None
        try:
            vagas = house.find('li', {'class': 'property-card__detail-garage'}).span.text.strip()
        except:
            vagas = None
        try:
            valor = house.find('div', {'class': 'js-property-card-prices'}).p.text.strip()
        except:
            valor = None
        try:
            condominio = house.find('strong', {'class': 'js-condo-price'}).text.strip()
        except:
            condominio = None
        try:
            wlink = 'https://www.vivareal.com.br' + house['href']
        except:
            wlink = None

        df.loc[df.shape[0]] = [
            descricao
            ,endereco
            ,area
            ,quartos
            ,wc
            ,vagas
            ,valor
            ,condominio
            ,wlink
        ]

#%%
print(descricao)
print(endereco)
print(area)
print(quartos)
print(wc)
print(vagas)
print(valor)
print(condominio)
print(wlink)

# %%
df

# %%
df.to_csv('banco_de_imoveis.csv', index=False, sep=';')
# %%
