import boto3
import threading
import tqdm


class S3Client:
    def __init__(self, bucket_name):
        self.pbar = None
        self.process = None
        self.s3 = []
        self.queue = []
        self.bucket_name = bucket_name

    def enqueue(self, new_task):
        self.queue.append(new_task)

    def execute(self):
        for task in self.queue:
            self.process = []
            self.pbar = tqdm.tqdm(total=task.total_size, unit="B", unit_scale=True, desc=task.task_name)
            for subtask in task.queue:
                self.s3.append(boto3.session.Session().resource('s3'))
                extra_arguments = {
                    "ContentDisposition": "attachment;filename=\"{file_name}\"".format(file_name=subtask[1]),
                    "ContentType": task.filetype,
                    "StorageClass": task.s3class
                }
                self.process.append(
                    threading.Thread(
                        target=self.s3[-1].meta.client.upload_file,
                        args=(
                            # Filename
                            subtask[0],
                            # Bucket
                            self.bucket_name,
                            # Key
                            "{base_prefix}/s{season}/e{episode}".format(
                                base_prefix=task.prefix,
                                season=str(task.season).zfill(2),
                                episode=str(subtask[2]).zfill(3)),
                            # Extra Args
                            extra_arguments,
                            # Callback
                            lambda bytes_transferred: self.pbar.update(bytes_transferred),
                            # Config
                            task.transfer_configuration,
                        )
                    )
                )

            for thread in self.process:
                thread.start()

            for thread in self.process:
                thread.join()
