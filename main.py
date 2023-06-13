from reactpy import component,html,use_state,use_effect
from reactpy.backend.fastapi import configure
from fastapi import FastAPI
import requests
app = FastAPI()


@component
def YouSearch():
    yousearch,set_yousearch = use_state("")
    allpost,set_allpost = use_state([])
    # NOW I WILL GET REST API FROM JSONPLACEHOLDER
    def getApi():
        response = requests.get("https://jsonplaceholder.typicode.com/posts")
        if response.status_code == 200:
            data = response.json()
            set_allpost(data)
        else:
            print("YOU CANOT GET API")

    use_effect(getApi,[])


    def youfindata(event):
        # AND I WILL SEARCH FILTER HERE
        search_value = event['target']['value']
        set_yousearch(search_value)
        # NOW IF YOU TYPE IN TEXT BOX 
        # AND SEARCH FILTER 
        if search_value:
            youfilter = [post for post in allpost if search_value.lower() in post['title'].lower()]
            set_allpost(youfilter)
        else:
            # IF YOU REMOVE YOU INPUT THEN PUSH ALL DATA AGAIN
            getApi()  


    return html.div(
        html.h1("Search input"),
        # NOW CREATE INPUT
        html.input({
            "type":"text",
            "placeholder":"YOU Search HERE",
            "onChange":youfindata

            }),
        # AND I WILL FOR LOOP DATA allpost HERE
        html.ul(
            [html.li(
                f"{i['id']} {i['title']}"
                ) for i in allpost]
            )


        )

configure(app,YouSearch)
