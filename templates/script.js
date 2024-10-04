document.getElementById("login_form").onsubmit = function(e) {
    let netid = document.getElementById("login").value;
    let password = document.getElementById("passwd").value;

    if (netid === "" || password === "") {
        e.preventDefault();
        alert("Please fill in both fields.");
    }
};
