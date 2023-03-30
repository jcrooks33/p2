from math import ceil, floor
from random import randint
import sys

def add_matrices(matrix_a, matrix_b):
    result_matrix = []
    for i in range(len(matrix_a)):
        row = []
        for j in range(len(matrix_a[0])):
            row.append(matrix_a[i][j] + matrix_b[i][j])
        result_matrix.append(row)
    return result_matrix


def subtract_matrices(matrix_a, matrix_b):
    result_matrix = []
    for i in range(len(matrix_a)):
        row = []
        for j in range(len(matrix_a[0])):
            row.append(matrix_a[i][j] - matrix_b[i][j])
        result_matrix.append(row)
    return result_matrix

def multiply_matrices(matrix_a, matrix_b):
    # Transpose matrix_b to make it easier to iterate over columns
    transposed_b = list(zip(*matrix_b))
    result_matrix = []
    for i in range(len(matrix_a)):
        row = []
        for j in range(len(transposed_b)):
            # Multiply corresponding elements of row i in matrix_a and column j in transposed_b and sum them up
            product_sum = sum([matrix_a[i][k] * transposed_b[j][k] for k in range(len(matrix_a[0]))])
            row.append(product_sum)
        result_matrix.append(row)
    return result_matrix

def read_file(filename, d):
    dims = range(d)
    a = [[0 for i in dims] for j in dims]
    b = [[0 for i in dims] for j in dims]
    with open(filename) as f:
        i = 0
        j = 0
        for line in f:
            if i < 2*d:
                if i < d:
                    a[i][j] = int(line.strip())
                else:
                    b[i-d][j] = int(line.strip())
                j += 1
                if j > d-1:
                    j = 0
                    i += 1
    return a, b

def strassens(a, b, crossover=2):
    n = len(a)

    # base case
    if n <= crossover:
        return multiply_matrices(a, b)

    # recursive case
    else:
        range_n = range(n)
        # if not a power of 2
        if n%2 != 0:
            # find next power of 2
            new_n = n + 1

            # pad with zeroes
            a = [a[i] + [0] for i in range_n] + [[0] * new_n]
            b = [b[i] + [0] for i in range_n] + [[0] * new_n]

        else:
            new_n = n

        split_idx = new_n // 2

# Define ranges for the first and second halves of the matrices
        first_half_range = range(0, split_idx)
        second_half_range = range(split_idx, new_n)

# Define sub-matrices
        A = [a[i][:split_idx] for i in first_half_range]
        B = [a[i][split_idx:new_n] for i in first_half_range]
        C = [a[i][:split_idx] for i in second_half_range]
        D = [a[i][split_idx:new_n] for i in second_half_range]
        E = [b[i][:split_idx] for i in first_half_range]
        F = [b[i][split_idx:new_n] for i in first_half_range]
        G = [b[i][:split_idx] for i in second_half_range]
        H = [b[i][split_idx:new_n] for i in second_half_range]
        # sub-multiplications
        P1 = strassens(A, subtract_matrices(F, H), crossover=crossover)
        P2 = strassens(add_matrices(A, B), H, crossover=crossover)
        P3 = strassens(add_matrices(C, D), E, crossover=crossover)
        P4 = strassens(D, subtract_matrices(G, E), crossover=crossover)
        P5 = strassens(add_matrices(A, D), add_matrices(E, H), crossover=crossover)
        P6 = strassens(subtract_matrices(B, D), add_matrices(G, H), crossover=crossover)
        P7 = strassens(subtract_matrices(A, C), add_matrices(E, F), crossover=crossover)

        # combine results
        intermediate_matrix_1 = subtract_matrices(add_matrices(P5, P4), P2)
        intermediate_matrix_2 = add_matrices(intermediate_matrix_1, P6)
        intermediate_matrix_3 = add_matrices(P1, P2)
        result = list(map(lambda x,y: x + y, intermediate_matrix_2, intermediate_matrix_3))

        # Compute intermediate matrices using add_matrices and subtract_matrices
        intermediate_matrix_4 = add_matrices(P5, P1)
        intermediate_matrix_5 = subtract_matrices(intermediate_matrix_4, P3)
        intermediate_matrix_6 = subtract_matrices(intermediate_matrix_5, P7)
        intermediate_matrix_7 = add_matrices(P3, P4)

        # Use map to apply element-wise addition to intermediate_matrix_4 and intermediate_matrix_3
        result_matrix = list(map(lambda x, y: x + y, intermediate_matrix_6, intermediate_matrix_7))
        result.extend(result_matrix)
        return [result[i][:n]for i in range_n]


if __name__ == "__main__":
    flag = int(sys.argv[1])
    dimension = int(sys.argv[2])
    filename = sys.argv[3]

    a, b = read_file(filename, dimension)

    product = strassens(a, b, crossover=128)

    for i in range(dimension):
        print(product[i][i])