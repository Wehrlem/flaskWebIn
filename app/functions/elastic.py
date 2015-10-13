
from .. import es
#def performQuery(term, filterString, page,es,indexName):
def performQuery(term):
	#filters = parseFilters(filterString)
	result = es.search(index='know', body={"min_score": 0.7,
  "query": {
    "bool": {
      "should": [
        { "match": {
            "title":  {
              "query": term,
              "boost": 1
        }}},
        { "match": {
            "text":  {
              "query": term,
              "boost": 3
        }}}
      ]
    }
  }
})
	#term = term.encode('utf-8')
	#query = getBasicQuery(filters, term, page)
	return result


def parseFilters(filters):
	filterDict = {}
	for f in filters.split(','):
		if f and len(f.split('-')) == 2:
			typ = f.split('-')[0].encode('utf-8')
			val = f.split('-')[1].encode('utf-8')
			filterDict[typ] = val

	return filterDict


#Those queries implement the filters as AND filter and the query as query_string_query
def getBasicQuery(filters, term, page):
	query = None

	if not page:
		page = 0
	start = int(page) * 12

	mustClauses = []
	for k,v in filters.iteritems():
		clause = {"term" : { k : v }}
        	mustClauses.append(clause)
	filterClauses = {"and" : mustClauses }

	aggregations = {}
	for el in aggregationFields:
		aggregations[el] = {"terms" : {"field" : el }}


	if term and filters:
		query = {
			"query": {
		         	"filtered": {
			 	      "filter": filterClauses,
			 	      "query": { "query_string" : { "query" : term } }
				   }
		   		},
		   	"size": 12,
		   	"from": start,
		   	"aggs" : aggregations
		}

	elif term:
		query = {
			"query": {
				"query_string" : { "query" : term }
			},
		   	"size": 12,
		   	"from": start,
		   	"aggs" : aggregations
		}


	return query