# 1. 가변 매개변수(*args)를 활용한 합계 계산 함수
def calculate_sum(*args):
    """모든 과목의 점수를  더합니다."""
    total = 0
    for scores in args:
        total += scores
    return total  # 계산된 총합을 반환합니다.


def main():
    # 2. 사용자 입력 활용하기 (input 사용)
    # PDF 04-2 사용자 입출력 자료를 기반으로 프롬프트를 띄워 입력을 받습니다.
    print("=== 학생 성적 처리 시스템 ===")
    print("과목 별 점수는 공배으로 구분하여 넣어주십시요..")
    print("(예: 홍길동 국어 수학 영어 과학 사회 100 100 100 100 100 )")
    student_data = input("이름 입력: ")
    subject_data = input("과목 입력 : ")
    score_data = input("점수 입력: ")
    
    # 입력받은 문자열을 리스트로 변환
    subject_list = subject_data.split()
    score_list = score_data.split()

    # 3. 딕셔너리 활용: 메뉴판 설정
    subject_board = {
        "국어": int (score_list[0]),
        "수학": int (score_list[1]),
        "영어": int (score_list[2]),
        "과학": int (score_list[3]),
        "사회": int (score_list[4])
    }
   # print(f"입력값 : {student_data} {subject_list[0]} {score_list[0]}")

    # 4. 리스트 조작 및 제어문: 주문된 메뉴의 가격들만 모으기
    input_scores = []
    valid_scores = [] 
    
    for item in subject_list:
        if item in subject_board:
            scores = subject_board[item]
            input_scores.append(scores)
            valid_scores.append(item)
        else:
            print(f"경고: '{item}'은(는) 없는 과목이므로 제외됩니다. (다시 입력해주세요.)")

    # 5. 함수 호출: 가변 매개변수 함수에 리스트 내용 전달 (언패킹)
    # 리스트의 가격 데이터들을 개별 인자로 풀어서 전달합니다.
    total_scores = calculate_sum(*input_scores)
    total_avg = total_scores // len(valid_scores)

    if total_avg>=90:
        grade = 'A'
    elif total_avg>=80:
        grade = 'B'
    elif total_avg>=70:
        grade = 'C'
    elif total_avg>=60:
        grade = 'D'
    else:
        grade ='F'


    # 6. 파일 입출력 및 f-문자열 포매팅: 정산 리포트 생성
    # PDF 04-3 파일 읽고 쓰기 자료의 'with' 문을 사용하여 파일을 작성합니다.
    with open("c:/python/score_report.txt", "w", encoding="utf-8") as f:
        f.write("--- 기말고사 성적 보고서 ---\n")
      #  f.write(f"총 주문 건수: {len(valid_orders)}건\n")
        f.write(f"대상 학생 : {student_data}\n")
        f.write(f"총 점수: {total_scores}점\n")
        f.write(f"평균 점수 :{total_avg}점\n")
        f.write(f"최종등급 : {grade}\n")
        f.write("----------------------\n")
     #   f.write("입력 데이터 : " + ", ".join(input_scores))

    print("\n" + "="*30)
    print(f"저장 위치 c:/pyton/score_report.txt 로 저장되었습니다.")
    print("="*30)



# 프로그램 시작점 (Entry Point)
if __name__ == "__main__":
    main()