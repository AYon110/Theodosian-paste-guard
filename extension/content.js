document.addEventListener("paste", function (event){
    const text = event.clipboardData.getData("text");
    console.log(text);

});

