import multiprocessing
from edgeiq._utils import MultiprocessingCircularQueue


class AppShared:
    """Process-safe shared memory and objects"""

    def __init__(self, stream_count: int):
        self.process_barrier = multiprocessing.Barrier(
            stream_count + 1
        )  # adding 1 for the barrier in dashboard UI/Server.

        self.queue_depth = 5
        self.frames_to_web_mp_queues = [
            MultiprocessingCircularQueue(self.queue_depth)
            for _ in range(stream_count)
        ]

        self.process_exit = multiprocessing.Event()
