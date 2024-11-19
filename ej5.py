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
            max_demanda_fil = max((d, i) for i, d in enumerate(demandas_fil) if d >= barco)
            max_demanda_col = max((d, j) for j, d in enumerate(demandas_col) if d >= barco)

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
            if not ubicado and max_demanda_fil[0] < barco and max_demanda_col[0] < barco:
                break

    return tablero


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
    largo_barcos = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    demandas_fila_og = [3, 2, 2, 4, 2, 1, 1, 2, 3, 0]
    demandas_columna_og = [1, 2, 1, 3, 2, 2, 3, 1, 5, 0]
    demandas_fila = [3, 2, 2, 4, 2, 1, 1, 2, 3, 0]
    demandas_columna = [1, 2, 1, 3, 2, 2, 3, 1, 5, 0]

    tablero_final = batalla_naval(largo_barcos, demandas_fila, demandas_columna)
    for i, fila in enumerate(tablero_final):
        print((fila, demandas_fila_og[i]))
    print('\n')
    print(demandas_columna_og)

main()