#!/usr/bin/env python3
import urllib.error
import urllib.request

class ApiError(object):

    @staticmethod
    def get_error(target, error):
        """Return error message."""
        return {'content': "\nCould not generate {}\nFull error code: {}".format(target, error), 'status': "Error occured"}

class Api(object):

    def get_boards(self):
        """Return boards' information."""
        data = {'error': False, 'result': None}

        try:
            data['result'] = urllib.request.urlopen("https://a.4cdn.org/boards.json").read().decode('utf-8')
        except urllib.error.HTTPError as error:
            data['error'] = ApiError.get_error("boards list", error)
        except urllib.error.URLError as error:
            data['error'] = ApiError.get_error("boards list", error)

        return data
    
    def get_threads(self, board, page=1):
        """Get threads by board and page."""
        data = {'error': False, 'result': None}

        try:
            data['result'] = urllib.request.urlopen("https://a.4cdn.org/{}/{}.json".format(board, page)).read().decode('utf-8')
        except urllib.error.HTTPError as error:
            data['error'] = ApiError.get_error("threads list", error)
        except urllib.error.URLError as error:
            data['error'] = ApiError.get_error("threads list", error)

        return data

    def get_thread(self, board, thread_id):
        """Get particular thread by id."""
        data = {'error': False, 'result': None}

        try:
            data['result'] = urllib.request.urlopen("https://a.4cdn.org/{}/thread/{}.json".format(board, thread_id)).read().decode('utf-8')
        except urllib.error.HTTPError as error:
            data['error'] = ApiError.get_error("thread list", error)
        except urllib.error.URLError as error:
            data['error'] = ApiError.get_error("thread list", error)

        return data

    def get_archive(self, board):
        """Get archive of board."""
        data = {'error': False, 'result': None}

        try:
            data['result'] = urllib.request.urlopen("https://a.4cdn.org/{}/archive.json".format(board)).read().decode('utf-8')
        except urllib.error.HTTPError as error:
            data['error'] = ApiError.get_error("archive list", error)
        except urllib.error.URLError as error:
            data['error'] = ApiError.get_error("archive list", error)

        return data
