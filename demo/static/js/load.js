//Defines start loading and end loading functions to be used on pages with loading screens added
var loader = document.getElementById('loader');

function startLoading() {
    loader.className = '';
};

function finishedLoading() {
    // first, toggle the class 'done', which makes the loading screen
    // fade out
    loader.className = 'done';
    setTimeout(function() {
        // then, after a half-second, add the class 'hide', which hides
        // it completely and ensures that the user can interact with the
        // map again.
        loader.className = 'hide';
    }, 500);
};