import sys, os, time

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
                    #if intentar_ubicar_barco(tablero, m, n, barco, i_fil, i_col, True):
                    if intentar_ubicar_barco(tablero, barco, i_fil, i_col, True, demandas_fil, demandas_col):
                        ubicar_barco(tablero, barco, i_fil, i_col, demandas_fil, demandas_col, True)
                        ubicado = True
                        break
            else:
                # Intenta ubicar por columna
                i_col = max_demanda_col[1]
                for i_fil in range(n):
                    #if intentar_ubicar_barco(tablero, m, n, barco, i_fil, i_col, False):
                    if intentar_ubicar_barco(tablero, barco, i_fil, i_col, False, demandas_fil, demandas_col):
                        ubicar_barco(tablero, barco, i_fil, i_col, demandas_fil, demandas_col, False)
                        ubicado = True
                        break

            # No se puede ubicar al barco
            if not ubicado:
                break

    return tablero, demandas_fil, demandas_col

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

            tiempo_inicio = time.perf_counter()
            tablero_final, demandas_fil_final, demandas_col_final  = batalla_naval(largo_barcos, demandas_fil.copy(), demandas_col.copy())
            tiempo_final = time.perf_counter()
            duracion = tiempo_final - tiempo_inicio
            
            print("---" + archivo_nombre + "---")
            for i, fila in enumerate(tablero_final):
                print(fila)
            demanda_total = sum(demandas_fil) + sum(demandas_col)
            demanda_incumplida = sum(demandas_fil_final) + sum(demandas_col_final)
            demanda_cumplida = demanda_total - demanda_incumplida
            print("Demanda cumplida:", demanda_cumplida)
            print("Demanda incumplida:", demanda_incumplida)
            print("Demanda total:", demanda_total)
            print("Duracion:", duracion, "ns")
            print("\n")

if __name__ == "__main__":
    main()