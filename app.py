import os
import secrets
import subprocess
from datetime import datetime

import pymysql
from flask import Flask, render_template, request, redirect, flash, jsonify, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # 生成随机的十六进制字符串作为密钥


# 注册
@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    # post:数据获取
    name = request.form.get("name")
    pwd = request.form.get("pwd")
    confirm = request.form.get("confirm")
    auth = request.form.get("auth")
    remarks = request.form.get("remarks")

    # 校验数据
    if not name:
        flash("姓名不能为空", category="error")
        return redirect("/register")
    if not pwd:
        flash("密码不能为空", category="error")
        return redirect("/register")
    if not confirm:
        flash("未确认密码", category="error")
        return redirect("/register")
    if not auth:
        flash("权限不能为空", category="error")
        return redirect("/register")
    if pwd != confirm:
        flash("密码输入不一致", category="error")
        return redirect("/register")

    # 连接数据库
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="password", charset='utf8', db='warehouse')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 判断姓名重复
    cursor.execute("select * from user where uname=%s", [name])
    data_list = cursor.fetchall()
    if len(data_list) != 0:
        flash("姓名已存在", category="error")
        return redirect("/register")

    # 权限转为smallint
    if auth == "superadmin":
        authority = 0
    else:
        authority = 1

    # 数据库安全性：密码加密
    hashed_pwd = generate_password_hash(pwd)

    # 添加用户
    sql = "insert into user(uname,pwd,auth,remarks) values(%s,%s,%s,%s)"
    cursor.execute(sql, [name, hashed_pwd, authority, remarks])
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/login')


# 登录
@app.route('/login', methods=["POST", "GET"])
@app.route('/', methods=["POST", "GET"])
def login():
    # 检查是否已登录
    if 'name' in session:
        if session['auth'] == 0:
            return redirect("/edit/admin")
        return redirect("/edit/client")

    if request.method == 'GET':
        return render_template("login.html")
    # 获取登录信息
    name = request.form.get('name')
    pwd = request.form.get('pwd')

    # 校验数据
    if not name:
        flash("姓名不能为空", category="error")
        return redirect("/login")
    if not pwd:
        flash("密码不能为空", category='error')
        return redirect("/login")

    # 连接数据库
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="password", charset='utf8', db='warehouse')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select pwd,auth from user where uname=%s"
    cursor.execute(sql, [name])
    data_list = cursor.fetchall()

    # 找不到记录，姓名错误或没有注册
    if len(data_list) == 0:
        flash("姓名错误或还没有注册", category="error")
        return redirect("/login")

    # 验证密码
    for data in data_list:
        if check_password_hash(data['pwd'], pwd):
            authority = data['auth']
            session['name'] = name
            session['pwd'] = pwd
            session['auth'] = authority
        else:
            flash("密码错误", category="error")
            return redirect("/login")

    cursor.close()
    conn.close()
    if authority == 0:
        return redirect("/edit/admin")
    return redirect("/edit/client")


# 编辑管理员页面
@app.route('/edit/admin', methods=["POST", "GET"])
def edit_admin():
    # 验证是否登录
    if 'name' not in session:
        flash("请先登录！", category="error")
        return redirect("/login")
    # 获取搜索信息
    search = request.args.get("search")
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='superadmin', passwd="superadmin", charset='utf8',
                           db='warehouse')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    if search is None:
        cursor.execute("select uid,uname,auth,remarks from user where auth=1")
    else:
        cursor.execute("select uid,uname,auth,remarks from user where uname like %s and auth=1", ["%" + search + "%"])

    data_list = cursor.fetchall()

    conn.close()
    cursor.close()
    return render_template("edit_admin.html", data_list=data_list, uname=session['name'])


# 修改管理员权限
@app.route('/edit/admin/<int:id>', methods=["POST"])
def change_auth(id):
    # 检查是否登录
    if 'name' not in session:
        flash("请先登录！", category="error")
        return redirect('/login')
    auth = request.form.get('RadioOption')
    # 未选择权限
    if not auth:
        return redirect('/edit/admin')
    # 更新user
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='superadmin', password='superadmin', charset='utf8',
                           db='warehouse')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select auth from user where uid=%s", [id])
    current_auth = cursor.fetchone()['auth']

    if auth == 'super_admin' and current_auth == 1:
        sql = "update user set auth=0 where uid=%s"
        cursor.execute(sql, [id])
        conn.commit()
    elif auth == 'admin' and current_auth == 0:
        sql = "update user set auth=1 where uid=%s"
        cursor.execute(sql, [id])
        conn.commit()

    cursor.close()
    conn.close()

    return redirect('/edit/admin')


# 删除用户
@app.route('/edit/admin/delete/<int:id>', methods=["POST", "GET"])
def delete_admin(id):
    # 检查是否登录
    if 'name' not in session:
        flash("请先登录！", category="error")
        return redirect('/login')
    # 删除用户
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='superadmin', password='superadmin', db='warehouse')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "delete from user where uid=%s"
    cursor.execute(sql, [id])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/edit/admin')


# 客户管理页面
@app.route('/edit/client', methods=["POST", "GET"])
def edit_client():
    # 检查是否登录
    if 'name' not in session:
        flash("请先登录！", category="error")
        return redirect('/login')
    search = request.args.get("search")
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='admin', passwd="admin", charset='utf8',
                           db='warehouse')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    cursor.execute("select cid,cname,type,contacts,contact_number,address,remarks from client")
    data_list = cursor.fetchall()

    if search is not None:
        cursor.execute("select cid,cname,type,contacts,contact_number,address,remarks from client where cname like %s "
                       + "or type like %s or contacts like %s or contact_number like %s or address like %s",
                       ["%" + search + "%", "%" + search + "%", "%" + search + "%", "%" + search + "%",
                        "%" + search + "%"])
        data_list = cursor.fetchall()

    conn.close()
    cursor.close()
    return render_template("edit_client.html", data_list=data_list, uname=session['name'])


# 修改客户信息
@app.route('/edit/client/<int:id>', methods=["POST", "GET"])
def change_client(id):
    # 检查是否登录
    if 'name' not in session:
        flash("请先登录！", category="error")
        return redirect('/login')
    cname = request.form.get('cname')
    type = request.form.get('type')
    contacts = request.form.get('contacts')
    contact_number = request.form.get('contact_number')
    address = request.form.get('address')
    remarks = request.form.get('remarks')
    # 校验数据:使用ajax
    if cname == "":
        return jsonify({'error_message': '客户姓名不能为空'})
    if contacts == "":
        return jsonify({'error_message': '联系人不能为空'})
    if contact_number == "":
        return jsonify({'error_message': '联系电话不能为空'})
    # 更新client
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='admin', password='admin', charset='utf8',
                           db='warehouse')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "update client set cname=%s,type=%s,contacts=%s,contact_number=%s,address=%s,remarks=%s where cid=%s"
    cursor.execute(sql, [cname, type, contacts, contact_number, address, remarks, id])
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/edit/client')


# 删除客户
@app.route('/edit/client/delete/<int:id>', methods=["POST", "GET"])
def delete_client(id):
    # 检查是否登录
    if 'name' not in session:
        flash("请先登录！", category="error")
        return redirect('/login')
    # 删除客户
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='admin', password='admin', db='warehouse')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "delete from client where cid=%s"
    cursor.execute(sql, [id])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/edit/client')


# 新增客户
@app.route('/edit/client/add', methods=["POST", "GET"])
def add_client():
    # 检查是否登录
    if 'name' not in session:
        flash("请先登录！", category="error")
        return redirect('/login')
    cname = request.form.get('cname')
    type = request.form.get('type')
    contacts = request.form.get('contacts')
    contact_number = request.form.get('contact_number')
    address = request.form.get('address')
    remarks = request.form.get('remarks')
    # 校验数据:使用ajax
    if cname == "":
        return jsonify({'error_message': '客户姓名不能为空'})
    if contacts == "":
        return jsonify({'error_message': '联系人不能为空'})
    if contact_number == "":
        return jsonify({'error_message': '联系电话不能为空'})

    # 新增client
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='admin', password='admin', charset='utf8',
                           db='warehouse')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "insert into client(cname,type,contacts,contact_number,address,remarks) values(%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, [cname, type, contacts, contact_number, address, remarks])
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/edit/client')


# 仓库管理页面
@app.route('/edit/warehouse', methods=["POST", "GET"])
def edit_warehouse():
    # 检查是否登录
    if 'name' not in session:
        flash("请先登录！", category="error")
        return redirect('/login')
    search = request.args.get("search")
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='admin', passwd="admin", charset='utf8',
                           db='warehouse')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    cursor.execute("select wid,wname,description from warehouse")
    data_list = cursor.fetchall()

    if search is not None:
        cursor.execute("select wid,wname,description from warehouse where wname like %s "
                       + "or description like %s", ["%" + search + "%", "%" + search + "%"])
        data_list = cursor.fetchall()

    conn.close()
    cursor.close()
    return render_template("edit_warehouse.html", data_list=data_list, uname=session['name'])


# 新增仓库
@app.route('/edit/warehouse/add', methods=["POST", "GET"])
def add_warehouse():
    # 检查是否登录
    if 'name' not in session:
        flash("请先登录！", category="error")
        return redirect('/login')
    wname = request.form.get('wname')
    description = request.form.get('description')
    # 校验数据:使用ajax
    if wname == "":
        return jsonify({'error_message': '仓库名称不能为空'})

    # 新增warehouse
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='admin', password='admin', charset='utf8',
                           db='warehouse')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "insert into warehouse(wname,description) values(%s,%s)"
    cursor.execute(sql, [wname, description])
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/edit/warehouse')


# 修改仓库
@app.route('/edit/warehouse/<int:id>', methods=["POST", "GET"])
def change_warehouse(id):
    # 检查是否登录
    if 'name' not in session:
        flash("请先登录！", category="error")
        return redirect('/login')
    wname = request.form.get('wname')
    description = request.form.get('description')
    # 校验数据:使用ajax
    if wname == "":
        return jsonify({'error_message': '仓库名称不能为空'})
    # 更新warehouse
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='admin', password='admin', charset='utf8',
                           db='warehouse')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "update warehouse set wname=%s,description=%s where wid=%s"
    cursor.execute(sql, [wname, description, id])
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/edit/warehouse')


# 删除仓库
@app.route('/edit/warehouse/delete/<int:id>', methods=["POST", "GET"])
def delete_warehouse(id):
    # 检查是否登录
    if 'name' not in session:
        flash("请先登录！", category="error")
        return redirect('/login')
    # 删除客户
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='admin', password='admin', db='warehouse')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "delete from warehouse where wid=%s"
    cursor.execute(sql, [id])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/edit/warehouse')


# 产品管理页面
@app.route('/edit/product', methods=["POST", "GET"])
def edit_product():
    # 检查是否登录
    if 'name' not in session:
        flash("请先登录！", category="error")
        return redirect('/login')
    search = request.args.get("search")
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='admin', passwd="admin", charset='utf8',
                           db='warehouse')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    cursor.execute("select pid,pname,specification,reference_price,maxlim,minlim from product")
    data_list = cursor.fetchall()

    if search is not None:
        cursor.execute("select pid,pname,specification,reference_price,maxlim,minlim from product where pname like %s" +
                       " or specification like %s or reference_price like %s or maxlim like %s or minlim like %s"
                       , ["%" + search + "%", "%" + search + "%", "%" + search + "%", "%" + search + "%",
                          "%" + search + "%"])
        data_list = cursor.fetchall()

    conn.close()
    cursor.close()
    return render_template("edit_product.html", data_list=data_list, uname=session['name'])


# 修改产品信息
@app.route('/edit/product/<int:id>', methods=["POST", "GET"])
def change_product(id):
    # 检查是否登录
    if 'name' not in session:
        flash("请先登录！", category="error")
        return redirect('/login')
    pname = request.form.get('pname')
    specification = request.form.get(' specification')
    reference_price = request.form.get('reference_price')
    maxlim = request.form.get('maxlim')
    minlim = request.form.get('minlim')
    # 校验数据:使用ajax
    if pname == "":
        return jsonify({'error_message': '产品名称不能为空'})
    if not reference_price.isdigit():
        if reference_price.count('.') != 1:
            return jsonify({'error_message': '参考价格需为小数'})
        left = reference_price.split('.')[0]
        right = reference_price.split('.')[1]
        if not (left.isdigit() and right.isdigit() and len(right) <= 2):
            return jsonify({'error_message': '参考价格需为小数'})
    if not maxlim.isdigit():
        return jsonify({'error_message': '数量上限需为整数'})
    if not minlim.isdigit():
        return jsonify({'error_message': '数量下限需为整数'})
    maxlim = int(maxlim)
    minlim = int(minlim)
    if maxlim < minlim:
        return jsonify({'error_message': '数量上限需大于下限'})
    # 更新product
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='admin', password='admin', charset='utf8',
                           db='warehouse')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "update product set pname=%s,specification=%s,reference_price=%s,maxlim=%s,minlim=%s where pid=%s"
    cursor.execute(sql, [pname, specification, reference_price, maxlim, minlim, id])
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/edit/product')


# 删除产品
@app.route('/edit/product/delete/<int:id>', methods=["POST", "GET"])
def delete_product(id):
    # 检查是否登录
    if 'name' not in session:
        flash("请先登录！", category="error")
        return redirect('/login')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='admin', password='admin', db='warehouse')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "delete from product where pid=%s"
    cursor.execute(sql, [id])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/edit/product')


# 新增产品
@app.route('/edit/product/add', methods=["POST", "GET"])
def add_product():
    # 检查是否登录
    if 'name' not in session:
        flash("请先登录！", category="error")
        return redirect('/login')
    pname = request.form.get('pname')
    specification = request.form.get(' specification')
    reference_price = request.form.get('reference_price')
    maxlim = request.form.get('maxlim')
    minlim = request.form.get('minlim')
    # 校验数据:使用ajax
    if pname == "":
        return jsonify({'error_message': '产品名称不能为空'})
    if not reference_price.isdigit():
        if reference_price.count('.') != 1:
            return jsonify({'error_message': '参考价格需为小数'})
        left = reference_price.split('.')[0]
        right = reference_price.split('.')[1]
        if not (left.isdigit() and right.isdigit() and len(right) <= 2):
            return jsonify({'error_message': '参考价格需为小数'})
    if not maxlim.isdigit():
        return jsonify({'error_message': '数量上限需为整数'})
    if not minlim.isdigit():
        return jsonify({'error_message': '数量下限需为整数'})
    maxlim = int(maxlim)
    minlim = int(minlim)
    if maxlim < minlim:
        return jsonify({'error_message': '数量上限需大于下限'})

    # 新增product
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='admin', password='admin', charset='utf8',
                           db='warehouse')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "insert into product(pname, specification, reference_price, maxlim, minlim) values(%s,%s,%s,%s,%s)"
    cursor.execute(sql, [pname, specification, reference_price, maxlim, minlim])
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/edit/product')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/backup')
def backup():
    # 检查是否登录
    if 'name' not in session:
        flash("请先登录！", category="error")
        return redirect('/login')
    # 备份文件存储路径
    BACKUP_DIR = "D:/PyCharm/ProductWarehouse/backups"
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    # 获取当前时间，用于生成唯一的备份文件名
    backup_filename = f"warehouse_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    backup_filepath = BACKUP_DIR + '/' + backup_filename

    # 使用 mysqldump 命令生成备份文件
    dump_command = [
        'mysqldump',
        '-h', '127.0.0.1',
        '-P', '3306',
        '-u', 'superadmin',
        f'--password=superadmin',  # 密码直接拼接
        'warehouse'
    ]
    print(dump_command)

    # 执行 mysqldump 命令
    try:
        with open(backup_filepath, 'wb') as f:
            subprocess.run(dump_command, stdout=f, stderr=subprocess.PIPE, check=True)
        return jsonify({'status': 'success'})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'fail'})


if __name__ == '__main__':
    app.run()
