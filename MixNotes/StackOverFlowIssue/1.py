def main():
    options = {
        'o1': ['1', '2', '3'],
        'o2': ['one', 'two', 'three'],
        'o3': ['uno', 'dos', 'tres']
    }

    values = []

    i = ''
    for _ in options.keys():
        print(_)
        # options[_].insert(-1, "or")
        while i not in options[_]:
            i = input(", ".join(options[_][:-1]) + ", or " + options[_][-1] + '?')
        values.append(i)

    print(values)

main()