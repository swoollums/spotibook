var client_id = '7191b80ce0364e7e96e282f04131013c'
var client_secret = '1ae0231f8bc14553ad736266be5aae80'
var redirect_uri = 'http://localhost:5000/callback'

function clickedon() {
    login()
}

function login() {
    fetch(`/login?client_id=${client_id}&redirect_uri=${redirect_uri}`)
    .then(function(resp) {
    return resp.json()
        })
    .catch(error => console.error('Error: ', error))
    .then(function(myJson) {
        console.log(myJson)
    })
}

