from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
import bleach
from flask import current_app, request, url_for
from flask.ext.login import UserMixin, AnonymousUserMixin
from app.exceptions import ValidationError
import random

from . import client
import nltk
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')

from nltk.stem.porter import *
class Granules():

    def get_paged(self,page):
        with client.connection():
            return client.query("SELECT * FROM concept ORDER BY Level ASC SKIP {0} LIMIT {1}".format((page-1)*20,20))
    def get_count(self):
        with client.connection():
            return client.query("SELECT count(*) from concept")
    def get_granules_by_name(self,username):
        with client.connection():
            return client.query("SELECT * FROM concept WHERE name ='{0}' ".format(username))
    def get_granules_by_search(self,get_granules_by_search):
        with client.connection():
            return client.query("SELECT FROM concept WHERE name like '%{0}%' ".format(get_granules_by_search))

class Experts():
    def get_experts(self):
        with client.connection():
            return client.query("SELECT * FROM Expert")

    def create_expert_init(self):
        with client.connection():
          client.command("DELETE VERTEX Expert")
          client.command('create property Expert.name string')
          client.command('create property Expert.LastAccessDate date')
          client.command('create property Expert.CommentCount integer')
          client.command('create property Expert.WebsiteUrl string')
          client.command('create property Expert.Reputation integer')
          client.command('create property Expert.Location string')
          client.command('create property Expert.Age integer')
          client.command('create property Expert.Views integer')
          client.command('create property Expert.CreationDate date')
          client.command('create property Expert.DownVotes integer')
          client.command('create property Expert.UpVotes integer')
    def get_expert_by_owner(self,PostId):
        with client.connection():
            return client.query("SELECT name from Expert WHERE ID={0}".format(PostId))
    def get_paged(self,page):
        with client.connection():
            return client.query("SELECT * FROM Expert SKIP {0} LIMIT {1}".format((page-1)*20,20))
    def get_count(self):
        with client.connection():
            return client.query("SELECT count(*) from Expert")
    def get_expert_by_name(self,username):
        with client.connection():
            return client.query("SELECT * FROM Expert WHERE name ='{0}' ".format(username))

    def update_expert_by_property(self,username,label,value):
        with client.connection():
            return client.command("UPDATE Expert SET {0} ='{1}' WHERE name='{2}'".format(label,value,username))

    def get_expert_by_search(self,get_expert_by_search):
        with client.connection():
            return client.query("SELECT FROM Expert WHERE name like '%{0}%' ".format(get_expert_by_search))

class Posts():
    #def __init__(self):

    def create_posts_init(self):
      client.command('create property Content.Title string')
      client.command('create property Content.Body string')
      client.command('create property Content.LastActivityDate date')
      client.command('create property Content.ViewCount integer')
      client.command('create property Content.AnswerCount integer')
      client.command('create property Content.FavoriteCount integer')
      client.command('create property Content.AcceptedAnswerId integer')
      client.command('create property Content.Tags string')
      client.command('create property Content.CommentCount integer')
      client.command('create property Content.PostTypeId string')
      client.command('create property Content.CommentCount integer')
      client.command('create property Content.Score integer')
      client.command('create property Content.ParentId integer')
      client.command('create property Content.OwnerUserId integer')
      client.command('create property Content.CreationDate date')
      client.command('create property Content.PostId integer')

    def get_paged(self,page):
        with client.connection():
            return client.query("SELECT * FROM Content WHERE Body <> '' ORDER BY postId SKIP {0} LIMIT {1}".format((page-1)*10,10))

    def get_count(self):
        with client.connection():
            return client.query("SELECT count(*) from Content")

    def get_post_id(self,postid):
        with client.connection():
            return client.query("SELECT * FROM Content WHERE PostId ='{0}' ".format(postid))

    def get_post_by_search(self,get_post_by_search):
        with client.connection():
            return client.query("SELECT FROM Content WHERE name like '%{0}%' ".format(get_post_by_search))

    def check_if_question(self,id):
        with client.connection():
            result = client.query("SELECT PostType FROM Content WHERE PostId ='{0}' ".format(id))
            if result[0] =='Question':
                return True
            return result[0]



    def get_answer_by_id(self,id):
        with client.connection():
            return client.query('SELECT EXPAND( BOTH( "parents" ) ) FROM Content WHERE PostId = {0} ORDER BY Score DESC '.format(id))

class KCFS:
    def get_related_question(self,query):
        with client.connection():
            word = tokenizer.tokenize(query)
            word = nltk.pos_tag(word)
            stemmer = PorterStemmer()
            stem = ['"%'+stemmer.stem(w[0])+'%"' for w in word if w[1].startswith('N')]
            #create query
            #added = ['Title:'+ st+'*' for st in word]
            full = ' and Title Like'.join(stem)
            return client.query('select * from Content where Title Like {0} AND PostType = "Question" ORDER By Score Limit 5'.format(full))
            #return client.query('select * from Content where [Title] LUCENE "({0})" AND PostType = "Question" ORDER By Score Limit 5'.format(full))

    def get_key_of_question(self,query):
        word = tokenizer.tokenize(query)
        word = nltk.pos_tag(word)
        # or w[1].startswith('W')
        return ', '.join([w[0] for w in word if w[1].startswith('N')])
    def get_key_of_question_next(self,query):
        word = tokenizer.tokenize(query)
        word = nltk.pos_tag(word)
        # or w[1].startswith('W')
        return [w[0] for w in word if w[1].startswith('N')]
    def get_answer_by_id(self,id):
        with client.connection():
            return client.query('SELECT EXPAND( BOTH( "parents" ) ) FROM Content WHERE PostId = {0} ORDER BY Score DESC LIMIT 1'.format(id))
    def return_expert_by_concept(self, concept):
        with client.connection():
            return client.query("SELECT * FROM Expert SKIP {0} LIMIT {1}".format(random.randint(0,6000),10))

