from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from api_name2path import Name2PathApi

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    # Add these headers to all responses
    def end_headers(self):
        self.send_header(
            "Access-Control-Allow-Headers",
            "Origin, X-Requested-With, Content-Type, Accept",
        )
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", "application/json; charset=utf-8")
        SimpleXMLRPCRequestHandler.end_headers(self)


# Create server
with SimpleXMLRPCServer(
    ("localhost", 8003), requestHandler=RequestHandler, encoding="utf-8"
) as server:

    server.register_instance(Name2PathApi())

    # Run the server's main loop
    server.serve_forever()
