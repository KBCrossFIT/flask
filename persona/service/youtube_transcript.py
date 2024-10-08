from youtube_transcript_api import YouTubeTranscriptApi

def get_video_transcript(video_url):
    script = ""
    
    if video_url == "":
        return

    video_id = get_video_id(video_url)
    try:
        # 자막 가져오기 (지원되는 자막 언어 확인)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # 자막 내용 출력
        for entry in transcript:
            script += entry['text']
            #print(f"{entry['text']}")
    
    except Exception as e:
        print(f"자막을 가져오는 중 오류 발생: {e}")
    return script

# 유튜브 비디오 ID로 자막을 가져옵니다.
def get_video_id(video_url):
    video_id = video_url.split('v=')[1][:11]
    return video_id

# video_id = get_video_id("")  # 여기에 실제 비디오 ID 입력
#get_video_transcript("https://www.youtube.com/watch?v=kWY9mNMz4iI")
