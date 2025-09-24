import asyncio

tree = {
    "value": 10,
    "left": {"value": 5, "left": None, "right": None},
    "right": {"value": 20, "left": None, "right": None}
}

async def process_node(node):
    if node is None:
        return 0
    left_task = asyncio.create_task(process_node(node['left']))
    right_task = asyncio.create_task(process_node(node['right']))
    await asyncio.gather(left_task, right_task)
    return node['value'] + left_task.result() + right_task.result()

async def main(tree):
    total = await process_node(tree)
    print(f"Total sum: {total}")

asyncio.run(main(tree=tree))