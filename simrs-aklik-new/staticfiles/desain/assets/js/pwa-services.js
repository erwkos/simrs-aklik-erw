'use strict'
/* PWA services worker register */
if ("serviceWorker" in navigator) {
    window.addEventListener("load", function (event) {
        navigator.serviceWorker
            .register("https://app.kma-jatiwangi.id/static/desain/serviceWorker.js", {
            //.register("https://mongtuh.com/website/cool/HTML/serviceWorker.js", {
                scope: './'
            })
            .then(reg => console.log("service worker registered"))
            .catch(err => console.log("service worker not registered"));
    });
}

window.addEventListener("appinstalled", function (event) {
    //app.logEvent("a2hs", "Installed");
    document.getElementById('toastinstall').style.display = 'none';
});


if (window.matchMedia('(display-mode: fullscreen)').matches) {
    $('#toastinstall').fadeOut()
} else {
    $('#toastinstall').fadeIn()
}
