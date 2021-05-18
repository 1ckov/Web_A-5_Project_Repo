function checkPasswordValidity() {
    var password1 = document.getElementById('password1');
    var password2 = document.getElementById('password2');
    var url = window.location.href;
    var res = url.slice(-11,-9);

    if (password1.value != password2.value) {
        if (res === "en"){
            password2.setCustomValidity('Passwords have to be the same!');
        }
        else if( res === "de"){
            password2.setCustomValidity('Passwörter müssen übereinstimmen!');
        }
        else if( res === "bg"){
            password2.setCustomValidity('Паролите трябва да са еднакви!');
        }
        else if( res === "fr"){
            password2.setCustomValidity('Les mots de passe doivent être les mêmes!');
        }
        else {
            password2.setCustomValidity('Passwords has to be the same!');
        }
    } else {
        password2.setCustomValidity('');
    }
};
