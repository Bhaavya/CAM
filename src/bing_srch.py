import requests
import json 
import time
import random 

bing_search_url = "https://api.bing.microsoft.com/v7.0/search"
bing_api_key = BING_API_KEY



def bing_search(search_term):
    headers = {"Ocp-Apim-Subscription-Key": bing_api_key}
    params = {"q": search_term, "textDecorations": True, "textFormat": "HTML","count":10,"responseFilter":"WebPages"}
    response = requests.get(bing_search_url, headers=headers, params=params, )
    response.raise_for_status()
    # print(response.json())
    results = response.json()
    # print(results['webPages']['value'])
    try:
    	return results['webPages']['value']
    except:
    	return []

if __name__ == '__main__':
	bing_search("+access AND analogy")