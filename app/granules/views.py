
from flask import render_template
from . import granules
from flask.ext.paginate import Pagination
from flask import request
from ..models import Granules
import random
from collections import OrderedDict
import hashlib

Granules =Granules()

@granules.route('/granules')
def get_granules():
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
        list = Granules.get_granules_by_search(search_parameter)
        return render_template('granules.html',list=list)

    else:

        list = Granules.get_paged(page)
        count = Granules.get_count()

        for i,k in enumerate(list):
            try:
                grans =[]
                list[i].count = random.randint(100,500)
                #for i in range (1,random.randint(2,4)):
                grans.append('G'+str(random.randint(1,22)))
                list[i].gran = 'G'+str(random.randint(1,22))
            except IndexError:
                continue
        pagination = Pagination(page=page, total=count[0].count, search=search, record_name='granules', per_page=20)
        return render_template('granules.html',list=list, pagination=pagination)



@granules.route('/granules/<name>')
def granule(name):
    granule = Granules.get_granules_by_name(name)
    gravatar_url= ''
    return render_template('granule.html', user=granule[0],grav = gravatar_url)