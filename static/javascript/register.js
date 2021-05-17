var password1 = document.getElementById('password1');
var password2 = document.getElementById('password2');

function checkPasswordValidity() {
    if (password1.value != password2.value) {
        password2.setCustomValidity('password has to be the same!');
    } else {
        password2.setCustomValidity('');
}
}
document.write(checkPasswordValidity());
