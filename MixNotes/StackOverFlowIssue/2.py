def main():
    options = {
        'o1': ['1', '2', '3'],
        'o2': ['one', 'two', 'three'],
        'o3': ['uno', 'dos', 'tres']
    }

    for _ in options.keys():
        i = list((', '.join(options[_]) + '?').rpartition(","))
        i[1] = " or"
        j = ''.join(i)
        print(j)

main()