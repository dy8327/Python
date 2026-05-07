import oracledb
import sys

db_config = {
    "user": "system",
    "password": "1234",
    "dsn": "localhost:1521/xe"
}


def get_connection():
    try:
        conn = oracledb.connect(
            user=db_config["user"],
            password=db_config["password"],
            dsn=db_config["dsn"]
        )
        return conn
    except oracledb.Error as e:
        print(f"DB 접속실패: {e}")
        sys.exit(1)


def insert_score_data(cursor, tch_string):  # , score_db):
    # 입력 받은 문자열 데이터 파싱하여 DB에 저장
    # split()을 이용한 데이터 분리
    try:
        t_string = [x.strip() for x in tch_string.split(',')]
        name = t_string[0]
        score = list(map(int, t_string[1:]))
        if len(score) != 5:
            print("입력된 과목 수가 다릅니다.")
            return
    except ValueError:
        print("점수는 숫자만 입력해주세요.")
        return
    total = sum(score)
    avg = round(total/len(score), 2)
    insert_sql = "INSERT INTO SCORE_BOX(STU_NAME, KOR, ENG, MATH, SOCI, SCIN, TOTAL, S_AVG) VALUES(:1, :2, :3, :4, :5, :6, :7, :8)"
    cursor.execute(insert_sql, [name] + score + [total, avg])
    return


def inquire_all_data(cursor):  # 학급 조회
    inquire_all_sql = """SELECT
        NVL(SUM(TOTAL),0) AS CLASS_TOTAL,
        NVL(AVG(S_AVG),0) AS CLASS_AVG,
        NVL(MAX(S_AVG),0) AS AVG_MAX,
        NVL(MIN(S_AVG),0) AS AVG_MIN,
        LISTAGG(STU_NAME||'('||S_AVG||')'||' ') WITHIN GROUP(ORDER BY TOTAL DESC) AS LIST_NAME
        FROM SCORE_BOX"""
    cursor.execute(inquire_all_sql)
    return cursor.fetchall()


def inquire_one_data(cursor, stu_name):  # 개별조회
    inquire_one_sql = "SELECT STU_NAME, KOR, ENG, MATH, SOCI, SCIN, COMENT FROM SCORE_BOX WHERE STU_NAME= :1"
    cursor.execute(inquire_one_sql, (stu_name,))
    return cursor.fetchone()


def insert_comment(cursor, comment, stu_name):  # 코멘트 입력
    s_name = stu_name.strip()
    in_comment_sql = "UPDATE SCORE_BOX SET COMENT= :1 WHERE STU_NAME= :2"
    cursor.execute(in_comment_sql, (comment, s_name,))
    return


def main():

    in_num = 0
    conn = get_connection()
    cursor = conn.cursor()
    # try:
    print("===== 성적관리 시스템=====\n")
    print("1. 교사")
    print("2. 학생")
    in_num = int(input("해당하는 번호를 입력하세요.\n"))
# 교사 메뉴
    if in_num == 1:
        while True:
            print("1. 성적 입력")
            print("2. 성적 조회")
            print("3. 코멘트 작성")
            print("4. 종료")
            tch_num = int(input("원하는 메뉴를 선택하세요: "))
            if tch_num == 1:
                while True:
                    tch_input = input(
                        "> 성적을 입력하세요(이름, 국어, 영어, 수학, 사회, 과학)\n")
                    insert_score_data(cursor, tch_input)
                    conn.commit()

                    again = input("계속입력(y/n): ")
                    if again.lower() != 'y':
                        break

            elif tch_num == 2:
                while True:
                    print("1. 전체 조회")
                    print("2. 개별 조회")
                    print("3. 뒤로가기")
                    sub = int(input("원하는 메뉴를 선택하세요: "))
                    if sub == 1:
                        all_data = inquire_all_data(cursor)
                        for cls_total, cls_avg, max_avg, min_avg, stu_name in all_data:
                            print(f"학급 총점: {cls_total}점, 학급 평균: {cls_avg}점")
                            print(f"최고점수: {max_avg}점, 최저점수: {min_avg}")
                            print(stu_name)

                    elif sub == 2:
                        stu_name = input("학생 이름을 입력하세요: ")
                        one_data = inquire_one_data(cursor, stu_name)
                        if one_data is None:
                            print("해당 학생이 없습니다.")
                        else:    
                            stu_name, kor, eng, math, soci, scin, coment = one_data
                            print(
                                f"{stu_name} 국어 {kor}, 영어{eng}, 수학{math}, 사회{soci}, 과학{scin}")
                            print(f"선생님 코멘트 : {coment}")

                    elif sub == 3:
                        break

            elif tch_num == 3:
                stu_name = input("학생 이름 : ")
                comment = input("코멘트를 작성해주세요(200자이내) : ")
                insert_comment(cursor, comment, stu_name)
                conn.commit()

                if cursor.rowcount == 0:
                    print("해당 학생을 찾을 수 없습니다.")
                else:
                    print("코멘트가 저장되었습니다.")

            elif tch_num == 4:
                print("프로그램 종료")
                break
    #학생메뉴
    elif 2:
        stu_name = input("학생 이름을 입력하세요: ")
        one_data = inquire_one_data(cursor, stu_name)
        if one_data is None:
            print("해당 학생이 없습니다.")
        else:    
            stu_name, kor, eng, math, soci, scin, coment = one_data
            print(f"{stu_name} 국어 {kor}, 영어{eng}, 수학{math}, 사회{soci}, 과학{scin}")
            print(f"선생님 코멘트 : {coment}")
            return


if __name__ == "__main__":
    main()
