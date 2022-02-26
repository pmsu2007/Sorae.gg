$(document).ready(function() {
   $(".page-link").on('click', function () {
       $("#page").val($(this).data("page"));
       $("#searchForm").submit();
   });

   // GET parameter query
   $("#search_button").on('click', function() {
       $("#target").val($(".target").val());
       $("#keyword").val($(".keyword").val());
       $("#page").val(1);
       $("#searchForm").submit();
   });

   // post list sort
   $(".post-sortbox").on('click', function() {
       $("#sort").val($(this).data("sort"));
       $("#page").val(1);
       $("#searchForm").submit();
   })
});