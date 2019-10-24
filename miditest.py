import mido
from time import sleep, perf_counter
from multiprocessing import Process, Value


def midi_clock_generator(out_port, bpm, run):
    midi_output = mido.open_output(out_port)
    clock_tick = mido.Message('clock')
    while run.value:
        pulse_rate = 60.0 / (bpm.value * 24)
        midi_output.send(clock_tick)
        t1 = perf_counter()
        if bpm.value <= 3000:
            sleep(pulse_rate * 0.8)
        t2 = perf_counter()
        while (t2 - t1) < pulse_rate:
            t2 = perf_counter()


if __name__ == '__main__':
    midi_ports = mido.get_output_names()
    print(midi_ports)

    shared_bpm = Value('i', 60)
    run_code = Value('i', 1)
    midi_clock_generator_proc = Process(target=midi_clock_generator, args=(midi_ports[0], shared_bpm, run_code))
    midi_clock_generator_proc.start()
    # sleep(.1)
    while run_code.value:
        bpm = input('Enter Tempo in BPM-> ')
        if bpm.isdigit():
            shared_bpm.value = int(bpm)
        else:
            run_code.value = False
    print('Shutting down process')
    midi_clock_generator_proc.join()
    midi_clock_generator_proc.close()
    print('exiting')
