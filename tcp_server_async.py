"""
TCP server with asyncIO
"""
import asyncio


msg_received = []


async def handle(reader, writer):
    addr = writer.get_extra_info('peername')
    data = await reader.read(100)
    print("Handling {}".format(addr))
    msg = data.decode()
    msg_received.append(msg)
    writer.close()
    print("{} says: {}".format(addr, msg))


async def driver(host, port):
    server = await asyncio.start_server(handle, host, port)
    print('Server is listening on on {}'.format(server.sockets[0].getsockname()))
    await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(driver('127.0.0.1', 2222))
    except KeyboardInterrupt:
        print("Messages received: {} ".format(msg_received))
        print(len(msg_received))
