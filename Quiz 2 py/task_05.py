# Task 05 | Expression Validator and Evaluator (uses stacks, no eval / ast)

PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "neg": 3}


def tokenize(text):
    if not isinstance(text, str):
        raise ValueError("Expression must be a string")

    tokens = []
    number = ""
    for ch in text:
        if ch in "0123456789":
            number = number + ch
        else:
            if number != "":
                tokens.append(int(number))
                number = ""
            if ch in " \t\n":
                continue
            elif ch in "+-*/()":
                tokens.append(ch)
            else:
                raise ValueError("Invalid character: " + ch)
    if number != "":
        tokens.append(int(number))
    return tokens


def apply_top_operator(numbers, operators):
    op = operators.pop()

    if op == "neg":                      
        if len(numbers) < 1:
            raise ValueError("Malformed expression")
        numbers.append(-numbers.pop())
        return

    if len(numbers) < 2:                  
        raise ValueError("Malformed expression")
    right = numbers.pop()
    left = numbers.pop()

    if op == "+":
        numbers.append(left + right)
    elif op == "-":
        numbers.append(left - right)
    elif op == "*":
        numbers.append(left * right)
    else:
        if right == 0:
            raise ValueError("Division by zero")
        numbers.append(left / right)


def calculate(expression):
    tokens = tokenize(expression)
    if len(tokens) == 0:
        raise ValueError("Empty expression")

    numbers = []       
    operators = []     
    expect_number = True   

    for token in tokens:
        if isinstance(token, int):
            if not expect_number:
                raise ValueError("Malformed expression: missing operator")
            numbers.append(token)
            expect_number = False

        elif token == "(":
            if not expect_number:
                raise ValueError("Malformed expression: missing operator")
            operators.append("(")

        elif token == ")":
            if expect_number:
                raise ValueError("Malformed expression: missing number")
            while len(operators) > 0 and operators[-1] != "(":
                apply_top_operator(numbers, operators)
            if len(operators) == 0:
                raise ValueError("Unbalanced parentheses")
            operators.pop()              

        else:  
            if expect_number:           
                if token == "-":
                    operators.append("neg")
                elif token == "+":
                    pass                 
                else:
                    raise ValueError("Malformed expression")
            else:
                while (len(operators) > 0 and operators[-1] != "("
                       and PRECEDENCE[operators[-1]] >= PRECEDENCE[token]):
                    apply_top_operator(numbers, operators)
                operators.append(token)
                expect_number = True

    if expect_number:
        raise ValueError("Malformed expression: ends with an operator")

    while len(operators) > 0:
        if operators[-1] == "(":
            raise ValueError("Unbalanced parentheses")
        apply_top_operator(numbers, operators)

    return numbers[0]


if __name__ == "__main__":
    print(calculate("-(3 + 2) * 4 + 18 / 3"))   # -14.0
    print(calculate(" 2 * -3 "))                # -6
    for bad in ["", "1 +", "(1 + 2", "1 + 2)", "4 / 0", "2 $ 3", "1 2", "0x10"]:
        try:
            print(bad, "->", calculate(bad))
        except ValueError as error:
            print(repr(bad), "-> Error:", error)