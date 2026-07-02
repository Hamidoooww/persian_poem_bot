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