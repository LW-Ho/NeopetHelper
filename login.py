import requests, Constants, web, pickle

#Login function
def login(session, username, password):
    logged_in = False

    try:
        file = pickle.load(open("cookies.p", "rb"))

        with open('cookies.p', 'rb') as file:
            session.cookies.update(pickle.load(file))

        #Navigate to login page to try/get initial cookies **if you don't do this step it requires an extra post field that I haven't found
        response = web.get(session, Constants.NEO_LOGIN)
        logged_in = verify_login(username, response)

        if logged_in:
            print("Logged in with cookies")

    except (OSError, IOError) as e:
        file = 3
        pickle.dump(file, open("cookies.p", "wb"))

    #If saved cookies don't work then log in again
    if not logged_in:
        destination = "" #value for a key:value pair required for POST request login

        #Data for POST request to login
        postFields = {"destination": destination, "username": username, "password": password, }

        #Send POST to login
        response = web.post(session, Constants.NEO_LOGIN_REQUEST, postFields, Constants.NEO_LOGIN)

        logged_in = verify_login(username, response)

    if not logged_in:
        print("Login Failed")
    else:
        print("Login Successful")

    return logged_in

def verify_login(username, source):
    logged_in = False

    if "/userlookup.phtml?user=" + username in source:
        logged_in = True
    else:
        logged_in = False

    return logged_in

def save_cookies(session):
    with open('cookies.p', 'wb') as f:
        pickle.dump(session.cookies, f)
