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

$(document).on("ready", function(){
	rcseConvertPortletToBootstrap();
});
