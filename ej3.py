TABLERO = 0
DEMANDA_INCUMPLIDA = 1


# Ejecuta el algoritmo de backtracking para la batalla naval individual, creando el tablero con las demandas de filas y columnas.
# Imprime el tablero final y los resultados de las demandas.
def batalla_naval(largo_barcos, demandas_fil, demandas_col):
    n = len(demandas_fil)
    m = len(demandas_col)
    tablero = [[0] * m for _ in range(n)]
    largo_barcos.sort(reverse=True)
    solucion = [tablero, float("inf")]

    batalla_naval_bt(tablero, largo_barcos, demandas_fil, demandas_col, solucion)

    # for fila in solucion[TABLERO]:
    #     print(fila)
    demanda_total = sum(demandas_fil) + sum(demandas_col)
    demanda_cumplida = demanda_total - solucion[DEMANDA_INCUMPLIDA]
    # print("Demanda incumplida:", solucion[DEMANDA_INCUMPLIDA])
    # print("Demanda cumplida:", demanda_cumplida)
    # print("Demanda total:", demanda_total)

    return (demanda_cumplida, demanda_total)


# Algoritmo de backtracking para resolver el problema de optimización de la batalla naval individual.
def batalla_naval_bt(
    tablero, largo_barcos, demandas_fil, demandas_col, solucion_parcial
):
    demanda_incumplida = sum(demandas_fil) + sum(demandas_col)
    # Actualizar mejor solución
    if demanda_incumplida < solucion_parcial[DEMANDA_INCUMPLIDA]:
        solucion_parcial[TABLERO] = [list(fila) for fila in tablero]
        solucion_parcial[DEMANDA_INCUMPLIDA] = demanda_incumplida
    # Caso base
    if not largo_barcos:
        return
    # Poda
    if solucion_parcial[DEMANDA_INCUMPLIDA] <= demanda_incumplida - sum(
        barco * 2 for barco in largo_barcos
    ):
        return

    # Pruebo sin colocar un barco
    batalla_naval_bt(
        tablero, largo_barcos[1:], demandas_fil, demandas_col, solucion_parcial
    )
    # Pruebo colocando un barco
    for i in range(len(tablero)):
        if demandas_fil[i] > 0:  # Procesar solo si hay demanda en la fila
            for j in range(len(tablero[0])):
                if demandas_col[j] > 0:  # Procesar solo si hay demanda en la columna
                    procesar_barco(
                        tablero,
                        largo_barcos,
                        i,
                        j,
                        demandas_fil,
                        demandas_col,
                        solucion_parcial,
                        True,
                    )
                    procesar_barco(
                        tablero,
                        largo_barcos,
                        i,
                        j,
                        demandas_fil,
                        demandas_col,
                        solucion_parcial,
                        False,
                    )


# Prueba de colocar el barco. Si se puede, sigue probando alternativas, hasta terminar y quitar el barco.
def procesar_barco(
    tablero,
    largo_barcos,
    i,
    j,
    demandas_fil,
    demandas_col,
    solucion_parcial,
    es_horizontal,
):
    if intentar_ubicar_barco(
        tablero, largo_barcos[0], i, j, es_horizontal, demandas_fil, demandas_col
    ):
        ubicar_barco(
            tablero, largo_barcos[0], i, j, demandas_fil, demandas_col, es_horizontal
        )
        batalla_naval_bt(
            tablero, largo_barcos[1:], demandas_fil, demandas_col, solucion_parcial
        )
        quitar_barco(
            tablero, largo_barcos[0], i, j, demandas_fil, demandas_col, es_horizontal
        )


# Intenta ubicar el barco, horizontalmente en la fila i_fil, o verticalmente en la columna i_col (segun el caso).
# Chequea que no se salga del tablero, que los casilleros a tomar no estén siendo utilizados por otro barco y que no tenga barcos adyacentes.
def intentar_ubicar_barco(
    tablero, largo_barco, i_fil, i_col, es_horizontal, demandas_fil, demandas_col
):
    n, m = len(tablero), len(tablero[0])

    # Verificar que el barco no salga del tablero
    if es_horizontal:
        if i_col + largo_barco > m:
            return False
    else:  # Es vertical
        if i_fil + largo_barco > n:
            return False
    # Verificar que no se violen las demandas de fila y columna
    if es_horizontal:
        if demandas_fil[i_fil] < largo_barco:
            return False
        for i in range(largo_barco):
            if demandas_col[i_col + i] < 1:
                return False
    else:  # Es vertical
        if demandas_col[i_col] < largo_barco:
            return False
        for i in range(largo_barco):
            if demandas_fil[i_fil + i] < 1:
                return False
    # Verificar que no haya barcos adyacentes o superpuestos
    for i in range(largo_barco):
        fil, col = (i_fil, i_col + i) if es_horizontal else (i_fil + i, i_col)
        # Revisa que el casillero no este ocupado por otro barco.
        if tablero[fil][col] != 0:
            return False
        # Revisa adyacencias (por fila, columna y diagonales)
        for dx, dy in [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]:
            adj_fil, adj_col = fil + dx, col + dy
            if 0 <= adj_fil < n and 0 <= adj_col < m and tablero[adj_fil][adj_col] != 0:
                return False
    # Verificar extremos del barco
    if es_horizontal:
        if i_col > 0 and tablero[i_fil][i_col - 1] != 0:
            return False
        if i_col + largo_barco < m and tablero[i_fil][i_col + largo_barco] != 0:
            return False
    else:  # Es vertical
        if i_fil > 0 and tablero[i_fil - 1][i_col] != 0:
            return False
        if i_fil + largo_barco < n and tablero[i_fil + largo_barco][i_col] != 0:
            return False

    return True


# Ubica al barco en el tablero, de forma horizontal o vertical.
def ubicar_barco(
    tablero, largo_barco, i_fil, i_col, demandas_fil, demandas_col, es_horizontal
):
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


# Quita al barco del tablero.
def quitar_barco(
    tablero, largo_barco, i_fil, i_col, demandas_fil, demandas_col, es_horizontal
):
    if es_horizontal:
        for i in range(i_col, i_col + largo_barco):
            tablero[i_fil][i] = 0
        demandas_fil[i_fil] += largo_barco
        for i in range(i_col, i_col + largo_barco):
            demandas_col[i] += 1
    else:
        for i in range(i_fil, i_fil + largo_barco):
            tablero[i][i_col] = 0
        demandas_col[i_col] += largo_barco
        for i in range(i_fil, i_fil + largo_barco):
            demandas_fil[i] += 1
