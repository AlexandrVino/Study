import asyncio
from random import randint

capacity: int = 10
tests = asyncio.Queue()
processed: asyncio.Queue[tuple[int, int]] = asyncio.Queue()
counter = [0 for item in range(capacity)]


async def process(send, data: bytes) -> int | None:
    if data == b'':
        return
    res = int(data.decode('utf-8').strip())
    await processed.put((send, res))


async def send_request():
    host, port = await tests.get()
    reader, writer = await asyncio.open_connection(host, port)

    value = randint(5, 9)
    print(f"send to server: {value}")
    writer.write(str(value).encode('utf8'))
    await writer.drain()
    writer.write_eof()

    await process(value, await reader.read(8))

    writer.close()
    await writer.wait_closed()


async def runner(identifier: int):
    print(f'start running: {identifier}')
    while not tests.empty():
        counter[identifier] += 1
        await asyncio.create_task(send_request())


async def main():
    for i in range(100):
        await tests.put(('127.0.0.1', 8000))

    await asyncio.sleep(3)
    await asyncio.gather(*(runner(i) for i in range(capacity)))
    print(*range(1, 1 + capacity), sep='\t')
    print(*counter, sep='\t')
    print(processed.empty(), processed.qsize())
    while not processed.empty():
        print(await processed.get(), end='\t')
        if processed.qsize() % capacity == 0:
            print()
    print()


if __name__ == '__main__':
    asyncio.run(main())
