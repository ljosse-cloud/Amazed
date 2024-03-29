#On définit les différentes cases par leur type et leur position
class Tile:
    def __init__(self, position, id):
        self.position = position
        self.id = id

class Portal(Tile):
    def __init__(self, position, id, portal_id):
        super().__init__(position, id)
        self.portal_id = portal_id
 
class Map:
    def __init__(self, tiles):
        self.tiles = tiles
        self.start = Tile((0, 0), -2)
        self.end = Tile((1, 0), -1)
    #On définit tois fonctions facilitant grandement l'écriture du code
    def get_tile(self, position):
        for tile in self.tiles:
            if tile.position == position:
                return tile

    def has(self, position, ids = []):
        for tile in self.tiles+[self.start, self.end]:
            if tile.position == position and (ids == [] or tile.id in ids):
                return True

        return False

    def remove(self, position):
        for i in range(0, len(self.tiles)):
            if self.tiles[i].position == position:
                del self.tiles[i]
                break
    
def load_map_file(path):
    m = Map([])
    content = []
    try : # Le but de ce try est de vérifier l'existence du fichier
        with open(path) as file:
            content = file.readlines()
            for line in content:
                line = line[0:-1].split(" ")
                line[0:3] = list(map(int, line[0:3]))

                if line[2] == 0:
                    m.tiles.append(Tile((line[0], line[1]), line[2]))
                elif line[2] == -1:
                    m.end.position = (line[0], line[1])
                elif line[2] == -2:
                    m.start.position = (line[0], line[1])
                elif line[2] == 1 and len(line) >= 4:
                    if line[3][0]+line[3][-1] == "()":
                        m.tiles.append(Portal((line[0], line[1]), line[2], int(line[3][1:-1]))) 
                #Dans chacun des 4 cas précédents on a implémenté de manière adéquate la liste des cases.


    except FileNotFoundError: #Si l'utilisateur a fait une faute, il ouvre un fichier vide
        m.tiles.append(Tile(0,0),-2) 
        m.tiles.append(Tile(0,1),-1)
    finally:



        return m


def update_portal_count(map): # Fonction comptant le nombre de portails pour l'actualiser après une ouverture de fichier.
    m = Map([])

    portal_count_updated=0
    for t in map.tiles :
        if type(t) is Portal :
            portal_count_updated +=1
    portal_count_updated //= 2 #car les portails vont en couple
    return portal_count_updated+1 #car il y a un couple de portails 0


def save_map(map, path):
    with open(path, "w") as file:
        for tile in map.tiles+[map.start, map.end]:
            file.write(str(tile.position[0])+" "+str(tile.position[1])+" "+str(tile.id)) #On écrit dans le fichier les coordonnées de l'objet, puis son type

            if type(tile) is Portal:
                file.write(" ("+str(tile.portal_id)+")") #Si c'est un portail on écrit aussi son id afin de recréer les "couples" de portails
            file.write(str("\n"))





