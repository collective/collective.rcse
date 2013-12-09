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
                src : [ '*.js', 'lang/**', 'plugins/**', 'skins/**'],
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
                        'app/bower_components/animate.css/animate.css',
                        '../desktop/css/app.css' ],
                dest : '../desktop/css/desktop.css'
            },
            desktopmincss : {
                src : [
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/font-awesome/css/font-awesome.min.css',
                        'app/bower_components/animate.css/animate.min.css',
                        '../desktop/css/app.min.css' ],
                dest : '../desktop/css/desktop.min.css'
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
                        'app/bower_components/animate.css/animate.css',
                        '../mobile/css/app.css' ],
                dest : '../mobile/css/mobile.css'
            },
            mobilemincss : {
                src : [
                       'app/bower_components/jquery-mobile-bower/css/jquery.mobile.structure-1.3.2.min.css',
                       'app/bower_components/jquery-mobile-bower/css/jquery.mobile.theme-1.3.2.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/animate.css/animate.min.css',
                        '../mobile/app.min.css' ],
                dest : '../mobile/css/mobile.min.css'
            }
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
                    compile : true,
                    compress : false
                },
                src : [ 'app/bower_components/chosen/chosen.css',
                        'app/bower_components/datatables/media/css/jquery.dataTables.css',
                        'app/bower_components/bootstrap/dist/css/bootstrap.css',
                        'app/bower_components/bootstrap/dist/css/bootstrap-theme.css',
                        'less/desktop.less',
                        'less/collective.polls.css'],
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
        },

        watch : {
            desktoprecess : {
                files : [
                         'less/desktop.plone.less',
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
    grunt.registerTask('desktop-dist-css', [ 'recess:desktopless', 'concat:desktopcss' ]);
    grunt.registerTask('mobile-dist-css', [ 'recess:mobileless', 'concat:mobilecss' ]);
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
