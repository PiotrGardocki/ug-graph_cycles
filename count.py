import numpy as np
import time

def read_matrix(filename):
    lines = []

    with open(filename, 'r') as file:
        for line in file:
            if line.strip() == '':
                break
            lines.append(line)

    return np.array([[int(i) for i in l.split()] for l in lines])

def create_cycle(a, b, c):
    return tuple(sorted([a, b, c]))

def get_cycles_naive(matrix):
    n = len(matrix)
    cycles = set()

    for i in range(n):
        for j in range(n):
            for k in range(n):
                if i == j or i == k or j == k:
                    continue
                if matrix[i][j] and matrix[j][k] and matrix[k][i]:
                    cycles.add(create_cycle(i, j, k))

    return cycles

def get_cycles_dfs(matrix):
    n = len(matrix)
    cycles = set()

    for i in range(n):
        stack = [i]
        last_neighbor = -1

        while stack:
            current = stack[-1]

            for j in range(last_neighbor + 1, n):
                if matrix[current][j]:
                    if len(stack) < 3 and j not in stack:
                        stack.append(j)
                        last_neighbor = -1
                        break
                    elif len(stack) == 3 and stack[0] == j:
                        cycles.add(create_cycle(*stack))
            else:
                last_neighbor = stack[-1]
                stack.pop()

    return cycles

def get_cycles_matrix_multiply(matrix):
    n = len(matrix)
    square = np.matmul(matrix, matrix)
    cycles = set()

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if square[i][j] and matrix[j][i]:
                for k in range(len(matrix[i])):
                    if matrix[i][k] and matrix[k][j]:
                        cycles.add(create_cycle(i, j, k))

    return cycles

def measure_function(func, *arguments):
    start = time.time()
    result = func(*arguments)
    end = time.time()
    return result, end - start

def run_tests():
    filebase = 'matrix'

    print('Wielkość\tCzas dla metody:')
    print('macierzy\tmacierzowej\tnaiwnej\t\tDFS')
    for i in range(1, 11):
        n = i * 10
        filename = filebase + str(n)
        matrix = read_matrix(filename)

        cycles1, time1 = measure_function(get_cycles_matrix_multiply, matrix)
        cycles2, time2 = measure_function(get_cycles_naive, matrix)
        cycles3, time3 = measure_function(get_cycles_dfs, matrix)

        if cycles1 != cycles2 or cycles1 != cycles3:
            print('Algorytmom wyszły różne cykle!')
            exit(1)

        print(f'{n:8}\t{time1:.5f}s\t{time2:.5f}s\t{time3:.5f}s')

if __name__ == '__main__':
    run_tests()
