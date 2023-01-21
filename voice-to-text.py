
# IHS <3

from   pynput.keyboard import Key, Listener
from   vosk import Model, KaldiRecognizer
import time, os, threading, pyaudio, wave, json

rec          = 0
stop         = 0
p            = pyaudio.PyAudio()
frames       = []
rate         = 44100
stream       = None
thread_rec   = 0
thread_recog = 0
model_load   = 0

def main():
    thread_recognize = threading.Thread(target=recognize, args=())
    thread_recognize.start()

    thread_task = threading.Thread(target=task, args=())
    thread_task.start()

    with Listener(on_press=on_press) as listener:
        listener.join()


def on_press(key):
    global rec

    try:
        if key.char == "1":
            rec = 1
        elif key.char == "2":
            rec = 2
    except AttributeError:
        if key == Key.esc:
            print("\n\nExit program.\n")
            os._exit(0)


def task():
    global rec, stop, thread_rec, thread_recog, model_load
    running = False
    thread_created = False

    while True:
        if model_load == 1:
            break
        time.sleep(1)

    os.system('clear')
    print("Iesus Hominum Salvator\n\n")
    print("1 = Start recording.\n2 = Stop recording.\nESC = quit program.\n\n")

    while True:
        if rec == 1 and running == False:
            print("Start recoding.")
            running = True
            rec     = 0
            
            if thread_created == False:
                thread_created = True
                thread_rec  = 1
                thread = threading.Thread(target=start_recording, args=())
                thread.start()
            else:
                thread_rec = 1

            running = False

        elif rec == 2:
            print("Stop recoding.")
            running = True
            rec     = 0
            stop    = 1
            stop_recording()
            running = False
            thread_recog = 1

        time.sleep(1)


def start_recording():
    global p, rate, frames, stream, stop, thread_rec

    while True:
        if thread_rec == 1:
            thread_rec = 0
            chunk      = 1024
            stream     = p.open(format            = pyaudio.paInt16,
                                channels          = 1,
                                rate              = rate,
                                input             = True,
                                frames_per_buffer = chunk)

            print("Recording...")
            frames = []
            
            while True:
                data = stream.read(chunk)
                frames.append(data)

                if stop == 1:
                    stop = 2
                    break

        time.sleep(1)


def stop_recording():
    global p, rate, frames, stream, stop

    while True:
        if stop == 2:
            stop = 0
            break
        time.sleep(1)

    stream.stop_stream()
    stream.close()

    wf = wave.open("output.wav", 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("Finished.")
    

def recognize():
    global thread_recog, model_load

    print("Loading model...")
    model = Model(r"/home/user/model/vosk-model-pt-fb-v0.1.1-20220516_2113")
    print("Model loaded.")
    model_load = 1

    while True:
        if thread_recog == 1:
            thread_recog = 0
            print("Recognize...")

            wf = wave.open("output.wav", "rb")
            recognizer = KaldiRecognizer(model, wf.getframerate())
            recognizer.SetWords(True)

            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                
                if recognizer.AcceptWaveform(data):
                    recognizerResult = recognizer.Result()
                    results = results + recognizerResult
    
            results = results + recognizer.FinalResult()
            content = json.loads(results)
            print("Results:\n\n{}\n\n".format(content["text"]))

        time.sleep(1)


main()


