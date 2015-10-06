
from flask import render_template
from . import posts
from .. import client,db_name
from flask.ext.paginate import Pagination
from flask import request
from ..models import Experts,Posts
Post = Posts()
Expert =Experts()
import hashlib

@posts.route('/posts')
def get_posts():
    search = False
    q = request.args.get('q')
    if q:
        search = True
        search_parameter = request.args.get('q', 1)
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1
    if(search):
        list = Post.get_paged(search_parameter)
        for i,k in enumerate(list):
            name = Expert.get_expert_by_owner(k.PostId)
            list[i].short = ' '.join(k.Body.split()[:5])
            try:
                list[i].name = name[0].name
            except IndexError:
                continue
        return render_template('posts.html',list=list)

    else:
        list = Post.get_paged(page)
        count = Post.get_count()

        for i,k in enumerate(list):
            name = Expert.get_expert_by_owner(k.PostId)
            list[i].short = ' '.join(k.Body.split()[:5])
            try:
                list[i].name = name[0].name
            except IndexError:
                continue
        pagination = Pagination(page=page, total=count[0].count, search=search, record_name='experts', per_page=10)

        return render_template('posts.html',list=list, pagination=pagination)

@posts.route('/post/<postid>')
def get_post(postid):
    post = Post.get_post_id(postid)
    answers = None
    if Post.check_if_question(postid):
        answers= Post.get_answer_by_id(postid)

    return render_template('post.html', post=post[0],answers=answers)