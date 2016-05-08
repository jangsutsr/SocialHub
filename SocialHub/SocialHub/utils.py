from subprocess import Popen, PIPE

def wav_to_mp3(data):
    return Popen('~/Downloads/SnowLeopard_Lion_Mountain_Lion_Mavericks_Yosemite_El-Captain_02.05.2016/ffmpeg -i pipe:0 -f mp3 pipe:1',
                 stdin=PIPE,
                 stdout=PIPE,
                 shell=True).communicate(data)[0]
