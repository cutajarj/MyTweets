def binary_search2(numbers, i)
  left, right = 0, numbers.size - 1
  while left <= right
    mid = ((left + right) / 2).floor
    left = mid + 1 if numbers[mid] < i
    right = mid - 1 if numbers[mid] > i
    return true if numbers[mid] == i
  end
  false
end





def binary_search(list, i, left = 0, right = list.size - 1)
  return false if left > right
  mid = (left + right) / 2
  return binary_search(list, i, mid + 1, right) if list[mid] < i
  return binary_search(list, i, left, mid - 1) if list[mid] > i
  true
end

puts(binary_search([1,2,3,4,5,6], 1))
puts(binary_search([1,2,3,4,5,6], 7))




puts(binary_search([1,2,3,4,5], 3))

puts(binary_search([1,2,3,4,5], 5))

puts(binary_search([1,2,3,4,5], 4))

puts(binary_search([1,2,3,4,5], 11))
