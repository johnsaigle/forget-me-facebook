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
        self.logger.debug("Got credentials. Email: {} and Password <some password>".format(email))
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

        # TODO: investigate whether this is the best place for this request
        # prepare a request for the 'On This Day' feature
        url = 'https://www.facebook.com/onthisday'
        yield scrapy.Request(url=url, callback=self.on_this_day)

    def on_this_day(self, response):
        """Scrape contents of Facebook's 'On this Day' page"""
        # Validate that we reached the right page
        if not page_has_title(response, 'On this Day'):
            # Don't proceed if we're on the wrong page
            self.logger.error('Failed to reach On This Day page.')
            write_response_body_to_file('onthisday_fail.html', response.body)
            return
        self.logger.debug("Writing successful response body to file. Learn from it!")
        self.write_response_body_to_file('onthisday_success.html', response.body)
        """TODO: Next steps: follow all the anchor tags with aria-label="Story options" -- these are the
        '...' buttons on each element on the 'On this Day' page.  When this is clicked, <li>s and more <a>
        tags will appear with 'data-feed-option-name="FeedDeleteOption"'.  These steps together should give
        a list of deletion choices.  Once we've got that, we can choose one to delete."""
