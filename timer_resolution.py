import math
import time

LOOPS = 10 ** 6

print(f'time.time_ns(): {time.time_ns()}')
print(f'time.time(): {time.time()}')
print(f'time.perf_counter_ns(): {time.perf_counter_ns()}')
print(f'time.perf_counter(): {time.perf_counter()}')
print(f'time.monotonic_ns(): {time.monotonic_ns()}')
print(f'time.monotonic(): {time.monotonic()}')
print(f'time.process_time_ns(): {time.process_time_ns()}')
print(f'time.process_time(): {time.process_time()}\n')

min_dt = [abs(time.time_ns() - time.time_ns()) for _ in range(LOOPS)]
min_dt = min([dt for dt in min_dt if dt != 0])
print(f'min time_ns() delta: {min_dt} ns')

min_dt = [abs(time.time() - time.time()) for _ in range(LOOPS)]
min_dt = min([dt for dt in min_dt if dt != 0])
print(f'min time() delta: {math.ceil(min_dt * 1e9)} ns')

min_dt = [abs(time.perf_counter_ns() - time.perf_counter_ns()) for _ in range(LOOPS)]
min_dt = min([dt for dt in min_dt if dt != 0])
print(f'min perf_counter_ns() delta: {min_dt} ns')

min_dt = [abs(time.perf_counter() - time.perf_counter()) for _ in range(LOOPS)]
min_dt = min([dt for dt in min_dt if dt != 0])
print(f'min perf_counter() delta: {math.ceil(min_dt * 1e9)} ns')

min_dt = [abs(time.monotonic_ns() - time.monotonic_ns()) for _ in range(LOOPS)]
min_dt = min([dt for dt in min_dt if dt != 0])
print(f'min monotonic_ns() delta: {min_dt} ns')

min_dt = [abs(time.monotonic() - time.monotonic()) for _ in range(LOOPS)]
min_dt = min([dt for dt in min_dt if dt != 0])
print(f'min monotonic() delta: {math.ceil(min_dt * 1e9)} ns')

min_dt = [abs(time.process_time_ns() - time.process_time_ns()) for _ in range(LOOPS)]
min_dt = min([dt for dt in min_dt if dt != 0])
print(f'min process_time_ns() delta: {min_dt} ns')

min_dt = [abs(time.process_time() - time.process_time()) for _ in range(LOOPS)]
min_dt = min([dt for dt in min_dt if dt != 0])
print(f'min process_time() delta: {math.ceil(min_dt * 1e9)} ns')