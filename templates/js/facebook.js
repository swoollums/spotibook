function statusChangeCallback(response) {
    console.log('statusChangeCallback');
    console.log(response);
    if (response.status === 'connected') {
        var uid = response.authResponse.userID;
        var accessToken = response.authResponse.accessToken;
        testAPI()
    } else {
    document.getElementById('status').innerHTML = 'Please log ' +
        'into this app.';
    }
}

function checkLoginState() {
    FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
    });
}

window.fbAsyncInit = function() {
    FB.init({
    appId      : '2081171995475522',
    cookie     : true,
    xfbml      : true,
    version    : 'v2.8'
    });

    FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
    });

};

(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

function post() {
    var message = ""
    for (let i = 0; i < 3; i++) {
        message += i+1 + "). " + document.getElementsByTagName('li')[i].innerText + "\n"
    }
    console.log("Posting...")
    FB.api("/me/feed","POST",{"message": "My Top 3 Songs on Spotify: \n" + message,"link": "https://woolsa01.pythonanywhere.com"},
        function (response) {
        if (response && !response.error) {
            console.log("Posted!")
        }
        else {
            console.log("Could not post")
        }
    }
    );
}

function testAPI() {
    console.log('Welcome!  Fetching your information.... ');
    FB.api('/me', function(response) {
        console.log('Successful login for: ' + response.name);
        x = document.getElementById("fbbtn")
        x.style.display = "none";
        var j = document.getElementById("postbtn");
        j.style.display = "block";
        document.getElementById('status').innerHTML =
        'Thanks for logging in, ' + response.name + '!';
    });
}