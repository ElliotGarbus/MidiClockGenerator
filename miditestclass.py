import mido
from time import sleep, perf_counter
from multiprocessing import Process, Value


class MidiClockGen:
    def __init__(self):
        self.shared_bpm = Value('i', 60)
        self.run_code = Value('i', 1)
        self.midi_process = None

    def midi_clock_generator(self, out_port, bpm, run):
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

    def launch_process(self, out_port):
        self.midi_process = Process(target=self.midi_clock_generator, args=(out_port,
                                                                            self.shared_bpm,
                                                                            self.run_code))
        self.midi_process.start()

    def end_process(self):
        self.run_code = False
        self.midi_process.join()
        self.midi_process.close()

if __name__ == '__main__':
    midi_ports = mido.get_output_names()
    print(midi_ports)

    mcg = MidiClockGen()
    mcg.launch_process(midi_ports[0])

    while mcg.run_code.value:
        bpm = input('Enter Tempo in BPM-> ')
        if bpm.isdigit():
            mcg.shared_bpm.value = int(bpm)
        else:
            mcg.run_code.value = False

    mcg.end_process()

