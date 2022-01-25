console.log("Hello this is from javascript")
function show(id, x) {
    var a = document.getElementById(id);
    if (a.type == "password") {
        a.type = "text";
    } else {
        a.type = "password";
    }
    x.firstElementChild.classList.toggle("fa-eye")
    x.firstElementChild.classList.toggle("fa-eye-slash");
}
