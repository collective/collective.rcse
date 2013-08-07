$.mobile.ajaxEnabled = false;
$(document).on("mobileinit", function(){

});
$(document).ready(function(){
	$("a.rcse_tile").each(function (){
	    var item = $(this);
	    $.ajax({
	      url: $(this).attr('href') + '/@@group_tile_view'
	    }).success(function(data){
	      item.replaceWith(data);
	      //trigger jquerymobile
	      $(document).trigger("create");
	      //trigger picturefill
	      picturefill();
	    });
	});
})

$( document ).on( "pageinit", ".page", function() {
	$( document ).on( "swipeleft swiperight", ".page", function( e ) {
		if ( $.mobile.activePage.jqmData( "panel" ) !== "open" ) {
            if ( e.type === "swipeleft"  ) {
            	$( "#panel-right" ).panel( "open" );
            } else if ( e.type === "swiperight" ) {
                $( "#panel-left" ).panel( "open" );
            }
        }
    });
});