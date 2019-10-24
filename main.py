import configstartup
from time import perf_counter, sleep
from multiprocessing import Process, Value
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ListProperty, StringProperty
from kivy.logger import Logger

import mido
import mido.backends.rtmidi  # required for pyinstaller to create an exe


class MidiClockGen:
    def __init__(self):
        self.shared_bpm = Value('i', 60)
        self._run_code = Value('i', 1)
        self.midi_process = None

    @staticmethod
    def _midi_clock_generator(out_port, bpm, run):
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
        self.midi_process = Process(target=self._midi_clock_generator, args=(out_port,
                                                                             self.shared_bpm,
                                                                             self._run_code))
        self.midi_process.start()

    def end_process(self):
        self._run_code = False
        self.midi_process.join()
        self.midi_process.close()


class MidiClockApp(App):
    midi_ports = ListProperty([])
    mcg = MidiClockGen()

    def on_start(self):
        self.midi_ports = mido.get_output_names()
        # self.mcg.launch_process(self.midi_ports[0])

    def on_stop(self):
        self.mcg.end_process()


MidiClockApp().run()
