#%%
#imports
import requests
import json


#%%
url = "http://economia.awesomeapi.com.br/json/last/USD-BRL" #,EUR-BRL,BTC-BRL"
ret = requests.get(url)

#%%
if ret:
    print(ret.text)
else:
    print("Falhou")

# %%
dolar = json.loads(ret.text)['USDBRL']

# %%
print(f"20 dolares hoje equivale a {20 * float(dolar['bid'])} reais")

# %%
def cotacao(quantidade, moeda):
    url = f"http://economia.awesomeapi.com.br/json/last/{moeda}"
    ret = requests.get(url)
    dolar = json.loads(ret.text)[moeda.replace('-','')]
    print(f"{quantidade} {moeda[:3]} hoje equivale a {quantidade * float(dolar['bid'])} {moeda[-3:]}")

#%%
cotacao(10, "USD-BRL")

# %%
cotacao(10, "EUR-BRL")

# %%
def mult_moedas(quantidade):
    lst_money = ["USD-BRL", "EUR-BRL", "BTC-BRL", "RPL-BRL", "JPY-BRL"]

    for moeda in lst_money:
        try:
            url = f"http://economia.awesomeapi.com.br/json/last/{moeda}"
            ret = requests.get(url)
            dolar = json.loads(ret.text)[moeda.replace('-','')]
            print(f"{quantidade} {moeda[:3]} hoje equivale a {quantidade * float(dolar['bid'])} {moeda[-3:]}")
        except Exception as e:
            print(f"Falha na moeda {e}")

# %%
mult_moedas(10)
# %%
def error_check(func):
    def inner_func(*args, **kargs):
        try:
            func(*args, **kargs)
        except Exception as e:
            print(f"{func.__name__} falhou")
    return inner_func

@error_check
def cotacao(quantidade, moeda):
    url = f"http://economia.awesomeapi.com.br/json/last/{moeda}"
    ret = requests.get(url)
    dolar = json.loads(ret.text)[moeda.replace('-','')]
    print(f"{quantidade} {moeda[:3]} hoje equivale a {quantidade * float(dolar['bid'])} {moeda[-3:]}")


# %%
lst_money = ["USD-BRL", "EUR-BRL", "BTC-BRL", "RPL-BRL", "JPY-BRL"]
for moeda in lst_money:
    cotacao(10, moeda)

# %%
import backoff
import random

@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries= 10)
def test_func(*args, **kargs):
    rnd = random.random()
    print(f"""
        RND: {rnd}
        args: {args if args else 'sem args'}
        kags: {kargs if kargs else 'sem kargs'}
    """)
    if rnd < .2:
        raise ConnectionAbortedError("Conexão foi finalizada")
    if rnd < .4:
        raise ConnectionRefusedError("Conexão foi recusada")
    if rnd < .6:
        raise TimeoutError("Tempo de espera excedido")
    else:
        return "OK!"


# %%
test_func()

# %%
import logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)


# %%
@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries= 10)
def test_func(*args, **kargs):
    rnd = random.random()
    log.debug(f"RND: {rnd}")
    log.debug(f"args: {args if args else 'sem args'}")
    log.debug(f"kags: {kargs if kargs else 'sem kargs'}")
    if rnd < .2:
        log.error("Conexão foi finalizada")
        raise ConnectionAbortedError("Conexão foi finalizada")
    if rnd < .4:
        log.error("Conexão foi recusada")
        raise ConnectionRefusedError("Conexão foi recusada")
    if rnd < .6:
        log.error("Tempo de espera excedido")
        raise TimeoutError("Tempo de espera excedido")
    else:
        return "OK!"

# %%
test_func(42, nome="Vini")
