import requests
BASE_URL = "https://jsonplaceholder.typicode.com/posts"

def get_filtered_posts():
    response = requests.get(BASE_URL)
    if response.ok:
        posts = response.json()
        filtered_posts = [
            post for post in posts
            if len(post['title'].split()) <= 6 and len(post['body'].split("\n")) <= 3
        ]
        print("Filtered GET Results:")
        for post in filtered_posts:
            print(post)
    else:
        print(f"GET Request Failed: {response.status_code}")


def create_post():
    new_post = {
        "title": "Simple Post",
        "body": "This is a test post.",
        "userId": 1
    }
    response = requests.post(BASE_URL, json=new_post)
    print("POST Response:", response.json() if response.ok else f"Failed: {response.status_code}")

def update_post(post_id):
    updated_post = {
        "title": "Updated Title",
        "body": "Updated body content.",
        "userId": 1
    }
    response = requests.put(f"{BASE_URL}/{post_id}", json=updated_post)
    print("PUT Response:", response.json() if response.ok else f"Failed: {response.status_code}")

def delete_post(post_id):
    response = requests.delete(f"{BASE_URL}/{post_id}")
    print("DELETE Response:", "Success" if response.ok else f"Failed: {response.status_code}")

get_filtered_posts()  
create_post()        
update_post(1)        
delete_post(1)       
