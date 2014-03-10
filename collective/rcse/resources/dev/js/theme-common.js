/**
 * 
  Functions for selecting all/none checkboxes in folder_contents/search_form view
  Provides global toggleSelect; see search_form.pt for example usage.
  global portal_url
  
  selectbutton= input checkbox,
  id='portal_type:list',
  initialState=true,
  formName=null
 */

CKEDITOR.editorConfig = function( config ) {
    config.language = 'fr';
    config.extraPlugins = 'sourcedialog';
    config.removePlugins = 'sourcearea,oembed';
};

function toggleSelect(selectbutton, id, initialState, formName) {
    /* required selectbutton: you can pass any object that will function as a toggle
     * optional id: id of the the group of checkboxes that needs to be toggled (default=ids:list
     * optional initialState: initial state of the group. (default=false)
     * e.g. folder_contents is false, search_form=true because the item boxes
     * are checked initially.
     * optional formName: name of the form in which the boxes reside, use this if there are more
     * forms on the page with boxes with the same name
     */
    var fid, state, base;

    fid = id || 'ids:list';  // defaults to ids:list, this is the most common usage
    state = selectbutton.isSelected;
    if (state === undefined) {
        state = Boolean(initialState);
    }

    // create and use a property on the button itself so you don't have to 
    // use a global variable and we can have as much groups on a page as we like.
    selectbutton.isSelected = !state;
    jQuery(selectbutton).attr('src', portal_url+'/select_'+(state?'all':'none')+'_icon.png');
    base = formName ? jQuery(document.forms[formName]) : jQuery(document);
    base.find('input[name="' + fid + '"]:checkbox').prop('checked', !state);
}
function getViewport() {

    var viewPortWidth;
    var viewPortHeight;

    // the more standards compliant browsers (mozilla/netscape/opera/IE7) use window.innerWidth and window.innerHeight
    if (typeof window.innerWidth != 'undefined') {
      viewPortWidth = window.innerWidth,
      viewPortHeight = window.innerHeight
    }

   // IE6 in standards compliant mode (i.e. with a valid doctype as the first line in the document)
    else if (typeof document.documentElement != 'undefined'
    && typeof document.documentElement.clientWidth !=
    'undefined' && document.documentElement.clientWidth != 0) {
       viewPortWidth = document.documentElement.clientWidth,
       viewPortHeight = document.documentElement.clientHeight
    }

    // older versions of IE
    else {
      viewPortWidth = document.getElementsByTagName('body')[0].clientWidth,
      viewPortHeight = document.getElementsByTagName('body')[0].clientHeight
    }
    return [viewPortWidth, viewPortHeight];
}
