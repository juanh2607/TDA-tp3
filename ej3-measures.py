import os
import time

from ej3 import batalla_naval

ROW_REQUIREMENTS = 0
COL_REQUIREMENTS = 1
BOAT_LENGTHS = 2


# Tests ej3 ----------------------------------------------------------------------------------------
def load_test_data(f):
    current_list = 0
    data = [[] for _ in range(3)]

    for line in f:
        if line.strip() == "":
            current_list += 1
            continue

        data[current_list].append(int(line.strip()))

    return data


def run_test(test_file, expected_result):
    with open(test_file, "r") as f:
        # Ignoro las primeras dos lineas
        next(f)
        next(f)

        data = load_test_data(f)

        start_time = time.time()
        result = batalla_naval(
            data[BOAT_LENGTHS], data[ROW_REQUIREMENTS], data[COL_REQUIREMENTS]
        )
        end_time = time.time()
        execution_time = end_time - start_time

        assert result == expected_result

        return execution_time


def run_test_files(dir, expected_results):
    runtimes = {}

    for file in os.listdir(dir):
        print(f"Running test {file}")

        route = os.path.join(dir, file)
        runtime = run_test(route, expected_results[file])

        print(f"Tiempo de ejecución test {file}: {runtime:.6f} segundos\n")

        runtimes[file] = runtime

    return runtimes


def get_expected_results():
    expected_results = {}
    with open("expected-results.txt", "r") as f:
        for line in f:
            if line.strip() == "":
                continue

            if ".txt" in line:
                current_file = line.strip()
            else:
                key, value = line.split(":")
                value = int(value.strip())

                if key == "Demanda cumplida":
                    expected_results[current_file] = (value, 0)
                elif key == "Demanda total":
                    cumplida, _ = expected_results[current_file]
                    expected_results[current_file] = (cumplida, value)

    return expected_results


runtimes = run_test_files("Pruebas", get_expected_results())
print(runtimes)
