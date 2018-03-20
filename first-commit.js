var casper = require('casper').create({
    pageSettings: {
        loadImages: false,
        loadPlugins: false,
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    }
});

// print out all the messages in the headless browser context
casper.on('remote.message', function(msg) {
    this.echo('remote message caught: ' + msg);
});

// print out all the messages in the headless browser context
casper.on("page.error", function(msg, trace) {
    this.echo("Page Error: " + msg, "ERROR");
});

var url = 'https://www.facebook.com/';

//First step is to open Facebook
casper.start().thenOpen(url, function() {
    console.log("Facebook website opened");
});

//Now we have to populate username and password, and submit the form
casper.then(function(){
    console.log("Login using username and password");
    this.evaluate(function(){
        document.getElementById("email").value="YOUR EMAIL"
    		document.getElementById("pass").value="YOUR PASS";
    		//document.getElementById("loginbutton").children[0].click();
    });
    this.capture('proof-of-concept.png');
});

casper.run(function() {
    console.log("In run function");
    this.echo('Done.').exit();
});
