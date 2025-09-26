# This function reads dimacs files & creates the clauses by it
import sys


def read_dimacs(filename):
    clauses = []
    num_vars = num_clauses = 0

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('c') or line == '':
                # Skip comments and empty lines
                continue
            elif line.startswith('p'):
                # Problem definition line
                parts = line.split()
                if parts[1] == 'cnf':
                    num_vars = int(parts[2])
                    num_clauses = int(parts[3])
            else:
                # Clause line
                clause = list(map(int, line.split()))
                if clause[-1] == 0:
                    clause = clause[:-1]  # Remove the trailing 0
                clauses.append(clause)

    return num_vars, num_clauses, clauses
#------------------------------------------------------------------------------------------------------#

def vertex_bool_val(num_vars, clauses):
    vertex_vals_arr = [0] * (num_vars)
    # go over each vertex
    for num in range(num_vars):
        val = 0
        # go over clauses
        for clause in clauses:
            val = val << 1
            if clause[num] > 0:
                val += 1
        vertex_vals_arr[num] = val
    return vertex_vals_arr


def calculate_block(vertex_vals):
    num_rows = 0
    for val in vertex_vals:
        num_rows += val

    sorted_vertex_vals = sorted(vertex_vals)
    print(sorted_vertex_vals)

    curr_row = sorted_vertex_vals[0]
    #curr_col = 0
    split_junctions = []
    reset_false_junctions = []
    # add split junction to 0,0
    split_junctions.append([0,0])
    sorted_vertex_vals.pop(0)

    for number in sorted_vertex_vals:
        print(f"number is {number}")
        print(f"row is {curr_row}")

        # logic
        for curr_col in range(curr_row+1):
            if(number & curr_col) != 0: # if overlapping
                # find reset false
                reset_false_col = number | curr_col
                reset_false_row = curr_row + reset_false_col - curr_col
                reset_false_junctions.append([reset_false_row, reset_false_col])
                # check position of reset false
                # if different than currrow, currcol, add split
                if (reset_false_row != curr_row) and (reset_false_col != curr_col):
                    split_junctions.append([curr_row, curr_col])
            else:
                split_junctions.append([curr_row, curr_col])
        curr_row += number

    print(split_junctions)
    print(reset_false_junctions)
    return split_junctions, reset_false_junctions


def save_results(output_file, split_arr, reset_arr, vertex_vals):
    header = str(vertex_vals[0])
    vertex_vals.pop(0)
    for val in vertex_vals:
        header += " + " + str(val)
    print(header)

    with open(output_file, "w") as file:
        file.write(header + "\n")
        file.write(f"[x,y] in {split_arr}\n")
        file.write(f"[x,y] in {reset_arr}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Dimacs file required")
        sys.exit()

    # Dimacs file to load
    filename = sys.argv[1]
    num_vars, num_clauses, clauses = read_dimacs(filename)

    # ----Print for verification----
    print(f"Number of variables: {num_vars}")
    print(f"Number of clauses: {num_clauses}")
    print("Clauses:")
    for clause in clauses:
        print(clause)

    vertex_vals = vertex_bool_val(num_vars, clauses)
    print(f"\nvertex values: {vertex_vals}")

    split_juncs, reset_false_juncs = calculate_block(vertex_vals)

    save_results("output.txt", split_juncs, reset_false_juncs, vertex_vals)
