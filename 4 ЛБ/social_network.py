
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class SocialNetworkDB:

    def __init__(self, db_path: str = "social_network.db"):
        self.db_path = db_path
        self.create_tables()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                bio TEXT,
                avatar_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                image_url TEXT,
                likes_count INTEGER DEFAULT 0,
                comments_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                likes_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES posts(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                post_id INTEGER,
                comment_id INTEGER,
                like_type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (post_id) REFERENCES posts(id),
                FOREIGN KEY (comment_id) REFERENCES comments(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS friends (
                user_id INTEGER NOT NULL,
                friend_id INTEGER NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, friend_id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (friend_id) REFERENCES users(id)
            )
        """)

        conn.commit()
        conn.close()

    def add_user(self, username: str, email: str, bio: str = "", avatar_url: str = "") -> int:

        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO users (username, email, bio, avatar_url)
                VALUES (?, ?, ?, ?)
            """, (username, email, bio, avatar_url))

            conn.commit()
            user_id = cursor.lastrowid
            return user_id

        except sqlite3.IntegrityError as e:
            print(f"Помилка: {e}")
            return None
        finally:
            conn.close()

    def get_user(self, user_id: int) -> Optional[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()

        if user:
            return {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'bio': user[3],
                'avatar_url': user[4],
                'created_at': user[5]
            }
        return None

    def get_all_users(self) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
        users = cursor.fetchall()
        conn.close()

        return [
            {
                'id': u[0],
                'username': u[1],
                'email': u[2],
                'bio': u[3],
                'avatar_url': u[4],
                'created_at': u[5]
            } for u in users
        ]
    def add_post(self, user_id: int, content: str, image_url: str = "") -> int:
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO posts (user_id, content, image_url)
                VALUES (?, ?, ?)
            """, (user_id, content, image_url))

            conn.commit()
            post_id = cursor.lastrowid
            return post_id
        finally:
            conn.close()

    def get_post(self, post_id: int) -> Optional[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.*, u.username, u.avatar_url
            FROM posts p
            JOIN users u ON p.user_id = u.id
            WHERE p.id = ?
        """, (post_id,))

        post = cursor.fetchone()
        conn.close()

        if post:
            return {
                'id': post[0],
                'user_id': post[1],
                'content': post[2],
                'image_url': post[3],
                'likes_count': post[4],
                'comments_count': post[5],
                'created_at': post[6],
                'username': post[7],
                'avatar_url': post[8]
            }
        return None

    def get_user_posts(self, user_id: int) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.*, u.username
            FROM posts p
            JOIN users u ON p.user_id = u.id
            WHERE p.user_id = ?
            ORDER BY p.created_at DESC
        """, (user_id,))

        posts = cursor.fetchall()
        conn.close()

        return [
            {
                'id': p[0],
                'user_id': p[1],
                'content': p[2],
                'image_url': p[3],
                'likes_count': p[4],
                'comments_count': p[5],
                'created_at': p[6],
                'username': p[7]
            } for p in posts
        ]


    def add_comment(self, post_id: int, user_id: int, content: str) -> int:

        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO comments (post_id, user_id, content)
                VALUES (?, ?, ?)
            """, (post_id, user_id, content))

            cursor.execute("""
                UPDATE posts SET comments_count = comments_count + 1 WHERE id = ?
            """, (post_id,))

            conn.commit()
            comment_id = cursor.lastrowid
            return comment_id
        finally:
            conn.close()

    def get_post_comments(self, post_id: int) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.*, u.username, u.avatar_url
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.post_id = ?
            ORDER BY c.created_at DESC
        """, (post_id,))

        comments = cursor.fetchall()
        conn.close()

        return [
            {
                'id': c[0],
                'post_id': c[1],
                'user_id': c[2],
                'content': c[3],
                'likes_count': c[4],
                'created_at': c[5],
                'username': c[6],
                'avatar_url': c[7]
            } for c in comments
        ]

    def add_like(self, user_id: int, post_id: int = None, comment_id: int = None) -> bool:

        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            like_type = 'post' if post_id else 'comment'

            cursor.execute("""
                INSERT INTO likes (user_id, post_id, comment_id, like_type)
                VALUES (?, ?, ?, ?)
            """, (user_id, post_id, comment_id, like_type))

            if post_id:
                cursor.execute("""
                    UPDATE posts SET likes_count = likes_count + 1 WHERE id = ?
                """, (post_id,))
            else:
                cursor.execute("""
                    UPDATE comments SET likes_count = likes_count + 1 WHERE id = ?
                """, (comment_id,))

            conn.commit()
            return True
        except sqlite3.IntegrityError:
            print("Ви вже залайкали це")
            return False
        finally:
            conn.close()


    def send_friend_request(self, user_id: int, friend_id: int) -> bool:

        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO friends (user_id, friend_id, status)
                VALUES (?, ?, 'pending')
            """, (user_id, friend_id))

            conn.commit()
            return True
        except sqlite3.IntegrityError:
            print("Запит вже існує")
            return False
        finally:
            conn.close()

    def accept_friend_request(self, user_id: int, friend_id: int) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE friends SET status = 'accepted'
                WHERE user_id = ? AND friend_id = ? AND status = 'pending'
            """, (friend_id, user_id))

            conn.commit()
            return True
        finally:
            conn.close()

    def get_user_friends(self, user_id: int) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT u.* FROM users u
            JOIN friends f ON u.id = f.friend_id
            WHERE f.user_id = ? AND f.status = 'accepted'
        """, (user_id,))

        friends = cursor.fetchall()
        conn.close()

        return [
            {
                'id': f[0],
                'username': f[1],
                'email': f[2],
                'bio': f[3],
                'avatar_url': f[4]
            } for f in friends
        ]

def main():

    db = SocialNetworkDB("social_network.db")

    print("=" * 60)
    print("ДЕМО: Соціальна мережа")
    print("=" * 60)

    print("\n Додавання користувачів...")
    user1_id = db.add_user("john_doe", "john@example.com", "Привіт, я John!")
    user2_id = db.add_user("jane_smith", "jane@example.com", "Люблю подорожувати")
    user3_id = db.add_user("alex_wilson", "alex@example.com", "Розробник ПО")
    print(f" Додано 3 користувачі")


    print("\n Додавання постів...")
    post1_id = db.add_post(user1_id, "Чудовий день для програмування!")
    post2_id = db.add_post(user2_id, "Новій подорож до Кракова")
    post3_id = db.add_post(user1_id, "Запустив новий проект")
    print(f" Додано 3 пості")

    print("\n Додавання коментарів...")
    db.add_comment(post1_id, user2_id, "Згоден, дуже добре!")
    db.add_comment(post1_id, user3_id, "Привіт, John!")
    db.add_comment(post2_id, user3_id, "Виглядає дивовижно!")
    print(f" Додано 3 коментарі")

    print("\n Додавання лайків...")
    db.add_like(user2_id, post_id=post1_id)
    db.add_like(user3_id, post_id=post1_id)
    db.add_like(user1_id, post_id=post2_id)
    print(f" Додано 3 лайки")

    print("\nЗапити на дружбу...")
    db.send_friend_request(user1_id, user2_id)
    db.accept_friend_request(user1_id, user2_id)
    print(f" John та Jane - друзі!")

    print("\n" + "=" * 60)
    print("ІНФОРМАЦІЯ ЗІ СИСТЕМИ")
    print("=" * 60)

    print("\n Користувачі:")
    for user in db.get_all_users():
        print(f"  - {user['username']} ({user['email']})")

    print(f"\n Пост #{post1_id}:")
    post = db.get_post(post1_id)
    print(f"  Автор: {post['username']}")
    print(f"  Вміст: {post['content']}")
    print(f"  Лайки: {post['likes_count']}, Коментарі: {post['comments_count']}")

    print(f"\n  Коментарі:")
    for comment in db.get_post_comments(post1_id):
        print(f"    - {comment['username']}: {comment['content']}")

    print(f"\n Друзі {db.get_user(user1_id)['username']}:")
    for friend in db.get_user_friends(user1_id):
        print(f"  - {friend['username']}")

if __name__ == "__main__":
    main()
