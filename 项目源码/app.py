from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
from chat_system import get_relevant_chain, handle_database_query
from tea_chatbot import handle_tea_chat, handle_tea_database_query
from book_chatbot import handle_book_chat, handle_book_database_query
from coffee_chatbot import handle_coffee_chat, handle_coffee_database_query

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL 配置
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='shops'
    )

# 路由
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user and user['password'] == password:
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            error = '用户名或密码错误'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            cursor.close()
            db.close()
            error = '用户名已存在'
            return render_template('register.html', error=error)
        else:
            cursor.execute("INSERT INTO Users (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
            cursor.close()
            db.close()
            return redirect(url_for('login'))
    return render_template('register.html', error=None)

@app.route('/index')
def index():
    user_id = session.get('user_id')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, user_message, bot_response FROM ChatHistory WHERE user_id = %s", (user_id,))
    chat_history = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('index.html', chat_history=chat_history)

@app.route('/book')
def book():
    user_id = session.get('user_id')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, user_message, bot_response FROM ChatHistory WHERE user_id = %s", (user_id,))
    chat_history = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('book.html', chat_history=chat_history)

@app.route('/book_shop', methods=['GET', 'POST'])
def book_shop():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Book_Goods")
    goods = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('book_shop.html', goods=goods)

@app.route('/add_to_book_order', methods=['POST'])
def add_to_book_order():
    user_id = session.get('user_id')
    goods_id = request.form['goods_id']
    quantity = int(request.form['quantity'])

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # 检查是否有未完成的订单
    cursor.execute("SELECT id FROM Book_Orders WHERE user_id = %s", (user_id,))
    order = cursor.fetchone()

    if order:
        order_id = order['id']
    else:
        # 创建一个新的订单
        cursor.execute(
            "INSERT INTO Book_Orders (user_id, order_date, total_amount) VALUES (%s, NOW(), 0)",
            (user_id,))
        db.commit()
        order_id = cursor.lastrowid

    # 添加商品到订单中
    cursor.execute("INSERT INTO Book_OrderGoods (order_id, goods_id, quantity) VALUES (%s, %s, %s)",
                   (order_id, goods_id, quantity))

    # 更新订单的总金额
    cursor.execute("""
    UPDATE Book_Orders
    SET total_amount = (SELECT SUM(Book_Goods.price * Book_OrderGoods.quantity)
                        FROM Book_OrderGoods
                        JOIN Book_Goods ON Book_OrderGoods.goods_id = Book_Goods.id
                        WHERE Book_OrderGoods.order_id = %s)
    WHERE id = %s
    """, (order_id, order_id))

    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('book_shop'))

@app.route('/coffee')
def coffee():
    user_id = session.get('user_id')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, user_message, bot_response FROM ChatHistory WHERE user_id = %s", (user_id,))
    chat_history = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('coffee.html', chat_history=chat_history)

@app.route('/coffee_shop', methods=['GET', 'POST'])
def coffee_shop():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Coffee_Goods")
    goods = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('coffee_shop.html', goods=goods)

@app.route('/add_to_coffee_order', methods=['POST'])
def add_to_coffee_order():
    user_id = session.get('user_id')
    goods_id = request.form['goods_id']
    quantity = int(request.form['quantity'])

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # 检查是否有未完成的订单
    cursor.execute("SELECT id FROM Coffee_Orders WHERE user_id = %s", (user_id,))
    order = cursor.fetchone()

    if order:
        order_id = order['id']
    else:
        # 创建一个新的订单
        cursor.execute(
            "INSERT INTO Coffee_Orders (user_id, order_date, total_amount) VALUES (%s, NOW(), 0)",
            (user_id,))
        db.commit()
        order_id = cursor.lastrowid

    # 添加商品到订单中
    cursor.execute("INSERT INTO Coffee_OrderGoods (order_id, goods_id, quantity) VALUES (%s, %s, %s)",
                   (order_id, goods_id, quantity))

    # 更新订单的总金额
    cursor.execute("""
    UPDATE Coffee_Orders
    SET total_amount = (SELECT SUM(Coffee_Goods.price * Coffee_OrderGoods.quantity)
                        FROM Coffee_OrderGoods
                        JOIN Coffee_Goods ON Coffee_OrderGoods.goods_id = Coffee_Goods.id
                        WHERE Coffee_OrderGoods.order_id = %s)
    WHERE id = %s
    """, (order_id, order_id))

    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('coffee_shop'))

@app.route('/cart')
def cart():
    user_id = session.get('user_id')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # 查询咖啡店订单
    cursor.execute("""
    SELECT 'Coffee' as type, Coffee_Goods.id, Coffee_Goods.name, Coffee_Goods.price, Coffee_OrderGoods.quantity
    FROM Coffee_OrderGoods
    JOIN Coffee_Goods ON Coffee_OrderGoods.goods_id = Coffee_Goods.id
    JOIN Coffee_Orders ON Coffee_OrderGoods.order_id = Coffee_Orders.id
    WHERE Coffee_Orders.user_id = %s
    """, (user_id,))
    coffee_items = cursor.fetchall()

    # 查询书店订单
    cursor.execute("""
    SELECT 'Book' as type, Book_Goods.id, Book_Goods.name, Book_Goods.price, Book_OrderGoods.quantity
    FROM Book_OrderGoods
    JOIN Book_Goods ON Book_OrderGoods.goods_id = Book_Goods.id
    JOIN Book_Orders ON Book_OrderGoods.order_id = Book_Orders.id
    WHERE Book_Orders.user_id = %s
    """, (user_id,))
    book_items = cursor.fetchall()

    # 查询茶叶店订单
    cursor.execute("""
    SELECT 'Tea' as type, Tea_Goods.id, Tea_Goods.name, Tea_Goods.price, Tea_OrderGoods.quantity
    FROM Tea_OrderGoods
    JOIN Tea_Goods ON Tea_OrderGoods.goods_id = Tea_Goods.id
    JOIN Tea_Orders ON Tea_OrderGoods.order_id = Tea_Orders.id
    WHERE Tea_Orders.user_id = %s
    """, (user_id,))
    tea_items = cursor.fetchall()

    # 合并所有订单项
    cart_items = coffee_items + book_items + tea_items

    cursor.close()
    db.close()
    return render_template('cart.html', cart_items=cart_items)

@app.route('/tea')
def tea():
    user_id = session.get('user_id')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, user_message, bot_response FROM ChatHistory WHERE user_id = %s", (user_id,))
    chat_history = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('tea.html', chat_history=chat_history)

@app.route('/tea_shop', methods=['GET', 'POST'])
def tea_shop():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Tea_Goods")
    goods = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('tea_shop.html', goods=goods)


@app.route('/add_to_tea_order', methods=['POST'])
def add_to_tea_order():
    user_id = session.get('user_id')
    goods_id = request.form['goods_id']
    quantity = int(request.form['quantity'])

    db = get_db_connection()
    cursor = db.cursor(dictionary=True, buffered=True)

    try:
        # 检查是否有未完成的订单
        cursor.execute("SELECT id FROM Tea_Orders WHERE user_id = %s", (user_id,))
        order = cursor.fetchone()

        if order:
            order_id = order['id']
        else:
            # 创建一个新的订单
            cursor.execute(
                "INSERT INTO Tea_Orders (user_id, order_date, total_amount) VALUES (%s, NOW(), 0)",
                (user_id,))
            db.commit()
            order_id = cursor.lastrowid

        # 添加商品到订单中
        cursor.execute("INSERT INTO Tea_OrderGoods (order_id, goods_id, quantity) VALUES (%s, %s, %s)",
                       (order_id, goods_id, quantity))

        # 更新订单的总金额
        cursor.execute("""
        UPDATE Tea_Orders
        SET total_amount = (SELECT SUM(Tea_Goods.price * Tea_OrderGoods.quantity)
                            FROM Tea_OrderGoods
                            JOIN Tea_Goods ON Tea_OrderGoods.goods_id = Tea_Goods.id
                            WHERE Tea_OrderGoods.order_id = %s)
        WHERE id = %s
        """, (order_id, order_id))

        db.commit()
    finally:
        cursor.close()

    return redirect(url_for('tea_shop'))


@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/chat-history/<int:chat_id>')
def get_chat_history(chat_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT user_message, bot_response FROM ChatHistory WHERE id = %s", (chat_id,))
    chat_history = cursor.fetchone()
    cursor.close()
    db.close()
    if chat_history:
        messages = [
            {"role": "user", "content": chat_history["user_message"]},
            {"role": "assistant", "content": chat_history["bot_response"]}
        ]
    else:
        messages = []
    return jsonify(messages)

@app.route('/chat', methods=['GET','POST'])
def chat():
    data = request.get_json()
    user_message = data['message']
    user_id = session.get('user_id')

    # 判断问题是否需要进行数据库查询
    is_db_query, db_response = handle_database_query(user_message)
    if is_db_query:
        ai_message = " ".join(str(item) for item in db_response)
    else:
        relevant_chain = get_relevant_chain(user_message)
        response = relevant_chain.invoke({
            "chat_history": [],
            "input": user_message
        })

        if isinstance(response, dict) and 'answer' in response:
            ai_message = response["answer"]
        else:
            ai_message = response

    # 将对话存储到数据库中
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO ChatHistory (user_message, bot_response, user_id) VALUES (%s, %s, %s)", (user_message, ai_message, user_id))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"answer": ai_message})

@app.route('/chat/tea', methods=['GET','POST'])
def chat_tea():
    data = request.get_json()
    user_message = data['message']
    user_id = session.get('user_id')

    # 判断问题是否需要进行数据库查询
    is_db_query, db_response = handle_tea_database_query(user_message)
    if is_db_query:
        ai_message = " ".join(str(item) for item in db_response)
    else:
        relevant_chain = handle_tea_chat(user_message)
        response = relevant_chain.invoke({
            "chat_history": [],
            "input": user_message
        })

        if isinstance(response, dict) and 'answer' in response:
            ai_message = response["answer"]
        else:
            ai_message = response

    # 将对话存储到数据库中
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO ChatHistory (user_message, bot_response, user_id) VALUES (%s, %s, %s)",
                   (user_message, ai_message, user_id))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"answer": ai_message})

@app.route('/chat/book', methods=['GET','POST'])
def chat_book():
    data = request.get_json()
    user_message = data['message']
    user_id = session.get('user_id')

    # 判断问题是否需要进行数据库查询
    is_db_query, db_response = handle_book_database_query(user_message)
    if is_db_query:
        ai_message = " ".join(str(item) for item in db_response)
    else:
        relevant_chain = handle_book_chat(user_message)
        response = relevant_chain.invoke({
            "chat_history": [],
            "input": user_message
        })

        if isinstance(response, dict) and 'answer' in response:
            ai_message = response["answer"]
        else:
            ai_message = response

    # 将对话存储到数据库中
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO ChatHistory (user_message, bot_response, user_id) VALUES (%s, %s, %s)",
                   (user_message, ai_message, user_id))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"answer": ai_message})

@app.route('/chat/coffee', methods=['POST'])
def chat_coffee():
    data = request.get_json()
    user_message = data['message']
    user_id = session.get('user_id')

    # 判断问题是否需要进行数据库查询
    is_db_query, db_response = handle_coffee_database_query(user_message)
    if is_db_query:
        ai_message = " ".join(str(item) for item in db_response)
    else:
        relevant_chain = handle_coffee_chat(user_message)
        response = relevant_chain.invoke({
            "chat_history": [],
            "input": user_message
        })

        if isinstance(response, dict) and 'answer' in response:
            ai_message = response["answer"]
        else:
            ai_message = response

    # 将对话存储到数据库中
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO ChatHistory (user_message, bot_response, user_id) VALUES (%s, %s, %s)",
                   (user_message, ai_message, user_id))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"answer": ai_message})

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.errorhandler(500)
def system_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
