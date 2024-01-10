import multiprocessing
import edgeiq
from edgeiq._utils import MultiprocessingCircularQueue


class AppShared:
    """Process-safe shared memory and objects"""

    def __init__(self):
        self.queue_depth = 5
        self.process_count = 2
        self._tx_queue = MultiprocessingCircularQueue(self.queue_depth)
        self.process_barrier = multiprocessing.Barrier(
            self.process_count + 1
        )  # adding 1 for the barrier in dashboard UI/Server.
        self.frames_to_web_mp_queues = [
            edgeiq._utils.MultiprocessingCircularQueue(self.queue_depth)
            for _ in range(self.process_count)
        ]  # adding 1 for the face registration application
        self.process_exit = multiprocessing.Event()
        self.application_logqueue = multiprocessing.Queue()
        self.application_errorqueue = multiprocessing.Queue()
