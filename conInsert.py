import oracledb
#데이터 베이스 연결 정보
db_config = {
    "user": "system",
    "password": "1234",
    "dsn": "localhost:1521/xe"
}
#데이터 베이스 연결

try:
    with oracledb.connect(**db_config) as conn:
    #conn = oracledb.connect(**db_config) _ with 사용 추천

# 데이터 삽입
        with conn.cursor() as cursor:
         #   sql = "INSERT INTO MEMBERS(ID, NAME, EMAIL) VALUES(:1, :2, :3)"
          #  cursor.execute(sql,(1, "홍길동", "hong@exmp.com"))
          #  conn.commit() #DML 구문은 꼭 커밋 해주기

            insert_sql = "INSERT INTO MEMBERS(ID, NAME, EMAIL) VALUES(:1, :2, :3)"
            user_data=(2, "이순신", "lee@exmp.com")

            try:
                cursor.execute(insert_sql, user_data)
                conn.commit()
                print("삽입 성공")
            except oracledb.IntegrityError:
                print("중복된 아이디가 있습니다.")
except oracledb.Error as e:
    print("오라클 오류",{e})
