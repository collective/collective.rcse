/* jshint node: true */

module.exports = function(grunt) {
    "use strict";
    // Project configuration.
    grunt.initConfig({

        // Metadata.
        pkg : grunt.file.readJSON('package.json'),
        banner : '/**\n' + '* RCSE theme by Makina-Corpus\n'
                + '*/\n',

        // Task configuration.
        bower: {
            install: {
                options: {
                    install: true,
                    copy: false
                  }
            }
        },
        copy : {
            ckeditor: {
                expand : true,
                cwd : 'app/bower_components/eo-ckeditor/',
                src : [ '*.js', '*.css', 'lang/**', 'plugins/**', 'skins/**', 'core/**'],
                dest : '../ckeditor'
            },
            ckeditorconfig: {
                expand : true,
                cwd : 'js/',
                src : [ 'config.js' ],
                dest : '../ckeditor'
            },
            desktopfont : {
                expand : true,
                cwd : 'app/bower_components/font-awesome/',
                src : [ 'font/**', ],
                dest : '../desktop/'
            },
            desktopdatatables : {
                expand : true,
                cwd : 'app/bower_components/datatables/media',
                src : [ 'images/*.png', ],
                dest : '../desktop/'
            },
            desktopchosen : {
                expand : true,
                cwd : 'app/bower_components/chosen/',
                src : [ '*.png' ],
                dest : '../desktop/css/'
            },
            desktopmediaelement : {
                expand : true,
                cwd : 'app/bower_components/mediaelement/build/',
                src : [ '*.png', '*.svg', '*.gif' ],
                dest : '../desktop/css/'
            },
	    desktopimages : {
		expand : true,
                cwd : 'less/images/desktop/',
                src : [ '*.png', '*.svg', '*.gif' ],
                dest : '../desktop/images/'
	    },
            mobilefont : {
                expand : true,
                cwd : 'app/bower_components/font-awesome/',
                src : [ 'font/**', ],
                dest : '../mobile/'
            },
            mobilemediaelement : {
                expand : true,
                cwd : 'app/bower_components/mediaelement/build/',
                src : [ '*.png', '*.svg', '*.gif' ],
                dest : '../mobile/css/'
            },
	    mobileimages : {
		expand : true,
                cwd : 'less/images/mobile/',
                src : [ '*.png', '*.svg', '*.gif' ],
                dest : '../mobile/images/'
	    },
            webshims: {
                expand : true,
                cwd : 'app/bower_components/webshim/demos/js-webshim/minified/shims/',
                src : [ '**', ],
                dest : '../webshims/'
            },
        },
        concat : {
            options : {
                banner : '<%= banner %>',
                stripBanners : false
            },
            desktopjs : {
                src : [
                        //'app/bower_components/modernizr/modernizr.js',
                        'app/bower_components/webshim/demos/js-webshim/minified/extras/modernizr-custom.js',
                        'app/bower_components/jquery/jquery.js',
 		        'app/bower_components/jquery-ui/ui/jquery.ui.position.js',
                        'app/bower_components/jqueryform/jquery.form.js',
                        'app/bower_components/matchmedia/matchMedia.js',
                        'app/bower_components/bootstrap/dist/js/bootstrap.js',
                        'app/bower_components/picturefill/picturefill.js',
                        'app/bower_components/chosen/chosen.jquery.js',
                        'app/bower_components/jquery-waypoints/waypoints.js',
                        'app/bower_components/jquery.lazyload/jquery.lazyload.js',
                        'app/bower_components/flot/jquery.flot.js',
                        'app/bower_components/flot/jquery.flot.pie.js',
                        'app/bower_components/excanvas/excanvas.js',
                        'app/bower_components/datatables/media/js/jquery.dataTables.js',

		        'app/bower_components/bootstrap-filestyle/src/bootstrap-filestyle.js',
                        'app/bower_components/eventEmitter/EventEmitter.js',
                        'app/bower_components/eventie/eventie.js',
                        'app/bower_components/doc-ready/doc-ready.js',
                        'app/bower_components/get-style-property/get-style-property.js',
                        'app/bower_components/get-size/get-size.js',
                        'app/bower_components/jquery-bridget/jquery.bridget.js',
                        'app/bower_components/jquery-once/jquery.once.js',
                        'app/bower_components/matches-selector/matches-selector.js',
                        'app/bower_components/outlayer/item.js',
                        'app/bower_components/outlayer/outlayer.js',
                        'app/bower_components/imagesloaded/imagesloaded.js',
                        'app/bower_components/masonry/masonry.js',
                        'app/bower_components/readmore/readmore.js',
		        'app/bower_components/tasksplease/jquery.tasksplease.js',

                        'app/bower_components/mediaelement/build/mediaelement-and-player.js',
                        'app/bower_components/webshim/demos/js-webshim/minified/polyfiller.js',
                        'js/custom/jquery.oembed.js',
                        'js/custom/cookie_functions.js',
                        'js/custom/comments.js',
                        'js/custom/jquery.highlightsearchterms.js',
                        'js/polls.js',
                        'js/collective.poll.js',
                        'js/theme-common.js',
                        'js/theme-desktop.js'],
                dest : '../desktop/js/desktop.js'
            },
            mobilejs : {
                src : [ 'app/bower_components/jquery-1.9/jquery.js',
                        'app/bower_components/jqueryform/jquery.form.js',
                        //'app/bower_components/jquery-mobile-bower/js/jquery.mobile-1.3.2.js',
                        'app/bower_components/jquery-once/jquery.once.js',
                        'js/jquery.mobile.js',
                        'app/bower_components/fastclick/lib/fastclick.js',
                        'app/bower_components/picturefill/picturefill.js',
                        'app/bower_components/mediaelement/build/mediaelement-and-player.js',
                        'app/bower_components/readmore/readmore.js',
                        'app/bower_components/flot/jquery.flot.js',
                        'app/bower_components/flot/jquery.flot.pie.js',
                        'app/bower_components/excanvas/excanvas.js',
                        'app/bower_components/jquery-waypoints/waypoints.js',
		        'app/bower_components/tasksplease/jquery.tasksplease.js',
                        'js/custom/jquery.oembed.js',
                        'js/custom/cookie_functions.js',
                        'js/custom/comments.js',
                        'js/custom/jquery.mobile.plone.js',
                        'js/polls.js',
                        'js/collective.poll.js',
                        'js/theme-common.js', 'js/theme-mobile.js'],
                dest : '../mobile/js/mobile.js'
            },

            desktopcss : {
                src : [
                        'app/bower_components/mediaelement/build/mediaelementplayer.css',
                        'app/bower_components/font-awesome/css/font-awesome.css',
                    '../desktop/css/app.css',
		    '../desktop/css/theme_default.css',
		    'less/collective.polls.css' ],
                dest : '../desktop/css/desktop.css'
            },
            desktopmincss : {
                src : [
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/font-awesome/css/font-awesome.min.css',
                    '../desktop/css/app.min.css',
		'../desktop/css/theme_default.min.css',
		'less/collective.polls.css'],
                dest : '../desktop/css/desktop.min.css'
            },
	    desktopAmelia : {
                src : [
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/font-awesome/css/font-awesome.min.css',
                    '../desktop/css/app.min.css',
		'../desktop/css/theme_amelia.min.css',
		'less/collective.polls.css'],
                dest : '../desktop/css/desktop-amelia.min.css'
	    },
	    desktopCosmo : {
                src : [
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/font-awesome/css/font-awesome.min.css',
                    '../desktop/css/app.min.css',
		'../desktop/css/theme_cosmo.min.css',
		'less/collective.polls.css'],
                dest : '../desktop/css/desktop-cosmo.min.css'
	    },
	    desktopFlatly : {
                src : [
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/font-awesome/css/font-awesome.min.css',
                    '../desktop/css/app.min.css',
		'../desktop/css/theme_flatly.min.css',
		'less/collective.polls.css'],
                dest : '../desktop/css/desktop-flatly.min.css'
	    },
	    desktopJournal : {
                src : [
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/font-awesome/css/font-awesome.min.css',
                    '../desktop/css/app.min.css',
		'../desktop/css/theme_journal.min.css',
		'less/collective.polls.css'],
                dest : '../desktop/css/desktop-journal.min.css'
	    },
	    desktopReadable : {
                src : [
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/font-awesome/css/font-awesome.min.css',
                    '../desktop/css/app.min.css',
		'../desktop/css/theme_readable.min.css',
		'less/collective.polls.css'],
                dest : '../desktop/css/desktop-readable.min.css'
	    },
	    desktopSlate : {
                src : [
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/font-awesome/css/font-awesome.min.css',
                    '../desktop/css/app.min.css',
		'../desktop/css/theme_slate.min.css',
		'less/collective.polls.css'],
                dest : '../desktop/css/desktop-slate.min.css'
	    },
	    desktopSuperhero : {
                src : [
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/font-awesome/css/font-awesome.min.css',
                    '../desktop/css/app.min.css',
		'../desktop/css/theme_superhero.min.css',
		'less/collective.polls.css'],
                dest : '../desktop/css/desktop-superhero.min.css'
	    },
	    desktopYeti : {
                src : [
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/font-awesome/css/font-awesome.min.css',
                    '../desktop/css/app.min.css',
		'../desktop/css/theme_yeti.min.css',
		'less/collective.polls.css'],
                dest : '../desktop/css/desktop-yeti.min.css'
	    },
	    desktopCerulean : {
                src : [
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/font-awesome/css/font-awesome.min.css',
                    '../desktop/css/app.min.css',
		'../desktop/css/theme_cerulean.min.css',
		'less/collective.polls.css'],
                dest : '../desktop/css/desktop-cerulean.min.css'
	    },
	    desktopCyborg : {
                src : [
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/font-awesome/css/font-awesome.min.css',
                    '../desktop/css/app.min.css',
		'../desktop/css/theme_cyborg.min.css',
		'less/collective.polls.css'],
                dest : '../desktop/css/desktop-cyborg.min.css'
	    },
	    desktopLumen : {
                src : [
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/font-awesome/css/font-awesome.min.css',
                    '../desktop/css/app.min.css',
		'../desktop/css/theme_lumen.min.css',
		'less/collective.polls.css'],
                dest : '../desktop/css/desktop-lumen.min.css'
	    },
	    desktopSimplex : {
                src : [
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/font-awesome/css/font-awesome.min.css',
                    '../desktop/css/app.min.css',
		'../desktop/css/theme_simplex.min.css',
		'less/collective.polls.css'],
                dest : '../desktop/css/desktop-simplex.min.css'
	    },
	    desktopSpacelab : {
                src : [
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/font-awesome/css/font-awesome.min.css',
                    '../desktop/css/app.min.css',
		'../desktop/css/theme_spacelab.min.css',
		'less/collective.polls.css'],
                dest : '../desktop/css/desktop-spacelab.min.css'
	    },
	    desktopUnited : {
                src : [
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/font-awesome/css/font-awesome.min.css',
                    '../desktop/css/app.min.css',
		'../desktop/css/theme_united.min.css',
		'less/collective.polls.css'],
                dest : '../desktop/css/desktop-united.min.css'
	    },

            mobilecss : {
                options : {
                    banner : '<%= banner %>',
                    stripBanners : false
                },
                src : [
                        'app/bower_components/mediaelement/build/mediaelementplayer.css',
                        'app/bower_components/jquery-mobile-bower/css/jquery.mobile.structure-1.3.2.css',
                        'app/bower_components/jquery-mobile-bower/css/jquery.mobile.theme-1.3.2.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.css',
                        '../mobile/css/app.css' ],
                dest : '../mobile/css/mobile.css'
            },
            mobilemincss : {
                src : [
                       'app/bower_components/jquery-mobile-bower/css/jquery.mobile.structure-1.3.2.min.css',
                       'app/bower_components/jquery-mobile-bower/css/jquery.mobile.theme-1.3.2.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        '../mobile/app.min.css' ],
                dest : '../mobile/css/mobile.min.css'
            },

            mobilemincssamelia : {
                src : [
                       'app/bower_components/jquery-mobile-bower/css/jquery.mobile.structure-1.3.2.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        '../mobile/css/theme_amelia.min.css' ],
                dest : '../mobile/css/mobile-amelia.min.css'
            },
            mobilemincsscerulean : {
                src : [
                       'app/bower_components/jquery-mobile-bower/css/jquery.mobile.structure-1.3.2.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        '../mobile/css/theme_cerulean.min.css' ],
                dest : '../mobile/css/mobile-cerulean.min.css'
            },
            mobilemincsscosmo : {
                src : [
                       'app/bower_components/jquery-mobile-bower/css/jquery.mobile.structure-1.3.2.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        '../mobile/css/theme_cosmo.min.css' ],
                dest : '../mobile/css/mobile-cosmo.min.css'
            },
            mobilemincsscyborg : {
                src : [
                       'app/bower_components/jquery-mobile-bower/css/jquery.mobile.structure-1.3.2.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        '../mobile/css/theme_cyborg.min.css' ],
                dest : '../mobile/css/mobile-cyborg.min.css'
            },
            mobilemincssflatly : {
                src : [
                       'app/bower_components/jquery-mobile-bower/css/jquery.mobile.structure-1.3.2.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        '../mobile/css/theme_flatly.min.css' ],
                dest : '../mobile/css/mobile-flatly.min.css'
            },
            mobilemincssjournal : {
                src : [
                       'app/bower_components/jquery-mobile-bower/css/jquery.mobile.structure-1.3.2.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        '../mobile/css/theme_journal.min.css' ],
                dest : '../mobile/css/mobile-journal.min.css'
            },
            mobilemincsslumen : {
                src : [
                       'app/bower_components/jquery-mobile-bower/css/jquery.mobile.structure-1.3.2.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        '../mobile/css/theme_lumen.min.css' ],
                dest : '../mobile/css/mobile-lumen.min.css'
            },
            mobilemincssreadable : {
                src : [
                       'app/bower_components/jquery-mobile-bower/css/jquery.mobile.structure-1.3.2.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        '../mobile/css/theme_readable.min.css' ],
                dest : '../mobile/css/mobile-readable.min.css'
            },
            mobilemincsssimplex : {
                src : [
                       'app/bower_components/jquery-mobile-bower/css/jquery.mobile.structure-1.3.2.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        '../mobile/css/theme_simplex.min.css' ],
                dest : '../mobile/css/mobile-simplex.min.css'
            },
            mobilemincssslate : {
                src : [
                       'app/bower_components/jquery-mobile-bower/css/jquery.mobile.structure-1.3.2.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        '../mobile/css/theme_slate.min.css' ],
                dest : '../mobile/css/mobile-slate.min.css'
            },
            mobilemincssspacelab : {
                src : [
                       'app/bower_components/jquery-mobile-bower/css/jquery.mobile.structure-1.3.2.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        '../mobile/css/theme_spacelab.min.css' ],
                dest : '../mobile/css/mobile-spacelab.min.css'
            },
            mobilemincsssuperhero : {
                src : [
                       'app/bower_components/jquery-mobile-bower/css/jquery.mobile.structure-1.3.2.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        '../mobile/css/theme_superhero.min.css' ],
                dest : '../mobile/css/mobile-superhero.min.css'
            },
            mobilemincssunited : {
                src : [
                       'app/bower_components/jquery-mobile-bower/css/jquery.mobile.structure-1.3.2.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        '../mobile/css/theme_united.min.css' ],
                dest : '../mobile/css/mobile-united.min.css'
            },
            mobilemincssyeti : {
                src : [
                       'app/bower_components/jquery-mobile-bower/css/jquery.mobile.structure-1.3.2.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        '../mobile/css/theme_yeti.min.css' ],
                dest : '../mobile/css/mobile-yeti.min.css'
            },
        },

        uglify : {
            desktopjs : {
                options : {
                    compress : true
                },
                src : [ '../desktop/js/desktop.js' ],
                dest : '../desktop/js/desktop.min.js'
            },
            mobilejs : {
                options : {
                    compress : true
                },
                src : [ '../mobile/js/mobile.js' ],
                dest : '../mobile/js/mobile.min.js'
            }
        },

        recess : {
            desktopless : {
                options : {
                    compile : false,
                    compress : true
                },
                src : [ 'app/bower_components/chosen/chosen.css',
                        'app/bower_components/datatables/media/css/jquery.dataTables.css',
                        'app/bower_components/bootstrap/dist/css/bootstrap.css',
                        'app/bower_components/bootstrap/dist/css/bootstrap-theme.css',
                        ],
                dest : '../desktop/css/app.css'
            },
            desktopmin : {
                options : {
                    compile : false,
                    compress : true
                },
                src : '../desktop/css/app.css',
                dest : '../desktop/css/app.min.css'
            },

	    desktopThemeDefaultLess : {
		options : {
                    compile : true,
                    compress : false
                },
		src : [ 'less/desktop.less' ],
		dest : '../desktop/css/theme_default.css'
	    },
	    desktopThemeDefaultMin : {
		options : {
                    compile : false,
                    compress : true
                },
		src : '../desktop/css/theme_default.css',
		dest : '../desktop/css/theme_default.min.css'
	    },

	    desktopThemeAmelia : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/amelia/desktop.less' ],
		dest : '../desktop/css/theme_amelia.min.css'
	    },
	    desktopThemeCosmo : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/cosmo/desktop.less' ],
		dest : '../desktop/css/theme_cosmo.min.css'
	    },
	    desktopThemeFlatly : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/flatly/desktop.less' ],
		dest : '../desktop/css/theme_flatly.min.css'
	    },
	    desktopThemeJournal : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/journal/desktop.less' ],
		dest : '../desktop/css/theme_journal.min.css'
	    },
	    desktopThemeReadable : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/readable/desktop.less' ],
		dest : '../desktop/css/theme_readable.min.css'
	    },
	    desktopThemeSlate : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/slate/desktop.less' ],
		dest : '../desktop/css/theme_slate.min.css'
	    },
	    desktopThemeSuperhero : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/superhero/desktop.less' ],
		dest : '../desktop/css/theme_superhero.min.css'
	    },
	    desktopThemeYeti : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/yeti/desktop.less' ],
		dest : '../desktop/css/theme_yeti.min.css'
	    },
	    desktopThemeCerulean : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/cerulean/desktop.less' ],
		dest : '../desktop/css/theme_cerulean.min.css'
	    },
	    desktopThemeCyborg : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/cyborg/desktop.less' ],
		dest : '../desktop/css/theme_cyborg.min.css'
	    },
	    desktopThemeLumen : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/lumen/desktop.less' ],
		dest : '../desktop/css/theme_lumen.min.css'
	    },
	    desktopThemeSimplex : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/simplex/desktop.less' ],
		dest : '../desktop/css/theme_simplex.min.css'
	    },
	    desktopThemeSpacelab : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/spacelab/desktop.less' ],
		dest : '../desktop/css/theme_spacelab.min.css'
	    },
	    desktopThemeUnited : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/united/desktop.less' ],
		dest : '../desktop/css/theme_united.min.css'
	    },

            mobileless : {
                options : {
                    compile : true,
                    compress : false
                },
                src : [ 'less/mobile.less'],
                dest : '../mobile/css/app.css'
            },
            mobilemin : {
                options : {
                    compile : true,
                    compress : true
                },
                src : [ 'less/mobile.less'],
                dest : '../mobile/app.min.css'
            },

	    // Theme
	    mobileThemeAmelia : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/amelia/mobile.less' ],
		dest : '../mobile/css/theme_amelia.min.css'
	    },
	    mobileThemeCosmo : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/cosmo/mobile.less' ],
		dest : '../mobile/css/theme_cosmo.min.css'
	    },
	    mobileThemeFlatly : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/flatly/mobile.less' ],
		dest : '../mobile/css/theme_flatly.min.css'
	    },
	    mobileThemeJournal : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/journal/mobile.less' ],
		dest : '../mobile/css/theme_journal.min.css'
	    },
	    mobileThemeReadable : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/readable/mobile.less' ],
		dest : '../mobile/css/theme_readable.min.css'
	    },
	    mobileThemeSlate : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/slate/mobile.less' ],
		dest : '../mobile/css/theme_slate.min.css'
	    },
	    mobileThemeSuperhero : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/superhero/mobile.less' ],
		dest : '../mobile/css/theme_superhero.min.css'
	    },
	    mobileThemeYeti : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/yeti/mobile.less' ],
		dest : '../mobile/css/theme_yeti.min.css'
	    },
	    mobileThemeCerulean : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/cerulean/mobile.less' ],
		dest : '../mobile/css/theme_cerulean.min.css'
	    },
	    mobileThemeCyborg : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/cyborg/mobile.less' ],
		dest : '../mobile/css/theme_cyborg.min.css'
	    },
	    mobileThemeLumen : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/lumen/mobile.less' ],
		dest : '../mobile/css/theme_lumen.min.css'
	    },
	    mobileThemeSimplex : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/simplex/mobile.less' ],
		dest : '../mobile/css/theme_simplex.min.css'
	    },
	    mobileThemeSpacelab : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/spacelab/mobile.less' ],
		dest : '../mobile/css/theme_spacelab.min.css'
	    },
	    mobileThemeUnited : {
		options : {
                    compile : true,
                    compress : true
                },
		src : [ 'less/themes/united/mobile.less' ],
		dest : '../mobile/css/theme_united.min.css'
	    },
        },

        watch : {
            desktoprecess : {
                files : [
                         'less/desktop.plone.less',
                         'less/desktop-theme.less',
                         'less/desktop.less',
                         'less/collective.polls.css'
                         ],
                tasks : [ 'desktop-dist-css' ]
            },
            mobilerecess : {
                files : ['less/mobile-theme.less',
                         'less/mobile-font-awesome.less',
                         'less/mobile.less'
                         ],
                tasks : [ 'mobile-dist-css' ]
            },
            desktopconcat : {
                files : [
                         'js/custom/jquery.oembed.js',
                         'js/custom/cookie_functions.js',
                         'js/custom/comments.js',
                         'js/custom/jquery.highlightsearchterms.js',
                         'js/polls.js',
                         'js/collective.poll.js',
                         'js/theme-common.js',
                         'js/theme-desktop.js'
                         ],
                tasks : [ 'desktop-dist-js' ]
           }
        }
    });

    // These plugins provide necessary tasks.
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-recess');
    grunt.loadNpmTasks('grunt-bower-task');

    // bower
    grunt.registerTask('install', [ 'bower:install' ]);
    // JS distribution task.
    grunt.registerTask('desktop-dist-js', [ 'concat:desktopjs' ]);
    grunt.registerTask('mobile-dist-js', [ 'concat:mobilejs' ]);
    grunt.registerTask('dist-js', [ 'desktop-dist-js', 'uglify:desktopjs',
                                    'mobile-dist-js', 'uglify:mobilejs' ]);

    // CSS distribution task.
    grunt.registerTask('desktop-dist-css', [ 'recess:desktopless',
					     'recess:desktopThemeDefaultLess', 'recess:desktopThemeDefaultMin',
					     'concat:desktopcss',
					     'recess:desktopThemeAmelia', 'concat:desktopAmelia',
					     'recess:desktopThemeCosmo', 'concat:desktopCosmo',
					     'recess:desktopThemeCerulean', 'concat:desktopCerulean',
					     'recess:desktopThemeCyborg', 'concat:desktopCyborg',
					     'recess:desktopThemeFlatly', 'concat:desktopFlatly',
					     'recess:desktopThemeJournal', 'concat:desktopJournal',
					     'recess:desktopThemeLumen', 'concat:desktopLumen',
					     //'recess:desktopThemeReadable', 'concat:desktopReadable',
					     'recess:desktopThemeSimplex', 'concat:desktopSimplex',
					     'recess:desktopThemeSlate', 'concat:desktopSlate',
					     'recess:desktopThemeSpacelab', 'concat:desktopSpacelab',
					     //'recess:desktopThemeSuperhero', 'concat:desktopSuperhero',
					     'recess:desktopThemeUnited', 'concat:desktopUnited',
					     'recess:desktopThemeYeti', 'concat:desktopYeti',
					   ]);

    grunt.registerTask('mobile-dist-css', [ 'recess:mobileless', 'concat:mobilecss',
					    'recess:mobileThemeAmelia', 'concat:mobilemincssamelia',
					    'recess:mobileThemeCerulean', 'concat:mobilemincsscerulean',
					    'recess:mobileThemeCosmo', 'concat:mobilemincsscosmo',
					    'recess:mobileThemeCyborg', 'concat:mobilemincsscyborg',
					    'recess:mobileThemeFlatly', 'concat:mobilemincssflatly',
					    'recess:mobileThemeJournal', 'concat:mobilemincssjournal',
					    'recess:mobileThemeLumen', 'concat:mobilemincsslumen',
					    //'recess:mobileThemeReadable', 'concat:mobilemincssreadable',
					    'recess:mobileThemeSimplex', 'concat:mobilemincsssimplex',
					    'recess:mobileThemeSlate', 'concat:mobilemincssslate',
					    'recess:mobileThemeSpacelab', 'concat:mobilemincssspacelab',
					    //'recess:mobileThemeSuperhero', 'concat:mobilemincsssuperhero',
					    'recess:mobileThemeUnited', 'concat:mobilemincssunited',
					    'recess:mobileThemeYeti', 'concat:mobilemincssyeti',
					  ]);
    grunt.registerTask('dist-css', [  'desktop-dist-css', 'recess:desktopmin',
                                      'mobile-dist-css' , 'recess:mobilemin',
                                      'concat:desktopmincss', 'concat:mobilemincss' ]);

    // Fonts distribution task.
    // grunt.registerTask('dist-fonts', ['copy']);

    // Full distribution task.
    grunt.registerTask('dist', [ 'copy', 'dist-css', 'dist-js' ]);

    // Default task.
    grunt.registerTask('default', [ 'install', 'dist']);

};
