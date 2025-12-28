import subprocess
from threading import Thread
from typing import Callable


class DownloadManager(Thread):
    def __init__(self, command_list: list[str], stdout_callback: Callable[[str], None], download_complete_callback: Callable[[], None]):
        self._command_list = command_list
        self._stdout_callback = stdout_callback
        self._download_complete_callback = download_complete_callback
        super().__init__()

    def run(self):
        process = subprocess.Popen(self._command_list, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            self._stdout_callback(line)

        self._download_complete_callback()

