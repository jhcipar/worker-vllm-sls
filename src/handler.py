import sys
import multiprocessing
import traceback
import runpod
from runpod import RunPodLogger
from engine_manager import EngineManager

log = RunPodLogger()

def _create_engines():
    try:
        from engine import OpenAIvLLMEngine, vLLMEngine

        vllm_engine = vLLMEngine()
        openai_engine = OpenAIvLLMEngine(vllm_engine)
        log.info("vLLM engines initialized successfully")
        return vllm_engine, openai_engine
    except Exception as error:
        log.error(f"Worker engine initialization failed: {error}\n{traceback.format_exc()}")
        sys.exit(1)


engines = EngineManager(_create_engines)


async def handler(job):
    try:
        from utils import JobInput
        job_input = JobInput(job["input"])
        vllm_engine, openai_engine = engines.get()
        engine = openai_engine if job_input.openai_route else vllm_engine
        results_generator = engine.generate(job_input)
        async for batch in results_generator:
            yield batch
    except Exception as e:
        error_str = str(e)
        full_traceback = traceback.format_exc()

        log.error(f"Error during inference: {error_str}")
        log.error(f"Full traceback:\n{full_traceback}")

        # CUDA errors = worker is broken, exit to let RunPod spin up a healthy one
        if "CUDA" in error_str or "cuda" in error_str:
            log.error("Terminating worker due to CUDA/GPU error")
            sys.exit(1)

        yield {"error": error_str}


# Only run in main process to prevent re-initialization when vLLM spawns worker subprocesses
if __name__ == "__main__" or multiprocessing.current_process().name == "MainProcess":

    runpod.serverless.start(
        {
            "handler": handler,
            "concurrency_modifier": lambda x: engines.max_concurrency,
            "return_aggregate_stream": True,
        }
    )
