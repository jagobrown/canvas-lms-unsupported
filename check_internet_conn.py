def checkNet():
    import requests
    site = "http://www.google.com"
    try:

        response = requests.get(site)
        print("Response code: " + str(response.status_code) + " from address : " + site)
    except requests.ConnectionError:
        print ("Could not connect to " + site)

checkNet()