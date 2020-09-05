import statistics
import re
import subprocess
import sys
import time

standalone = False
if __name__ == "__main__":

    t0 = time.time()
    last_time = t0

    stats = {}

    if standalone:
        loops = 10
        if len(sys.argv) > 1:
            loops = int(sys.argv[1])

        for i in range(loops):
            # results = subprocess.run(['echo', 'bazel', 'run', '-c', 'opt', '--copt="-mavx"', 'benchmarks_test', '--', '--benchmarks=benchmark_defun_matmul_2_by_2_CPU'], stdout=subprocess.PIPE)
            results = subprocess.run('bazel run -c opt --copt="-mavx" benchmarks_test -- --benchmarks=benchmark_defun_matmul_2_by_2_CPU', stdout=subprocess.PIPE, shell=True)
            regex = re.findall('entry \{.*?name: \"(.*?)\"\s*?iters:.*?wall_time: ([\d\.]*?)\s*?extras', results.stdout.decode('utf-8'), re.DOTALL)
            end_time = time.time()
            print(f'Trial {i} complete in {end_time - last_time} sec')
            last_time = end_time
    else:
        input_str = sys.stdin.read()
        regex = re.findall('entry \{.*?name: \"(.*?)\"\s*?iters:.*?wall_time: ([\d\.]*?)\s*?extras', input_str, re.DOTALL)

    for bname, wall_time in regex:
        if bname not in stats:
            stats[bname] = []
        stats[bname].append(float(wall_time))

    print()
    for bname, times in stats.items():
        print(f'Summary Statistics over {len(regex) / len(stats)} trials for {bname}')
        print(f'Times: {times}')
        print(f'Min: {min(times)}')
        print(f'Mean: {statistics.mean(times)}')
        print(f'Median: {statistics.median(times)}')
        if len(regex) / len(stats) > 1:
            print(f'Std. dev.: {statistics.stdev(times)}')

    print(f'Total time elapsed: {time.time() - t0} sec')
