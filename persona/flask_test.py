from flask import Flask, request, jsonify
from config import api_key
import openai

# OpenAI API Key 설정
openai.api_key = api_key

app = Flask(__name__)

# 유명인 페르소나 목록
personas = {
    "warren_buffett": {
        "name": "Warren Buffett",
        "style": "value investing",
        "prompt": "You are Warren Buffett, a master of value investing. Recommend a portfolio strategy for a conservative investor."
    },
    "benjamin_graham": {
        "name": "Benjamin Graham",
        "style": "defensive and enterprising investor",
        "prompt": "You are Benjamin Graham, a pioneer of defensive and enterprising investing. Suggest a strategy for a cautious investor with medium risk tolerance."
    },
    "ray_dalio": {
        "name": "Ray Dalio",
        "style": "hedge fund strategy",
        "prompt": "You are Ray Dalio, a hedge fund manager known for risk parity. Propose a portfolio strategy for a balanced investor."
    },
    "george_soros": {
        "name": "George Soros",
        "style": "speculative trading",
        "prompt": "You are George Soros, famous for speculative trading and global macro strategies. Recommend a portfolio strategy for an aggressive investor."
    },
    "peter_lynch": {
        "name": "Peter Lynch",
        "style": "growth investing",
        "prompt": "You are Peter Lynch, an expert in growth investing. What would you recommend for an investor seeking high-growth opportunities?"
    }
}

@app.route('/persona', methods=['POST'])
def get_persona_strategy():
    # 클라이언트로부터 요청 데이터 받기
    data = request.get_json()
    persona_id = data.get('persona_id', '').lower()

    # 페르소나 검증
    if persona_id not in personas:
        return jsonify({'error': 'Invalid persona selected'}), 400

    persona = personas[persona_id]

    # OpenAI GPT-3.5-turbo 모델을 사용해 페르소나 응답 생성
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": persona['prompt']},
                {"role": "user", "content": "What is your recommended portfolio strategy?"}
            ]
        )
        strategy = response.choices[0].message.content
        return jsonify({'persona': persona['name'], 'strategy': strategy}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
