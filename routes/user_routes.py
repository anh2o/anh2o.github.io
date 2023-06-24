from fastapi import APIRouter
from models.user_model import User
from schemas.user_schema import users_serializer
from bson import ObjectId
from config.db import collection

user = APIRouter()

@user.post("/")
async def create_user(user: User):
    _id = collection.insert_one(dict(user))
    user = users_serializer(collection.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": user}

@user.get("/")
async def find_all_users():
    users = users_serializer(collection.find())
    return {"status": "Ok","data": users}
            
@user.get("/{id}")
async def get_one_user(id: str):
   user = users_serializer(collection.find({"tgid": str(id)}))
   return {"status": "Ok","data": user}

@user.put("/{id}")
async def update_user(id: str, user: User):
    collection.find_one_and_update(
        {
          "tgid": id
        }, 
        {
         "$set": dict(user)
        })
    user = users_serializer(collection.find({"tgid": id}))
    return {"status": "Ok","data": user}

@user.delete("/{id}")
async def delete_user(id: str):
   collection.find_one_and_delete({"tgid": id})
   users = users_serializer(collection.find())
   return {"status": "Ok","data": []} 

async def create_user_page(user:User):
    with open(f'{user.tgid}.html','w+') as f:
        f.write("""
                <!DOCTYPE html>
<html>
<head>
  <style>
    .error {
        color: red;
    }
  </style>
  <script type="text/javascript" src="https://cdn.jsdelivr.net/npm//vega@5"></script>
  <script type="text/javascript" src="https://cdn.jsdelivr.net/npm//vega-lite@4.8.1"></script>
  <script type="text/javascript" src="https://cdn.jsdelivr.net/npm//vega-embed@6"></script>
</head>
<body>
  <div id="vis"></div>
  <script>
    (function(vegaEmbed) {
      var spec = {"config": {"view": {"continuousWidth": 400, "continuousHeight": 300}}, "data": {"url": "https://cdn.jsdelivr.net/npm/vega-datasets@v1.29.0/data/cars.json"}, "mark": "point", "encoding": {"color": {"type": "nominal", "field": "Origin"}, "x": {"type": "quantitative", "field": "Horsepower"}, "y": {"type": "quantitative", "field": "Miles_per_Gallon"}}, "$schema": "https://vega.github.io/schema/vega-lite/v4.8.1.json"};
      var embedOpt = {"actions": false, "mode": "vega-lite"};
function showError(el, error){
          el.innerHTML = ('<div class="error" style="color:red;">'
                          + '<p>JavaScript Error: ' + error.message + '</p>'
                          + "<p>This usually means there's a typo in your chart specification. "
                          + "See the javascript console for the full traceback.</p>"
                          + '</div>');
          throw error;
      }
      const el = document.getElementById('vis');
      vegaEmbed("#vis", spec, embedOpt)
        .catch(error => showError(el, error));
    })(vegaEmbed);
</script>
</body>
</html>
                """)