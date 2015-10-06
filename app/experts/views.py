
from flask import render_template
from . import experts
from .. import client,db_name,db_type
from flask.ext.paginate import Pagination
from flask import request
from ..models import Experts
import hashlib
import json

Expert =Experts()

@experts.route('/experts')
def get_experts():
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
        list = Expert.get_expert_by_search(search_parameter)
        return render_template('expertList.html',list=list)

    else:
        list = Expert.get_paged(page)
        count = Expert.get_count()
        pagination = Pagination(page=page, total=count[0].count, search=search, record_name='experts', per_page=20)
        return render_template('expertList.html',list=list, pagination=pagination)



@experts.route('/experts/<username>')
def user(username):
    user = Expert.get_expert_by_name(username)
    gravatar= hashlib.md5("{0}@example.com".format(user[0].name)).hexdigest()
    gravatar_url= 'http://www.gravatar.com/avatar/'+gravatar+'?s=200'
    categories={'Contribution':['Semantic','Sentiment'],'Relationship':['Type','Strength'],'Metadata':['Structural-Depth','Structural-Coverage','Descriptive'],'Administrative':['Background','Reputation']}
    return render_template('experts.html', user=user[0],grav = gravatar_url,categories=categories)

@experts.route('/expertssave', methods=['POST'])

def save_proprieties():
    option =  request.form['selected']
    use = request.form['user'];
    feature = request.form['feature']
    Expert.update_expert_by_property(use.strip(),feature,option)
    return json.dumps({'status':'OK'});