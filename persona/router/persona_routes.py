from flask import Blueprint, request, jsonify
from persona.service.youtube_transcript import get_video_transcript
from persona.repositories.persona_repository import insert_persona, get_persona
from persona.service.persona_prompt import get_persona_response


persona_routes = Blueprint('persona_routes', __name__)

persona_cache = {}

@persona_routes.route('/api/persona/register', methods=['POST'])
def register_persona():
    try:
        
        # 요청 본문에서 데이터 추출 (JSON 형식으로 요청 받음)
        persona_data = request.json
        persona_id = persona_data.get('persona_id').lower()
        name = persona_data.get('name')
        
        if not persona_id and not name:
            return jsonify({'error': 'Missing required fields: persona_id or name'}), 400

        attributes = {}
        
        for key, value in persona_data.items():
            if key not in ['persona_id', 'name', 'url_1', 'url_2']:  # 'persona_id', 'name' 제외한 나머지 필드 처리
                attributes[key] = value
        
        print(attributes)
                
        urls = [persona_data.get('url_1'), persona_data.get('url_2')]
        print(urls)
        
        for idx, url in enumerate(urls):
            print('script_' + str(idx+1))
            attributes['script_'+str(idx+1)] = get_video_transcript(url)
            print("자막추출 성공")
        return insert_persona(persona_id, name, attributes)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@persona_routes.route('/api/persona', methods=['POST'])
def get_persona_by_id():
    
    data = request.json
    id = data.get('id')
    message = data.get('message')
    
    if id not in persona_cache:
        persona_cache[id] = get_persona(id)
    
    persona_data = persona_cache[id]
    
    resp = get_persona_response(persona_data, message)
    return jsonify({'data':resp}), 200
