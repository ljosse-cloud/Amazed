from map import *

#Comme son nom l'indique, c'est ici qu'on crée les fonctions utiles pour Game à partir de map, la plus importante étant l'algorithme de résolution.
def right(position, step = 1):
    return (position[0]+step, position[1])

def left(position, step = 1):
    return (position[0]-step, position[1])

def down(position, step = 1):
    return (position[0], position[1]+step)

def up(position, step = 1):
    return (position[0], position[1]-step)


#Début du codage de l'algorithme de résolution.
nbLigs = 200
nbCols = 200
nbCases = nbLigs * nbCols 
adja = []
pred = [-1] * nbCases

def initialise() :
  adja.clear()
  for i in range(nbCases) :
    adja.append([])
    pred[i] = -1


pred = [-1] * nbCases
def estDedans(lig, col) :
    if ((lig < 0) or (col < 0) or (lig >= nbLigs) or (col >= nbCols)) :
        return False
    return True

def convertirCase(lig, col) :
    return lig * nbLigs + col

def convertirPosition(numero) :
    return (numero // nbLigs, numero % nbLigs)

def ajoutePortail(lig1, col1, lig2, col2) :
    adja[convertirCase(lig1, col1)].append(convertirCase(lig2, col2))
    adja[convertirCase(lig2, col2)].append(convertirCase(lig1, col1))

def construireGrapheBase(m, x0, y0) :
    
    dirx = [0, 1, -1, 0]
    diry = [1, 0, 0, -1]
    for i in range(nbLigs):
        for j in range(nbCols):
                if (not m.has((i+x0, j+y0), [0])) :
                    for idir in range(4) :
                        if (estDedans(i+dirx[idir], j+diry[idir]) and (not m.has((i+x0 + dirx[idir], j+y0 + diry[idir]), [0]))) :
                            ajoutePortail(i, j, i + dirx[idir], j + diry[idir])
    for tile in m.tiles:
        if type(tile) is Portal:
            for other in m.tiles:
                if type(other) is Portal and tile.position != other.position and tile.portal_id == other.portal_id:
                    ajoutePortail(tile.position[0]-x0, tile.position[1]-y0, other.position[0]-x0, other.position[1]-y0)

def find_path(m, ligdep, coldep, ligfin, colfin) :
    if abs(ligdep-ligfin) > 100 or abs(coldep-colfin) > 100:
        return []

    initialise()
    construireGrapheBase(m, -50, -50)

    ligfin -= (-50)
    colfin -= (-50)
    ligdep -= (-50)
    coldep -= (-50)

    caseDep = convertirCase(ligdep, coldep)
    caseFin = convertirCase(ligfin, colfin)
    queue = []
    queue.append(caseDep)
    pred[caseDep] = caseDep
    while len(queue) > 0 :
        sommet = queue.pop(0)
        for voisin in adja[sommet] :
            if pred[voisin] == -1 :
                queue.append(voisin)
                pred[voisin] = sommet
        if (pred[caseFin] != -1) :
            print("Voici le chemin le plus court (il peut en avoir plusieurs) : ")
            caseCur = caseFin
            chemin = []
            while pred[caseCur] != caseCur :
                chemin.append(convertirPosition(caseCur))
                caseCur = pred[caseCur]
            chemin.append(convertirPosition(caseDep))
            print([[pos[0]+(-50), pos[1]+(-50)] for pos in chemin[::-1]])
            return [[pos[0]+(-50), pos[1]+(-50)] for pos in chemin[::-1]]
        
            #REMPLACER LA LISTE DES POSITIONS A VISITER PAR UNE LISTE DE MOUVEMENTS ?

    print("il n'y a pas de chemin")
    return []

