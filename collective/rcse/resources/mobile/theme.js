//$.mobile.ajaxEnabled = true;
var rcseDisableAjax = function(){
	$("#popup-globalsections a").attr("data-ajax", "false");
	$('form[method="post"]').attr("data-ajax", "false");
}

var rcseOpenAuthorInDialog = function(){
	$('a[rel="author"]"').click(function(eventObject){
		eventObject.stopImmediatePropagation();
		eventObject.preventDefault();
		var portal_path = portal_url.slice(window.location.origin.length + 1);
		$.mobile.changePage(
			portal_path + "/@@user_dialog_view",
			{
				role: "dialog",
				data: {memberid: $(this).attr("href").split("/").pop()}
			}
		);
	})
}

var rcseInitAjaxAction = function(){
	$(".document-actions-wrapper a.action").attr("data-ajax", "false");
	$(".document-actions-wrapper a.action").click(function(eventObject){
		eventObject.stopImmediatePropagation();
		eventObject.preventDefault();
		$.ajax({
			url: $(this).attr('href'),
			context: eventObject,
			data: {'ajax': true}
		}).success(function(data){
			var parent = $(eventObject.target).parents(".document-actions-wrapper");
			parent.replaceWith(data['document-actions-wrapper']);
			rcseUpdateUI();
		});
	})
	$('.commenting form').attr("action", portal_url);
	$('.commenting form').submit(function(e){
		e.preventDefault();
	});
	$('.commenting input[type="submit"]').on("click", function(eventObject){
		var form = $(eventObject.target).parents("form");
		var data = {
			ajax: true,
			uid: $(eventObject.target).parents(".rcsetile").attr("id")
		}
		data[$(eventObject.target).attr("name")] = 1;
		form.ajaxSubmit({
			context: form,
			data: data,
			url: portal_url + "/@@plone.comments.ajax",
			success: function(response, status, xhr, jqform){
				var parent = jqform.parents(".document-actions-wrapper");
				parent.replaceWith(response['document-actions-wrapper']);
				rcseUpdateUI();
				parent.find("textarea").val("");
			}
		});
	})
	//make the delete an ajax action to not render the page
	var ajaxDeleteComment = document.createElement("input");
	ajaxDeleteComment.type = "hidden";
	ajaxDeleteComment.name = "ajax";
	ajaxDeleteComment.value = "1";
	$("input[name='form.button.DeleteComment']").parents('form').append(ajaxDeleteComment);
}

var rcseBindChangeEventStartDate = function(){
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

var rcseUpdateNotifications = function(){
    var rcseReloadNotifications = function(eventObject){
	$.ajax({
	    url: portal_url + '/@@notifications_ajax',
	    context: eventObject
	}).success(function(data){
	    var see_all = $("#popup-notifications ul").children("li").last();
	    var see_all_href = see_all.attr('href');
	    var see_all_text = see_all.text();

	    $("#notifications .ui-btn-text").text(data['unseenCount']);

	    $("#popup-notifications ul").remove();
	    $("#popup-notifications").append('<ul data-role="listview" data-inset="true" data-icon="false"></ul>');

	    for (var i = 0 ; i < data['notifications'].length ; i++){
		var notification = data['notifications'][i];
		$("#popup-notifications ul").append('<li><a></a></li>');
		var a = $("#popup-notifications ul li:last").children('a');

		a.attr('href', notification.url);
		if (notification.seen == 0)
		    a.attr('class', 'notification-not-seen');
		a.text(notification.title);
	    }

	    var see_all = '<li><a href="'+ see_all_href +'">'+ see_all_text +'</a></li>';
	    $("#popup-notifications ul").append(see_all);
	    $("#popup-notifications").trigger("create");
	});
    }

    $("#notifications").click(function(){
	rcseReloadNotifications();
    });
}

var rcseUpdateUI = function(){
	rcseDisableAjax();
	rcseInitAjaxAction();
	rcseBindChangeEventStartDate();
	rcseOpenAuthorInDialog();
        rcseUpdateNotifications();
	$("a.oembed,.oembed a").oembed(null, jqueryOmebedSettings);
	picturefill();
	$(document).trigger("create");
}
/* CALL OUR STUFF on jquerymobile events*/

$(document).on("mobileinit", function(){

});

$(document).on("pagebeforeshow", function(){
	rcseUpdateUI();
});

$(document).ready(function(){

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