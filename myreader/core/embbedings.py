import os
import http.client
import json
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from myreader.config.config import Config
class Embbeding:
  def __init__(self, cache_file="defalt.json"):
    module_root = os.path.dirname(os.path.dirname(__file__))
    self.caches = module_root+'/caches/'+cache_file
    config = Config()
    self.auth = 'Bearer '+ config.openai_api_key


  def build(self, contents):
    pass

  def text2vec(self, content):
    vecs = self.texts2vecs(content, using_cache=False)
    if vecs is None:
      return None
    else:
      return vecs[0]['embedding']

  def texts2vecs(self, content, using_cache=True):
    if using_cache and os.path.isfile(self.caches):
      print('use cache')
      with open(self.caches, 'r') as file:
          content = file.read()
          jdata = json.loads(content)
          return jdata['data']
    else:
      print('Requesting openai embbeding api...')

    conn = http.client.HTTPSConnection("api.openai.com")
    payload = json.dumps({
      "input": content,
      "model": "text-embedding-ada-002"
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': self.auth
    }
    try:
      conn.request("POST", "/v1/embeddings", payload, headers)
      res = conn.getresponse()
      data = res.read()
      result = data.decode("utf-8")

      jdata = json.loads(result)

      d = jdata['data']
      
      if using_cache:
          with open(self.caches,'w') as f:
              f.write(result)
      return d

    except TimeoutError:
      print("connect to openai server time out, check your networks,and try again!")
      return None
    except KeyError:
      print("KeyError result:"+result)
      return None
