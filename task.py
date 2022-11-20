import os
import json
import convert
from math import ceil
from boto3.s3.transfer import TransferConfig


def calculate_thread_count():
    file = json.load(open("conf.json"))
    thread_count = int(ceil(int(file["speed"])/2))
    print("Thread Count: {}".format(thread_count))
    return thread_count


class Task:
    def __init__(self, directory, key, season, filetype, s3class, taskname, start):
        self.queue = None
        self.directory = directory
        self.prefix = key
        self.season = season
        self.filetype = filetype
        self.s3class = s3class
        self.task_name = taskname
        self.episode_start = int(start)
        self.total_size = 0

        # Determine Thread Count, SEA -> USWest per thread speed is about 2Mbps.
        self.threshold = calculate_thread_count()

        self.read_data()
        # 1GB Chunk Size Default
        # 100Mbps -> 2Mbps Per Thread by Default. ~50 Threads Optimal.
        self.chunk_size = 134217728
        self.calculate_chunk_size()
        self.transfer_configuration = TransferConfig(max_concurrency=self.threshold, multipart_chunksize=self.chunk_size)

    def calculate_chunk_size(self):
        left = 134217728
        right = 1073741824
        while left <= right:
            middle = left + (right-left)//2
            chunk_count = 0
            for file in self.queue:
                chunk_count += ceil(file[3]/middle)
            if chunk_count >= self.threshold:
                right = middle-1
                self.chunk_size = max(self.chunk_size, middle)
            else:
                left = middle+1
        print("Chunk Size : {converted}".format(converted=convert.convert_size(self.chunk_size)))

    def read_data(self):
        self.queue = []
        for counter, file in enumerate(os.listdir(self.directory), self.episode_start):
            tokens = file.split("\\")
            filepath = self.directory + "\\" + file
            current_filesize = os.path.getsize(filepath)
            if current_filesize != 0:
                self.total_size += current_filesize
                self.queue.append([filepath, tokens[-1], counter, current_filesize])

    def print_queue(self):
        queue_data = []
        for file in self.queue:
            td = dict()
            td["directory"] = file[0]
            td["filename"] = file[1]
            td["episode"] = file[2]
            td["filesize"] = file[3]
            queue_data.append(td)

        json_file = open("output.json", "w")
        json_file.write(json.dumps(queue_data))
        json_file.close()
