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

var rcseConvertPortletToBootstrap = function(){
	console.log('rcseConvertPortletToBootstrap');
	$('dl.portlet').each(function(){
		var newPortlet = document.createElement("div");
		var newTitle = document.createElement("nav");
		var newList = document.createElement("div");
		var titleWrapper = document.createElement("div")
		var title = $(this).find("dt").remove(".portletTopLeft").remove(".portletTopRight").text();

		$(newPortlet).addClass($(this).attr("class"));
		$(titleWrapper).addClass("navbar-brand");
		$(newTitle).attr("role", "navigation").addClass("navbar navbar-inverse").addClass($(this).attr("class"));
		$(titleWrapper).html(title);
		$(newTitle).append(titleWrapper);
		$(newList).addClass("list-group");
		$(newPortlet).append(newTitle);
		if ($(this).hasClass('portletNavigationTree')){
			console.log('navtree');
			$(this).find('a').addClass('list-group-item');
			$(this).find('div > a').unwrap();
			$(this).find('a > img').remove();
			$(this).find("li").each(function(){
				console.log("li");
				$(newList).append($(this).html());
			})
		}else{
			$(this).find("dd").each(function(){
				console.log('others');
				$(this).find('a').addClass('list-group-item');
				$(newList).append($(this).html());
			});
		}
		newPortlet.appendChild(newList);
		$(this).replaceWith(newPortlet);
	});
}

var rcseMakePortletColumnsAffix = function(){
/*	FIXME: At the moment if fix on the left ...
 * $('#portal-column-one').attr('data-spy', "affix");
	$('#portal-column-two').attr('data-spy', "affix");*/
}

var rcseLoadTimeline = function(){
	$("a.rcse_tile").each(function (){
	    var item = $(this);
	    $.ajax({
	      url: $(this).attr('href') + '/@@group_tile_view'
	    }).success(function(data){
	      item.replaceWith(data);
	      rcseUpdateUI();
	    });
	});
}


var rcseInitAjaxAction = function(){
	console.log("init ajax action");
	$(document).on("click", ".document-actions-wrapper a.action", function(eventObject){
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
	$(document).on("click", '.commenting input[type="submit"]', function(eventObject){
		eventObject.stopImmediatePropagation();
		eventObject.preventDefault();
		console.log("ajax: comment submit");
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
//				rcseUpdateUI();
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

var rcseUpdateUI = function(){
	rcseConvertPortletToBootstrap();
	$("a.oembed,.oembed a").oembed(null, jqueryOmebedSettings);
	picturefill();
}
$(document).on("ready", function(){
	rcseInitAjaxAction();
	rcseLoadTimeline();
	rcseUpdateUI();
});
