import multiprocessing as mp
from queue import Empty
import time
import glob
from os.path import splitext
from os import getpid
from os import getppid


class ProcessAFile:

    @staticmethod
    def do(q, scale):

        empty_count = 0
        max_empty_count = 10
        while True:
            try:
                input_file_name = q.get(False)
                if input_file_name is None:
                    break
            except Empty:
                empty_count += 1
                if empty_count == max_empty_count:
                    print("Queue is empty.")
                    break
                time.sleep(0.1)
            else:
                # generate output file name
                output_file_name = splitext(input_file_name)[0] + "_out.txt"
                print("PPID:" + str(getppid()) + ", PID:" + str(
                    getpid()) + " Processing:" + input_file_name + "-->" + output_file_name)
                # time.sleep(0.1)


def main():
    # put tasks in queue
    q = mp.Queue()
    # glob file names and put them in queue as task list.
    input_file_names = glob.glob('*.txt')
    for input_file_name in input_file_names:
        q.put(input_file_name)

    # put end command
    n_processes = mp.cpu_count()
    print("Start " + str(n_processes) + " processes.")
    for i in range(n_processes):
        q.put(None)

    # Start resize processes
    list_processes = []
    for i in range(n_processes):
        p = mp.Process(target=ProcessAFile.do, args=(q, 0.5))
        p.start()
        list_processes.append(p)

    # join
    for p in list_processes:
        p.join()


if __name__ == "__main__":
    main()
