import asyncio

# Async queues aren't thread-safe but designed for async codes.
msg_received = asyncio.Queue()


async def handle_echo(reader, writer):
    addr = writer.get_extra_info('peername')
    data = await reader.read(100)
    msg = data.decode()
    print("{} says: {}".format(addr, msg))
    writer.close()
    print("Handling {}".format(addr))
    msg_received.put_nowait(msg)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_echo, '127.0.0.1', 2222, loop=loop)
    server = loop.run_until_complete(coro)

    print('Server is listening on on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        msg = [msg_received.get_nowait() for _ in range(msg_received.qsize())]
        print("Messages received: {} ".format(msg))
        print(len(msg))

    # Cleaning up
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()