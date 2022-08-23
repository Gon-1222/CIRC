$.get('/party')
.done(function( data ) {

    //$('main').html( data );
    $('.loading').html( '<i class="fa-solid fa-face-frown"></i><div class="japanese">取得できませんでした。</div><div>再読込してください。</div>' );

}).fail( function() {
  $('.loading').html( '<i class="fa-solid fa-face-frown"></i><div class="japanese">取得できませんでした。</div><div>再読込してください。</div>' );
} )

$.get('/news')
.done(function( data ) {
  console.log(data);
    $('.news-banner__content').html( data );

}).fail( function() {
    console.log(data);
  $('.news-banner__content').html( '<p><i class="fa-solid fa-face-frown"></i>取得できませんでした。</p>');
} )
