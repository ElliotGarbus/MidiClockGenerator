# MidiClockGenerator
Download here: https://github.com/ElliotGarbus/MidiClockGenerator/releases

This is a simple MIDI clock generator.  It can generate midi beat clock between 47 and 6000 BPM

Directions:
* Select the midi connection
* Use the Slider, Tap, or input the Beats per Minute
* The Range control selects differnt ranges for the slider

Developer notes:
Most of the code of interst in is main.py.  The program uses multi-processing to run the GUI in one process, and the midi clock generator in another process.
The method, _midi_clock_generator, of the class MidiClockGen, has a sleep command in the inner loop.  This is used to save power for most of the time between beats.
At beats of 3000 BPM or above sleep() is not used.

The midi clock spec bases BPM on quater notes, and sends 24 messages per quater note.

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

\_\_name\_\_ will get a differnt name in the process that is created by the program (\_\_mp_main\_\_).  The test "if \_\_name__ == '\_\_main\_\_':"
prevents the kiy code from being loaded in both procesess.  If this 'guard' is not in place, the app will create 2 windows.


There are a few other files in the respository that are not part of the project, but were part of the development:
* timer_resolution.py - Runs the timers from the time standard module back to back, and resports the results.
* miditest.py - a simple test of multiprocessing using functions
* miditestclass.py - a simple test of multiprocessing using a class

The standalone executables on the release page are built with pyinstaller using the platform specific release files in the MidiClockDist directory.
