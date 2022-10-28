import math


def check_prime(number, primes):
    limit = math.sqrt(number)
    for prime in primes:
        if prime > limit:
            return True
        if number % prime == 0:
            return False
    return True


def solution(i):
    primes = []
    number = 2
    while len(primes) < (i + 5):
        is_prime = check_prime(number, primes)
        if is_prime:
            primes.append(number)
        number += 1
    five_digit = "".join([str(x) for x in primes])[i : i + 5]
    return five_digit


print(solution(0))
print(solution(3))
print(solution(30))
