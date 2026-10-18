def counting_sort(arr):
  
    if not arr:
        return []
    lo = min(arr)
    k = max(arr) - lo                     
    count = [0] * (k + 1)               
    output = [0] * len(arr)               

    for x in arr:                    
        count[x - lo] += 1
    for i in range(1, k + 1):              
        count[i] += count[i - 1]
    for i in range(len(arr) - 1, -1, -1): 
        j = arr[i] - lo
        count[j] -= 1
        output[count[j]] = arr[i]
    return output

def _counting_sort_by_digit(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10                       # digits 0..9
    for x in arr:
        count[(x // exp) % 10] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    for i in range(n - 1, -1, -1):         # stable
        d = (arr[i] // exp) % 10
        count[d] -= 1
        output[count[d]] = arr[i]
    return output


def _radix_non_negative(arr):
    if not arr:
        return []
    exp = 1
    biggest = max(arr)
    while biggest // exp > 0:             
        arr = _counting_sort_by_digit(arr, exp)
        exp *= 10
    return arr


def radix_sort(arr):
    
    neg = [-x for x in arr if x < 0]
    pos = [x for x in arr if x >= 0]
    neg_sorted = [-x for x in reversed(_radix_non_negative(neg))]
    return neg_sorted + _radix_non_negative(pos)

def insertion_sort(bucket):
    for i in range(1, len(bucket)):
        key = bucket[i]
        j = i - 1
        while j >= 0 and bucket[j] > key:
            bucket[j + 1] = bucket[j]
            j -= 1
        bucket[j + 1] = key
    return bucket


def bucket_sort(arr):
   
    n = len(arr)
    if n == 0:
        return []
    buckets = [[] for _ in range(n)]
    for x in arr:
        buckets[int(n * x)].append(x)      # needs 0 <= x < 1
    result = []
    for b in buckets:
        result.extend(insertion_sort(b))
    return result

if __name__ == '__main__':
    a = [-5, -10, 0, -3, 8, 5, -1, 10]
    print('Counting sort')
    print('  Input :', a)
    print('  Output:', counting_sort(a))
    assert counting_sort(a) == [-10, -5, -3, -1, 0, 5, 8, 10]

    b = [110, 45, 65, 50, 90, 602, 24, 2, 66]
    print('\nRadix sort')
    print('  Input :', b)
    print('  Output:', radix_sort(b))
    assert radix_sort(b) == [2, 24, 45, 50, 65, 66, 90, 110, 602]

    c = [0.897, 0.565, 0.656, 0.1234, 0.665, 0.3434]
    print('\nBucket sort')
    print('  Input :', c)
    print('  Output:', bucket_sort(c))
    assert bucket_sort(c) == [0.1234, 0.3434, 0.565, 0.656, 0.665, 0.897]

    # extra checks against the built-in sort
    import random
    for _ in range(300):
        xs = [random.randint(-50, 50) for _ in range(random.randint(0, 40))]
        assert counting_sort(xs) == sorted(xs)
        assert radix_sort(xs) == sorted(xs)
        fs = [random.random() for _ in range(random.randint(0, 40))]
        assert bucket_sort(fs) == sorted(fs)
    print('\nAll tests passed.')