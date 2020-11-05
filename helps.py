import json
import ast
import os
import gzip
import codecs
import multiprocessing as mp


def raw_json_reader(path):
    if type(path) == file:
        f = path
    elif os.path.isdir(path):
        for fname in os.listdir(path):
            if fname.endswith(".gz"):
                f = gzip.open(path, 'r')
            else:
                f = codecs.open(os.path.join(path, fname), 'r', encoding="utf-8", errors="ignore")
            for line in f:
                try:
                    yield json.loads(line)
                except:
                    try:
                        yield ast.literal_eval(line.strip())
                    except:
                        pass
    else:

        if path.endswith(".gz"):
            f = gzip.open(path, 'r')
        else:
            f = codecs.open(path, 'r', encoding="utf-8", errors="ignore")

    for line in f:
        try:
            yield json.loads(line.strip())
        except:
            try:
                yield ast.literal_eval(line.strip())
            except:
                pass
    f.close()

class ParallelBucket:
    def __init__(self, cpu_limit=True):
        self.jobs = []
        if cpu_limit:
            self.ncpus = mp.cpu_count()
        else:
            self.ncpus = float("inf")

    def add_job(self, func, args=()):
        t = mp.Process(target=func, args=args)
        t.start()
        self.jobs.append(t)

        if len(self.jobs) >= self.ncpus:
            self.joinall()

    def joinall(self):
        for job in self.jobs:
            job.join()
        self.jobs = []

class Iterator(object):
    def __init__(self, path):
        self.path = path

    def __iter__(self):
        if type(self.path) == file:
            f = self.path
        elif os.path.isdir(self.path):
            for fname in os.listdir(self.path):
                if fname.endswith(".gz"):
                    f = gzip.open(self.path, 'r')
                else:
                    f = codecs.open(os.path.join(self.path, fname), 'r', encoding="utf-8")
                for line in f:
                    try:
                        document = json.loads(line)
                        yield document['title']+document['body']
                    except:
                        try:
                            document = ast.literal_eval(line.strip())
                            yield document['title']+document['body']
                        except:
                            pass
        else:

            if self.path.endswith(".gz"):
                f = gzip.open(self.path, 'r')
            else:
                f = codecs.open(self.path, 'r', encoding="utf-8", errors="ignore")

        for line in f:
            try:
                document = json.loads(line)
                yield document['title']+document['body']
            except:
                try:
                    document = ast.literal_eval(line.strip())
                    yield document['title']+document['body']
                except:
                    pass
        f.close()
