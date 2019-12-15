from api import get_friends, zapr
from igraph import Graph, plot
import igraph
import numpy as np
import time
import requests
import config

def pol(user_id):
    domain = config.VK_CONFIG['domain']
    access_token = config.VK_CONFIG['access_token']
    v = config.VK_CONFIG['version']
    fields = 'bday'
    query = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}"
    response = zapr(query)
    ids = []
    coun = response.json()['response']['count']
    for i in range(coun):
            ids.append(response.json()['response']['items'][i]['id'])
    return ids #[3656705, 11819822, 12742533, 26477084, 39703865, 43063510, 46764640, 70748226, 76163640, 77400971, 85986907, 87393116, 106290840, 113554341, 119465413, 120831486, 122511861, 125483792, 125827334, 132146155, 137688928, 137780359, 137937464, 138173569, 139125636, 139395155, 143668129, 146608007, 147302816, 150982702, 151782201, 153011095, 154032965, 157417743, 157815031, 158864639, 163457979, 163659919, 168468531, 168652295, 168900120, 170810514, 171494699, 171928321, 172942278, 175915226, 176650482, 181692280, 187024824, 188286293, 196938389, 198673863, 198811117, 206593407, 215660702, 216037873, 216746804, 219556901, 219755318, 221654804, 223197329, 227547392, 227656030, 229123746, 234182926, 238472934, 239130006, 246110107, 247177920, 264842900, 273044086, 298509448, 299955321, 319397138, 326695321, 328444279, 386718947, 394254792, 397192059, 404111371, 460104701, 496722634, 497545785, 511037615]

def convert(ids): #массив id друзей
    d = {}
    c = 0
    for i in ids:
        d[i] = c
        c += 1
    return d    # {3656705: 0, 11819822: 1, 12742533: 2, 26477084: 3, 39703865: 4, 43063510: 5, 46764640: 6, 70748226: 7, 76163640: 8, 77400971: 9, 85986907: 10, 87393116: 11, 106290840: 12, 113554341: 13, 119465413: 14, 120831486: 15, 122511861: 16, 125483792: 17, 125827334: 18, 132146155: 19, 137688928: 20, 137780359: 21, 137937464: 22, 138173569: 23, 139125636: 24, 139395155: 25, 143668129: 26, 146608007: 27, 147302816: 28, 150982702: 29, 151782201: 30, 153011095: 31, 154032965: 32, 157417743: 33, 157815031: 34, 158864639: 35, 163457979: 36, 163659919: 37, 168468531: 38, 168652295: 39, 168900120: 40, 170810514: 41, 171494699: 42, 171928321: 43, 172942278: 44, 175915226: 45, 176650482: 46, 181692280: 47, 187024824: 48, 188286293: 49, 196938389: 50, 198673863: 51, 198811117: 52, 206593407: 53, 215660702: 54, 216037873: 55, 216746804: 56, 219556901: 57, 219755318: 58, 221654804: 59, 223197329: 60, 227547392: 61, 227656030: 62, 229123746: 63, 234182926: 64, 238472934: 65, 239130006: 66, 246110107: 67, 247177920: 68, 264842900: 69, 273044086: 70, 298509448: 71, 299955321: 72, 319397138: 73, 326695321: 74, 328444279: 75, 386718947: 76, 394254792: 77, 397192059: 78, 404111371: 79, 460104701: 80, 496722634: 81, 497545785: 82, 511037615: 83}

def names(user_id): #мой id
    domain = config.VK_CONFIG['domain']
    access_token = config.VK_CONFIG['access_token']
    v = config.VK_CONFIG['version']
    fields = 'bday'
    otvet = []
    ids = pol(user_id)
    fname = ''
    sname = ''
    for i in range(len(ids)):
        query = f"{domain}/users.get?access_token={access_token}&user_id={ids[i]}&fields={fields}&v={v}"
        response = zapr(query)
        a = response.json()['response'][0]['first_name']
        b = response.json()['response'][0]['last_name']
        c = a + ' ' + b
        print(c)
        otvet.append(c)
        time.sleep(0.7)
    return otvet #имена друзей

def get_network(users_ids): #ids друзей
    otvet = []
    for i in users_ids:
        friend2 = pol(i)
        comm = list(set(friend2)&set(users_ids))
        if comm != []:
            for j in comm:
                otvet.append((i, j))
        time.sleep(0.7)
    slov = convert(pol(559574644))
    newgrap = []
    a = 0
    b = 0
    for i in range(len(otvet)):
        for j in range(len(otvet[0])):
            for k in slov:
                if otvet[i][j] == k:
                    if j == 0:
                        a = slov[k]
                    else:
                        b = slov[k]
        newgrap.append((a, b))  # edges
    return newgrap #edges 0-83

# Создание графа
asd = pol(559574644)
vertices = names(559574644)
edges = get_network(asd)

g = Graph(vertex_attrs={"label":vertices},
    edges=edges, directed=False)

# Задаем стиль отображения графа
N = len(vertices)
visual_style = {}
visual_style["layout"] = g.layout_fruchterman_reingold(
    maxiter=1000,
    area=N**3,
    repulserad=N**3)

# Отрисовываем граф

#g.simplify(multiple=True, loops=True)
#def plot_graph(graph):
    # PUT YOUR CODE HERE
g.simplify(multiple=True, loops=True)

communities = g.community_edge_betweenness(directed=False)
clusters = communities.as_clustering()
pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
g.vs['color'] = pal.get_many(clusters.membership)
plot(g, **visual_style)