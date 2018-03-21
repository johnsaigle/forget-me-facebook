import scrapy
import getpass

def prompt_for_credentials():
    """Prompt for user email and password on the command-line"""
    print("Enter email:")
    email = input()
    print("Enter password:")
    password = getpass.getpass()
    credentials = (email, password)
    return credentials

class LoginSpider(scrapy.Spider):
    """Submits login credentials to Facebook"""
    name = "login"

    def start_requests(self):
        url = 'https://facebook.com/login.php'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        credentials = prompt_for_credentials()
        email = credentials[0]
        password = credentials[1]
        return scrapy.FormRequest.from_response(
            response,
            formdata={'email': email, 'pass': password},
            callback=self.after_login
        )

    def after_login(self, response):
        """Steps to do after successful login"""
        # make sure login was successful
        if b'Sign up for Facebook' in response.body:
            self.logger.error("Login failed")
            return

        self.logger.info("Login success.")
