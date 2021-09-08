#%%
import datetime
import math

#%%
class Pessoa:
    def __init__(self, nome:str, sobrenome:str, data_de_nascimento:datetime.date):
        self.nome = nome
        self.sobrenome = sobrenome
        self.data_de_nascimento = data_de_nascimento

    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)

    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome} tem {self.idade} anos"

#%%
vinicius = Pessoa(nome='Vinicius', sobrenome='Nascimento', data_de_nascimento=datetime.date(year=1993, month=1, day=6))
print(vinicius)
print(vinicius.nome)
print(vinicius.idade)
