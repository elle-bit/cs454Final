import requests
import json



def get_response(a_key, parameters):
    """responsible for the request to the api
    returing the response object's json data"""


    api_key = '&apikey=' + a_key
    musixmatch_url = "https://api.musixmatch.com/ws/1.1/"
    url = musixmatch_url + parameters + api_key

    max_retry = 3
    while max_retry:
        try:
            api_response = requests.get(url, timeout=(3.05, 60))

            api_response.raise_for_status() #raises only if there is an HTTP error
        except requests.HTTPError as httpE:
            print(f'HTTP error: {httpE}')
            return None

        except requests.Timeout as t:
            print(f'timeout type: {t}')
            print('attempting again')
            max_retry -= 1

        except Exception as e:
            raise SystemExit(f'undefined error: {e}')

        else:
            #handling EMBEDDED status response in json obj. requests 200 status code, api status code error (404,401, etc)
            response = json.loads(api_response.text)
            _status = response["message"]["header"]["status_code"]

            if _status == 200: return response
            elif _status == 401 or _status == 404 or _status == 402:
                print("Error code", _status)
                return {}
            else: 
                raise requests.ConnectionError(_status)

    raise requests.RetryError(f'max retries has been reached')
    return None 






