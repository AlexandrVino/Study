import asyncio

counter = 0


async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    global counter

    data = int((await reader.read(8)).decode('utf8'))
    counter += 1

    val = counter
    print(f'receive {data} from {val}, sleep for it')

    await asyncio.sleep(data)

    print(f'awake from {val}')
    writer.write(str(data).encode('utf8'))
    await writer.drain()

    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handler, '127.0.0.1', 8000)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
