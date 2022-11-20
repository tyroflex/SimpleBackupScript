import json
import s3client
from task import Task


if __name__ == '__main__':
    config = json.load(open("conf.json"))
    s3 = s3client.S3Client(config["bucket"])
    file = json.load(open("input.json"))
    for task in file["tasks"]:
        t = Task(directory=task["directory"],
                 key=task["key"],
                 season=task["season"],
                 filetype=task["filetype"],
                 s3class=task["s3class"],
                 taskname=task["name"],
                 start=task["start"])
        # print(len(t.queue))
        s3.enqueue(t)
        # t.print_queue()

    s3.execute()
