import asyncio

import runpod
from runpod import RunPodLogger

log = RunPodLogger()


async def handler(job):
    await asyncio.sleep(30)
    return {"output": job["input"]}


if __name__ == "__main__":
    log.info("Starting delayed echo worker")
    runpod.serverless.start(
        {
            "handler": handler,
            "concurrency_modifier": lambda _: 1,
        }
    )
