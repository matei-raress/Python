import asyncio

 #calcul simultan pentru 4 valori diferite ale lui n luate dintr-o coada de catre 4 corutine

async def sum(queue):
    n = await queue.get()
    s = n * (n + 1) / 2
    print("Sum is equal to: " + str(s))


async def main():
    queue = asyncio.Queue()
    queue.put_nowait(5)
    queue.put_nowait(17)
    queue.put_nowait(10)
    queue.put_nowait(7)

    await asyncio.gather(
        sum(queue),
        sum(queue),
        sum(queue),
        sum(queue)
    )


if __name__ == '__main__':
    asyncio.run(main())
