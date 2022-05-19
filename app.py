from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return '<Message %r>' % self.id


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message_content = request.form['content']
        new_message = Message(content=message_content)

        try:
            db.session.add(new_message)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue posting your message"
    else:
        messages = Message.query.order_by(Message.date_created).all()
        return render_template("index.html", messages=messages)


if __name__ == "__main__":
    app.run(debug=True)
