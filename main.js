(function ($) {
    'use strict';

    var form = $('#upload'),fdata;
    // var fd = new FormData();
    // fd.append('file',file);
    
    form.submit(function (e) {
        e.preventDefault();
        console.log("saujaya");
        fdata = $(this).serialize();
        // console.log(form_data.substring(8));
        $.ajax({
            type: 'POST',
            url: "http://127.0.0.1:5000/upload",
            data : fdata,
            xhrFields: {
                withCredentials: true
            },
            crossDomain: true,
            contentType: 'application/json; charset=utf-8',
            headers: { 'Access-Control-Allow-Origin':'*' }, 
            processData: false,
            success : function(datas){
                console.log("done");
            }
        });
    });
    
})(jQuery);