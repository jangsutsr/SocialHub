from subprocess import Popen, PIPE

def wav_to_mp3(data):
    '''Function that convert .wav to .mp3 using ffmpeg.
    '''
    return Popen('/usr/bin/ffmpeg -i pipe:0 -f mp3 pipe:1',
                 stdin=PIPE,
                 stdout=PIPE,
                 shell=True).communicate(data)[0]
