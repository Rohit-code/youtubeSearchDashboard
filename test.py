from elasticsearch import Elasticsearch
##setup connection
es=Elasticsearch([{"host":"localhost","port":9200,"scheme":"https"}],http_auth=('elastic', 'Mt-i5zkzBtcy*RXEYmtJ'))
#es = Elasticsearch()
#cloud_id = "6862346324714aa2a72edba4f4ddbc3b:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDdhYzY1M2Q1NzExNTQ0NzI5ZDRiNWM1ZDUzYWYzYmQ5JDYyZjM5NjgzNDA2ODQyZDhhZWQwNTkwY2VmM2NjYThk"

print(es.ping())
##create index
#es.indices.create(index="tutorial2-16_10_2021")
##dis`play all indices
