from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_mail import Mail, Message


app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'csi_fb'

##################################################################
############### Confedential_API-KEYS ############################
##################################################################
app.config['MAIL_SERVER']='live.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'api'
app.config['MAIL_PASSWORD'] = '4a5022039c7a482fe960fa665862af19'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
##################################################################
############### Confedential_API-KEYS ############################
##################################################################


mysql = MySQL(app)
mail = Mail(app)


@app.route('/', methods=['POST', 'GET'])
def feedback_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO feedback (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
        mysql.connection.commit()
        cur.close()

        msg = Message('New Feedback Submission', sender='CSI@kousicreddy.eu.org', recipients=['kousicreddy39@gmail.com'])
        msg.body = f'Name: {name}\nEmail: {email}\nMessage: {message}'
        mail.send(msg)

        flash('Feedback submitted successfully!', 'success')
    return render_template('feedback_form.html')


@app.route('/feedbacks')
def view_feedbacks():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM feedback")
    feedbacks = cur.fetchall()
    cur.close()
    # app.logger.info(feedbacks)
    
    return render_template('feedbacks.html', feedbacks=feedbacks)
    



@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO feedback (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
        mysql.connection.commit()
        cur.close()

        msg = Message('New Feedback Submission', sender='CSI@kousicreddy.eu.org', recipients=['kousicreddy39@gmail.com'])
        msg.body = f'Name: {name}\nEmail: {email}\nMessage: {message}'
        mail.send(msg)

        flash('Feedback submitted successfully!', 'success')
        
        return redirect(url_for('feedback_form'))

if __name__ == '__main__':
    app.secret_key = 'your_secret_key'
    app.run(debug=True)
