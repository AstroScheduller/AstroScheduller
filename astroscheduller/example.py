import requests

class example():
    def __init__(self, url):
        '''
        Initialize the example.

        url: URL to the example.
        '''
        
        self.example(url)

    def example(self, url):
        '''
        Download an example for demostration.

        url: URL to the example.
        '''

        try:
            r = requests.get(url)
            open("./example.xml", "wb").write(r.content)
        except Exception as e:
            raise Exception("scheduller", "unable to load the example", e)

        return True