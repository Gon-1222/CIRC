$.get('/party')
.done(function( data ) {

    $('main').html( data );

}).fail( function() {
  $('main').html( "<p><i class=\"fa-solid fa-face-confused\"></i>取得できませんでした。</p>" );
} )

$.get('/news')
.done(function( data ) {
  console.log(data);
    $('.news-banner__content').html( data );

}).fail( function() {
    console.log(data);
  $('.news-banner__content').html( "<p><i class=\"fa-solid fa-face-confused\"></i>取得できませんでした。</p>" );
} )
