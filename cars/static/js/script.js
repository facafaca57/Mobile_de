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