import asyncio

async def square(num):
    await asyncio.sleep(1)
    return num * num

async def main(nums):
    tasks = [square(n) for n in nums]
    results = await asyncio.gather(*tasks)
    print(sum(results))

asyncio.run(main([1, 2, 3, 4, 5]))