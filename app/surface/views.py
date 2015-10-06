from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from . import surface
from ..models import KCFS
import random
from .. import client,db_name,db_type
KCFS = KCFS()
import  numpy as np, numpy.random
from collections import OrderedDict
@surface.route('/', methods=['GET', 'POST'])
def index():
    q = request.args.get('q')
    e = request.args.get('e')
    d = request.args.get('d')
    if d:
        search_parameter = request.args.get('q', 1)
        ds = request.args.get('d', 1)
        si = float(ds)/10
        result =[]
        keywords = KCFS.get_key_of_question_next(search_parameter)
        for k,i in enumerate(keywords):
            result.append([])
            for i in range(0,10,2):
                val =  round(random.uniform(0, 1-si), 2)
                result[k].append(round(si+val,2))
                result[k].append(round(si-val,2))


        return render_template('needdetail.html',list= result,keywords=keywords)
    elif e:
        search_parameter = request.args.get('q', 1)
        keywords = KCFS.get_key_of_question(search_parameter)
        experts = KCFS.return_expert_by_concept('lala')


        rands=[]
        for i in range(0,10):
            rands.append(round(random.uniform(5, 8), 1))
        sor = sorted(rands,reverse=True)
        for i,k in enumerate(experts):
            try:
                experts[i].score = sor[i]
            except IndexError:
                continue
        return render_template('need.html',search_parameter = search_parameter,list= experts,keywords=keywords)
    elif q:
        search_parameter = request.args.get('q', 1)
        result =KCFS.get_related_question(search_parameter)
        keywords = KCFS.get_key_of_question(search_parameter)
        for i,k in enumerate(result):
            result[i].short = ' '.join(k.Title.split())
            answer = KCFS.get_answer_by_id(k.PostId)
            if answer:
                if (len(answer[0].Body.split())>19):
                    result[i].answer = ' '.join(answer[0].Body.split()[:20])
                else:
                    result[i].answer = ' '.join(answer[0].Body.split())
            else:
                result[i].answer =''
        return render_template('result.html',search_parameter = search_parameter,list= result,keywords=keywords)

    else:
        return render_template('index.html')


