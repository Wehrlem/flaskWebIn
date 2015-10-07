# coding=utf-8
import re

import os
from pyorient import orient
from pymongo import MongoClient
from dateutil import parser
import re
from nltk import FreqDist
import nltk
import operator


from sklearn.feature_extraction.text import TfidfVectorizer


def cleanhtml(raw_html):

  cleanr =re.compile('<.*?>')

  cleantext = re.sub(cleanr,'', raw_html)

  return cleantext
# Each of our data files which will be used as collection names also.
files = [ "Badges", "Comments", "Posts", "Users", "Votes","Tags" ]
db_name = 'history'

connection = MongoClient()
client = orient.OrientDB("localhost", 2424)
client.db_open( db_name, "root", "don1664" )



# Name our database, can change this for Server Fault/etc..
db = connection['history_stack']

#for file in files:
def create_posts(db):
  db = getattr(db, "Posts")
  #client.command("CREATE CLASS Content extends V")
  #client.command("CREATE CLASS similar extends V")

  data =  db.find()
  for d in data:
    if '_id' in d:

      if not 'Body' in d:
        display= ''
      else:
        display= cleanhtml(d['Body'].encode('utf-8').replace('\n', ' ').replace('\r', '').replace('\\', ''))

      if not 'LastActivityDate' in d:
        Down= '1999-05-12'
      else:
        Down= d['LastActivityDate'].encode('utf-8')[:10]

      if not 'PostTypeId' in d:
        vie= 'None'
      elif d['PostTypeId'].encode('utf-8') =='1':
        vie= 'Question'
      elif d['PostTypeId'].encode('utf-8') =='2':
        vie= 'Answer'
      elif d['PostTypeId'].encode('utf-8') =='3':
        vie= 'Tag Wiki'


      if not 'CommentCount' in d:
        About= 0
      else:
        About= d['CommentCount'].encode('utf-8')

      if not 'Title' in d:
        Title= ''
      else:
        Title= d['Title'].encode('utf-8')

      if not 'Score' in d:
        LastA= 0
      else:
        LastA= d['Score'].encode('utf-8')

      if not 'ParentId' in d:
        Website= 0
      else:
        Website= d['ParentId'].encode('utf-8')

      if not 'OwnerUserId' in d:
        Rep= 0
      else:
        Rep= d['OwnerUserId'].encode('utf-8')

      if not 'CreationDate' in d:
        Loc= '1999-05-12'
      else:
        Loc= d['CreationDate'].encode('utf-8')[:10]
      if not '_id' in d:
        Ag= ''
      else:
        Ag= d['_id']

      if not 'ViewCount' in d:
        ViewCount= 0
      else:
        ViewCount= d['ViewCount']

      if not 'AnswerCount' in d:
        AnswerCount= 0
      else:
        AnswerCount= d['AnswerCount']

      if not 'FavoriteCount' in d:
        FavoriteCount= 0
      else:
        FavoriteCount= d['FavoriteCount']

      if not 'AcceptedAnswerId' in d:
        AcceptedAnswerId= 0
      else:
        AcceptedAnswerId= d['AcceptedAnswerId']

    client.command("INSERT INTO Content (body,LastActivityDate,PostType,CommentCount,Score,ParentId,OwnerUserId,CreationDate,PostId,Title,ViewCount,AnswerCount,FavoriteCount,AcceptedAnswerId) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}')".format(display.replace("'",""),Down,vie,About,LastA,Website,Rep,Loc,Ag,Title.replace("'",""),ViewCount,AnswerCount,FavoriteCount,AcceptedAnswerId))



def create_expert(db):
  db = getattr(db, "Users")
  data =  db.find()
  client.command("CREATE CLASS Expert extends V")
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

  for d in data:
    if 'DisplayName' in d:

      if not 'DisplayName' in d:
        display= ''
      else:
        display= d['DisplayName'].encode('utf-8')
      if not 'DownVotes' in d:
        Down= 0
      else:
        Down= d['DownVotes'].encode('utf-8')

      if not 'Views' in d:
        vie= 0
      else:
        vie= d['Views'].encode('utf-8')


      if not 'LastAccessDate' in d:
        LastA= '1999-09-12'
      else:
        LastA= d['LastAccessDate'].encode('utf-8')[:10]

      if not 'WebsiteUrl' in d:
        Website= ''
      else:
        Website= d['WebsiteUrl'].encode('utf-8')

      if not 'Reputation' in d:
        Rep= 0
      else:
        Rep= d['Reputation'].encode('utf-8')

      if not 'Location' in d:
        Loc= ''
      else:
        Loc= d['Location'].encode('utf-8')

      if not 'Age' in d:
        Ag= 0
      else:
        Ag= d['Age'].encode('utf-8')

      if not 'UpVotes' in d:
        Up= 0
      else:
        Up= d['UpVotes'].encode('utf-8')

      if not 'CreationDate' in d:
        Creation= '1999-09-12'
      else:
        Creation= d['CreationDate'].encode('utf-8')[:10]

      try:
        client.command("INSERT INTO Expert (name,DownVotes,Views,LastAccessDate,WebsiteUrl,Reputation,Location,Age,UpVotes,CreationDate,ID) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')".format(display.replace("'",""),Down,vie,LastA,Website,Rep,Loc,Ag,Up,Creation,d['_id']))
      except:
        continue

def create_edge_post_user():
    client.command("CREATE CLASS created EXTENDS E")
    client.command("DELETE EDGE created")
    list = client.query("SELECT distinct(OwnerUserId) FROM Content",-1)
    for k in list:
      try:
        client.command("CREATE EDGE created FROM (SELECT FROM Expert WHERE ID = {0}) TO (SELECT FROM Content WHERE OwnerUserId = {1})".format(k.distinct,k.distinct))
      except:
        continue

def create_edge_post_post():

  client.command("CREATE CLASS parents EXTENDS E")
  client.command("DELETE EDGE parents")
  list = client.query("SELECT distinct(ParentId) FROM Content",-1)
  print len(list)
  for k in list:
    print k.distinct
    if k.distinct != 0:
      try:
        client.command("CREATE EDGE parents FROM (SELECT FROM Content WHERE ParentId = {0}) TO (SELECT FROM Content WHERE PostId = {1})".format(k.distinct,k.distinct))
      except:
        continue
def extract_tags_make_concept(db):
  db = getattr(db, "Posts")
  data =  db.find()
  tags={}
  lev = {}
  tokens=[]
  tagsds = []
  #client.command("DELETE EDGE similar")
  #client.command("DELETE VERTEX concept")
  #client.command("CREATE CLASS similar extends E")

  for d in data:
    if 'Tags' in d:
      tag = d['Tags']
      tag = tag.split("><")
      tag=[t.replace('<','').replace('>','') for t in tag]
      tagss=[]

      for t in tag:
        if t not in tags:
          tags[t] = 1
        else:
          tags[t] += 1
        tagss.append(t)
      tagsds.append(tagss)

  for k,v in tags.items():
    if v > 80:
      Level = 1
    elif 10<v<80:
      Level=2
    else:
      Level=3
    lev[k] = Level
    client.command("INSERT INTO concept (name,Level) VALUES ('{0}',{1})".format(k,Level))
  trination={}
  for iss in tagsds:
    for e,i in enumerate(iss):
        k = e+1
        if e == len(iss)-1:
          k=0
        if iss[e]+'_'+iss[k] not in trination or iss[k]+'_'+iss[e] not in trination:
          trination[iss[e]+'_'+iss[k]] = 1
        else:
          trination[iss[e]+'_'+iss[k]] += 1

  for iss in tagsds:
    for e,i in enumerate(iss):
        k = e+1
        if e == len(iss)-1:
          k=0
        if [iss[e],iss[k]] not in tokens and [iss[k],iss[e]] not in tokens and iss[k] != iss[e] and abs(int(lev[iss[e]])-int(lev[iss[k]]))<2:
          number = trination[iss[e]+'_'+iss[k]]
          if number < 2:
              number= 'medium'
          elif 2 <= number <11:
              number= 'strong'
          else:
              number='very strong'
          client.command("CREATE EDGE similar FROM (SELECT FROM concept WHERE name = '{0}') TO (SELECT FROM concept WHERE name = '{1}') SET number='{2}'".format(iss[e],iss[k],number))
          tokens.append([iss[e],iss[k]])



def create_word_freq(db):
  db = getattr(db, "Posts")
  #client.command("CREATE CLASS concepted EXTENDS E")

  client.command("DELETE EDGE concepted")
  #client.command('create property frequency.freq string')

  #client.command("DELETE VERTEX frequency")
  data =  db.find().batch_size(50)
  concept = client.command("SELECT name FROM concept")
  c = [c.name for c in concept]
  for d in data:
    if not 'Body' in d:
        display= ''
    else:
        display= cleanhtml(d['Body'].replace('\n', ' ').replace('\r', '').replace('\\', ''))
        tokens = nltk.word_tokenize(display)
        fdist=FreqDist(tokens)
        i  = fdist.most_common()
        for k in i:
          if k[0].lower() in c:
            try:
                client.command("CREATE EDGE concepted FROM (SELECT FROM concept WHERE name = '{0}') TO (SELECT FROM Content WHERE PostId = {1}) SET strength = {2}".format(k[0].lower(),d['_id'],k[1]))
            except:
              continue

def create_links_from_3_4(db):
  db = getattr(db, "Posts")
  #client.command("CREATE CLASS concepted EXTENDS E")

  client.command("DELETE EDGE similar")
  #client.command('create property frequency.freq string')

  #client.command("DELETE VERTEX frequency")
  data =  db.find().batch_size(50)
  concept = client.command("SELECT name FROM concept WHERE Level = 4")
  casa = [c.name for c in concept]
  concepst = client.command("SELECT name FROM concept WHERE Level = 3")
  cs = [c.name for c in concepst]
  textils=[]
  trination={}
  for d in data:
    if 'Body' and 'Tags' in d:
        display= cleanhtml(d['Body'].replace('\n', ' ').replace('\r', '').replace('\\', ''))
        tokens = nltk.word_tokenize(display)
        tag = d['Tags']
        tag = tag.split("><")
        tag=[t.replace('<','').replace('>','') for t in tag]
        for word in casa:
          if word in tokens:
            for t in tag:
              if t in cs:
                if word+'_'+t not in trination or t +'_'+word not in trination:
                  trination[word+'_'+t] = 1
                else:
                  trination[word+'_'+t] += 1
        for word in casa:
          if word in tokens:
            for t in tag:
              if t in cs:
                if [t,word] not in textils or [word,t] not in textils:
                  number = trination[word+'_'+t]
                  if number < 2:
                    number= 'medium'
                  elif 2 <= number <11:
                    number= 'strong'
                  else:
                    number='very strong'
                  client.command("CREATE EDGE similar FROM (SELECT FROM concept WHERE name = '{0}') TO (SELECT FROM concept WHERE name = '{1}') SET number='{2}'".format(t,word,number))
                  textils.append([t,word])

def add_tags_to_post_step_1(db):
  db = getattr(db, "Posts")    #  client.command("CREATE EDGE knows FROM (SELECT FROM concept WHERE name = '{0}') TO (SELECT FROM Expert WHERE ID = '{1}') SET strength={2}".format(v,i.ID,trination[v]))

  data =  db.find().batch_size(50)
  for d in data:
    if 'Tags' in d:
      tag = d['Tags']
      tag = tag.split("><")
      tag=[t.replace('<','').replace('>','') for t in tag]

      client.command("UPDATE Content SET Tags ='{0}' WHERE PostId={1}".format(','.join(tag),d['_id']))


def add_tag_to_all():
  sets = client.query('SELECT PostId, ParentId FROM Content',-1)
  for i in sets:
    if i.ParentId !=0:
      subsets = client.query('SELECT Tags From Content WHERE PostId ={0}'.format(i.ParentId))
      client.command("UPDATE Content SET Tags ='{0}' WHERE PostId={1}".format(subsets[0].Tags,i.PostId))

def update_concept_count():
  client.command("DELETE EDGE knows")

  sets = client.query('SELECT ID FROM Expert',-1)
  trination={}
  for i in sets:
    subnation = client.query('SELECT Tags FROM Content WHERE OwnerUserId={0} and Tags <>""'.format(i.ID))
    trination={}
    for k in subnation:
      se = k.Tags.split(',')
      for j in se:
        if j not in trination:
          trination[j] = 1
        else:
          trination[j] += 1
    if trination:
      for v in trination:
         client.command("CREATE EDGE knows FROM (SELECT FROM concept WHERE name = '{0}') TO (SELECT FROM Expert WHERE ID = '{1}') SET strength={2}".format(v,i.ID,trination[v]))

def update_concept_count_2(db):
  db = getattr(db, "Posts")
  #client.command("CREATE CLASS concepted EXTENDS E")

  #client.command('create property frequency.freq string')

  #client.command("DELETE VERTEX frequency")
  data =  db.find().batch_size(50)
  concept = client.command("SELECT name FROM concept WHERE Level = 4",-1)
  casa = [c.name for c in concept]
  textils=[]
  trination={}
  for d in data:
    if 'Body' and 'OwnerUserId' in d:
        display= cleanhtml(d['Body'].replace('\n', ' ').replace('\r', '').replace('\\', ''))
        tokens = nltk.word_tokenize(display)
        for word in casa:
          if word in tokens:

            results = client.query("select name AS user_name, ID ,in(knows).name AS concepts , inE(knows).strength AS comment, inE(knows).@rid as edgeid from Expert WHERE ID ={0}".format(d['OwnerUserId']))

            if results:
              if word in results[0].concepts:

                index= results[0].concepts.index(word)
                strength= results[0].comment[index] +1
                client.command("UPDATE knows SET strength ={0} WHERE @rid={1}".format(strength, results[0].edgeid[index]))
              else:
                client.command("CREATE EDGE knows FROM (SELECT FROM concept WHERE name = '{0}') TO (SELECT FROM Expert WHERE ID = '{1}') SET strength={2}".format(word,results[0].ID,1))




update_concept_count_2(db)