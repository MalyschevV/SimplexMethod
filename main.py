import math
from fractions import Fraction
from utils import *

ZLP = [list(map(Fraction, line.split())) for line in open(r"input.txt")]

def main():
   
    infinity_basis = 1
    iteration_of_simplex_method = 0
    
    number_of_lines = len(ZLP)
    number_of_cols = len(ZLP[0])

    type_and_inequalities(number_of_cols, number_of_lines, ZLP)
    
    numbers_of_variables = number_of_cols - 2  
    nums = number_of_lines - 1  
    max_or_min = ZLP[0][number_of_cols - 1]  
    add_variables_from_simplex_table = 0
    artificial_basis_amount = 0

    for i in range(1, number_of_lines):
        if ZLP[i][number_of_cols - 2] == 1:
            add_variables_from_simplex_table += 2
            artificial_basis_amount += 1
        if ZLP[i][number_of_cols - 2] == 0:
            add_variables_from_simplex_table += 1
            artificial_basis_amount += 1
        if ZLP[i][number_of_cols - 2] == -1:
            add_variables_from_simplex_table += 1

    columns_from_simplex_table = nums + 2  
    rows_from_simplex_table = number_of_cols + add_variables_from_simplex_table - 1  
    
    simplex_table = [[Fraction(0) for x in range(rows_from_simplex_table)] for y in range(columns_from_simplex_table)]  

    for i in range(number_of_lines - 1):
        simplex_table[i][0] = ZLP[i + 1][number_of_cols - 1]
    for i in range(number_of_lines):
        for j in range(number_of_cols - 2):
            simplex_table[i - 1][j + 1] = ZLP[i][j]

    Z_string_from_table = [Fraction(0) for x in range(rows_from_simplex_table - 1)]  
    M_string_from_table = [Fraction(0) for x in range(rows_from_simplex_table - 1)]  

    for i in range(numbers_of_variables):
        Z_string_from_table[i] = ZLP[0][i]

    artificial_basis = [Fraction(0) for x in range(artificial_basis_amount)]  
    k = 0
    j = number_of_cols - 1
    for i in range(1, columns_from_simplex_table - 1):
        if ZLP[i][number_of_cols - 2] == 1:
            simplex_table[i - 1][j] = Fraction(-1)
            j += 1
            artificial_basis[k] = j
            k += 1
            simplex_table[i - 1][j] = Fraction(1)
            j += 1
            M_string_from_table[j - 2] = -1 * max_or_min
        if ZLP[i][number_of_cols - 2] == 0:
            M_string_from_table[j - 1] = -1 * max_or_min
            artificial_basis[k] = j
            k += 1
            simplex_table[i - 1][j] = Fraction(1)
            j += 1
        if ZLP[i][number_of_cols - 2] == -1:
            simplex_table[i - 1][j] = Fraction(1)
            j += 1

    basis = [Fraction(0) for x in range(nums)] 
    k = 0
    for j in range(rows_from_simplex_table):
        summ = 0
        quan = 0
        for i in range(columns_from_simplex_table - 2):
            summ += simplex_table[i][j]
            if simplex_table[i][j] != 0:
                quan += 1
        if summ == 1 and quan == 1:
            basis[k] = j - 1
            k += 1

    calculating_new_simplex_table(simplex_table, basis, Z_string_from_table, M_string_from_table, columns_from_simplex_table, rows_from_simplex_table)
    print(f"Итерация: {iteration_of_simplex_method}")
    print_simplex_table(simplex_table, basis, columns_from_simplex_table, rows_from_simplex_table)

    while check_simplex_method(simplex_table, columns_from_simplex_table, rows_from_simplex_table, max_or_min) == False: 
        in_base = 1
        for i in range(2, rows_from_simplex_table):
            if simplex_table[columns_from_simplex_table - 2][i] * max_or_min < simplex_table[columns_from_simplex_table - 2][in_base] * max_or_min:
                in_base = i
            if simplex_table[columns_from_simplex_table - 2][i] == simplex_table[columns_from_simplex_table - 2][in_base] \
                    and simplex_table[columns_from_simplex_table - 1][i] * max_or_min < simplex_table[columns_from_simplex_table - 1][in_base] * max_or_min:
                in_base = i

        simplex_relation = [Fraction(0) for x in range(columns_from_simplex_table - 2)] 
        for i in range(columns_from_simplex_table - 2):
            if simplex_table[i][in_base] <= 0:
                simplex_relation[i] = -math.inf
                continue
            simplex_relation[i] = simplex_table[i][0] / simplex_table[i][in_base]

        out_base = -1
        for i in range(columns_from_simplex_table - 2):
            if simplex_relation[i] >= 0:
                if out_base == -1:
                    out_base = i
                    continue
                if simplex_relation[i] < simplex_relation[out_base]:
                    out_base = i
                    continue
                if simplex_relation[i] == simplex_relation[out_base]:
                    pass
        if out_base == -1:
            break

        enabling_element = simplex_table[out_base][in_base]  
        
        print_interim_result(in_base, columns_from_simplex_table, simplex_relation, out_base, basis, enabling_element)

        m_ = [[0 for x in range(rows_from_simplex_table)] for y in range(columns_from_simplex_table - 2)]
        for i in range(columns_from_simplex_table - 2):
            for j in range(rows_from_simplex_table):
                m_[i][j] = simplex_table[i][j]
        for i in range(columns_from_simplex_table - 2):
            for j in range(rows_from_simplex_table):
                if i == out_base:
                    simplex_table[i][j] = m_[i][j] / enabling_element
                else:
                    simplex_table[i][j] = m_[i][j] - m_[i][in_base] * m_[out_base][j] / enabling_element
        basis[out_base] = in_base - 1
        calculating_new_simplex_table(simplex_table, basis, Z_string_from_table, M_string_from_table, columns_from_simplex_table, rows_from_simplex_table)
        iteration_of_simplex_method += 1
        print(f"Итерация: {iteration_of_simplex_method}")
        print_simplex_table(simplex_table, basis, columns_from_simplex_table, rows_from_simplex_table)

    if check_simplex_method(simplex_table, columns_from_simplex_table, rows_from_simplex_table, max_or_min) == False:
        print("Нет ответа, в Z_string_from_table строке отрицательные элементы!")
        exit(0)

    for i in range(columns_from_simplex_table - 2):
        for j in range(artificial_basis_amount):
            if basis[i] + 1 == artificial_basis[j] and simplex_table[i][0] != 0:
                print("Нет ответа, в М строке есть ненулевые значения")
                print(f"X{basis[i] + 1} = {simplex_table[i][0]}")
                exit(0)

    print("\nРешение:")
    print(72 * '+')
    for i in range(columns_from_simplex_table - 2):
        if basis[i]  >= numbers_of_variables:
            print(" ! ", end='')
        print(f"X{basis[i] + 1} = {simplex_table[i][0]}")
    print(f"Z = {simplex_table[columns_from_simplex_table-1][0]}")
    print(84 * '+')


    secondAnswer = 0
    
    for j in range(1, infinity_basis + 1):
        if simplex_table[columns_from_simplex_table-1][j] == 0:
            secondAnswer = secondAnswer+1
            
    
    for x in range(1, rows_from_simplex_table):
        for i in range(x, rows_from_simplex_table):
            for j in range (0, columns_from_simplex_table-3):
                if simplex_table[j][i]!=0 and simplex_table[j][i]!=1 and simplex_table[columns_from_simplex_table - 1][i]==0:
                    in_base = i
                    break
            if simplex_table[j][i]!=0 and simplex_table[j][i]!=1:
                break
            
        simplex_relation = [Fraction(0) for x in range(columns_from_simplex_table - 2)] 
        for i in range(columns_from_simplex_table - 2):
            if simplex_table[i][in_base] <= 0:
                simplex_relation[i] = -math.inf
                continue
            simplex_relation[i] = simplex_table[i][0] / simplex_table[i][in_base]

        out_base = -1
        for i in range(columns_from_simplex_table - 2):
            if simplex_relation[i] >= 0:
                if out_base == -1:
                    out_base = i
                    continue
                if simplex_relation[i] < simplex_relation[out_base]:
                    out_base = i
                    continue
                if simplex_relation[i] == simplex_relation[out_base]:
                    pass

        enabling_element = simplex_table[out_base][in_base] 
        if enabling_element!=1:
            break
    
    print_interim_result(in_base, columns_from_simplex_table, simplex_relation, out_base, basis, enabling_element)
    
    m_ = [[0 for x in range(rows_from_simplex_table)] for y in range(columns_from_simplex_table - 2)]
    for i in range(columns_from_simplex_table - 2):
        for j in range(rows_from_simplex_table):
            m_[i][j] = simplex_table[i][j]
    for i in range(columns_from_simplex_table - 2):
        for j in range(rows_from_simplex_table):
            if i == out_base:
                simplex_table[i][j] = m_[i][j] / enabling_element
            else:
                simplex_table[i][j] = m_[i][j] - m_[i][in_base] * m_[out_base][j] / enabling_element
    basis[out_base] = in_base - 1
    calculating_new_simplex_table(simplex_table, basis, Z_string_from_table, M_string_from_table, columns_from_simplex_table, rows_from_simplex_table)
    iteration_of_simplex_method += 1
    print(f"Итерация: {iteration_of_simplex_method}")
    print_simplex_table(simplex_table, basis, columns_from_simplex_table, rows_from_simplex_table)

    if check_simplex_method(simplex_table, columns_from_simplex_table, rows_from_simplex_table, max_or_min) == False:
        print("Нет ответа, в Z_string_from_table строке отрицательные элементы!")
        exit(0)

    for i in range(columns_from_simplex_table - 2):
        for j in range(artificial_basis_amount):
            if basis[i] + 1 == artificial_basis[j] and simplex_table[i][0] != 0:
                print("Нет ответа, в М строке есть ненулевые значения!")
                print(f"X{basis[i] + 1} = {simplex_table[i][0]}")
                exit(0)

    print("\nРешение:")
    print(72 * '+')
    for i in range(columns_from_simplex_table - 2):
        if basis[i]  >= numbers_of_variables:
            print(" ! ", end='')
        print(f"X{basis[i] + 1} = {simplex_table[i][0]}")
    print(f"Z = {simplex_table[columns_from_simplex_table-1][0]}")
    print(96 * '+')


if __name__ == '__main__':
	main()