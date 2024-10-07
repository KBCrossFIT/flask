from persona.youtube_transcript import get_video_transcript

class persona_repo:

    personas = {}

    # 스크립트 추출하여 저장
    def script_insert(self,name, url):

        self.set_persona_name(name)
        self.personas[name]["youtube_scripts"].append("1." + get_video_transcript(url))


    # 페르소나 db에 키 값 생성
    def set_persona_name(self,name):

        if name in self.personas:
            return
    
        self.personas[name] = {
            'name' : name,
            'youtube_scripts' : []
        }

    