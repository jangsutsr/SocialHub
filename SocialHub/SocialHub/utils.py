from subprocess import Popen, PIPE

def wav_to_mp3(data):
    return Popen('/usr/bin/ffmpeg -i pipe:0 -f mp3 pipe:1',
                 stdin=PIPE,
                 stdout=PIPE,
                 shell=True).communicate(data)[0]
