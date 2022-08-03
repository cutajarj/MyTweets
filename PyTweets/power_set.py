def power_set(input_set):
    for i in range(2 ** len(input_set)):
        sub_set = []
        for j in range(len(input_set)):
            if i & (2 ** j):
                sub_set.append(input_set[j])
        print(sub_set)


power_set(['a', 'b', 'c'])
