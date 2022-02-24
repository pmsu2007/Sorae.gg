$(document).ready(function(){
    $(".delete").on('click', function() {
        if(confirm("글을 삭제하시겠습니까?")) {
            location.href = $(this).data('uri');
        }
    });

    $(".recommend").on('click', function() {
        if(confirm("글을 추천하시겠습니까?")) {
            location.href = $(this).data('uri');
        }
    });
});