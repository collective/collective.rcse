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

var rcseUpdateFluidMedia = function(element){
    if (element == undefined) {
        element = document;
    }
    var transform = function(targetelement){
        // console.log('transform');
        var target = $(targetelement)
        var width = parseInt(target.attr("width"));
        var height = parseInt(target.attr("height"));
        var ratio = height / width;
        target.wrap('<div class="fluid-media"></div>')
          .parent().css('padding-top', (ratio * 100)+"%");
        target.removeAttr('height').removeAttr('width');
    }
    $(element).once('fluid-media', function(){
        $('iframe[width][height]').each(function(){
            transform(this);
        });
    });
}
var rcseInitFluidMedia = function(){
    // console.log('init fluid');
    $(document).on('oembed', function(event, data){
        // console.log('event oembed');
        rcseUpdateFluidMedia($(event.target).parent());
    });
}

var rcseUpdatePortlets = function(element) {
    if (element == undefined) {
        element = document;
    }
    //This handle the @@manage-portlets screen
    if ($("body.template-manage-portlets").length != 0){
        $(element).find('.portletHeader').each(function(){
            var portlet = $(this);
            var title = portlet.find('a').text();
            var link = portlet.find('a').addClass("edit-portlet");
            portlet.find('.portlet-action').addClass('btn-group');
            portlet.find('button').addClass("btn btn-default btn-sm");
            portlet.find('a').wrap('<div class="portlet-title"></div>');
        });
        $(element).find(".edit-portlet").prepend('<i class="icon-pencil"></i> ');
        $("#portal-column-content").attr('class', 'col-md-4');
        $("#portal-column-one").attr('class', 'col-md-4');
        $("#portal-column-two").attr('class', 'col-md-4');
    }
    $(element).find('.managePortletsLink a').addClass('btn btn-default');
    $(element).find('div.portletStaticText').addClass('portletStaticTextNoBorder');
    $(element).find('dl.portlet').each(function() {
        var portlet = $(this);
        var portletSupported = true;
        var newPortlet = document.createElement("div");
        var newTitle = document.createElement("nav");
        var newList = document.createElement("div");
        var titleWrapper = document.createElement("div");
        var title = portlet.find("dt").remove(".portletTopLeft")
                .remove(".portletTopRight").text();
        $(newPortlet).addClass(portlet.attr("class"));
        $(newPortlet).attr('id', portlet.attr("id"));
        $(titleWrapper).addClass("navbar-brand");
        $(newTitle).attr("role", "navigation").addClass("navbar navbar-inverse");
//                        .addClass($(this).attr("class"));
        $(titleWrapper).html(title);
        $(newTitle).append(titleWrapper);
        $(newList).addClass("list-group");
        $(newPortlet).append(newTitle);

        if (portlet.hasClass('portletCalendar')) {
            //add btn and pull-left/right to button;
            portlet.remove('.portletBottomLeft').remove('.portletBottomRight');
            var next = portlet.find(".calendarNext").addClass("navbar-btn btn btn-default").get();
            var prev = portlet.find(".calendarPrevious").addClass("navbar-btn btn btn-default").get();
            $(newPortlet).find(".navbar").append('<div class="controlgroup pull-right"></div>')
                .find('.controlgroup').append(prev).append(next);
            $(newPortlet).find(".navbar-brand").text(
                $(newPortlet).find(".navbar-brand").text().replace("«", "").replace("»", "")
            );
            //do not add list-group-item
            $(newList).append(portlet.find(".portletItem").html());
            newPortlet.appendChild(newList);
            $(newPortlet).find('.event a').tooltip(
		{
		    html:true,
		    delay: {
			show: 0,
			hide: 2000
		    }
		}
	    );
        }else if (portlet.hasClass('portletNavigationTree')) {
            portlet.find('a').addClass('list-group-item');
            portlet.find('div > a').unwrap();
            portlet.find('li > a').unwrap();
            portlet.find('ul > a').unwrap();
            portlet.find('a > img').remove();
            $(newList).append(portlet.html());
            newPortlet.appendChild(newList);

        }else if (portlet.hasClass('portletEvents')){
            /* <a>AA</a>
             * <span class="portletItemDetails">DD</span>
             * ->
             * <a>
                <h4 class="list-group-item-heading">AA</h4>
                <p class="list-group-item-text">DD</p>
              </a>
             */
            portlet.find("dd").each(function() {
                $(this).remove('.portletBottomLeft').remove('.portletBottomRight');
                var link = $(this).find('a');
                var details = $(this).find('.portletItemDetails');
                if (details.length == 0){
                    link.addClass('list-group-item');
                }else{
                    link.wrapInner('<h4 class="list-group-item-heading"></h4>');
                    link.addClass('list-group-item');
                    details.wrap('<p class="list-group-item-text"></p>');
                    $(this).find('.list-group-item-text').detach().appendTo(link);
                }
                $(newList).append($(this).html());
                newPortlet.appendChild(newList);
            });

        }else if (portlet.hasClass('portletLocalUsers')){
            $(newList).append(portlet.find('.portletItem').html());
            $(newList).find('img').tooltip();
            newPortlet.appendChild(newList);
        }else if (portlet.hasClass('portletStaticText')){
            var content = portlet.find('.portletItem').wrapInner('<div class="portletStaticTextInner"></div>').html();
            $(newPortlet).append(content);

        }else if (portlet.hasClass('portletRss')){
            portlet.find("dd").each(function() {
                var link = $(this).find('a');
                link.addClass('list-group-item');
                $(newList).append($(this).html());
            });
            newPortlet.appendChild(newList);

        }else if (portlet.hasClass('portletRecent')){
            portlet.find("dd").each(function() {
                var link = $(this).find('a');
                link.addClass('list-group-item');
                $(newList).append($(this).html());
            });
            newPortlet.appendChild(newList);

        }else if (portlet.hasClass('votePortlet')){
            var content = portlet.find('.portletItem').wrapInner('<div class="portletVoteInner"></div>').html();
            $(newPortlet).append(content);

        }else if (portlet.hasClass('portletFavoritingPortlet')){
            portlet.find("dd").each(function() {
                var link = $(this).find('a');
                link.addClass('list-group-item');
                $(newList).append($(this).html());
            });
            newPortlet.appendChild(newList);

        }else if (portlet.hasClass('portletNews')){
            /*  <dd class="portletItem odd">
                    <a href="#" class="tile" title="">AA</a>
                    <span class="portletItemDetails">DD</span>
                </dd>
                -> 
                <a>
                  <h4 class="list-group-item-heading">AA</h4>
                  <p class="list-group-item-text">DD</p>
                </a>
             */
            portlet.find('dd').each(function(){
                var link = $(this).find('a');
                var details = $(this).find('.portletItemDetails');
                if (details.length == 0){
                    link.addClass('list-group-item');
                }else{
                    link.wrapInner('<h4 class="list-group-item-heading"></h4>');
                    link.addClass('list-group-item');
                    details.wrap('<p class="list-group-item-text"></p>');
                    $(this).find('.list-group-item-text').detach().appendTo(link);
                }
                $(newList).append($(this).html());
            });
            newPortlet.appendChild(newList);
        }else if (portlet.attr('id') == 'portlet-prefs'){
            portlet.find('li').addClass('list-group-item');
            $(newList).append(portlet.html());
            newPortlet.appendChild(newList);
        }else{
            portletSupported = false;
        }
        if (portletSupported){
            portlet.replaceWith(newPortlet);
        }else{
            newPortlet.remove();
        }
    });
    $(element).find('.portletCalendar').each(function(){
    });
}
/**
<dl class="portalMessage error">
  <dt>Erreur</dt>
  <dd>Il y a des erreurs.</dd>
</dl>
 */
var rcseUpdatePortalMessage = function(element){
    $(document).find('.portalMessage:visible').each(function(){
        var wrapper = $(this);
        var title = wrapper.find('dt').html(); // -> str
    if (!title)
        return
        var message = wrapper.find('dd').html();
        var cssclasses = wrapper.attr('class');
        var level = "info";
        if (cssclasses.indexOf("error") != -1){
            level = "error";
        }
        var newWrapper = document.createElement("div");
        $(newWrapper).addClass("alert portalMessage");
        if (level == "info"){
            $(newWrapper).addClass("alert-info portalMessage-info");
        }else if (level == "error"){
            $(newWrapper).addClass("alert-danger portalMessage-danger");
        }
        var newTitle = document.createElement('h4');
        $(newTitle).html(title);
        var newMessage = document.createElement('span');
        $(newMessage).html(message);
        newWrapper.appendChild(newTitle);
        newWrapper.appendChild(newMessage);
        wrapper.replaceWith(newWrapper);
    })
}


/**
 * http://getbootstrap.com/css/#forms
 */
var rcseUpdateForms = function(element){
    if ($(":focus").length==0){
        $(element).find("#form-widgets-IDublinCore-title").each(function(){
            var title = $(this);
            var value = title.val();
            title.focus().val(value);
        });
    }

    //transform form fields for bootstrap
    $(element).find('.field').each(function(){
        var field = $(this);
        field.addClass('form-group');
        field.find('input,textarea').each(function(){
            var input = $(this);
            if (input.attr('type')=="checkbox"){
                return true; // continue
            }
            if (input.attr('type')=="radio"){
                return true; // continue
            }
            if (input.attr('type')=="file"){
		input.filestyle({
		    classButton: 'btn btn-default',
		    buttonText: 'Choisissez un fichier',
		});
                return true; // continue
            }
            input.addClass('form-control');
        });
    });
    //transform form actions for bootstrap
    $(element).find('.formControls').each(function(){
        var formwrapper = $(this);
        var formactions = formwrapper.find('input[type="submit"]');
        if (!formwrapper.hasClass("btn-group")){
            formwrapper.addClass("btn-group");
            formactions.each(function(){
                var input = $(this);
                input.addClass('btn');
                if (input.hasClass('context')){
                    input.addClass('btn-primary');
                }
                else if (input.hasClass('destructive')){
                    input.addClass('btn-danger');
                }
                else{
                    input.addClass('btn-default');
                }
            });
        }
    });
    $(element).find(".workflow-transition-delete").addClass("btn-danger");
    //move the input into the label, this is for checkbox and radio
    var transformlabel = function(input){
        var label = input.siblings("label").first();
        if (label.length == 0){
            return label;
        }
        var innerlabel = label.find('.label');
        var labelText = "";
        if (innerlabel.length != 0){
            labelText = innerlabel.text();
            label.text(labelText);
            innerlabel.remove();
        }else{
            labelText = label.text();
        }
        input.prependTo(label);
        if (label.parents('span.option').length != 0){
            label.unwrap();
        }
        return label;
    }
    //transform checkbox for bootstrap
    $(element).find('input[type="checkbox"]').each(function(){
        var input = $(this);
        var label = transformlabel(input);
        label.wrap('<div class="checkbox"/>');
    });
    //transform checkbox for bootstrap
    $(element).find('input[type="radio"]').each(function(){
        var input = $(this);
        var label = transformlabel(input);
        label.wrap('<div class="radio"/>');
    });
    //transform help message for bootstrap
    $(element).find(".formHelp").each(function(){
        $(this).addClass('help-block');
    });
    $(element).find('span.named-image-widget').each(function(){
        $(this).find('br').remove();
    })
    /*required field -> add a required red * using font awesome
     * <span class="required horizontal" title="Requis">&nbsp;</span>
     * ->
     * <span class="required icon-asterisk"></span>
     * */
    $(element).find('.required.horizontal').each(function(){
        $(this).addClass('icon-asterisk');
    });
    /* ERROR DISPLAY in a field
     * <div class="fieldErrorBox">
            <div class="error">Champ obligatoire</div>
       </div>
       ->
       <div class="alert alert-danger">
            <div class="error">Champ obligatoire</div>
       </div>
     */
    $(element).find('.fieldErrorBox .error').each(function(){
        $(this).parent().addClass('portalMessage alert alert-danger');
    });
    /*
     * <div class="field error form-group">
          <div class="error">You must provide at least a file or a link</div>
       </div>
       ->
       <div class="alert alert-danger">
          <div class="error">You must provide at least a file or a link</div>
       </div>
     */
    $(element).find('.field.error').each(function(){
        $(this).addClass('portalMessage alert alert-danger').removeClass('field error');
    });
    /*
     * Lazy load CKEDITOR if there is contenteditable in the page
     */
    $(element).find('div[contenteditable="true"]').each(function(){
        $(this).addClass('form-control');
        if ($("#ckeditor-script").length == 0){
            var script = document.createElement( 'script' );
            script.type = 'text/javascript';
            script.id = 'ckeditor-script'
            script.src = portal_url + '/++resource++ckeditor/ckeditor.js';
            document.body.appendChild(script);
        }
    });
}
var rcseUpdateOthers = function(element){
    $('#region-content,#content').highlightSearchTerms();
}

var rcseInitPortletCalendar = function(){
    //paste from portlet_calendar.js
    function load_portlet_calendar(event, elem) {
        // depends on plone_javascript_variables.js for portal_url
        event.preventDefault();
        var pw = elem.closest('.portletWrapper');
        var elem_data = elem.data();
        var portlethash = pw.attr('id');
    if (portlethash !== undefined) {
            portlethash = portlethash.substring(15, portlethash.length);
            url = portal_url +
        '/@@render-portlet?portlethash=' + portlethash +
        '&year=' + elem_data.year +
        '&month=' + elem_data.month;
            $.ajax({
        url: url,
        success: function(data) {
                    pw.html(data);
                    rcseApplyTransform(pw);
        }
            });
    }
    else {
        // On events_view
        var location = document.location.href;
        location = location.substr(0, location.lastIndexOf('/'));
            url = location + '/@@calendar_events_view?' +
        'year=' + elem_data.year +
        '&month=' + elem_data.month;
            $.ajax({
        url: url,
        success: function(data) {
                    pw.html(data);
                    rcseApplyTransform(pw);
        }
            });
    }
    }
    //forked from portlet_calendar.js to use on

    $(document).on("click", '.portletCalendar a.calendarNext', function(event) {
        load_portlet_calendar(event, $(this));
    });
    $(document).on("click", '.portletCalendar a.calendarPrevious', function(event) {
        load_portlet_calendar(event, $(this));
    });
}
var rcseInitManagePortlets = function(){
    $('body.template-manage-portlets #portal-columns').on('submit', '.portlet-action', function(e){
        $('#kss-spinner').show();
        var form = $(this);
        var formdata = form.serializeArray();
        var data = {};
        for(var i=0; i<formdata.length; i++){
            data[formdata[i].name] = formdata[i].value;
        }
        data.ajax = true;
        $.ajax({
            url: form.attr('action'),
            data: data,
            type: 'POST',
            success: function(data){
                var container = form.parents('.portlets-manager');
                var parent = container.parent();
                container.replaceWith($(data));
                rcseApplyTransform(parent);
                $('#kss-spinner').hide();
            },
            error: function(){
                $('#kss-spinner').hide();
            }
        });
        return false;
    });
}
var rcseInitTimeline = function() {
    $("a.rcse_tile").append('<div><i class="icon-spinner icon-spin icon-large"></i></div>');
    $("a.rcse_tile").waypoint(function(direction) {
        var item = $(this);
        var parent = item.parent();
        if (typeof(item.attr('href')) == "undefined"){
            return
        }
        var url = item.attr('href') + '/@@group_tile_view';
        $.ajax({
            url : url,
        }).success(function(data) {
//            parent.hide();
            item.replaceWith(data)
            rcseApplyTransform(parent);
            //parent.addClass('animated pulse').show();
//            parent.show();
//            rcseUpdateReadMore(parent);
        });
    }, {offset: '100%'});
}

var rcseUpdateComments = function(element) {
    if (element == undefined) {
        element = document;
    }
    $(element).find('.commenting form').attr("action", portal_url);

    // make the delete an ajax action to not render the page
/*
    var form = $(element).find("input[name='form.button.DeleteComment']")
            .parents('form');
    if (form.length != 0) {
        var ajaxDeleteComment = document.createElement("input");
        ajaxDeleteComment.type = "hidden";
        ajaxDeleteComment.name = "ajax_load";
        ajaxDeleteComment.value = "1";
        form.append(ajaxDeleteComment);
    }
*/
}

/**
 * rcseInitEditBar
 * <div id="edit-bar">
        <ul class="contentViews" id="content-views">
          <li class="selected"><a href="#">Utilisateurs</a></li>
          <li><a href="#">Groupes</a></li>
        </ul>
    </div>
    ->
    <ul class="nav nav-tabs">
      <li class="active"><a href="#">Home</a></li>
      <li><a href="#">Profile</a></li>
      <li><a href="#">Messages</a></li>
    </ul>
 */
var rcseInitEditBar = function(){
    $('#edit-bar ul').each(function(){
        var self = $(this);
        self.addClass('nav nav-tabs');
        self.find('.selected').addClass('active');
    });
}


/**
 * just check query param about a portal_type and update portal_header
 */
var rcseInitFilter = function(){
    var filters = $("#portal-filters"),
        current_view = filters.attr('data-currentview');
    filters.find('.filter-'+current_view).addClass('filter-current');
}

var rcseInitAjaxAction = function() {
    var ajax_blacklist = [
    'add_request_access',
    'add_invite_access',
    'review_requests',
    'ics_view'
    ];

    $(document).on("click", ".document-actions-wrapper a.action", function(eventObject) {
    if (ajax_blacklist.indexOf($(this).attr('id')) != -1)
        return ;
        eventObject.stopImmediatePropagation();
        eventObject.preventDefault();
        var link = $(this);
        if (link.hasClass('btn')){
            link.attr('disabled', 'disabled');
        }
        var container = $(eventObject.target).parents(".document-actions-wrapper");
        var parent = container.parent();
        $.ajax({
            url : $(this).attr('href'),
            context : eventObject,
            data : {
                'ajax_load' : true
            }
        }).success(function(data) {
            var element = data['document-actions-wrapper'];
            container.replaceWith(element);
            rcseApplyTransform(parent);
        }).error(function(){
            link.removeAttr('disabled');
        }).fail(function() {
            link.removeAttr('disabled');
        }).always(function() {
            link.removeAttr('disabled');
        });
    });
    $(document).on("submit", '.commenting form', function(e) {
        e.preventDefault();
    });
    $(document).on("click", '.commenting input[type="submit"]', function(eventObject) {
        eventObject.stopImmediatePropagation();
        eventObject.preventDefault();
        var form = $(eventObject.target).parents("form"),
            uid = $(eventObject.target).parents(".discussion").attr("id"),
            data = {
                ajax_load : true,
                uid : uid
            };
	var btn = $(eventObject.target);
	btn.attr('disabled', 'disabled');
        data[$(eventObject.target).attr("name")] = 1;
        form.ajaxSubmit({
            context : form,
            data : data,
            url : portal_url + "/@@plone.comments.ajax",
            success : function(response, status, xhr, jqform) {
                var parent = jqform.parents(".document-actions-wrapper"),
                    content = parent.parent();
                parent.replaceWith(response['document-actions-wrapper']);
                $("textarea").val('');
                rcseApplyTransform(content);
            },
	    always : function() {
		btn.removeAttr('disabled');
	    }
        });
    });
}

var rcseInitNotifications = function() {
    function hideIfNoNew() {
	if ($('#notifications-count').text() == '0')
	    $('#notifications-count').hide();
	else
	    $('#notifications-count').show();
    }

    var rcseReloadNotifications = function(eventObject) {
        $.ajax({
            url : portal_url + '/@@notifications_ajax',
            context : eventObject
        }).success(function(data) {
            var see_all = $("#notifications ul").children("li").last().find('a');
            var see_all_href = see_all.attr('href');
            var see_all_text = see_all.text();

            $("#notifications-count").text(data['unseenCount']);
            $("#notifications ul").remove();
            $("#notifications")
                .append('<ul class="dropdown-menu"></ul>');

            for (var i = 0; i < data['notifications'].length; i++) {
                var notification = data['notifications'][i];
                $("#notifications ul").append(
                    '<li><a></a></li>');
                var a = $("#notifications ul li:last")
                    .children('a');

                a.attr('href', notification.url);
                if (notification.seen == 0)
                    a.attr('class', 'notification-not-seen');
                a.text(notification.title);
            }

            var see_all = '<li><a href="' + see_all_href + '">'
                + see_all_text + '</a></li>';
            $("#notifications ul").append(see_all);
            $("#notifications").trigger("create");
	    hideIfNoNew();
        });
    }

    $("#notifications > a").click(function() {
        rcseReloadNotifications();
    });

    hideIfNoNew();
}

var rcseInitAddButton = function(){
    $(document).on("click", "#rcseaddform .btn-primary", function(){
        var where = $("#form-widgets-where").val();
        var what = $("#form-widgets-what").val();
        //TODO: add precondition
        window.location = portal_url + '/resolveuid/' + where + '/++add++' + what;
    })
    function checkWhere() {
	var where = $("#form-widgets-where");
	if (where.val() == where.find('option:eq(0)').attr('value')) {
	    $('#form-widgets-what option[value="collective.rcse.group"]')
		.prop('selected', true);
	    $('#form-widgets-what option').each(function(){
		if ($(this).attr('value') != "collective.rcse.group")
		    $(this).prop('disabled', 'disabled');
	    })
	    $('#form-widgets-what').trigger('chosen:updated');
	}
	else {
	    $('#form-widgets-what option').each(function(){
		$(this).prop('disabled', false);
	    })
	    $('#form-widgets-what').trigger('chosen:updated');
	}
    }
    checkWhere();
    $(document).on("change", "#rcseaddform #form-widgets-where", checkWhere);
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

var rcseInitBreadCrumb = function(){
    $(document).on("change", ".breadcrumb select", function(){
        var select = $(this);
        var option = select.find('option:selected');
        window.location = option.val();
    })
}

var rcseInitSearchForm = function(){
    $(document).on("click", '#search-results-bar button.btn-primary, .searchButton', function(event){
        event.stopImmediatePropagation();
        event.preventDefault();
//        console.log("serialize our values to build a new search URL and redirect to it");
        var searchURL = location.href.split('?')[0];
        var query = location.search.split('?')[1];
        var created = $('input[name="created.query:record:list:date"][checked="checked"]').val();
        var SearchableText = $('input[name="SearchableText"]').val();
        var portal_type = ""

        searchURL+= '?'
        $('[name="portal_type:list"]:checked').each(function(){
            portal_type += "&portal_type:list=" + encodeURIComponent($(this).val());
        });
        if (SearchableText != undefined){
            searchURL += 'SearchableText=' + SearchableText;
        }
        if (portal_type != ""){
            searchURL += portal_type;
        }
        if (created != undefined){
            searchURL += '&created.query:record:list:date=' + encodeURIComponent(created);
            searchURL += '&created.range:record=min';
        }
        window.location = searchURL;
    });
    $(document).on("click", "#search-results-bar a.btn-primary", function(){
//        console.log("serialize our search URL to update our inputs");
        var qp = window.location.search.substr(1).split('&');
        for (var i=0,len=qp.length; i<len; i++){
            var p=qp[i].split('=');
            if (p.length != 2) continue;
            var value = decodeURIComponent(p[1].replace(/\+/g, " "));
            var name = p[0];
            if (name == 'SearchableText'){
                $('input[name="SearchableText"]').val(value);
            }else if (name == 'portal_type:list'){
                $('input[name="portal_type:list"][value="' + value + '"]').attr('checked', 'checked');
            }else if (name == 'created.query:record:list:date'){
                $('input[name="created.query:record:list:date"][value="' + value + '"]').attr('checked', 'checked');
            }
        }
    })
}

var rcseInitLoadTileContentInModal = function(){
    $(document).on("click", ".load-content-tile-in-modal", function(event){
        event.stopImmediatePropagation();
        event.preventDefault();
        var title = $(this).text();
        var href = $(this).attr('href');
        var url = href + '/@@group_tile_view?modal=1';
        var modal = $("#content-modal");
        var parent = modal.find('modal-body');
        var item = modal.find('modal-body a');
        modal.find(".modal-title").text(title);
        $.ajax({
            url: url
        }).success(function(data) {
            // console.log('load content in modal');
            // console.log(item);
            $("#content-modal .modal-body").html(data);
            $("#content-modal").modal();
            rcseApplyTransform($("#content-modal .modal-body"));
        });
    });
    $(document).on("click", ".load-img-in-modal", function(event){
        event.stopImmediatePropagation();
        event.preventDefault();
        var title = $(this).find('img').attr('alt');
        var href = $(this).attr('href');
        var modal = $("#img-modal");
        $("#img-modal .modal-body").html('<img src="'+href+'"/>');
        $("#img-modal").modal();
        modal.find(".modal-title").text(title);
        /*update CSS things, by default modal has:
         * .modal-dialog {
                right: auto;
                left: 50%;
                width: 600px;
                padding-top: 30px;
                padding-bottom: 30px;
            }
         */
        modal.find('.modal-dialog').attr('style', 'width: auto; text-align: center;');
    });
}
var rcseInitDeleteConfirmationInModal = function(){
    $(document).on("click", "#form-modal form #form-buttons-cancel", function(event){
        event.stopImmediatePropagation();
        event.preventDefault();
        $("#form-modal").modal('hide');
    });
    //first: display the form in the modal form.
    $(document).on("click", ".workflow-transition-delete", function(event){
        event.stopImmediatePropagation();
        event.preventDefault();
        //is comment or content in tile ?
        var deleteaction = $(this);
        var url = deleteaction.attr("href");
        var isComment = deleteaction.parents(".editbar").length == 0;
        var modal = $("#form-modal");
        var data = {};
        var comment = deleteaction.parents('.comment');
        var tile = deleteaction.parents('.rcse_tile_wrapper');
        var tileurl = tile.find("h2.content-title a").attr('href');
        data.ajax = 1;
        $.ajax({
            url: url,
            data: data
        }).success(function(data) {
            $("#form-modal .modal-body").html($("#content", data).html());
            rcseApplyTransform($("#form-modal .modal-body")[0]);
            modal.modal();
            var options = {success: function showResponse(responseText, statusText, xhr, $form){
                modal.modal('hide');
                //delete the dom elements corresponding to the form
                if (isComment){
                    comment.remove();
                }else{
                    //detect if the current page is the one we are deleting
                    if (window.location == tileurl){
                        window.location = portal_url;
                    }else{
                        tile.remove();
                    }
                }
            }}
            $("#form-modal form").ajaxForm(options);
        });
    });
    //first: handle form action
/*    $(document).on("submit", "#form-modal form", function(event){
//        event.stopImmediatePropagation();
//        event.preventDefault();
        var showResponse = function(responseText, statusText, xhr, $form){
            $("#form-modal .modal-body").html(responseText);
        }
        $(this).ajaxSubmit({
            success: showResponse  // post-submit callback 
        });
        return false;
    });*/
}
var rcseInitMasonry = function(){
    var $container = $('.masonry');
    $container.imagesLoaded(function() {
        window.setTimeout($container.masonry(), 1000);
    });
}

var rcseInitDatatable = function(){
    var settings = {
        "iDisplayLength" : -1,
        "aaSorting" : [ [ 2, "asc" ] ],
        "oLanguage": {
            "sUrl": "@@collective.js.datatables.translation"
        },
        "bRetrieve": true,
        "aLengthMenu" : [ [ 20, 30, 50, -1 ],
                        [ 20, 30, 50, "Tous" ] ]
    }
    $(".datatable").dataTable(settings);
    $("#members-datatable").dataTable(settings);
    $("#favorites-datatable").dataTable(settings);
    $("#review-requests-datatable").dataTable(settings);
    $("#invitations-datatable").dataTable(settings);
    $("#requests-datatable").dataTable(settings);
}

var rcseInitScrollableColumns = function(){
    var ccontent = $('#portal-column-content');
    var cone = $('#portal-column-one');
    var ctwo = $('#portal-column-two');
    var columns = $('#portal-columns');
    var hasone = cone.length == 1;
    var hastwo = ctwo.length == 1;
    var viewport = getViewport();
    var wwidth = viewport[0];
    var wheight = viewport[1];
    var columnsoffset = columns.offset();

    // Configuration
    var padding = 8;

    // Init
    moveColumns();

    function moveColumn(column) {
        if (wwidth < 992){
            //do nothing because columns will be displayed later
	    column.css('margin-top', '0px');
            return ;
        }
        var scrolltop = $(this).scrollTop();

	if (scrolltop < columnsoffset.top) {
	    // Reset
	    column.css('margin-top', '0px');
	    return ;
	}

	var scrollbottom = scrolltop + wheight;
	var columns_bottom = columnsoffset.top + columns.height();
	var bottom = columnsoffset.top + column.height()
	    + parseInt(column.css('padding-top')) + padding;

	if (bottom > scrollbottom) {
	    column.css('margin-top', '0px');
	    // Still something to show, do nothing
	}
	else {
	    // Let's move the column
	    if (column.height() < wheight)
		// Columns is smaller than window, stick to top
		margin = scrolltop - columnsoffset.top;
	    else
		// Stick to bottom
		margin = scrollbottom - bottom;
	    // Check if adding margin will push out the columns
	    if (bottom + margin > columns_bottom) {
		// Set margin to max possible
		if (column.height() < ccontent.height())
		    // Column is smaller than content
		    margin = columnsoffset.top + ccontent.height() - bottom;
		else
		    return ;
	    }
	    column.animate({"margin-top": (margin).toString() + 'px'},
			   {'queue': false,
			    'duration': 100});
	    //column.css('margin-top', (margin).toString() + 'px');
	}
    }

    function moveColumns() {
	if (hasone)
	    moveColumn(cone);
	if (hastwo)
	    moveColumn(ctwo);
    }

    $(window).resize(function(eventObject){
        viewport = getViewport();
        wwidth = viewport[0];
	wheight = viewport[1];
        columnsoffset = columns.offset();
	moveColumns();
    });

    $(window).scroll(function(eventObject){
	moveColumns();
    });
}

var rcseInitMemberDatatables = function(){
    datatableconfig = {
            "iDisplayLength": -1,
            "aLengthMenu": [[100, 200, 500, -1],[100, 200, 500, "All"]],
            "oLanguage": {
                "sUrl": "@@collective.js.datatables.translation"
            }
    };
        $('body.template-member_search_results .listing').dataTable(datatableconfig);
        $('body.template-prefs_group_members .listing').dataTable(datatableconfig);
        $('body.template-usergroup-groupprefs .listing').dataTable(datatableconfig);
        $('body.template-usergroup-userprefs .listing').dataTable(datatableconfig);
        $('body.template-usergroup-userroles .listing').dataTable(datatableconfig);
        $('body.template-sharing #user-group-sharing').dataTable(datatableconfig);
        $('body.template-usergroup-groupmembership .listing').dataTable(datatableconfig);

}
/**
 * hack to make ckeditor working on chrome.
 * http://ckeditor.com/forums/Support/inline-editor-div-contenteditable-when-loaded-hidden-doesnt-work.
 */
var rcseInitChromeContentEditableWorkaround = function(){
    $(document).on("click", '[contenteditable="false"]', function(){
        var name;
        for(name in CKEDITOR.instances) {
            var instance = CKEDITOR.instances[name];
            if(this && this == instance.element.$) {
                instance.destroy();
            }
        }

        $(this).attr('contenteditable', true);
        CKEDITOR.inline(this);
    });
}
var rcseUpdateSelect = function(element){
    if (element == undefined) {
        element = document;
    }
    var select = $(element).find("select").each(function(){
        var select = $(this);
        select.chosen({disable_search_threshold: 15, width: "95%"});
    });
}
var rcseUpdateReadMore = function(element){
    $(element).find(".readmore").removeClass('readmore').readmore({
        moreLink: '<a href="#">' + rcse18n['readmore_more'] + '</a>',
        lessLink: '<a href="#">' + rcse18n['readmore_close'] + '</a>'
    });
}

var rcseUpdatePoll = function(element) {
    $('.poll-data, .votePortlet form').drawpoll();
}

var rcseApplyTransform = function(element) {
    if (element == undefined) {
        element = document;
    }
    rcseUpdateSelect(element);
    rcseUpdatePortlets(element);
    $(element).find('video,audio').mediaelementplayer();
    $(element).find('a.oembed, .oembed a').oembed(null, jqueryOmebedSettings);
    rcseUpdateForms(element);
    picturefill(element);
    rcseUpdatePortalMessage(element);
    $(element).find("img.lazy")
        .removeClass("lazy").lazyload({skip_invisible: false});
//    rcseUpdateFluidMedia(element);
    rcseUpdateOthers(element);
    rcseUpdateReadMore(element);
    rcseUpdatePoll(element);
    return element;
}

$(document).on("ready", function() {
    rcseInitLoadTileContentInModal();
    rcseInitAjaxAction();
    rcseApplyTransform();
    rcseInitTimeline();
    rcseInitVideo();
    rcseInitNotifications();
    rcseInitFilter();
    rcseInitBreadCrumb();
    rcseInitAddButton();
    rcseInitSearchForm();
    rcseInitPortletCalendar();
    rcseInitMasonry();
    rcseInitDatatable();
    $('a[data-toggle="tooltip"]').tooltip();
    rcseInitScrollableColumns();
    rcseInitMemberDatatables();
    rcseInitEditBar();
    rcseInitChromeContentEditableWorkaround();
    rcseInitManagePortlets();
    rcseInitFluidMedia();
    rcseInitDeleteConfirmationInModal();
});
$.webshims.setOptions("basePath", portal_url + "/++resource++webshims/");
$.webshims.setOptions('forms', {
    customDatalist: true
});
$.webshims.setOptions('forms-ext', {
    replaceUI: false,
    types: 'datetime-local month date time number'
});
$.webshims.polyfill();
