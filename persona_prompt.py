from openai import OpenAI

api_key
client = OpenAI(api_key)

def get_persona_strategy(persona_id, personas, user_input):
    persona_id = persona_id.lower()
    if persona_id not in personas:
        raise ValueError("유효하지 않은 페르소나가 선택되었습니다.")

    scripts = personas[persona_id]["youtube_scripts"]
    prompt = (
    f"너는 이제 {persona_id}입니다. "
    "친근하고 간결한 한국어로 정중한 90세의 말투로 대답하세요. "
    "투자 철학이나 경험을 간략히 공유하되, 사용자 질문의 맥락에 맞게 사람처럼 흐름에 맞는 짧고 요점만 말하도록 하세요. "
    "다음 youtube 스크립트에서 당신의 말투와 철학을 반영해서 대답해 주되 대화의 흐름에 맞는 말만 하세요"
    )
    # prompt = "너는 지금부터 " + persona_id + "입니다." + "~해요, ~요의 90세의 말투로 한국어로 대답한다."+"다음 youtube 스크립트에서 당신의 인터뷰 내용을 통해 당신의 철학, 성격, 말투를 익힌 사람이 되세요."
    
    for script in scripts:
        prompt += script
    
    response = client.chat.completions.create(
        #model = "gpt-3.5-turbo",
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ],
        max_tokens=1000,
        temperature=0.5
    )
    
    strategy = response.choices[0].message.content
    return strategy