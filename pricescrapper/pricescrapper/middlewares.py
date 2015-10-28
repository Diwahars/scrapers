
class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = "http://111.161.126.100:80"
