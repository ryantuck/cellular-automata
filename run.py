import time
import typer

cli = typer.Typer()

window_order = list(reversed(range(8)))

def binary_rep(rule_no):
    binary_vals = {}
    remainder = int(rule_no)
    denominator = 128

    for wo in window_order:

        new_remainder = remainder % denominator

        if new_remainder == remainder:
            binary_vals[wo] = 0
        else:
            binary_vals[wo] = 1

        remainder = new_remainder
        denominator = denominator / 2

    return binary_vals


def calculate_cell(rule_no, window):
    """
    """
    binary_vals = binary_rep(rule_no)
    window_value = 4*window[0] + 2*window[1] + 1*window[2]
    return binary_vals[window_value]


def iterate(rule_no, current_line, left_side, right_side):
    """
    """
    new_line = []

    window = [left_side, current_line[0], current_line[1]]
    cell_val = calculate_cell(rule_no, window)
    new_line.append(cell_val)

    for idx in range(len(current_line)-2):
        window = current_line[idx:idx+3]
        cell_val = calculate_cell(rule_no, window)
        new_line.append(cell_val)

    window = [current_line[-2], current_line[-1], right_side]
    cell_val = calculate_cell(rule_no, window)
    new_line.append(cell_val)

    return new_line


def print_line(line, symbols, delimiter=''):
    symbolic_line = [symbols[x] for x in line]
    print(delimiter.join(symbolic_line))


@cli.command()
def run(rule_no, seed, left_side, right_side, sleep_ms, symbols, iterations):
    """
    Run
    """

    # supports binary notation or wolfram rule numbers
    if len(rule_no) == 8:
        binary_rule = rule_no
    else:
        binary_rule = ''.join(str(x) for x in binary_rep(int(rule_no)).values())

    current_line = [int(x) for x in list(seed)]
    left_side = int(left_side)
    right_side = int(right_side)
    sleep_ms = int(sleep_ms)
    iterations = int(iterations)


    config = {'rule_no': rule_no, 'binary_rule': binary_rule, 'seed_length': len(seed), 'sides': f'{left_side}{right_side}', 'symbols': symbols, 'iterations': iterations}
    print(config)

    for _ in range(iterations):
        print_line(current_line, symbols)
        current_line = iterate(rule_no, current_line, left_side, right_side)
        time.sleep(sleep_ms / 1000)


@cli.command()
def howto():
    """
    Print howto
    """
    print('TODO')

if __name__ == '__main__':
    cli()
