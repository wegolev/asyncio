import asyncio

async def multiply_row(row_a, matrix_b):
    """
    Асинхронно умножает одну строку матрицы A на матрицу B.

    Args:
        row_a (list): Одна строка матрицы A.
        matrix_b (list[list]): Матрица B.

    Returns:
        list: Строка результирующей матрицы C.
    """
    await asyncio.sleep(0) 
    
    cols_b = len(matrix_b[0]) if matrix_b else 0
    result_row = [0] * cols_b
    
    for j in range(cols_b):
        dot_product = 0
        for k in range(len(row_a)):
            dot_product += row_a[k] * matrix_b[k][j]
        result_row[j] = dot_product
    return result_row

async def multiply_matrices_async(matrix_a, matrix_b):
    """
    Асинхронно умножает две матрицы, обрабатывая строки матрицы A параллельно.

    Args:
        matrix_a (list[list]): Первая матрица.
        matrix_b (list[list]): Вторая матрица.

    Returns:
        list[list] or None: Результирующая матрица C, или None, если матрицы нельзя умножить.
    """
    rows_a = len(matrix_a)
    cols_a = len(matrix_a[0]) if rows_a > 0 else 0
    rows_b = len(matrix_b)
    cols_b = len(matrix_b[0]) if rows_b > 0 else 0

    # Проверка возможности умножения матриц
    if cols_a != rows_b:
        print("Ошибка: Невозможно умножить матрицы. Количество столбцов первой матрицы не равно количеству строк второй.")
        return None

    tasks = []
    for row_a in matrix_a:
        task = asyncio.create_task(multiply_row(row_a, matrix_b))
        tasks.append(task)

    result_matrix = await asyncio.gather(*tasks)

    return result_matrix

async def main():
    matrix_a = [
        [1, 2, 3],
        [4, 5, 6]
    ]

    matrix_b = [
        [7, 8],
        [9, 10],
        [11, 12]
    ]

    print("Матрица A:")
    for row in matrix_a:
        print(row)

    print("\nМатрица B:")
    for row in matrix_b:
        print(row)

    result = await multiply_matrices_async(matrix_a, matrix_b)

    if result:
        print("\nРезультат умножения (Матрица C = A * B):")
        for row in result:
            print(row)

    matrix_c = [
        [1, 2],
        [3, 4]
    ]
    matrix_d = [
        [5, 6, 7],
        [8, 9, 10]
    ]
    print("\n--- Пример с невозможностью умножения ---")
    print("Матрица C:")
    for row in matrix_c:
        print(row)
    print("\nМатрица D:")
    for row in matrix_d:
        print(row)
    await multiply_matrices_async(matrix_c, matrix_d)

if __name__ == "__main__":
    asyncio.run(main())
