import requests

class StepicClient:
    """
    Client to communicate with api
    """

    token = None

    def __init__(self, stepik_id, stepik_secret):
        """Получаем токен при создании клиента
        """
        self.get_token(stepik_id, stepik_secret)



    def request(self, request_type, link, **kwargs):
        resp = None

        kwargs["headers"] = {'Authorization': 'Bearer ' + self.token}

        try:
            resp = requests.__dict__[request_type](link, **kwargs)
        except Exception as e:
            exit_util(e.args[0])
        if resp.status_code >= 400:
            exit_util("Something went wrong.")

        return resp


    def get_token(self, stepik_id, stepik_secret):

        auth = requests.auth.HTTPBasicAuth(stepik_id, stepik_secret)
        response = requests.post('https://stepik.org/oauth2/token/', data={'grant_type': 'client_credentials'},
                                 auth=auth)
        token = response.json().get('access_token', None)
        if not token:
            print('Unable to authorize with provided credentials')
            exit(1)

        self.token = token
        return True


    def get_token_from_config(self):
        """DEPRECATED"""
        self.get_token(config["stepik_id"], config["stepik_secret"])
        return True
