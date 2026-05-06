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


def insert_score_data(cursor, tch_string):#, score_db):
    # 입력 받은 문자열 데이터 파싱하여 DB에 저장
    # split()을 이용한 데이터 분리
    t_string = tch_string.split(',')
    insert_sql = "INSERT INTO SCORE_BOX(STU_NAME, KOR, ENG, MATH, SOCI, SCIN) VALUES(:1, :2, :3, :4, :5, :6)"
    cursor.execute(insert_sql,t_string)
    return

def main():
    
    in_num = 0
    conn = get_connection()
    cursor = conn.cursor()
    #try:
    print("===== 성적관리 시스템=====\n")
    print("1. 교사\n")
    print("2. 학생\n")
    in_num = input("해당하는 번호를 입력하세요.\n")
    #conti_num=0

    if in_num == '1':
            
        #while conti_num != 1:
            tch_input = input("> 성적을 입력하세요(이름, 국어, 영어, 수학, 사회, 과학)\n")
            insert_score_data(cursor, tch_input)
            conn.commit()

        #conti_num=int(input("계속입력=0, 입력중단=1 :"))

    #else:
    #    print("이름을 입력하세요.")
    #except oracledb.Error as e:
    #    print(f"에러 발생{e}")
    
    


if __name__ == "__main__":
    main()