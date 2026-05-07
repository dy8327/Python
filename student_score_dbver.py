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

# 입력 받은 문자열 데이터 파싱하여 DB에 저장
def insert_score_data(cursor, tch_string, conn):  # , score_db):
    # split()을 이용한 데이터 분리
    try:
        t_string = [x.strip() for x in tch_string.split(',')]
        name = t_string[0]
        score = list(map(int, t_string[1:]))
        if len(score) != 5:
            print("😨  입력된 과목 수가 다릅니다.")
            return
        for s in score: #db에 예외 처리 되어있지만 입력시 미리 에러 잡기
            if s<0 or s>100:
                print("😨  점수는 0~100사이 입니다. 저장에 실패했습니다.")
                print("다시 입력해주세요.")
                return
    except ValueError:
        print("😨  점수는 숫자만 입력해주세요.")
        return
    try:
        total = sum(score)
        avg = round(total/len(score), 2)
        insert_sql = "INSERT INTO GRADES_MASTER(STU_NAME, KOR, ENG, MATH, SOCI, SCIN, TOTAL, S_AVG) VALUES(:1, :2, :3, :4, :5, :6, :7, :8)"
        cursor.execute(insert_sql, [name] + score + [total, avg])

        conn.commit()
        print(f"😀  DB 저장 성공! {name} 학생의 데이터가 저장되었습니다.")
    except oracledb.Error as e:
        print(f"😨  DB저장 실패: {e}")
        conn.rollback() #저장 실패 시 롤백
    return

# 학급 조회
def inquire_all_data(cursor):  
    inquire_all_sql = """SELECT
        NVL(SUM(TOTAL),0) AS CLASS_TOTAL,
        NVL(AVG(S_AVG),0) AS CLASS_AVG,
        NVL(MAX(S_AVG),0) AS AVG_MAX,
        NVL(MIN(S_AVG),0) AS AVG_MIN,
        LISTAGG(RANK_NUM ||'위 '||STU_NAME||'('||S_AVG||')'||' | ') WITHIN GROUP(ORDER BY RANK_NUM) AS RANK_LIST
        FROM (SELECT STU_NAME, TOTAL, S_AVG, RANK() OVER(ORDER BY TOTAL DESC) AS RANK_NUM
        FROM GRADES_MASTER)"""
    cursor.execute(inquire_all_sql)
    return cursor.fetchall()

# 개별조회
def inquire_one_data(cursor, stu_name):  
    inquire_one_sql = "SELECT STU_NAME, KOR, ENG, MATH, SOCI, SCIN, TEACHER_NOTE FROM GRADES_MASTER WHERE STU_NAME= :1"
    cursor.execute(inquire_one_sql, (stu_name,))
    return cursor.fetchone()

#학생 조회
def stu_one_data(cursor, stu_name): 
    #순위 빼려면 한번 더 감싸서 꺼내와야한다.
    one_sql = "SELECT * FROM (SELECT STU_NAME, TOTAL, S_AVG, TEACHER_NOTE, RANK() OVER(ORDER BY TOTAL DESC) AS STRANK FROM GRADES_MASTER) WHERE STU_NAME= :1"
    cursor.execute(one_sql,(stu_name,))
    return cursor.fetchone()

# 코멘트 입력
def insert_comment(cursor, comment, stu_name, conn):  
    try:
        s_name = stu_name.strip()
        in_comment_sql = "UPDATE GRADES_MASTER SET TEACHER_NOTE= :1 WHERE STU_NAME= :2"
        cursor.execute(in_comment_sql, (comment, s_name,))
        conn.commit()
    except oracledb.Error as e:
        print(f"DB저장 실패: {e}")
        conn.rollback() #저장 실패 시 롤백
    return

#교사 메뉴
def teacher_menu(cursor, conn):
    while True:
            
            print("1. 성적 입력")
            print("2. 성적 조회")
            print("3. 코멘트 작성")
            print("4. 종료")
            tch_num = int(input("📄  원하는 메뉴를 선택하세요: "))
            if tch_num == 1:
                while True:
                    tch_input = input(
                        "> 성적을 입력하세요(이름, 국어, 영어, 수학, 사회, 과학)\n")
                    insert_score_data(cursor, tch_input, conn)
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
                            print("----- 학급 리포트 -----")
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
                            print(f"✍  선생님 코멘트 : {coment}")

                    elif sub == 3:
                        break

            elif tch_num == 3:
                stu_name = input("학생 이름 : ")
                comment = input("코멘트를 작성해주세요(200자이내) : ")
                insert_comment(cursor, comment, stu_name, conn)
                #rowcount 수정 필요...
                if cursor.rowcount == 0:
                    print("해당 학생을 찾을 수 없습니다.")
                else:
                    print("코멘트가 저장되었습니다.")

            elif tch_num == 4:
                print("프로그램 종료")
                break

#학생 메뉴
def student_menu(cursor):
    stu_name = input("본인 이름을 입력하세요: ")
    one_data = stu_one_data(cursor, stu_name)
    if one_data is None:
            print("해당 학생이 없습니다.")
    else:    
            stu_name, total, avg, coment, rank = one_data
            #성취도
            if avg>=90:
                grade = 'A'
            elif avg>=80:
                grade = 'B'
            elif avg>=70:
                grade = 'C'
            elif avg>=60:
                grade = 'D'
            else: grade = 'F'
            print(f"{stu_name} 학생은 '{rank}위'이며, 성취도는 '{ grade}'입니다.")
            print(f"총점은 {total}점, 평균은 {avg}점 입니다.")
            print(f"✍  선생님 코멘트 : {coment}")
            return

#실행 메인
def main():
    try:
        in_num = 0
        conn = get_connection()
        cursor = conn.cursor()
        while True:
            try:
                print("===== 성적관리 시스템=====\n")
                print("1. 교사")
                print("2. 학생") 
                in_num = int(input("해당하는 번호를 입력하세요.\n"))
                break
            except ValueError:
                print("숫자만 입력하세요.")
                continue
        # 교사 메뉴
        if in_num == 1:
            teacher_menu(cursor, conn)

        #학생메뉴
        elif in_num==2:
            student_menu(cursor)
    except oracledb.Error as e:
        print(f" SQL 실행 오류 발생: {e}")
        # 오류 시 복구
        conn.rollback() 
    finally:
        # 자원 반납
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
