(function ($) {
    $('.select').change(function(){
        window.location.href = $(this).val();
    });
})(jQuery);
