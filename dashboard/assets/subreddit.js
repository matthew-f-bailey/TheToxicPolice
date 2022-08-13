document.addEventListener( "click", scrollAfterSelectSub );

function scrollAfterSelectSub(event){
    // Hacky way to scroll content into view
    const targetNode = document.getElementById('subreddit_content');
    const scrollTo = document.getElementById('subreddit_info')
    const config = { childList: true };
    const callback = function(mutationsList, observer) {
        for(let mutation of mutationsList) {
            if (mutation.type === 'childList') {
                scrollTo.scrollIntoView();
                break;
            }
        }
    };
    const observer = new MutationObserver(callback);
    observer.observe(targetNode, config);
}