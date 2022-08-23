$.get('/party')
.done(function( data ) {

    $('main').html( data );
    $('main').html( '<div class="reload_mark"><p><i class="fa-solid fa-face-confused"></i>取得できませんでした。</p><p>再読込してください。</p></div>' );

}).fail( function() {
  $('main').html( '<div class="reload_mark"><p><i class="fa-solid fa-face-confused"></i>取得できませんでした。</p><p>再読込してください。</p></div>' );
} )

$.get('/news')
.done(function( data ) {
  console.log(data);
    $('.news-banner__content').html( data );

}).fail( function() {
    console.log(data);
  $('.news-banner__content').html( "<p><i class=\"fa-solid fa-face-confused\"></i>取得できませんでした。</p>" );
} )
