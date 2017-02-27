# imports
from peewee import *
from flask import Flask, render_template, \
    request, redirect, url_for
from connectdatabase import ConnectDatabase
from models import UserStoryManager

app = Flask(__name__)


def init_db():
    ConnectDatabase.db.connect()
    ConnectDatabase.db.create_tables([UserStoryManager], safe=True)


@app.route("/story", methods=['GET'])
def show_adding_page():
    new_story = UserStoryManager(story_title="",
                                 user_story="",
                                 acceptance_criteria="",
                                 business_value=100,
                                 estimation=0.5, status="New")

    add = "add"
    return render_template('form.html', add=add, story=new_story)


@app.route("/story", methods=['POST'])
def save_adding_page():
    new_story = UserStoryManager.create(story_title=request.form['story_title'],
                                        user_story=request.form['user_story'],
                                        acceptance_criteria=request.form['acceptance_criteria'],
                                        business_value=request.form['business_value'],
                                        estimation=request.form['estimation'], status=request.form['status'])

    new_story.save()
    return redirect(url_for('list_page'))


@app.route('/story/<int:story_id>', methods=['GET'])
def show_editor_page(story_id):
    story = UserStoryManager.select().where(UserStoryManager.id == story_id).get()
    return render_template("form.html", story=story)


@app.route('/story/<int:story_id>', methods=['POST'])
def save_editor_page(story_id):
    modify = UserStoryManager.update(story_title=request.form['story_title'],
                                     user_story=request.form['user_story'],
                                     acceptance_criteria=request.form['acceptance_criteria'],
                                     business_value=request.form['business_value'],
                                     estimation=request.form['estimation'],
                                     status=request.form['status']) \
        .where(UserStoryManager.id == story_id)
    modify.execute()
    return redirect(url_for('list_page'))


@app.route("/", methods=['GET', 'POST'])
@app.route("/list", methods=['GET', 'POST'])
def list_page():
    user_stories = UserStoryManager.select().order_by(UserStoryManager.id.asc())
    return render_template("list.html", user_stories=user_stories)


@app.route("/delete/<int:story_id>")
def delete(story_id):
    story = UserStoryManager.select().where(UserStoryManager.id == story_id).get()
    UserStoryManager.delete_instance(story)
    return redirect("list")


def main():
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()
