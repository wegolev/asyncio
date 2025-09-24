import asyncio

async def delay_and_append(result_list, value):
    await asyncio.sleep(value)
    result_list.append(value)

async def main():
    input_str = input()
    numbers = list(map(int, input_str.split(',')))
    result_list = []
    tasks = [delay_and_append(result_list, num) for num in numbers]
    await asyncio.gather(*tasks)

    print(result_list)

if __name__ == "__main__":
    asyncio.run(main())