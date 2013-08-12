$(document).ready(function(){

    function sendEvent(e)
    {
        console.log("sent: " + e);
    };

    // implement keypress on body
    $(document).keypress(function(e) {
        sendEvent(String.fromCharCode(e.which));
    });

    // add sendEvent() to all buttons
    $("button[id^='btn_']").each( function() {
        var btn = this.id.replace(/btn_/gi, "");

        $(this).click(function(){
            sendEvent(btn);
        });
    });

});

