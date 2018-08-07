var id_ = 0;

$('.more').click(function(){
    id_ += 10;
    $.ajax(
    {
        type:"GET",
        url: "/load",
        data:{
            _id: id_
        },
        success: function( data ) 
        {
            if (data.length < 50){
                $('.more').remove();
                $('#message').css("display","block");
            }
            else{
                $('.col-md-11').append(data);
            }
        }
     })
});

$('.search').click(function(){
    fuels = $(".zapravka").val();
    kpp = $(".kpp").val();
    categories = $(".categories").val();
    year = $(".year").val();

    $.ajax(
    {
        type:"GET",
        url: "/search",
        data:{
            fuels: fuels,
            kpp:kpp,
            categories:categories,
            year:year
        },
        success: function(data) 
        {
            $('#msg').css("display", "inline");
            $('#msg').text("Знайдено: " + data);
        },
        error: function (data) {
            $('#msg').css("display", "inline");
            $('#msg').text("Перегляд");
        }
     })
});