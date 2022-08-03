
def find_closest_elements(arr, k, x):
    abs_list = list(map(lambda n: abs(n -x), arr))
    abs_sum_min = abs_sum = sum(abs_list[0:k])
    min_i = 0
    for i in range(1, len(arr) - k + 1):
        abs_sum = abs_list[i + k - 1] + abs_sum - abs_list[i - 1]
        if abs_sum < abs_sum_min:
            abs_sum_min = abs_sum
            min_i = i
    return arr[min_i:min_i + k]


print(find_closest_elements([5, 7, 8, 9, 10, 13], k=3, x=8))  # [7, 8, 9]


print(find_closest_elements([5, 7, 8, 9, 10, 13], k=4, x=8))  # [7, 8, 9, 10]


print(find_closest_elements([5, 5, 8, 9, 10, 13], k=3, x=8))  # [8, 9, 10]


print(find_closest_elements([0, 1, 2, 2, 2, 3, 6, 9, 10], k=3, x=5))  # [2, 3, 6]


print(find_closest_elements([0, 1, 2, 2, 2, 3, 6, 8, 8, 9], k=5, x=9))  # [3, 6, 8, 8, 9]


print(find_closest_elements([0, 1, 2, 2, 2, 3, 6, 8, 8, 9], k=3, x=20))  # [8, 8, 9]
