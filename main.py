from time import perf_counter, sleep, time
import mido
import mido.backends.rtmidi  # required for pyinstaller to create an exe


class MidiClockGen:
    def __init__(self):
        self.shared_bpm = Value('i', 60)
        self._run_code = Value('i', 1)
        self._midi_process = None

    @staticmethod
    def _midi_clock_generator(out_port, bpm, run):
        # print(f'__name__: {__name__}')
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
        if self._midi_process:  # if the process exists, close prior to creating a new one
            self.end_process()
        else:                  # if this is the first time, start flashing the panel led
            app = App.get_running_app()
            app.flash_led_on(None)
        self._run_code.value = 1
        self._midi_process = Process(target=self._midi_clock_generator, args=(out_port, self.shared_bpm,
                                                                              self._run_code))
        self._midi_process.start()

    def end_process(self):
        self._run_code.value = 0
        self._midi_process.join()
        self._midi_process.close()


if __name__ == '__main__':
    import configstartup
    from multiprocessing import Process, Value, freeze_support
    from kivy.app import App
    from kivy.clock import Clock
    from kivy.properties import ListProperty, BooleanProperty
    from kivy.uix.textinput import TextInput
    from kivy.uix.spinner import Spinner
    from kivy.uix.button import Button


    class IntegerInput(TextInput):
        def insert_text(self, substring, from_undo=False):
            s = substring if substring.isdigit() else ''
            return super().insert_text(s, from_undo=from_undo)

        def on_text_validate(self):
            if int(self.text) < 47:
                self.text = '47'
            if int(self.text) > 6000:
                self.text = '6000'
            app = App.get_running_app()
            app.root.ids.bpm_slider.value = int(self.text)
            return super().on_text_validate()


    class RangeSpinner(Spinner):
        range = {'47-500': (47, 500), '400-1000': (400, 1000), '1200': (47, 6000),
                 '1500': (47, 6000), '2000': (47, 6000), '3000': (47, 6000), '6000': (47, 6000)}

        def set_min_max(self):
            p = App.get_running_app().root.ids.bpm_slider
            p.min, p.max = self.range[self.text]
            if self.text in ['1200', '1500', '2000', '3000', '6000']:
                p.value = int(self.text)
                p.disabled = True
            else:
                p.disabled = False


    class TapButton(Button):
        def __init__(self, **kwargs):
            self.start_time = 0
            self.tap_num = 0
            self.beats = []
            self.timer = None
            self.time_limit = 1.5
            super().__init__(**kwargs)

        def process_tap(self, bpm, range_select):
            range_select.text = '47-500'
            if self.tap_num == 0:
                self.start_time = time()
                self.tap_num += 1
                self.timer = Clock.schedule_once(self.tap_time_out, self.time_limit)

            elif self.tap_num == 1:
                self.timer.cancel()
                t1 = time()
                self.beats.append(t1 - self.start_time)
                self.start_time = t1
                self.tap_num += 1
                bpm.value = int(60/self.beats[0])
                self.timer = Clock.schedule_once(self.tap_time_out, self.time_limit)

            elif self.tap_num == 2:
                self.timer.cancel()
                t1 = time()
                new_beat = t1 - self.start_time
                self.start_time = t1
                avg = sum(self.beats)/len(self.beats)
                if 1.2 < avg/new_beat > 0.8:
                    bpm.value = int(60 / new_beat)
                    self.beats.clear()
                    self.beats.append(new_beat)
                else:
                    self.beats.append(new_beat)
                    avg = sum(self.beats) / len(self.beats)
                    bpm.value = int(60/avg)
                self.timer = Clock.schedule_once(self.tap_time_out, self.time_limit)

        def tap_time_out(self, _):
            self.start_time = 0
            self.tap_num = 0
            self.beats.clear()

    class MidiClockApp(App):
        midi_ports = ListProperty([])
        mcg = MidiClockGen()
        panel_led = BooleanProperty(False)

        def flash_led_off(self, dt):
            self.panel_led = self.root.ids.bpm_slider.value >= 667
            rate = (60 / int(self.root.ids.bpm_slider.value)) * .75
            Clock.schedule_once(self.flash_led_on, rate)

        def flash_led_on(self, dt):
            self.panel_led = True
            rate = (60 / int(self.root.ids.bpm_slider.value)) * .25
            Clock.schedule_once(self.flash_led_off, rate)

        def on_start(self):
            self.midi_ports = mido.get_output_names()

        def on_stop(self):
            self.mcg.end_process()


    freeze_support()  # multiprocessor support for Pyinstaller
    MidiClockApp().run()
