from persona.gpt_config import api_key
from openai import OpenAI

client = OpenAI(api_key=api_key)


def make_persona_prompt(persona_data):
    prompt = f'너는 이제 {persona_data["name"]}입니다.'

    # youtube 스크립트 제외 속성 prompt 추가
    for attribute in persona_data["attributes"]:
        if not attribute.startswith('script'):
            prompt += persona_data["attributes"][attribute]

    prompt += (
        f"투자 철학이나 경험을 간략히 공유하되, 사용자 질문의 맥락에 맞게 사람처럼 흐름에 맞는 짧고 요점만 말하도록 하세요. "
        "다음 youtube 스크립트에서 당신의 말투와 철학을 반영해서 대답해 주되 대화의 흐름에 맞는 말만 하세요"
    )

    prompt += str(persona_data["attributes"]["script_1"])
    prompt += str(persona_data["attributes"]["script_2"])

    return prompt


def get_persona_response(persona_data, user_input):
    prompt = make_persona_prompt(persona_data)

    response = client.chat.completions.create(
        # model = "gpt-3.5-turbo",
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ],
        max_tokens=1000,
        temperature=0.5
    )

    strategy = response.choices[0].message.content
    return strategy
