/* ========================================================================
 * RCSE THEME
 * ========================================================================
 * Copyright 2013 Makina-Corpus
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ======================================================================== */

var rcseUpdatePortlets = function(element) {
    if (element == undefined) {
        element = document;
    }
    $(element).find('dl.portlet').each(
            function() {
                var newPortlet = document.createElement("div");
                var newTitle = document.createElement("nav");
                var newList = document.createElement("div");
                var titleWrapper = document.createElement("div")
                var title = $(this).find("dt").remove(".portletTopLeft")
                        .remove(".portletTopRight").text();

                $(newPortlet).addClass($(this).attr("class"));
                $(titleWrapper).addClass("navbar-brand");
                $(newTitle).attr("role", "navigation").addClass(
                        "navbar navbar-inverse")
                        .addClass($(this).attr("class"));
                $(titleWrapper).html(title);
                $(newTitle).append(titleWrapper);
                $(newList).addClass("list-group");
                $(newPortlet).append(newTitle);
                if ($(this).hasClass('portletNavigationTree')) {
                    console.log('navtree');
                    $(this).find('a').addClass('list-group-item');
                    $(this).find('div > a').unwrap();
                    $(this).find('a > img').remove();
                    $(this).find("li").each(function() {
                        console.log("li");
                        $(newList).append($(this).html());
                    })
                } else {
                    $(this).find("dd").each(function() {
                        console.log('others');
                        $(this).find('a').addClass('list-group-item');
                        $(newList).append($(this).html());
                    });
                }
                newPortlet.appendChild(newList);
                $(this).replaceWith(newPortlet);
            });
}

var rcseInitTimeline = function() {
    $("a.rcse_tile").each(function() {
        var item = $(this);
        $.ajax({
            url : $(this).attr('href') + '/@@group_tile_view'
        }).success(function(data) {
            element = rcseApplyTransform(data);
            item.replaceWith(element);
        });
    });
}

var rcseUpdateComments = function(element) {
    if (element == undefined) {
        element = document;
    }
    $(element).find('.commenting form').attr("action", portal_url);
    // make the delete an ajax action to not render the page
    var form = $(element).find("input[name='form.button.DeleteComment']")
            .parents('form');
    if (form.length != 0) {
        var ajaxDeleteComment = document.createElement("input");
        ajaxDeleteComment.type = "hidden";
        ajaxDeleteComment.name = "ajax_load";
        ajaxDeleteComment.value = "1";
        form.append(ajaxDeleteComment);
    }
}

var rcseInitAjaxAction = function() {
    $(document).on(
            "click",
            ".document-actions-wrapper a.action",
            function(eventObject) {
                eventObject.stopImmediatePropagation();
                eventObject.preventDefault();
                $.ajax({
                    url : $(this).attr('href'),
                    context : eventObject,
                    data : {
                        'ajax_load' : true
                    }
                }).success(
                        function(data) {
                            var element = data['document-actions-wrapper'];
                            element = rcseApplyTransform(element);
                            var parent = $(eventObject.target).parents(
                                    ".document-actions-wrapper");
                            parent.replaceWith(element);
                        });
            })
    $(document).on("submit", '.commenting form', function(e) {
        e.preventDefault();
    });
    $(document)
            .on(
                    "click",
                    '.commenting input[type="submit"]',
                    function(eventObject) {
                        eventObject.stopImmediatePropagation();
                        eventObject.preventDefault();
                        console.log("ajax: comment submit");
                        var form = $(eventObject.target).parents("form");
                        var data = {
                            ajax : true,
                            uid : $(eventObject.target).parents(".rcsetile")
                                    .attr("id")
                        }
                        data[$(eventObject.target).attr("name")] = 1;
                        form
                                .ajaxSubmit({
                                    context : form,
                                    data : data,
                                    url : portal_url + "/@@plone.comments.ajax",
                                    success : function(response, status, xhr,
                                            jqform) {
                                        var parent = jqform
                                                .parents(".document-actions-wrapper");
                                        parent
                                                .replaceWith(response['document-actions-wrapper']);
                                        parent.find("textarea").val("");
                                    }
                                });
                    })

}

var rcseInitVideo = function(){
    $(document).on('mouseenter', 'div.download',
	function(){
            $(this).find('.dl-links').show();
	});

    $(document).on('mouseleave', 'div.videobar',
	function(){
            $(this).find('.dl-links').fadeOut(500);
	});

    function changeSrc(player, src){
	var currentTime = player.getCurrentTime();
	player.setSrc(src);

	setTimeout(function(){
	    if (currentTime > 0){
		player.setCurrentTime(currentTime);
		player.play();
	    }
	}, 100);
    }

    $(document).on('click', '.player-low', function (event) {
	var videoElement = $(this).parents('.videobar')
	    .siblings('.mejs-container').find('video');
	var player = new MediaElementPlayer(videoElement);
	createCookie('videores', 'low');
	$(this).parents('.hi-lo').find('.player-high').show();
	$(this).parents('.hi-lo').find('.player-low').hide();
	var newSrc = videoElement.attr('src').replace('high/', 'low/');
	changeSrc(player, newSrc);
	event.preventDefault();
    });

    $(document).on('click', '.player-high', function (event) {
	var videoElement = $(this).parents('.videobar')
	    .siblings('.mejs-container').find('video');
	var player = new MediaElementPlayer(videoElement);
	createCookie('videores', 'high');
	$(this).parents('.hi-lo').find('.player-high').hide();
	$(this).parents('.hi-lo').find('.player-low').show();
	var newSrc = videoElement.attr('src').replace('low/', 'high/');
	changeSrc(player, newSrc);
	event.preventDefault();
    });

}

var rcseUpdateVideo = function(element) {
    if (element == undefined)
	element = document;
    $(document).find('video').mediaelementplayer();
}

var rcseApplyTransform = function(element) {
    if (element == undefined) {
        element = document;
    }
    console.log('rcseApplyTransform' + $(element).find(".readmore"));
//    $(element).find("a.oembed,.oembed a").oembed(null, jqueryOmebedSettings);
    $(element).find("select").select2();
    $(element).find(".readmore").readmore();
    rcseUpdatePortlets(element);
    rcseUpdateVideo(element);
    return element;
}

$(document).on("ready", function() {
    rcseInitAjaxAction();
    rcseApplyTransform();
    rcseInitTimeline();
    rcseInitVideo();
});
