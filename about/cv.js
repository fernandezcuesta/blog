$(document).ready(function($){
     adjustTop();


    $(window).resize(function(){
        adjustTop();
    });

    var jumboTron = $('.navbar'),
         window_height = $(window).height();

    $(window).scroll(function() {
        var scroll = $(window).scrollTop(),
            scrollMiddle = $(window).scrollTop() + (window_height/2);

        if (scroll >= jumboTron.height()/3) {
            jumboTron.css({'opacity': 0});
            jumboTron.css({'z-index': 0});
        } else {
            jumboTron.css({'opacity': 1});
            jumboTron.css({'z-index': 1});
        }
        $('.card').each(function() {
            elTop = $(this).offset().top;
            elBtm = elTop + $(this).height();
            if (elTop < scrollMiddle && elBtm > scrollMiddle) {
                $(this).find('.label').removeClass('label-default').addClass('label-primary');
                $(this).find('.btn').removeClass('btn-default').addClass('btn-primary');
                $(this).find('.fa-chevron-circle-up').removeClass('text-primary').addClass('text-success');
            } else {
                $(this).find('.label').removeClass('label-primary').addClass('label-default');
                $(this).find('.btn').removeClass('btn-primary').addClass('btn-default');
                $(this).find('.fa-chevron-circle-up').removeClass('text-success').addClass('text-primary');
            }
        });
    });
});


function adjustTop() {
        var height = $('.navbar').height();
        $('.content').css({'padding-top': height + 'px'});
}

/*

var entryBlocks = $('.card');
      entryBlocks.each(function(){
            if ( $(this).offset().top <= 100 && $(this).find('.label').hasClass('label-success') ) {
                $(this).find('.label').removeClass('label-success').addClass('label-primary');
            }
            if ( $(this).offset().top > 100 && $(this).find('.label').hasClass('label-') ) {
            {
                $(this).find('.label').removeClass('label
*/