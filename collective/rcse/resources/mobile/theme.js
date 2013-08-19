$.mobile.ajaxEnabled = false;
$(document).on("mobileinit", function(){

});
var openAuthorInDialog = function(){
	$('a[rel="author"]"').click(function(eventObject){
		eventObject.stopImmediatePropagation();
		eventObject.preventDefault();
		
		$.mobile.changePage(
			portal_url + "/@@user_dialog_view",
			{
				role: "dialog",
				data: {memberid: $(this).attr("href").split("/").pop()}
			}
		);
	})
}
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
var bindChangeEventStartDate = function(){
	$("#form-widgets-IEventBasic-start").blur(function(e){
		var endItem = $("#form-widgets-IEventBasic-end");
		if (endItem.attr('value') === ""){
			endItem.attr('value', $(this).attr('value'));
		}
		else if (new Date(document.getElementById("form-widgets-IEventBasic-start").value) > new Date(document.getElementById("form-widgets-IEventBasic-end").value)){
			endItem.attr('value', $(this).attr('value'));
		}
	})
	$("#form-widgets-IEventBasic-end").blur(function(e){
		var startItem = $("#form-widgets-IEventBasic-start");
		if (startItem.attr('value') === ""){
			startItem.attr('value', $(this).attr('value'));
		}
		else if (new Date(document.getElementById("form-widgets-IEventBasic-start").value) > new Date(document.getElementById("form-widgets-IEventBasic-end").value)){
			startItem.attr('value', $(this).attr('value'));
		}
	})
}
$(document).ready(function(){
	initRCSEAjaxAction();
	bindChangeEventStartDate();
	openAuthorInDialog();
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