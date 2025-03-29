import asyncio

counter = 0


async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    global counter

    data = int((await reader.read()).decode('utf8'))
    counter += 1

    val = counter
    print(f'receive {data} from {val}, sleep for it')
    await writer.drain()

    await asyncio.sleep(data)
    print(f'awake from {val}')
    writer.write(str(data).encode('utf8'))
    writer.write_eof()
    await writer.drain()

    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handler, '127.0.0.1', 8080)
    await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
