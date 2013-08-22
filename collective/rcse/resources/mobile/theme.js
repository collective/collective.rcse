//$.mobile.ajaxEnabled = true;
/*!
 * Readmore.js jQuery plugin
 * Author: @jed_foster
 * Project home: jedfoster.github.io/Readmore.js
 * Licensed under the MIT license
 */

;(function($) {

  var readmore = 'readmore',
      defaults = {
        speed: 100,
        maxHeight: 200,
        moreLink: '<a href="#">More</a>',
        lessLink: '<a href="#">Less</a>'
      },

      styles = '.readmore-js-toggle, .readmore-js-section { display: block; width: 100%; }\
.readmore-js-section { overflow: hidden; }';

    (function(d,u) {
      if(d.createStyleSheet) {
        d.createStyleSheet( u );
      }
      else {
        var css=d.createElement('style');
        css.appendChild(document.createTextNode(u));
        d.getElementsByTagName("head")[0].appendChild(css);
      }
    }(document, styles));

  function Readmore( element, options ) {
    this.element = element;

    this.options = $.extend( {}, defaults, options) ;

    this._defaults = defaults;
    this._name = readmore;

    this.init();
  }

  Readmore.prototype = {

    init: function() {
      var $this = this;

      $(this.element).each(function() {
        var current = $(this),
            maxHeight = (current.css('max-height').replace(/[^-\d\.]/g, '') > $this.options.maxHeight) ? current.css('max-height').replace(/[^-\d\.]/g, '') : $this.options.maxHeight;

        current.addClass('readmore-js-section');

        if(current.css('max-height') != "none") {
          current.css("max-height", "none");
        }

        current.data("boxHeight", current.outerHeight(true));

        if(current.outerHeight(true) < maxHeight) {
          // The block is shorter than the limit, so there's no need to truncate it.
          return true;
        }
        else {
          current.after($($this.options.moreLink).on('click', function(event) { $this.toggleSlider(this, current, event) }).addClass('readmore-js-toggle'));
        }

        sliderHeight = maxHeight;

        current.css({height: sliderHeight});
      });
    },

    toggleSlider: function(trigger, element, event)
    {
      event.preventDefault();

      var $this = this,
          newHeight = newLink = '';

      if ($(element).height() == sliderHeight) {
        newHeight = $(element).data().boxHeight + "px";
        newLink = 'lessLink';
      }

      else {
        newHeight = sliderHeight;
        newLink = 'moreLink';
      }

      $(element).animate({"height": newHeight}, {duration: $this.options.speed });

      $(trigger).replaceWith($($this.options[newLink]).on('click', function(event) { $this.toggleSlider(this, element, event) }).addClass('readmore-js-toggle'));
    }
  };

  $.fn[readmore] = function( options ) {
    var args = arguments;
    if (options === undefined || typeof options === 'object') {
      return this.each(function () {
        if (!$.data(this, 'plugin_' + readmore)) {
          $.data(this, 'plugin_' + readmore, new Readmore( this, options ));
        }
      });
    } else if (typeof options === 'string' && options[0] !== '_' && options !== 'init') {
      return this.each(function () {
        var instance = $.data(this, 'plugin_' + readmore);
        if (instance instanceof Readmore && typeof instance[options] === 'function') {
          instance[options].apply( instance, Array.prototype.slice.call( args, 1 ) );
        }
      });
    }
  }
})(jQuery);


/* SMART SCOLL
 * 
$(window).bind('smartscroll', function() {
	// Check if near bottom
	var pixelsFromWindowBottomToBottom = 0 + $(document).height()
			- ($(window).scrollTop()) - $(window).height();

	// if distance remaining in the scroll (including buffer) is less
	// than the orignal nav to bottom....
	if (pixelsFromWindowBottomToBottom - 40 < $(document).height() - $a.offset().top) {
		console.log("do some stuff...");
	}
});
 */

// define a custom event
/*
 * smartscroll: debounced scroll event for jQuery *
 * https://github.com/lukeshumard/smartscroll Based on smartresize by
 * @louis_remi: https://github.com/lrbabe/jquery.smartresize.js * Copyright 2011
 * Louis-Remi & Luke Shumard * Licensed under the MIT license. *
 */
/*
var event = $.event, scrollTimeout;

event.special.smartscroll = {
	setup : function() {
		$(this).bind("scroll", event.special.smartscroll.handler);
	},
	teardown : function() {
		$(this).unbind("scroll", event.special.smartscroll.handler);
	},
	handler : function(event, execAsap) {
		// Save the context
		var context = this, args = arguments;

		// set correct event type
		event.type = "smartscroll";

		if (scrollTimeout) {
			clearTimeout(scrollTimeout);
		}
		scrollTimeout = setTimeout(function() {
			$(context).trigger('smartscroll', args);
		}, execAsap === "execAsap" ? 0 : 100);
	}
};

$.fn.smartscroll = function(fn) {
	return fn ? this.bind("smartscroll", fn) : this.trigger("smartscroll",
			[ "execAsap" ]);
};
*/
var rcseLoadTimeline = function(){
	$("a.rcse_tile").each(function (){
	    var item = $(this);
	    $.ajax({
	      url: $(this).attr('href') + '/@@group_tile_view'
	    }).success(function(data){
	      item.replaceWith(data);
	      rcseUpdateUI();
	      $(document).trigger("create");
	    });
	});
}
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
			$(document).trigger("create");
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
				$(document).trigger("create");
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
			$("#popup-notifications ul").remove();
			$("#popup-notifications").append('<ul data-role="listview" data-inset="true" data-icon="false"></ul>');

			for (var i = 0 ; i < data.length ; i++){
				var notification = data[i];
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
//	console.log('rcseUpdateUI');
	rcseDisableAjax();
	rcseInitAjaxAction();
	rcseBindChangeEventStartDate();
	rcseOpenAuthorInDialog();
        rcseUpdateNotifications();
	$("a.oembed,.oembed a").oembed(null, jqueryOmebedSettings);
	picturefill();
	$(".readmore").readmore();
}
$(document).on("pagebeforeshow", function(){
//	console.log("pagebeforeshow");
	rcseUpdateUI();
});
$(document).on("pageshow", function(){
	console.log("pageshow");
	rcseLoadTimeline();
});
