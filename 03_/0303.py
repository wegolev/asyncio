import asyncio

async def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

async def filter_primes(nums):
    tasks = [is_prime(n) for n in nums]
    results = await asyncio.gather(*tasks)
    return [n for n, prime in zip(nums, results) if prime]

async def main(nums):
    primes = await filter_primes(nums)
    print(primes)

nums = [int(x) for x in input().split()]
asyncio.run(main(nums))