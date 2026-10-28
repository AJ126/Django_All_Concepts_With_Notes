// show hide eye icon changes
function togglePassword(){
    const password = document.getElementById('password');
    const icon = document.getElementById('passwordIcon');
    if(password.type === 'password'){
        password.type = 'text';
        icon.classList.replace('bi-eye', 'bi-eye-slash');
    }else{
        password.type = 'password';
        icon.classList.replace('bi-eye-slash', 'bi-eye');
    }
}

// show hide button changes
// function togglePassword(){
//     const password = document.getElementById('password');
//     const button = password.nextElementSibling;
//     if(password.type === 'password'){
//         password.type = 'text';
//         button.textContent = 'Hide';
//     }else{
//         password.type = 'password';
//         button.textContent = 'Show';
//     }
// }