from flask import request, jsonify
from pymongo import MongoClient


# MongoDB 클라이언트 설정 (로컬 MongoDB 사용)
client = MongoClient('mongodb://localhost:27017/')
db = client['persona_db']  # MongoDB 데이터베이스
persona_collection = db['personas']  # MongoDB 컬렉션

# 페르소나 조회
def get_persona(persona_id):
    
    try:
        persona = persona_collection.find_one({'persona_id':persona_id})
        if not persona:
            return jsonify({'error': 'Persona not found'}), 404

        # 조회된 데이터를 JSON 형식으로 반환
        return persona

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 페르소나 데이터 등록
def insert_persona(persona_id, name, attributes):
    print("insert 들어옴")
    try:
        # 페르소나 중복 여부 체크
        existing_persona = persona_collection.find_one({'name': name.lower()})
        if existing_persona:
            return jsonify({'error': 'A persona with this name already exists.'}), 400

        persona_document = {
                'persona_id': persona_id,
                'name': name.lower(),
                'attributes': attributes  # 추가 속성들을 'attributes'로 저장
            }
        
        persona_collection.insert_one(persona_document)
        
        return jsonify({'message': 'Persona created successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500