# 사용자에게 새로운 종료 명령어(!quit)를 안내합니다.
print("프로그램을 종료하려면 '!quit'을 입력하세요.")

while True:
    # 매번 사용자에게 문장을 입력받아 sentence 변수에 보관합니다.
    sentence = input("문장을 입력하세요: ")
    
    # 사용자가 정확히 '!quit'이라고 입력했는지 확인합니다.
    if sentence == "!quit":
        print("프로그램을 종료합니다.")
        break  # !quit이 입력되면 while 반복문을 종료하고 빠져나갑니다.
        
    # '!quit'이 아니라면 사용자가 입력한 문장을 그대로 화면에 보여줍니다.
    print(sentence)