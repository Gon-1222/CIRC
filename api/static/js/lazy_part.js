$.ajax({type:"GET",
        url:'/party',
        cache: false,
        timeout: 10000})
  .done(function(data) {
    $('main').html(data).trigger('create');
  }).fail(function() {
    $('.loading').html('<i class="fa-solid fa-face-frown"></i><div class="japanese">取得できませんでした</div><div class="japanese">再読込してください</div>');
    //setTimeout(function(){$.ajax(this)}, 500 );
  })
/*$.get('/party')
  .done(function(data) {
    $('main').html(data).trigger('create');
  }).fail(function() {
    $('.loading').html('<i class="fa-solid fa-face-frown"></i><div class="japanese">取得できませんでした</div><div class="japanese">再読込してください</div>');
  })*/

$.get('/news')
  .done(function(data) {
    $(".news-banner__content2").addClass("news-banner__content");
    $('.news-banner__content2').html(data).trigger('create');
  }).fail(function() {
    $(".news-banner__content2").addClass("news-banner__content");
    $('.news-banner__content2').html('<p><i class="fa-solid fa-face-frown"></i>取得できませんでした。</p>');
  })
