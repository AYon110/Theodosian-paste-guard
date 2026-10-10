document.addEventListener("paste", function (event){
    const text = event.clipboardData.getData("text");
    const emails = emaildetect(text);
    console.log(emails);

});

const EMAIL = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;

function emaildetect(text) {

    return text.match(EMAIL) || [];

}

