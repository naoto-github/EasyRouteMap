import subprocess
import base64

class JTalk:
        
    def _generate(text, wav_file):

        open_jtalk = "/usr/local/bin/open_jtalk"
        dic_path = "/usr/local/Cellar/open-jtalk/1.11/dic"        
        voice_path = "/usr/local/Cellar/open-jtalk/1.11/voice/mei/mei_normal.htsvoice"
        speed = "1.0"
        
        command = f"{open_jtalk} -x {dic_path} -m {voice_path} -r {speed} -ow {wav_file}"
        c = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE)
        c.stdin.write(text.encode("utf-8"))
        c.stdin.close()
        c.wait()

    @classmethod
    def save(self, route, output_path):
        
        instruction_list = []
        sound_list = []
        
        for step in route["steps"]:
            instruction = step["instruction"]
            sound = step["sound"]
            instruction_list.append(instruction)
            sound_list.append(sound)
            
        for instruction, sound in zip(instruction_list, sound_list):
            output_wav_file = output_path + sound
            self._generate(instruction, output_wav_file)
            print(f"Save as {output_wav_file}")        

    @classmethod
    def load(self, route, input_path):

        sound_list = []
        audio_list = []

        for step in route["steps"]:
            sound = step["sound"]
            sound_list.append(sound)
            
        for sound in sound_list:
            sound_file_path = input_path + sound
            
            with open(sound_file_path, "rb") as audio_file:
                encode_text = base64.b64encode(audio_file.read())
                audio_list.append(encode_text.decode("utf-8"))
            
            print(f"Load from {sound_file_path}")

        return audio_list
