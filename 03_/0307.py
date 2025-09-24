import asyncio

async def multiply_row(row, matrix):
    result = []
    for col in zip(*matrix):
        result.append(sum(r * c for r, c in zip(row, col)))
    return result

async def matrix_multiply(matrix1, matrix2):
    tasks = [multiply_row(row, matrix2) for row in matrix1]
    result = await asyncio.gather(*tasks)
    return result

async def main(m1, m2):
    result = await matrix_multiply(m1, m2)
    print(result)

matrix1 = [[1, 2], [3, 4]]
matrix2 = [[5, 6], [7, 8]]
asyncio.run(main(m1=matrix1, m2=matrix2))