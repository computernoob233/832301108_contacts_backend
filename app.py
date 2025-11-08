# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_PATH = "contacts.db"


def init_db():
    """初始化数据库，如果表不存在则创建，并确保包含 email 和 address 字段"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建表（如果不存在）
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)
    
    # 检查是否已有 email 字段，没有则添加（兼容旧数据库）
    cursor.execute("PRAGMA table_info(contacts)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'email' not in columns:
        cursor.execute("ALTER TABLE contacts ADD COLUMN email TEXT")
    
    if 'address' not in columns:
        cursor.execute("ALTER TABLE contacts ADD COLUMN address TEXT")
    
    conn.commit()
    conn.close()


@app.route('/contacts', methods=['GET'])
def get_contacts():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM contacts").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


@app.route('/contacts', methods=['POST'])
def add_contact():
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体不能为空"}), 400

    name = data.get('name', '').strip()
    phone = data.get('phone', '').strip()
    email = data.get('email', '').strip() or None
    address = data.get('address', '').strip() or None

    if not name or not phone:
        return jsonify({"error": "姓名和电话不能为空"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
        (name, phone, email, address)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({
        "id": new_id,
        "name": name,
        "phone": phone,
        "email": email,
        "address": address
    }), 201


@app.route('/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体不能为空"}), 400

    name = data.get('name', '').strip()
    phone = data.get('phone', '').strip()
    email = data.get('email', '').strip() or None
    address = data.get('address', '').strip() or None

    if not name or not phone:
        return jsonify({"error": "姓名和电话不能为空"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE contacts SET name = ?, phone = ?, email = ?, address = ? WHERE id = ?",
        (name, phone, email, address, contact_id)
    )
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "联系人不存在"}), 404
    conn.close()
    return jsonify({
        "id": contact_id,
        "name": name,
        "phone": phone,
        "email": email,
        "address": address
    })


@app.route('/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "联系人不存在"}), 404
    conn.close()
    return jsonify({"message": "删除成功"}), 200


if __name__ == '__main__':
    init_db()  # 启动时自动初始化或升级数据库
    app.run(host='0.0.0.0', port=5000, debug=True)