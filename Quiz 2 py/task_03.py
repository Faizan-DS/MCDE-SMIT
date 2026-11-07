# Task 03 | Recursive JSON Path Explorer

def same_value(a, b):
    if isinstance(a, bool) != isinstance(b, bool):
        return False
    return a == b


def find_paths(data, target, current_path=""):
    paths = []

    if current_path != "" and same_value(data, target):
        paths.append(current_path)

    if isinstance(data, dict):
        for key, value in data.items():
            if current_path == "":
                new_path = str(key)
            else:
                new_path = current_path + "." + str(key)
            paths = paths + find_paths(value, target, new_path)

    elif isinstance(data, list):
        for index in range(len(data)):
            new_path = current_path + "[" + str(index) + "]"
            paths = paths + find_paths(data[index], target, new_path)

    return paths


if __name__ == "__main__":
    data = {"a": [{"x": 5}, 5], "b": {"y": 5}}
    print(find_paths(data, 5))                     
    print(find_paths({"a": True, "b": 1}, 1))     
    print(find_paths([[1, [1]], {"k": [1]}], 1))   
    print(find_paths({}, 5))                       