import oracledb

with oracledb.connect(user="system", password="1234", dsn="localhost:1521/xe") as conn: #conn은 connect 객체가 들어있는 거다.
    cursor = conn.cursor() #자바의 prepared가 파이썬에서는 cursor다. 
    
    # 기존 테이블이 있다면 삭제 (연습용)
    try:
        cursor.execute("DROP TABLE members")
    except oracledb.DatabaseError: ##파이썬은 트라이 캐치가 트라이 엑셉트 이다. 
        pass ##엑셉트 걸리며 그냥 패스~

    # 새 테이블 생성
    create_sql = """ 
    CREATE TABLE members (
        id NUMBER PRIMARY KEY,
        name VARCHAR2(50) NOT NULL,
        email VARCHAR2(100) UNIQUE,
        join_date DATE DEFAULT SYSDATE
    )
    """
    cursor.execute(create_sql)
    print("테이블 생성 완료")