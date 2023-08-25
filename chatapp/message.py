from flask import Flask,Blueprint,request,redirect,url_for,render_template,jsonify
from .models import User,ChatMessage
from . import db 

message = Blueprint('message', __name__)


@message.route('/chat_with_user/<name>', methods=['GET', 'POST'])
def chat_with_user(name):
    user = User.query.filter_by(name=name).first()

    if request.method == 'POST':
        content = request.form['content']

        if user:
            message = ChatMessage(content=content, user=user)
            db.session.add(message)
            db.session.commit()
            return redirect(url_for('auth.chat_with_user', name=name))

    messages = ChatMessage.query.filter_by(user=user).order_by(ChatMessage.timestamp).all()
    return render_template('chat_with_user.html', user=user, messages=messages)

@message.route('/get_messages/<name>', methods=['GET'])
def get_messages(name):
    try:
        user = User.query.filter_by(name=name).first()

        if user:
            messages = user.messages
            message_list = [{
                "sender": message.sender.name,
                "content": message.content,
                "timestamp": message.timestamp
            } for message in messages]
            return jsonify(messages=message_list)
        else:
            return jsonify(messages=[]), 404  # Return a 404 status if user not found
    except Exception as e:
        return jsonify(error=str(e)), 500  # Return a 500 status if an error occurs

