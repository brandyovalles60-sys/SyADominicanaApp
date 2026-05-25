import psycopg2

def conectar():
    return psycopg2.connect(
        host="db.keqyexhbucfprmqsapwi.supabase.co",
        database="postgres",
        user="postgres",
        password="TU_PASSWORD",
        port="5432"
    )