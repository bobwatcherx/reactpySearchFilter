from reactpy import html, component, use_state, use_effect
from reactpy.backend.fastapi import configure
from fastapi import FastAPI
import requests

app = FastAPI()

@component
def myapp():
    yousearch, set_yousearch = use_state("")
    allpost, set_allpost = use_state([])

    def getapi():
        response = requests.get("https://jsonplaceholder.typicode.com/posts")
        if response.status_code == 200:
            data = response.json()
            set_allpost(data)
        else:
            print("API request failed")

    use_effect(getapi, [])

    def youfinddata(event):
        search_value = event['target']['value']
        set_yousearch(search_value)
        if search_value:
            filtered_data = [post for post in allpost if search_value.lower() in post['title'].lower()]
            set_allpost(filtered_data)
        else:
            getapi()

    return html.div(
        html.input({
            "type": "text",
            "placeholder": "search You data Here",
            "onChange": youfinddata
        }),
        html.ul(
            [html.li(f"{post['id']} - {post['title']}") for post in allpost]
        )
    )

configure(app, myapp)
