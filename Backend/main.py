@app.get("/test-db")
def test_db():
    try:
        from database import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}