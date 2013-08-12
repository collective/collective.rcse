$.mobile.ajaxEnabled = false;
$(document).on("mobileinit", function(){

});
var initRCSEAjaxAction = function(){
	$("a.ajaxaction").click(function(eventObject){
		eventObject.stopImmediatePropagation();
		eventObject.preventDefault();
		$.ajax({
			url: $(this).attr('href'),
			data: {'ajax': true}
		}).success(function(data){
			var uid = "#"+data['uid']
			$(uid).replaceWith(data['tile']);
			$(document).trigger("create");
			initRCSEAjaxAction();
			picturefill();
		});
	})
}
$(document).ready(function(){
	initRCSEAjaxAction();
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