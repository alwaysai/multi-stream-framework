import time
import edgeiq
import cv2

from itertools import cycle
from .config import ClassifierAppConfig
from edgeiq._utils import empty_queue


class ClassifierApp:
    def __init__(self, args):
        self._config_filepath = args[0]
        self._app_shared = args[1]
        self._app_config = ClassifierAppConfig(self._config_filepath)
        self._process_idx = self._app_config.process_idx
        self._last_update = time.time()

        # App properties
        self._process_idx = self._app_config.process_idx
        self._app_fps = self._app_config.app_fps
        self._update_time = (
            1 / self._app_fps
        )  # Update frequency in seconds 5 fps -> 0.2 s
        self._input_folder = self._app_config.source_directory
        self._classifier_model = self._app_config.classifier_model

    def close(self):
        empty_queue(self._app_shared.frames_to_web_mp_queues[
            self._process_idx])

    def run(self):
        self._classifier = edgeiq.Classification(self._classifier_model)
        self._classifier.load(engine=edgeiq.Engine.DNN)

        self._images = sorted(edgeiq.list_images(self._input_folder))
        self._app_shared.process_barrier.wait()

        try:
            for image_path in cycle(self._images):
                self._current_time = time.time()
                elapsed_time = self._current_time - self._last_update

                if self._app_shared.process_exit.is_set():
                    break

                if elapsed_time >= self._update_time:
                    self._last_update = self._current_time

                    frame = cv2.imread(image_path)

                    results = self._classifier.classify_image(frame)

                    if results.predictions:
                        image_text = "Label: {}, {:.2f}".format(
                            results.predictions[0].label,
                            results.predictions[0].confidence,
                        )
                        cv2.putText(
                            frame,
                            image_text,
                            (5, 25),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 0, 255),
                            2,
                        )

                    # Submit frames to the queue
                    self._app_shared.frames_to_web_mp_queues[0].put(frame)

                else:
                    remaining_time = self._update_time - elapsed_time
                    time.sleep(remaining_time)

        finally:
            self.close()
