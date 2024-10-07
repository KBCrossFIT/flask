from repo import persona_repo
from persona_prompt import get_persona_strategy

def main():
    
    # https://www.youtube.com/watch?v=dn0TyBZD2Fs
    repo = persona_repo()
    
    while True:
        
        name = input("등록할 인물의 이름을 입력하세요(종료를 원할 시 x를 입력하세요.) : ")
        if name == "x":
            break
        
        url = input("인물의 정보를 가져올 youtube url을 입력하세요 : ")

        repo.script_insert(name, url)
    
    print("정보를 모두 입력했습니다. 만나볼 인물의 이름을 입력하여 대화를 할 수 있습니다.")
    
    name = input("대화할 인물을 입력하세요 : ")
    if (name == "x"):
        return
    
    while True:
        msg = input("질문하세요. (종료는 x를 입력하세요.) : ")
        
        if msg == "x":
            break
        
        print(get_persona_strategy(name, repo.personas, msg))
        print("\n")
        
    
    



if __name__ == "__main__":
    main()