function validateForm() {
    'use strict';

    // Get references to the form elements:
    var username = document.getElementById('username');
    var password = document.getElementById('password');

    // Validate the login
    if ((username.value.length > 0) && (password.value.length > 0)) {
        check(this);
    } else {
        alert('Please complete the form!');
        return false;
    }
}

function check(form) {

    var usernameArray = ("admin");
    var passwordArray = ("admin");

    if (username.value == usernameArray && password.value == passwordArray) {
        localStorage.setItem("username", username);
        localStorage.setItem("password", password);
        window.open('index.html');
    } else {
        alert('Please enter correct username or password!');
        return false;
    }   
}

function init() {
    'use strict';
    // Confirm that document.getElementById() can be used:
    if (document && document.getElementById) {
        var loginForm = document.getElementById('lgform');
        loginForm.onsubmit = validateForm;
    }
}
window.onload = init;