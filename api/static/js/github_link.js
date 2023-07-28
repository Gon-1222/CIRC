//参加者一覧
$(function(){
$.ajax({type:"GET",
        url:'https://api.github.com/repos/Gon-1222/CIRC-issues/issues',
        dataType:"json",
        cache: false,
        timeout: 5000})
  .done(function(data) {
    console.log("party:success");
    console.log(data);
    var data_stringify = JSON.stringify(data);
    var data_json = JSON.parse(data_stringify);
    var text_data=""
    Object.keys(data_json).forEach(function (key) {
    text_data+="<p>・"
    text_data+=data_json[key]["title"]
    text_data+="</p>"
});
$('.issues').append(text_data);

    //setTimeout(function(){$('main').html(data).trigger('create');}, 500 );
  }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
    console.log("party:fail");
    console.log(XMLHttpRequest.status);
    console.log(textStatus);
    console.log(errorThrown);
    $('.issues').append('<i class="fa-solid fa-face-frown"></i><div class="japanese">取得できませんでした</div><div class="japanese">再読込してください</div>');
    //setTimeout(function(){$.ajax(this)}, 500 );
  }).always(function() {
  console.log('party:complete');
});
});
