import sys, os

DIR_PRUEBAS = "Pruebas/"

# Ubica los barcos en el tablero, eligiendo la fila/columna mas demandada y eligiendo el barco más grande posible que cubra esa demanda.
# Recibe la lista de longitud de barcos, y las listas de demandas de filas y columnas.
def batalla_naval(largo_barcos, demandas_fil, demandas_col):
    n = len(demandas_fil)
    m = len(demandas_col)
    tablero = [[0] * m for _ in range(n)]
    largo_barcos.sort(reverse=True)

    for barco in largo_barcos:
        ubicado = False

        while not ubicado:
            max_demanda_fil = max((d, i) for i, d in enumerate(demandas_fil))
            max_demanda_col = max((d, j) for j, d in enumerate(demandas_col))
            
            # El barco es mas grande que la demanda
            if max_demanda_fil[0] < barco and max_demanda_col[0] < barco:
                break

            if max_demanda_fil[0] >= max_demanda_col[0]:
                # Intenta ubicar por fila
                i_fil = max_demanda_fil[1]
                for i_col in range(m):
                    if intentar_ubicar_barco(tablero, m, n, barco, i_fil, i_col, True):
                        ubicar_barco(tablero, barco, i_fil, i_col, demandas_fil, demandas_col, True)
                        ubicado = True
                        break
            else:
                # Intenta ubicar por columna
                i_col = max_demanda_col[1]
                for i_fil in range(n):
                    if intentar_ubicar_barco(tablero, m, n, barco, i_fil, i_col, False):
                        ubicar_barco(tablero, barco, i_fil, i_col, demandas_fil, demandas_col, False)
                        ubicado = True
                        break

            # No se puede ubicar al barco
            if not ubicado:
                break

    return tablero, demandas_fil, demandas_col


# Intenta ubicar el barco, horizontalmente en la fila i_fil, o verticalmente en la columna i_col (segun el caso).
# Chequea que no se salga del tablero, que los casilleros a tomar no estén siendo utilizados por otro barco y que no tenga barcos adyacentes.
def intentar_ubicar_barco(tablero, m, n, largo_barco, i_fil, i_col, es_horizontal):
    if es_horizontal:
        if i_col + largo_barco > m:
            return False
        for i in range(i_col, i_col + largo_barco):
            # Revisa que el casillero no este ocupado por otro barco.
            if tablero[i_fil][i] == 1:
                return False
            # Revisa adyacencias (por fila, columna y diagonales)
            adyacencias = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for dx, dy in adyacencias:
                nx, ny = i_fil + dx, i + dy
                if 0 <= nx < n and 0 <= ny < m and tablero[nx][ny] != 0:
                    return False
        # Busca barcos adyacentes a los costados del barco.
        if (i_col > 0 and tablero[i_fil][i_col - 1] != 0) or (i_col + largo_barco < m and tablero[i_fil][i_col + largo_barco] != 0):
            return False
    
    else:
        if i_fil + largo_barco > n:
            return False
        for i in range(i_fil, i_fil + largo_barco):
            # Revisa que el casillero no este ocupado por otro barco.
            if tablero[i][i_col] == 1:
                return False
            # Revisa adyacencias (por fila, columna y diagonales)
            adyacencias = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for dx, dy in adyacencias:
                nx, ny = i + dx, i_col + dy
                if 0 <= nx < n and 0 <= ny < m and tablero[nx][ny] != 0:
                    return False
        # Busca barcos adyacentes por encima y por debajo del barco.
        if (i_fil > 0 and tablero[i_fil - 1][i_col] == 1) or (i_fil + largo_barco < n and tablero[i_fil + largo_barco][i_col] == 1):
            return False
    
    return True


# Ubica al barco en el tablero, de forma horizontal o vertical.
def ubicar_barco(tablero, largo_barco, i_fil, i_col, demandas_fil, demandas_col, es_horizontal):
    if es_horizontal:
        for i in range(i_col, i_col + largo_barco):
            tablero[i_fil][i] = 1
        demandas_fil[i_fil] -= largo_barco
        for i in range(i_col, i_col + largo_barco):
            demandas_col[i] -= 1
    else:
        for i in range(i_fil, i_fil + largo_barco):
            tablero[i][i_col] = 1
        demandas_col[i_col] -= largo_barco
        for i in range(i_fil, i_fil + largo_barco):
         demandas_fil[i] -= 1


def main():
    if len(sys.argv) > 1:
        nombre_archivo = sys.argv[1]
        archivos_a_procesar = [nombre_archivo]
    else:
        archivos_a_procesar = [f for f in os.listdir(DIR_PRUEBAS) if os.path.isfile(os.path.join(DIR_PRUEBAS, f))]

    for archivo_nombre in archivos_a_procesar:
        with open(os.path.join(DIR_PRUEBAS, archivo_nombre)) as archivo:
            lines = [line.strip() for line in archivo if not line.strip().startswith('#')]
            sections = "\n".join(lines).strip().split("\n\n")

            demandas_fil = [int(x) for x in sections[0].strip().split("\n")]
            demandas_col = [int(x) for x in sections[1].strip().split("\n")]
            largo_barcos = [int(x) for x in sections[2].strip().split("\n")]

            tablero_final, demandas_fil_final, demandas_col_final  = batalla_naval(largo_barcos, demandas_fil.copy(), demandas_col.copy())
            #for i, fila in enumerate(tablero_final):
            #    print((fila, demandas_fila[i]))
            #print('\n')
            #print(demandas_columna)
            
            # CORREGIR: mal calculadas las demandas cumplidas e incumplidas.
            
            for i, fila in enumerate(tablero_final):
                #print(fila, demandas_fil[i] - sum(fila))
                print(fila)
            demanda_cumplida = sum(l1 - l2 for l1, l2 in zip(demandas_fil, demandas_fil_final)) + sum(l3 - l4 for l3, l4 in zip(demandas_col, demandas_col_final))
            demanda_incumplida = sum(demandas_fil_final) + sum(demandas_col_final)
            demanda_total = sum(demandas_fil) + sum(demandas_col)
            print("Demanda cumplida:", demanda_cumplida)
            print("Demanda incumplida:", demanda_incumplida)
            print("Demanda total:", demanda_total)
            print("\n")
if __name__ == "__main__":
    main()
