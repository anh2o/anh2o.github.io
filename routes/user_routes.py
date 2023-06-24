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
                <html>
     <head>
     <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />       
     <title>Test Dash</title>
     </head>
     <body>

     <div id="container" style="width:500px;height:500px;"></div>

     <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
     <script>window.jQuery || document.write('<script src="js/jquery-1.8.3.min.js"><\/script>')</script>
     <script src="http://code.highcharts.com/highcharts.js"></script>
     <script src="http://code.highcharts.com/highcharts-more.js"></script>
     <script src="http://code.highcharts.com/modules/exporting.js"></script>

     <script>
     //My highchart script

     $(function () {
        var chart;
        $(document).ready(function() {
            // $.getJSON("data.php", function(json) {

                chart = new Highcharts.Chart({
                    chart: {
                        renderTo: 'container',
                        type: 'line',
                        marginRight: 130,
                        marginBottom: 25
                    },
                    title: {
                        text: 'Disease',
                        x: -20 //center
                    },
                    subtitle: {
                        text: '',
                        x: -20
                    },
                    xAxis: {
                        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    },
                    yAxis: {
                        title: {
                            text: 'Patient Count'
                        },
                        plotLines: [{
                            value: 0,
                            width: 1,
                            color: '#808080'
                        }]
                    },
                    tooltip: {
                        formatter: function() {
                                return '<b>'+ this.series.name +'</b><br/>'+
                                this.x +': '+ this.y;
                        }
                    },
                    legend: {
                        layout: 'vertical',
                        align: 'right',
                        verticalAlign: 'top',
                        x: -10,
                        y: 100,
                        borderWidth: 0
                    },
                    series: [{
                        name: 'Jane',
                        data: [1, 0, 4]
                    }, {
                        name: 'John',
                        data: [5, 7, 3]
                    }]
                });
        //  });

        });

     });

     </script>
 </body>
                """)