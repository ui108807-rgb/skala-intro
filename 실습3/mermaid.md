flowchart TD
    Start(["시작: 코드 문제 발생"]) --> Step1["1. 요구사항 분석"]
    Step1 -->|"입출력 데이터 타입 및 제약조건 파악"| Step2["2. 해결 계획 설계"]
    Step2 -->|"알고리즘 구상 및 의사코드 작성"| Step3["3. 파이썬 코드 구현"]
    Step3 --> Step4{"실행 결과는?"}
    
    Step4 -->|"A. 에러 발생 Syntax/Runtime Error"| Err["4-A. 에러 메시지 Traceback 분석"]
    Err -->|"원인 파악 및 코드 수정"| Step3
    
    Step4 -->|"B. 오답 / 시간 초과 Logical Error"| Wrong["4-B. 극단적 예외 케이스 및 알고리즘 점검"]
    Wrong -->|"로직 및 시간복잡도 수정"| Step2
    
    Step4 -->|"C. 정상 작동 통과"| Step5["5. 리팩토링 및 가독성 개선"]
    Step5 -->|"변수명 정리, 주석 작성, 최적화"| End(["종료: 해결 완료"])
    
    %% 스타일 정의
    style Start fill:#4CAF50,stroke:#388E3C,color:#fff
    style End fill:#2196F3,stroke:#1976D2,color:#fff
    style Step4 fill:#FF9800,stroke:#F57C00,color:#fff
    style Err fill:#F44336,stroke:#D32F2F,color:#fff
    style Wrong fill:#F44336,stroke:#D32F2F,color:#fff