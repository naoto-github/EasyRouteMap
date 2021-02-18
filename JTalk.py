import subprocess

class JTalk:

    def __init__(self):
        self.open_jtalk = "/usr/local/bin/open_jtalk"
        self.dic_path = "/usr/local/Cellar/open-jtalk/1.11/dic"        
        self.voice_path = "/usr/local/Cellar/open-jtalk/1.11/voice/mei/mei_normal.htsvoice"
        self.speed = "1.0"
        
    def generate(self, text, wav_file):
        command = f"{self.open_jtalk} -x {self.dic_path} -m {self.voice_path} -r {self.speed} -ow {wav_file}"
        c = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE)
        c.stdin.write(text.encode("utf-8"))
        c.stdin.close()
        c.wait()

