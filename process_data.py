import json
import math
import numpy as np
pokedex = json.load(open('pokedex.json'))
l = 807
data = np.empty(shape=(0, 807))
weight = np.empty(shape=(0))
types = {'Normal': 0, 'Fire': 1, 'Water': 2, 'Electric': 3, 'Grass': 4, 'Ice': 5, 'Fighting': 6,
         'Poison': 7, 'Ground': 8, 'Flying': 9, 'Psychic': 10, 'Bug': 11, 'Rock': 12, 'Ghost': 13,
         'Dragon': 14, 'Dark': 15, 'Steel': 16, 'Fairy': 17}
with open('rentalTeams.json') as rental:
    for line in rental:
        line_dic = json.loads(line)
        data_entry = np.zeros([1, l])
        #type_entry = np.zeros([1, 18])
        for i in range(0, 6):
            info = pokedex[line_dic['pokemons'][0]]
            data_entry[0][info['num']-1] = 1
        data = np.concatenate((data, data_entry))
        weight = np.concatenate((weight, np.array([math.log(int(line_dic['winCount'].replace(',', '')))])))
with open('showdown.csv') as showdown:
    for line in showdown:
        line = line[0:-1]
        pokemons = line.split(',')
        for i in range(0, 6):
            if 'Minior' in pokemons[i]:
                pokemons[i] = 'Minior'
            if 'Gastrodon' in pokemons[i]:
                pokemons[i] = 'Gastrodon'
            if '-*' in pokemons[i]:
                pokemons[i] = pokemons[i][0:-2]
            if 'Florges' in pokemons[i]:
                pokemons[i] = 'Florges'
            info = pokedex[pokemons[i]]
            data_entry[0][info['num']-1] = 1
        data = np.concatenate((data, data_entry))
        weight = np.concatenate((weight, np.array([5.7])))
print(data.shape)
