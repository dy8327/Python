def calculate_sum(*args):
    total = 0
    for scores in args:
        total += scores
    return total


def main():
    in_num = 0
    student_list = []

    print("=== 학생 성적 처리 시스템 ===")
    print("과목 별 점수는 공백으로 구분하여 넣어주십시요..")
    print("(순서는 국어 수학 영어 과학 사회 순 입니다. )")

    while in_num != 1:
        student_data = input("이름 입력: ")
        subject_data = ("국어 수학 영어 과학 사회")
        score_data = input("점수 입력: ")

        subject_list = subject_data.split()
        score_list = score_data.split()

        # 점수 딕셔너리 생성
        subject_board = {
            "국어": int(score_list[0]),
            "수학": int(score_list[1]),
            "영어": int(score_list[2]),
            "과학": int(score_list[3]),
            "사회": int(score_list[4])
        }

        # 점수 리스트 생성
        input_scores = []
        for item in subject_list:
            input_scores.append(subject_board[item])

        # 총점, 평균 계산
        total_scores = calculate_sum(*input_scores)
        total_avg = total_scores // len(input_scores)

        # 등급 계산
        if total_avg >= 90:
            grade = 'A'
        elif total_avg >= 80:
            grade = 'B'
        elif total_avg >= 70:
            grade = 'C'
        elif total_avg >= 60:
            grade = 'D'
        else:
            grade = 'F'

        # 학생 정보 저장 (이름 + 평균 + 총점)
        student_list.append({
            "name": student_data,
            "avg": total_avg,
            "total": total_scores
        })

        # 개인 리포트 저장
        with open("c:/python/score_report.txt", "a", encoding="utf-8") as f:
            f.write("--- 기말고사 성적 보고서 ---\n")
            f.write(f"대상 학생 : {student_data}\n")
            f.write(f"총 점수: {total_scores}점\n")
            f.write(f"평균 점수 : {total_avg}점\n")
            f.write(f"최종등급 : {grade}\n")
            f.write("----------------------\n")

        in_num = int(input("계속입력=0, 입력중단=1 : "))

    # 순위 헤더
    with open("c:/python/score_report.txt", "a", encoding="utf-8") as f:
        f.write("----- 순 위 -----\n")

    # 평균 기준 내림차순 정렬
    result = sorted(student_list, key=lambda x: x['avg'], reverse=True)

    # 순위 출력 및 저장
    with open("c:/python/score_report.txt", "a", encoding="utf-8") as f:
        for rank, stu in enumerate(result, start=1):
            f.write(f"{rank}등 : {stu['name']} (평균 {stu['avg']})\n")

    print("\n" + "="*30)
    print("저장 위치 c:/python/score_report.txt 로 저장되었습니다.")
    print("="*30)


if __name__ == "__main__":
    main()
