//参加者一覧
$.ajax({type:"GET",
        url:'/party',
        cache: false,
        timeout: 5000})
  .done(function(data) {
    console.log("party:success");
    setTimeout(function(){$('main').html(data).trigger('create');}, 500 );
  }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
    console.log("party:fail");
    console.log(XMLHttpRequest.status);
    console.log(textStatus);
    console.log(errorThrown);
    $('.loading').html('<i class="fa-solid fa-face-frown"></i><div class="japanese">取得できませんでした</div><div class="japanese">再読込してください</div>');
    //setTimeout(function(){$.ajax(this)}, 500 );
  }).always(function() {
  console.log('party:complete');
});
//ニュース欄
$.ajax({type:"GET",
        url:'/news',
        cache: false,
        timeout: 5000})
  .done(function(data) {
    console.log("party:success");
    setTimeout(function(){
    $(".news-banner__content2").addClass("news-banner__content");
    $('.news-banner__content2').html(data).trigger('create');
    }, 500 );
  }).fail(function() {
    $(".news-banner__content2").addClass("news-banner__content");
    $('.news-banner__content2').html('<p><i class="fa-solid fa-face-frown"></i>取得できませんでした。</p>');
  })
  //マネージメントページ
  function ManagementButton(){
    var paramstr = document.location.search;
    window.location.href = '/management'+paramstr;
  }
  function SignUpButton(){
    var paramstr = document.location.search;
    window.location.href = '/signup'+paramstr;
  }
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
