(function ($){
    // 'use strict';

    var form=$("#upload-file");
    form.submit(function (e) {
    e.preventDefault();
    var form_data = new FormData($('#upload-file')[0]);
    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:5000/upload',
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        success: function(data) {
            console.log("ho gya");
        },
    });
    document.getElementById("generate").style.display = "block";
});
})(jQuery);