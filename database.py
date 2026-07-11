import sqlite3

def get_random_poem():
    conn = sqlite3.connect("poems.db")
    cur = conn.cursor()

    id_import = (1,3,4,8,9,10,11,12,13,14,15,16,17,18,19,21,22,23)

    query = f'''
            SELECT poems.verse, parts.part_name, poets.poet_name
            FROM poems
            JOIN parts ON poems.parts_id = parts.id
            JOIN books ON parts.book_id = books.id
            JOIN poets ON books.poets_id = poets.id
            WHERE poems.parts_id IN {id_import}
            ORDER BY RANDOM()
            LIMIT 1;    
                '''
    
    cur.execute(query)
    poem = cur.fetchone()

    if poem:
        khrooji = f'{poem[0]}\n\n```{poem[2]}\n{poem[1]}\n```'
        return khrooji
    else:
        return None
    
def get_books_by_poet(poet_name):
    conn = sqlite3.connect("poems.db")
    cur = conn.cursor()

    query ='''
            SELECT books.book_name
            FROM books
            JOIN poets ON books.poets_id = poets.id
            WHERE poets.poet_name = ?;
                '''
    
    cur.execute(query, (poet_name,))
    books = cur.fetchall()
    return books

def get_parts_by_book(book_name):
    conn = sqlite3.connect("poems.db")
    cur = conn.cursor()

    query ='''
            SELECT parts.part_name
            FROM parts
            JOIN books ON parts.book_id = books.id
            WHERE books.book_name = ?;
                '''
    
    cur.execute(query, (book_name,))
    parts = cur.fetchall()
    return parts

#یه فانکشن اینجا باشه که وقتی پارت رو بهش میدی تعداد شعر های اون پارت رو بهت برگردونه که مثلا باب اول بوستان ۲۵ دونه شعر داره
def get_poem_count_by_part(part_name,book_name):
    conn = sqlite3.connect("poems.db")
    cur = conn.cursor()

    query ='''
            SELECT COUNT(*)
            FROM poems
            JOIN parts ON poems.parts_id = parts.id
            JOIN books ON parts.book_id = books.id
            WHERE parts.part_name = ? AND books.book_name = ?;
                '''
    
    cur.execute(query, (part_name, book_name))
    count = cur.fetchone()[0]
    return count

def get_poem_text_by_number(part_name, book_name, poem_number):
    conn = sqlite3.connect("poems.db")
    cur = conn.cursor()

    query ='''
            SELECT poems.verse, parts.part_name, poets.poet_name
            FROM poems
            JOIN parts ON poems.parts_id = parts.id
            JOIN books ON parts.book_id = books.id
            JOIN poets ON books.poets_id = poets.id
            WHERE parts.part_name = ? AND books.book_name = ?
            ORDER BY poems.id
            LIMIT 1 OFFSET ?;
                '''
    
    cur.execute(query, (part_name, book_name, poem_number - 1))
    poem_text = cur.fetchone()
    return poem_text if poem_text else None

def get_poets ():
    conn = sqlite3.connect("poems.db")
    cur = conn.cursor()

    query = '''
        SELECT poets.poet_name
        FROM poets
'''
    cur.execute(query)
    poem_text = cur.fetchall
    return poem_text