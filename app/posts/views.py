
from flask import render_template,flash
from . import posts
from flask.ext.paginate import Pagination
from flask import request
from ..models import Experts,Posts
from .. import cache
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
        return render_template('posts.html',list=list)

    else:
        count = cache.get('postcount')
        #list = cache.get('posts'+str(page))
        if count is None:
            count = Post.get_count()
            count = count[0].count
            cache.set('postcount', count, timeout=300)
        list = Post.get_paged(page)
        #if list is None:
        #
        #    cache.set('posts'+str(page),set(list),timeout=300)
        pagination = Pagination(page=page, total=count, search=search, record_name='experts', per_page=10)

        return render_template('posts.html',list=list, pagination=pagination)

@posts.route('/post/<postid>')
def get_post(postid):
    post = Post.get_post_id(postid)
    answers = None
    if Post.check_if_question(postid):
        answers= Post.get_answer_by_id(postid)

    return render_template('post.html', post=post[0],answers=answers)