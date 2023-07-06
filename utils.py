import math
from fractions import Fraction


def get_result_from_column(matrix, i):
    return [row[i] for row in matrix]




def check_simplex_method(simplex_table, n, m, max_or_min):
    out_of_bounds = 0
    for j in range(1, m):
        if simplex_table[n - 2][j] * max_or_min < out_of_bounds:
            return False
        if simplex_table[n - 2][j] == out_of_bounds and simplex_table[n - 1][j] * max_or_min < out_of_bounds:
            return False    
    return True

def print_interim_result(in_base, columns_from_simplex_table, simplex_relation, out_base, basis, enabling_element):
    print(f"Новая базисная переменная: X{in_base}")
    print("Cимплексное отношение:", end='')
    for i in range(columns_from_simplex_table - 2):
        print(simplex_relation[i], end=' ')
    print(f"\nминимальное симплексное отношение = {simplex_relation[out_base]}")
    print(f"В пересечении со строкой: X{basis[out_base] + 1}")
    print(f"Разрешающий элемент: {enabling_element}")

def type_and_inequalities(tm, tn, task):
    for j in range(tm - 2):
        if j > 0:
            print(" + ", end='')
        print(f"{task[0][j]}X{j + 1}", end='')
    print(" -> ", end='')
    if task[0][tm - 1] == 1:
        print("max")
    else:
        print("min")
    for i in range(1, tn):
        print("{ ", end='')
        for j in range(tm - 2):
            if j > 0:
                print(" + ", end='')
            print(f"{task[i][j]}X{j + 1}", end='')
        if task[i][tm - 2] == 0:
            print(" = ", end='')
        print(f"{task[i][tm - 1]}")



def print_simplex_table(simplex_table, basis, n, m):
    print(f"{1:11}|", end='')
    for i in range(m - 1):
        print(f"{'X' + str(i + 1):>8}|", end='')
    print('\n' + (84 * '='))
    for i in range(n):
        if i < n - 2:
            print(f"X{basis[i] + 1}|", end='')
        elif i == n - 2:
            print("M |", end='')
        else:
            print("Z |", end='')
        for j in range(m):
            print(f"{str(simplex_table[i][j]):>8}|", end='')
        print()
    print(84 * '=')


def calculating_new_simplex_table(simplex_table, basis, Z, M, n, m):
    for i in range(m):
        Z_string = 0
        M_string = 0
        c = get_result_from_column(simplex_table, i)
        for el in range(len(c) - 2):
            Z_string += c[el] * Z[basis[el]]
            M_string += c[el] * M[basis[el]] 
        if i > 0:
            Z_string -= Z[i - 1]
            M_string -= M[i - 1]
        simplex_table[n - 2][i] = M_string
        simplex_table[n - 1][i] = Z_string


