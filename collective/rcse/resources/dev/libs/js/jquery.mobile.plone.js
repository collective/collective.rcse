//$.mobile.ajaxEnabled = false;

/**
@function responsiveIframes
 */
var PloneThemeJQMResponsiveIframes = function()
{
  $('iframe').each(function(){
    var
    $this       = $(this),
    proportion  = $this.data( 'proportion' ),
    w           = $this.attr('width'),
    actual_w    = $this.width();
    
    if ( ! proportion )
    {
        proportion = $this.attr('height') / w;
        $this.data( 'proportion', proportion );
    }
  
    if ( actual_w != w )
    {
        $this.css( 'height', Math.round( actual_w * proportion ) + 'px' );
    }
  });
}


/**
@function convertStatusMessageToJQM

  <dl class="portalMessage warning">
       <dt>Avertissement</dt>
       <dd>MESSASGE HTML <p>paragraph</p></dd>
   </dl>
transformed to ->
    <div class="ui-bar portalMessage portalMessage-info ui-bar-b">
        <h3>Bienvenue ! Vous êtes maintenant connecté(e).</h3>
        <div class="ui-icon ui-icon-info"></div>
    </div>
*/
var PloneThemeJQMConvertStatusMessageToJQM = function(){
	$('dl.portalMessage:visible').each(function() {
		console.log("status message transformed ");
		var message = $(this).find("dd").html();
		var parent = $(this).parent();
		var newMessage = document.createElement("div");
		var newMessageTitle = document.createElement("h3");
		$(newMessageTitle).html(message);
		newMessage.appendChild(newMessageTitle);
		$(newMessage).addClass("ui-bar").addClass('ui-bar-b').addClass($(this).attr('class'));
		parent.append($(newMessage));
		$(this).replaceWith(newMessage);
	});
}
/**
@function convertControlPanelToJQM
<div style="float:left; margin-right: 1em; width: 29%">
    <ul class="configlets">
        <li>
            <a href="http://localhost:8080/Plone/@@calendar-controlpanel">
                <img src="http://localhost:8080/Plone/event_icon.png" alt="Calendrier">
                Calendrier
            </a>
        </li>
        ...
    </ul>
</div>
converted To ->
<div>
    <ul class="configlets ui-listview" data-role="listview">
        <li>
            <a href="http://localhost:8080/adria-rcse/@@rcse-security-controlpanel">
                RCSE configuration
            </a>
        </li>
        ...
    </ul>
</div>
*/
var PloneThemeJQMConvertControlPanelToJQM = function(){
	$('ul.configlets').attr('data-role', 'listview').parent().removeAttr('style');
	$('ul.configlets img').remove();
}
/**
@function convertFormsToJQM
This function converts forms to JQM. It wraps actions into a controlgroup
and add data-theme="b" to the first action (which should be the most important).
*/
var PloneThemeJQMConvertFormsToJQM = function(){
	var formselector = ".formControls span";
	if ($(formselector ).length == 0){
		formselector = ".formControls";
	}
	if ($(formselector).length != 0){
		$(formselector).each(function(){
			var attr = $(this).attr("data-role");
			$(this).attr("data-role", "controlgroup").attr("data-type", "horizontal");
			$(this).find("input[type='submit']").first().attr("data-theme", "b");
		})
	}
}
/**
@function convertTableToJQM
This add data-role="table" attribute to table with listing class.

Make sure table uses thead/tbody tags
*/
var PloneThemeJQMConvertTableToJQM = function (){
	$('table.listing[data-role!="table"]').each(function(){
		//TODO: exclude vertical (eventdetails)
		//TODO: add a tbody wrapper
		if( $(this).find("thead").length == 0 ){
			$(this).find("tr:first").wrap("<thead>");
		}
		$(this).attr("data-role", "table").attr("data-mode", "reflow").addClass("ui-responsive table-stroke");
	});
}
/**
@function convertPortletToJQM
update portlet structure to make it collapsible
theme: use theme-b
<dl class="portlet portletRecent">
    <dt class="portletHeader">
        <span class="portletTopLeft"></span>
        <a href="http://localhost:8080/adria-rcse/recently_modified" class="ui-link">Modifications récentes</a>
        <span class="portletTopRight"></span>
    </dt>
    <dd class="portletItem odd">
        <a href="http://localhost:8080/adria-rcse/groupe-de-travail/test/view" class="state-private tile contenttype-collective-rcse-document ui-link" title="">
             test
             <span class="portletItemDetails">20/06/2013</span>
         </a>
    </dd>
    <dd class="portletItem even">
        <a href="http://localhost:8080/adria-rcse/groupe-de-travail/view" class="state-private tile contenttype-collective-rcse-group" title="">
             groupe de travail
             <span class="portletItemDetails">20/06/2013</span>
         </a>
    </dd>
    <dd class="portletFooter">
        <a href="http://localhost:8080/adria-rcse/recently_modified" class="tile">Toutes les modifications récentes…</a>
        <span class="portletBottomLeft"></span>
        <span class="portletBottomRight"></span>
    </dd>
</dl>
-> should be changed to
<div data-role="collapsible" data-collapsed="false" class="portlet portletNews" data-theme="b">
    <h4>Actualités</a></h4>
    <ul data-role="listview">
    <li>
        <a href="http://localhost:8080/adria-rcse/test-actu-1" class="tile" title="">
            test actu 1
            <span class="portletItemDetails">13/06/2013</span>
         </a>
    </li>
    </ul>
</div></div>
*/
var PloneThemeJQMConvertPortletToJQM = function (){
	$("dl.portlet").each(function(){
		var newPortlet = document.createElement("div");
		var newTitle = document.createElement("h4");
		var newList = document.createElement("ul");

		var title = $(this).find("dt").remove(".portletTopLeft").remove(".portletTopRight").text();
		$(newPortlet).attr("data-role", "collapsible").attr("data-collapsed", "false").addClass($(this).attr("class"));
		$(newTitle).html(title);
		$(newPortlet).append(newTitle);
		$(newList).attr("data-role", "listview");
		$(this).find("dd").each(function(){
			var newItem = document.createElement("li");
			newItem.appendChild(this);
			newList.appendChild(newItem);
		});
		newPortlet.appendChild(newList);
		$(this).replaceWith(newPortlet);
	});
	$('.portlet[data-role="collapsible"]').attr("data-theme", "b");
	$('.portlet[data-role="collapsible"]').parent().trigger("create");
	$('fieldset[data-role="collapsible"]').attr("data-theme", "b");
}
var PloneThemeJQMUpdate = function(){
//	console.log('PloneThemeJQMUpdate');
	PloneThemeJQMResponsiveIframes();
	PloneThemeJQMConvertPortletToJQM();
	PloneThemeJQMConvertTableToJQM();
	PloneThemeJQMConvertControlPanelToJQM();
	PloneThemeJQMConvertFormsToJQM();
	PloneThemeJQMConvertStatusMessageToJQM();
}
$(document).on("pagebeforeshow", function(){
//	console.log("pagebeforeshow");
	PloneThemeJQMUpdate();
});

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