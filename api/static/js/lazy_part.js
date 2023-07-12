$.ajax({type:"GET",
        url:'/party',
        cache: false,
        timeout: 5000})
  .done(function(data) {
    console.log("成功");
    $('main').html(data).trigger('create');
  }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
    console.log(XMLHttpRequest.status);
    console.log(textStatus);
    console.log(errorThrown);
    $('.loading').html('<i class="fa-solid fa-face-frown"></i><div class="japanese">取得できませんでした</div><div class="japanese">再読込してください</div>');
    //setTimeout(function(){$.ajax(this)}, 500 );
  })

$.ajax({type:"GET",
        url:'/news',
        cache: false,
        timeout: 5000})
  .done(function(data) {
    $(".news-banner__content2").addClass("news-banner__content");
    $('.news-banner__content2').html(data).trigger('create');
  }).fail(function() {
    $(".news-banner__content2").addClass("news-banner__content");
    $('.news-banner__content2').html('<p><i class="fa-solid fa-face-frown"></i>取得できませんでした。</p>');
  })
/*$.get('/party')
  .done(function(data) {
    $('main').html(data).trigger('create');
  }).fail(function() {
    $('.loading').html('<i class="fa-solid fa-face-frown"></i><div class="japanese">取得できませんでした</div><div class="japanese">再読込してください</div>');
  })*/
/*
$.get('/news')
  .done(function(data) {
    $(".news-banner__content2").addClass("news-banner__content");
    $('.news-banner__content2').html(data).trigger('create');
  }).fail(function() {
    $(".news-banner__content2").addClass("news-banner__content");
    $('.news-banner__content2').html('<p><i class="fa-solid fa-face-frown"></i>取得できませんでした。</p>');
  })
  */
