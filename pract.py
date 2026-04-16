import random

class WumpusWorld:
    def __init__(self, size=6):
        self.size = size
        self.grid = [[{'brisa': False, 'hedor': False, 'resplandor': False, 
                       'pozo': False, 'wumpus': False, 'oro': False} 
                      for _ in range(size)] for _ in range(size)]
        self._generar_mundo()

    def _generar_mundo(self):
        posiciones = [(r, c) for r in range(self.size) for c in range(self.size) if (r,c) != (0,0)]
        for r, c in posiciones:
            if random.random() < 0.15: self.grid[r][c]['pozo'] = True
        
        w_pos = random.choice(posiciones)
        self.grid[w_pos[0]][w_pos[1]]['wumpus'] = True
        o_pos = random.choice(posiciones)
        self.grid[o_pos[0]][o_pos[1]]['oro'] = True
        self.grid[o_pos[0]][o_pos[1]]['resplandor'] = True
        self._set_percepciones()

    def _set_percepciones(self):
        for r in range(self.size):
            for c in range(self.size):
                adj = self.get_adjacentes(r, c)
                if self.grid[r][c]['pozo']:
                    for nr, nc in adj: self.grid[nr][nc]['brisa'] = True
                if self.grid[r][c]['wumpus']:
                    for nr, nc in adj: self.grid[nr][nc]['hedor'] = True

    def get_adjacentes(self, r, c):
        res = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.size and 0 <= nc < self.size: 
                res.append((nr, nc))
        return res

    def imprimir_tablero(self, pos_agente):
        """Imprime el estado real del mundo y la posición del agente."""
        print("\n--- ESTADO DEL MUNDO ---")
        for r in range(self.size - 1, -1, -1): # Invertir para que (0,0) sea abajo-izq
            fila = "|"
            for c in range(self.size):
                char = ""
                if (r, c) == pos_agente: char += "A" # Agente
                if self.grid[r][c]['wumpus']: char += "W"
                if self.grid[r][c]['pozo']: char += "P"
                if self.grid[r][c]['oro']: char += "G"
                
                # Relleno para mantener alineación
                fila += char.center(4) + "|"
            print(fila)
            print("-" * (self.size * 6))
        print("Leyenda: A=Agente, W=Wumpus, P=Pozo, G=Oro\n")

    def obtener_percepcion(self, r, c):
        return self.grid[r][c]

class AgenteLogico:
    def __init__(self, size=6):
        self.size = size
        self.pos_actual = (0, 0)
        self.visitados = set()
        self.seguras = set([(0,0)])
        self.kb = {(r, c): {'p_pozo': 'u', 'p_wumpus': 'u' , 'segura': None} 
                   for r in range(size) for c in range(size)}
        self.wumpus_muerto = False
       
     
       
    
    def integrar_percepcion(self, r, c, perc):
        self.visitados.add((r,c))
        adjacentes = mundo.get_adjacentes(r,c)

        """ Definicion de logica 
            Reglas con persepcion 
        """
        #Verificamos que no hay brisa, por lo tanto no existe un pozo
        if not perc['brisa']:
            for nr, nc in adjacentes:
                self.kb[(nr, nc)]['p_pozo'] = False      

        #Verificamos que no hay hedor, por lo tanto no existe un Wuampus
        if not perc['hedor']:
            for nr, nc in adjacentes:
                self.kb[(nr, nc)]['p_wumpus'] = False
        # Evaluamos todos los vecinos que no contengan un pozo o wunpus

        """ Reglas con persepcion """
        #Verificamos si existe una brisa, por lo tanto hay un pozo 
        if perc['brisa']:
            for nr, nc in adjacentes:
                if self.kb[(nr,nc)]['p_pozo'] == 'u':
                    self.kb[(nr,nc)]['p_pozo'] = True

        # Buscar el wuampus para lanzar la flecha
        if perc['hedor'] and not self.wumpus_muerto:
            sospechosos_wuampus = []
            #obtner los posibles sospechosos
            for nr,nc in adjacentes:
                if self.kb[(nr, nc)]['p_wumpus'] != False:
                    sospechosos_wuampus.append((nr,nc))
            #Filtrar solo los posibles
            """
            posibles_wampus = []
            for pos in sospechosos_wuampus:
                if self.kb[pos]['p_wumpus'] == True:
                    posibles_wampus.append(pos)
            """
            # Si hay uno → disparar
            if len(sospechosos_wuampus) == 1:
                pos_wumpus = sospechosos_wuampus[0]
                print("Lanzar flecha\n") 
                print("Wumpus eliminado casilla segura......!")
                self.kb[pos_wumpus]['p_wumpus'] = False
                self.wumpus_muerto = True
                #Ahora es una casilla segura
                self.seguras.add(pos_wumpus)
                self.kb[pos_wumpus]['segura'] = True
               
    
        """ Motor de inferencia"""
        for nr, nc in adjacentes:
            if self.kb[(nr, nc)]['p_pozo'] == False and self.kb[(nr, nc)]['p_wumpus'] == False:
                self.kb[(nr,nc)]['segura'] = True
                self.seguras.add((nr, nc))
        

                
        print(f"Percepciones en {r,c}: {'Brisa ' if perc['brisa'] else ''}{'Hedor ' if perc['hedor'] else ''}{'Resplandor' if perc['resplandor'] else ''}")
    

       
    def planificar_siguiente_paso(self):
        opciones = [p for p in self.seguras if p not in self.visitados]
        if opciones:
            # Intentar ir a una adyacente primero
            for opt in opciones:
                if opt in mundo.get_adjacentes(*self.pos_actual):
                    return opt
            return opciones[0]
        return None
    
    #
    
        
        
# --- Simulación Principal ---
mundo = WumpusWorld()
agente = AgenteLogico()

for turno in range(1, 20):
    print(f"*** MOVIMIENTO {turno} ***")
    mundo.imprimir_tablero(agente.pos_actual)
    
    r, c = agente.pos_actual
    percepcion = mundo.obtener_percepcion(r, c)
    
    agente.integrar_percepcion(r, c, percepcion)
    
    if percepcion['oro']:
        print("¡VICTORIA! El agente ha encontrado el Oro.")
        break
        
    proxima = agente.planificar_siguiente_paso()
    
    if proxima:
        agente.pos_actual = proxima
    else:
        print("RESULTADO: El agente no encuentra más caminos seguros. Fin de la simulación.")
        break