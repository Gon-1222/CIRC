$.get('/party')
.done(function( data ) {

    $('main').html( data );

}).fail( function() {
  $('main').html( "<p><i class=\"fa-solid fa-face-confused\"></i>取得できませんでした。</p>" );
} )
