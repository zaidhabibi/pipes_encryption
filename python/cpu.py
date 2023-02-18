#!/usr/bin/env python

import sys
import asyncio

async def main():
    mem = await asyncio.subprocess.create_subprocess_exec(
            "python", "mem.py", stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE
                        )
    for i in range(10,0,-1):
        mem.stdin.write(bytes("write\n"+str(i)+"\n",'utf-8'))
        sys.stdout.write("Set to ")
        mem.stdin.write(b"read\n")
        tmp = await mem.stdout.readline()
        print(int(tmp.rstrip()))

    mem.stdin.write(b"halt\n")

    await mem.wait()

asyncio.run(main())
