import scrapy
import getpass
import logging

def prompt_for_credentials():
    """Prompt for user email and password on the command-line"""
    print("Enter email:")
    email = input()
    print("Enter password:")
    password = getpass.getpass()
    credentials = (email, password)
    return credentials

def response_body_contains_string(response_body, canary_string):
    """Check if response body contains the canary_string value.  This should be given as a bytes."""
    if canary_string not in response_body:
        return False
    return True

def page_has_title(response, title):
    """Check if the response HTML has a title attribute equal to `title`."""
    if not response.css('title::text').extract_first() == title:
        return False
    return True

class LoginSpider(scrapy.Spider):
    """Submits login credentials to Facebook"""
    name = "login"

    def __init__(self, *args, **kwargs):
        # set log level to warning for the middlware (i.e. silence INFO logs)
        logger = logging.getLogger('scrapy.middleware')
        logger.setLevel(logging.WARNING)
        logger = logging.getLogger('scrapy.statscollectors')
        logger.setLevel(logging.WARNING)
        super().__init__(*args, **kwargs)

    def write_response_body_to_file(self, filename, response_body):
        """Write HTML response body to a file for debugging"""
        with open(filename, 'wb') as filehandle:
            filehandle.write(response_body)
        self.logger.debug("Wrote the response to {} for debugging.".format(filename))

    def start_requests(self):
        url = 'https://facebook.com/login.php'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """After receiving the login page, prompt user for FB credentials and submit them."""
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
        # If the below string is in the reponse, we failed
        if response_body_contains_string(response.body, b'Sign up for Facebook'):
            self.logger.error("Login failed")
            return
        self.logger.info("Login success.")

        # get the profile username
        profile_link = response.xpath('//div[@data-click="profile_icon"]/a/@href').extract_first()
        nickname = profile_link.split('/')[3] # e.g. https://facebook.com/nickname; nickname is the 4th element
        self.logger.debug("Nickname is " + nickname)
        url = 'https://facebook.com/' + nickname + '/activitylog'
        self.logger.debug('Navigating to your timeline (in a future version!)')

        """TODO: Next steps: Navigate to timeline and delete from there. It's simpler than On This Day.

        Example of timeline deletion
        ajaxify="/ajax/timeline/delete/confirm?identifier=S%3A_I520626340%3A10150283244796341&location=3&story_dom_id=u_jsonp_10_3&causal_container_id=u_jsonp_10_i"
        The actual POST requst: /ajax/timeline/delete?identifier=S%3A_I520626340%3A10150283244786341&location=3&story_dom_id=u_jsonp_10_5
        """
