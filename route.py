from flask import Flask, render_template,request
from flask_bootstrap import Bootstrap
import sqlite3

app = Flask(__name__)

Bootstrap(app)

conn = sqlite3.connect("mycontact.db")
cur = conn.cursor()

cur.execute("select count(*) from sqlite_master where type='table' and name='contact'")
count_table = cur.fetchone()[0]
print(count_table)
if count_table == 1:
    print("Table Already Exists")
else:
    conn.execute("CREATE TABLE contact (cont_name TEXT,phone TEXT, email TEXT)")
    print("Contact Created")
conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deleteInput')
def delete_input():
    return render_template('delete_input.html')

@app.route('/deleteContact', methods=['POST'])
def delete_contact():
    cont_name = request.form.get('name')
    try:
        with sqlite3.connect('mycontact.db') as conn:
            my_query = "DELETE FROM contact WHERE name='" + cont_name + "';"
            conn.execute(my_query)
            conn.commit()
            msg = "Total Rows Deleted are: " + str(conn.total_changes)
    except:
        conn.rollback()
        msg = "Sorry..Could not Delete Any Records"
    finally:
        conn.close()
    return render_template('success.html', msg=msg)




@app.route('/updateInput')
def update_input():
    return render_template('update_input.html')

@app.route('/updateContact',methods=['POST'])
def update_contact():
    cont_name = request.form.get('cont_name')
    phone = request.form.get('phone')
    email = request.form.get('email')

    try:
        with sqlite3.connect('mycollege.db') as conn:
            my_query = "update contact set phone='" + phone + "' where name='" + cont_name + "';"
            conn.execute(my_query)
            conn.commit()
            msg = "Total Rows Affected are: " + str(conn.total_changes)
    except:
        conn.rollback()
        msg = 'Could not Update Record'
    finally:
        conn.close()
    return render_template('search.html',msg=msg)

@app.route('/addContact')
def add_contact():
    return render_template('add_contact.html')

@app.route('/saveContact', methods=['GET','POST'])
def save_contact():
    msg = ''
    if request.method == 'POST':
        try:
            cont_name = request.form.get('cont_name')
            phone = request.form.get('phone')
            email = request.form.get('email')

            with sqlite3.connect('mycontact.db') as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO contact (cont_name, phone, email) values (?,?,?)", (cont_name, phone, email))
                conn.commit()
                msg = "Data Inserted Successfully"
        except:
            conn.rollback()
            msg = "Could Not Insert Data"
        finally:
            conn.close()
    return render_template('search.html', msg=msg)

@app.route('/listContact')
def list_contact():
    conn = sqlite3.connect('mycontact.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute('select * from contact')
    rows = cur.fetchall()

    return render_template('view.html',rows=rows)


if __name__ == '__main__':
    app.run(debug=True)