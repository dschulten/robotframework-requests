import requests

import urllib
import urllib2
import json

import robot

from robot.libraries.BuiltIn import BuiltIn


class RequestsLibrary(object):
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        '''
        TODO: probably can set global proxy here
        '''

        self._cache = robot.utils.ConnectionCache('No sessions created')

        self.builtin = BuiltIn()


    def create_session(self, alias, url, headers=None, cookies=None, auth=None, timeout=None, proxies=None):
        ''' Create Session: create a HTTP session to a server

        *url:* Base url of the server
        *alias:* Robot Framework alias to identify the session
        *headers:* Dictionary of default headers
        *auth:* Dictionary of username & password for HTTP Basic Auth
        *timeout:* connection timeout
        *proxies:* proxy server url
        '''

        def baseurlhook(args):
            # url is the base url. Request url is uri
            args['url'] = '%s%s' %(url, args['url'])
        
        self.builtin.log('Creating session: %s' %alias, 'DEBUG')

        session = requests.session(hooks=dict(args=baseurlhook), auth=auth, headers=headers,
                cookies=cookies, timeout=timeout, proxies=proxies )
        self._cache.register(session, alias=alias)
        return session


    def delete_all_sessions(self):
        ''' Delete Session: removes all the session objects
        '''

        self._cache.empty_cache()


    def to_json(self, content):
        return json.loads(content)

    
    def get(self, alias, uri, **kwargs):
        ''' Get: send a GET request on the session object found using the given alias 
        '''

        session = self._cache.switch(alias)
        resp = session.get(uri, **kwargs)

        # store the last response object
        session.last_resp = resp
        return resp


    def post(self, alias, uri, **kwargs):
        ''' Post: send a POST request on the session object found using the given alias 
        '''

        session = self._cache.switch(alias)
        resp = session.post(uri, **kwargs)

        # store the last response object
        session.last_resp = resp
        return resp


    def put(self, alias, uri, **kwargs):
        ''' Put: send a GET request on the session object found using the given alias 
        '''

        session = self._cache.switch(alias)
        resp = session.put(uri, **kwargs)

        # store the last response object
        session.last_resp = resp
        return resp


    def delete(self, alias, uri, **kwargs):
        ''' Delete: send a DELETE request on the session object found using the given alias 
        '''

        session = self._cache.switch(alias)
        resp = session.delete(uri, **kwargs)

        # store the last response object
        session.last_resp = resp
        return resp


    def head(self, alias, uri, **kwargs):
        ''' Delete: send a HEAD request on the session object found using the given alias 
        '''

        session = self._cache.switch(alias)
        resp = session.head(uri, **kwargs)

        # store the last response object
        session.last_resp = resp
        return resp

    

if __name__ == '__main__':
    rl = RequestsLibrary()
    session = rl.create_session('github', 'http://github.com/api/v2/json')
    #resp = rl.get('github', '/user/search/bulkan')
    #jsondata = rl.to_json(resp.content)


    auth = ('user', 'passwd')
    session = rl.create_session('httpbin', 'http:/httpbin.org', auth=auth)
    resp = rl.get('httpbin', '/basic-auth/user/passwd')
    import pdb; pdb.set_trace() 
    

    
    #with requests.session(auth=auth) as c:
    #    resp = c.get('http://httpbin.org/basic-auth/user/passwd')
    #    print resp


    
    # sometimes you just need pdb
