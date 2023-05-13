from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from views.post import create_post, get_all_posts, delete_post, update_post
from views.user import create_user, login_user, get_all_users, update_user, delete_user
from views.tag import create_tag, get_all_tags, delete_tag, update_tag
from views.posttag import create_posttag, get_all_posttags, delete_posttag, update_posttag
from views.comment import create_comment, get_all_comments, update_comment, delete_comment
from views.subscriptions import create_subscription,get_all_subscriptions,delete_subscription
from views.postreactions import create_postreaction,get_all_postreactions,delete_postreactions

class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self):
        """Parse the url into the resource and id"""
        path_params = self.path.split('/')
        resource = path_params[1]
        if '?' in resource:
            param = resource.split('?')[1]
            resource = resource.split('?')[0]
            pair = param.split('=')
            key = pair[0]
            value = pair[1]
            return (resource, key, value)
        else:
            id = None
            try:
                id = int(path_params[2])
            except (IndexError, ValueError):
                pass
            return (resource, id)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        """_summary_
        """
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url()

        # If the path does not include a query parameter, continue with the original if block
        if self.path == "/users":
            response = get_all_users()
        elif self.path == "/posts":
            response = get_all_posts()
        elif self.path == "/tags":
            response = get_all_tags()
        elif self.path == "/posttags":
            response = get_all_posttags()
        elif self.path == "/comments":
            response = get_all_comments()
        elif self.path == "/subscriptions":
            response = get_all_subscriptions()
        elif self.path == "/postreactions":
            response = get_all_postreactions()        
        else:
            response = []
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Make a post request to the server
        """
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len))
        # response = ''
        resource, _ = self.parse_url()

        if resource == 'login':
            response = login_user(post_body)
            self.wfile.write(response.encode())
        if resource == 'register':
            response = create_user(post_body)
            self.wfile.write(response.encode())
        if resource == 'posts':
            response = create_post(post_body)
        if resource == 'comments':
            response = create_comment(post_body)
            self.wfile.write(response.encode())
        if resource == 'tags':
            response = create_tag(post_body)
            self.wfile.write(response.encode())
        if resource == 'posttags':
            response = create_posttag(post_body)
            self.wfile.write(response.encode())
        if resource == 'subscriptions':
            response = create_subscription(post_body)
            self.wfile.write(response.encode()) 
        if resource == 'postreactions':
            response = create_postreaction(post_body)
            self.wfile.write(response.encode())       

    def do_PUT(self):
        """Handles PUT requests to the server"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url()

        # set default value of success
        success = False

        if resource == "users":
            success = update_user(id, post_body)
        if resource == "posts":
            success = update_post(id, post_body)
        if resource == "tags":
            success = update_tag(id, post_body)
        if resource == "posttags":
            success = update_posttag(id, post_body)
        if resource == "comments":
            success = update_comment(id, post_body)

         # handle the value of success
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)
        
        # Encode the new animal and send in response
        self.wfile.write("".encode())

    def do_DELETE(self):
        """Handle DELETE Requests
        """
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url()

        # Delete a single user from the list
        if resource == "users":
            delete_user(id)
        if resource == "tags":
            delete_tag(id)
        if resource == "posttags":
            delete_posttag(id)
        # Delete a single post from the list
        if resource == "posts":
            delete_post(id)
        # Delete a single comment from the list
        if resource == "comments":
            delete_comment(id)
        if resource == "subscriptions":
            delete_subscription(id)
        if resource == "postreactions":
            delete_postreactions(id)        

        # Encode the new animal and send in response
            self.wfile.write("".encode())


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
