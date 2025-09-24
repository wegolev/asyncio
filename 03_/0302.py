import asyncio

async def count_words(filename):
    with open(filename) as f:
        file_content = f.read()
    return len(file_content.split())

async def main(files):
    tasks = [count_words(filename) for filename in files]
    word_counts = await asyncio.gather(*tasks)
    print(sum(word_counts))

files = input().split()
asyncio.run(main(files))