from flask import Flask, request, jsonify, render_template
import sqlite3
import json

app = Flask(__name__)

DB_NAME = "ShoppingDB.db"

# ================== Câu 1 ==================
@app.route('/')
def index():
    return "1_TranPhuongDuy_1"   # sửa lại thông tin của anh

# ================== DB connect ==================
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ================== Câu 2 ==================
# GET ALL
@app.route('/Customers', methods=['GET'])
def get_customers():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Customers")
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# DELETE
@app.route('/Customers', methods=['DELETE'])
def delete_customer():
    id = request.args.get('id')
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM Customers WHERE customer_id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Deleted successfully"})

# ================== Câu 3 ==================
# ADD
@app.route('/Customers', methods=['POST'])
def add_customer():
    data = request.json
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO Customers(first_name,last_name,company,address,email)
        VALUES (?,?,?,?,?)
    """, (data['first_name'], data['last_name'],
          data['company'], data['address'], data['email']))

    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    return jsonify({"new_id": new_id})

# UPDATE
@app.route('/Customers', methods=['PUT'])
def update_customer():
    data = request.json
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE Customers
        SET first_name=?, last_name=?, company=?, address=?, email=?
        WHERE customer_id=?
    """, (data['first_name'], data['last_name'],
          data['company'], data['address'], data['email'], data['customer_id']))

    conn.commit()
    conn.close()
    return jsonify({"message": "Updated successfully"})

# ================== Câu 4 ==================
# a) check tồn tại
@app.route('/checkCustomer', methods=['POST'])
def check_customer():
    data = request.json
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM Customers WHERE email=? AND first_name=?
    """, (data['email'], data['first_name']))

    result = cur.fetchone()
    conn.close()

    return jsonify({"exists": True if result else False})

# b) search gần đúng
@app.route('/searchCustomer', methods=['GET'])
def search_customer():
    keyword = request.args.get('q')
    conn = get_db()
    cur = conn.cursor()

    query = f"""
        SELECT * FROM Customers
        WHERE first_name LIKE '%{keyword}%'
        OR last_name LIKE '%{keyword}%'
        OR company LIKE '%{keyword}%'
        OR address LIKE '%{keyword}%'
        OR email LIKE '%{keyword}%'
    """

    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])

# c) giả lập đơn hàng
@app.route('/customerOrders/<int:id>', methods=['GET'])
def get_orders(id):
    # giả lập vì DB không có bảng Orders
    return jsonify({
        "customer_id": id,
        "orders": ["Order1", "Order2"]
    })

# d) insert list
@app.route('/bulkCustomers', methods=['POST'])
def bulk_insert():
    data = request.json  # list

    conn = get_db()
    cur = conn.cursor()

    for c in data:
        cur.execute("""
            INSERT INTO Customers(first_name,last_name,company,address,email)
            VALUES (?,?,?,?,?)
        """, (c['first_name'], c['last_name'],
              c['company'], c['address'], c['email']))

    conn.commit()
    conn.close()

    return jsonify({"message": "Inserted list successfully"})

# ================== Câu 5 ==================
@app.route('/view')
def view():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)