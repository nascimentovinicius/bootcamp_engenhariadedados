#%%
import datetime
import math
from typing import List

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
class Curriculo:
    def __init__(self, pessoa: Pessoa, experiencias: List[str]):
        self.pessoa = pessoa
        self.experiencias = experiencias

    @property
    def quantidade_de_experiencias(self) -> int:
        return len(self.experiencias)

    @property
    def empresa_atual(self) -> str:
        return self.experiencias[-1]

    def adiciona_experiencia(self, experiencia: str) -> None:
        self.experiencias.append(experiencia)

    def __str__(self) -> str:
        return f"{self.pessoa.nome} {self.pessoa.sobrenome} tem {self.pessoa.idade} anos e " \
        f"já trabalhou em {self.quantidade_de_experiencias} empresas e atualmente trabalha na " \
        f"empresa {self.empresa_atual}"


# %%
vinicius = Pessoa(nome='Vinicius', sobrenome='Nascimento', data_de_nascimento=datetime.date(1993,1,6))
print(vinicius)

curriculo_vinicius = Curriculo(
    pessoa = vinicius, 
    experiencias=['Iteris', 'Cignify', 'S4R', 'Bradesco', 'Carrefour', 'Distrito'])


# %%
print(curriculo_vinicius.pessoa)
print(curriculo_vinicius)

# %%
curriculo_vinicius.adiciona_experiencia('Facebook')
print(curriculo_vinicius)


#%%
class Vivente:
    def __init__(self, nome:str, data_de_nascimento:datetime.date) -> None:
        self.nome = nome
        self.data_de_nascimento = data_de_nascimento

    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)

    def emite_ruido(self, ruido: str):
        print(f"{self.nome} fez ruido: {ruido}")

# %%
class PessoaHeranca(Vivente):
    def __str__(self) -> str:
        return f"{self.nome} tem {self.idade} anos"

    def fala(self, frase):
        return self.emite_ruido(frase)

class Cachorro(Vivente):
    def __init__(self, nome: str, data_de_nascimento: datetime.date, raca: str) -> None:
        super().__init__(nome, data_de_nascimento)
        self.raca = raca

    def __str__(self) -> str:
        return f"{self.nome} é da raça {self.raca} e tem {self.idade} anos"

    def late(self):
        return self.emite_ruido("Au Au!")

# %%
vinicius2 = PessoaHeranca(nome="Vinicius", data_de_nascimento=datetime.date(1993,1,6))
print(vinicius2)

# %%
duke = Cachorro("Duke", datetime.date(2015,12,25), "Vira-Lata")
print(duke)

# %%
duke.late()
duke.late()
vinicius2.fala("Cala a boca!")
duke.late()
