import requests, login

session = requests.Session()

def main():
    username = ""
    password = ""

    login.login(session, username, password)
    login.save_cookies(session)

if __name__ == "__main__":
    main()
