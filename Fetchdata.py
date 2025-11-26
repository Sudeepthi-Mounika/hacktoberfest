import asyncio
import aiohttp
import time
import logging
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import lru_cache

# ──────────────────────────────────
# Logging Setup
# ──────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ──────────────────────────────────
# CPU Intensive Task (Multiprocessing)
# ──────────────────────────────────
def heavy_computation(n: int) -> int:
    """CPU heavy Fibonacci calculation"""
    if n <= 1:
        return n
    return heavy_computation(n - 1) + heavy_computation(n - 2)

# ──────────────────────────────────
# Caching for Optimization
# ──────────────────────────────────
@lru_cache(maxsize=128)
def cached_computation(n):
    return heavy_computation(n)

# ──────────────────────────────────
# Asynchronous Web Request (I/O Task)
# ──────────────────────────────────
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

# ──────────────────────────────────
# OOP Design: A Complex Pipeline
# ──────────────────────────────────
class DataEngine:

    def __init__(self, urls):
        self.urls = urls
        self.results = []

    async def fetch_all(self):
        async with aiohttp.ClientSession() as session:
            tasks = [fetch(session, url) for url in self.urls]
            return await asyncio.gather(*tasks)

    def compute_parallel(self, numbers):
        with ProcessPoolExecutor() as executor:
            return list(executor.map(cached_computation, numbers))

    async def process_pipeline(self, numbers):
        start = time.time()
        logging.info("Starting Data Pipeline 🧠")

        # Thread executor for mixed async + sync work
        loop = asyncio.get_running_loop()
        url_task = loop.create_task(self.fetch_all())

        # CPU work in parallel
        with ThreadPoolExecutor() as executor:
            compute_task = loop.run_in_executor(executor, self.compute_parallel, numbers)

        fetched_data = await url_task
        computed_data = await compute_task

        self.results = {"web_data": fetched_data, "computed_values": computed_data}
        logging.info(f"Completed in {time.time() - start:.2f} seconds 🚀")

        return self.results

# ──────────────────────────────────
# Program Execution
# ──────────────────────────────────
if __name__ == "__main__":
    urls = [
        "https://example.com",
        "https://httpbin.org/get",
        "https://jsonplaceholder.typicode.com/posts"
    ]
    numbers = [30, 32, 34]  # heavy Fibonacci jobs

    engine = DataEngine(urls)

    final_output = asyncio.run(engine.process_pipeline(numbers))
    print("\n📌 Final Output:")
    print(final_output)
