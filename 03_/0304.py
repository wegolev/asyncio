import asyncio

async def find_min(nums):
    await asyncio.sleep(1)  # Моделируем вычисления
    return min(nums)

async def main(nums):
    middle = len(nums) // 2
    tasks = [
        find_min(nums[:middle]),
        find_min(nums[middle:])
    ]
    results = await asyncio.gather(*tasks)
    print(min(results))

nums = [7, 3, 9, 4, 2, 8, 5, 1]
asyncio.run(main(nums))