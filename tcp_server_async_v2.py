"""
# Self-assessment 3/5

I have already dealt with TCP servers in python, but my needs were so small that synchronous
single threaded servers were enough for me. They were either installed as:
- embedded server on small devices (no need to worry about scaling/concurrency)
- centralized servers gathering data sent sporadically from less than
  a thousand of remote device. Traffic was very low.
For the centralized server, I was running multithreaded flask servers.

I picked up asyncio over threading because scaling up is easier and lighter on the CPU than
dealing with threads. Asyncio is also simpler for avoiding race conditions.

Ex: here msg_received is a list whereas I should have used a thread-safe queue for a multithreading
server.
"""
import asyncio


msg_received = []


async def handle(reader, writer):
    addr = writer.get_extra_info('peername')
    data = await reader.read(100)
    msg = data.decode()
    msg_received.append(msg)
    writer.close()
    print("Handling {}".format(addr))
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
