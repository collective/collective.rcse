/*!
 * Readmore.js jQuery plugin
 * Author: @jed_foster
 * Project home: jedfoster.github.io/Readmore.js
 * Licensed under the MIT license
 */

;
(function($) {

    var readmore = 'readmore', defaults = {
        speed : 100,
        maxHeight : 200,
        moreLink : '<a href="#">More</a>',
        lessLink : '<a href="#">Less</a>'
    },

    styles = '.readmore-js-toggle, .readmore-js-section { display: block; width: 100%; }\
.readmore-js-section { overflow: hidden; }';

    (function(d, u) {
        if (d.createStyleSheet) {
            d.createStyleSheet(u);
        } else {
            var css = d.createElement('style');
            css.appendChild(document.createTextNode(u));
            d.getElementsByTagName("head")[0].appendChild(css);
        }
    }(document, styles));

    function Readmore(element, options) {
        this.element = element;

        this.options = $.extend({}, defaults, options);

        this._defaults = defaults;
        this._name = readmore;

        this.init();
    }

    Readmore.prototype = {

        init : function() {
            var $this = this;

            $(this.element)
                    .each(
                            function() {
                                var current = $(this), maxHeight = (current
                                        .css('max-height').replace(/[^-\d\.]/g,
                                                '') > $this.options.maxHeight) ? current
                                        .css('max-height').replace(/[^-\d\.]/g,
                                                '')
                                        : $this.options.maxHeight;

                                current.addClass('readmore-js-section');

                                if (current.css('max-height') != "none") {
                                    current.css("max-height", "none");
                                }

                                current.data("boxHeight", current
                                        .outerHeight(true));

                                if (current.outerHeight(true) < maxHeight) {
                                    // The block is shorter than the limit, so
                                    // there's no need to truncate it.
                                    return true;
                                } else {
                                    current.after($($this.options.moreLink).on(
                                            'click',
                                            function(event) {
                                                $this.toggleSlider(this,
                                                        current, event)
                                            }).addClass('readmore-js-toggle'));
                                }

                                sliderHeight = maxHeight;

                                current.css({
                                    height : sliderHeight
                                });
                            });
        },

        toggleSlider : function(trigger, element, event) {
            event.preventDefault();

            var $this = this, newHeight = newLink = '';

            if ($(element).height() == sliderHeight) {
                newHeight = $(element).data().boxHeight + "px";
                newLink = 'lessLink';
            }

            else {
                newHeight = sliderHeight;
                newLink = 'moreLink';
            }

            $(element).animate({
                "height" : newHeight
            }, {
                duration : $this.options.speed
            });

            $(trigger).replaceWith(
                    $($this.options[newLink]).on('click', function(event) {
                        $this.toggleSlider(this, element, event)
                    }).addClass('readmore-js-toggle'));
        }
    };

    $.fn[readmore] = function(options) {
        var args = arguments;
        if (options === undefined || typeof options === 'object') {
            return this.each(function() {
                if (!$.data(this, 'plugin_' + readmore)) {
                    $.data(this, 'plugin_' + readmore, new Readmore(this,
                            options));
                }
            });
        } else if (typeof options === 'string' && options[0] !== '_'
                && options !== 'init') {
            return this.each(function() {
                var instance = $.data(this, 'plugin_' + readmore);
                if (instance instanceof Readmore
                        && typeof instance[options] === 'function') {
                    instance[options].apply(instance, Array.prototype.slice
                            .call(args, 1));
                }
            });
        }
    }
})(jQuery);


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
