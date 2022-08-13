document.addEventListener( "click", scrollAfterSelectSub );

function scrollAfterSelectSub(event){
    let element = event.target;
    if(element.className == 'Select-value-label'){
        alert('Clicked a sub');
    }
}