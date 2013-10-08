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
            desktopselect2 : {
                expand : true,
                cwd : 'app/bower_components/select2/',
                src : [ '*.png', '*.gif' ],
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
                        'app/bower_components/select2/select2.js',
                        'app/bower_components/jquery-waypoints/waypoints.js',
                        'app/bower_components/jquery.lazyload/jquery.lazyload.js',
                        'app/bower_components/flot/jquery.flot.js',
                        'app/bower_components/flot/jquery.flot.pie.js',
                        'app/bower_components/excanvas/excanvas.js',
                        'app/bower_components/datatables/media/js/jquery.dataTables.js',

                        'app/bower_components/eventEmitter/EventEmitter.js',
                        'app/bower_components/eventie/eventie.js',
                        'app/bower_components/doc-ready/doc-ready.js',
                        'app/bower_components/get-style-property/get-style-property.js',
                        'app/bower_components/get-size/get-size.js',
                        'app/bower_components/jquery-bridget/jquery.bridget.js',
                        'app/bower_components/matches-selector/matches-selector.js',
                        'app/bower_components/outlayer/item.js',
                        'app/bower_components/outlayer/outlayer.js',
                        'app/bower_components/imagesloaded/imagesloaded.js',
                        'app/bower_components/masonry/masonry.js',

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
                src : [ 'js/jquery-1.9.1.js',
                        'app/bower_components/jqueryform/jquery.form.js',
                        //'app/bower_components/jquery-mobile-bower/js/jquery.mobile-1.3.2.js',
                        'js/jquery.mobile.js',
                        'app/bower_components/picturefill/picturefill.js',
                        'app/bower_components/mediaelement/build/mediaelement-and-player.js',
                        'app/bower_components/jquery-waypoints/waypoints.js',
                        'js/custom/jquery.oembed.js',
                        'js/custom/cookie_functions.js',
                        'js/custom/comments.js',
                        'js/custom/jquery.mobile.plone.js',
                        'js/theme-common.js', 'js/theme-mobile.js'],
                dest : '../mobile/js/mobile.js'
            },
            desktopcss : {
                src : [
                        'app/bower_components/mediaelement/build/mediaelementplayer.css',
                        'app/bower_components/font-awesome/css/font-awesome.css',
                        'app/bower_components/animate.css/animate.css',
                        '../desktop/app.css' ],
                dest : '../desktop/css/desktop.css'
            },
            desktopmincss : {
                src : [
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/font-awesome/css/font-awesome.min.css',
                        'app/bower_components/animate.css/animate.min.css',
                        '../desktop/app.min.css' ],
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
                        'app/bower_components/mediaelement/build/mediaelementplayer.css',
                        'app/bower_components/animate.css/animate.css',
                        '../desktop/mobile.css' ],
                dest : '../mobile/css/mobile.css'
            },
            mobilemincss : {
                src : [
                        'app/bower_components/jquery-mobile-bower/css/jquery.mobile.structure-1.3.2.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
                        'app/bower_components/animate.css/animate.min.css',
                        '../desktop/mobile.min.css' ],
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
                src : [ 'app/bower_components/select2/select2.css',
                        'app/bower_components/datatables/media/css/jquery.dataTables.css',
                        'less/desktop.plone.less',
                        'less/desktop.less',
                        'less/collective.polls.css'],
                dest : '../desktop/app.css'
            },
            desktopmin : {
                options : {
                    compile : false,
                    compress : true
                },
                src : '../desktop/app.css',
                dest : '../desktop/app.min.css'
            },
            mobileless : {
                options : {
                    compile : true,
                    compress : false
                },
                src : [ 'less/font-awesome-mobile.less',
                        'less/mobile.plone.less', 'less/mobile.less'],
                dest : '../desktop/mobile.css'
            },
            mobilemin : {
                options : {
                    compile : false,
                    compress : true
                },
                src : [ 'less/font-awesome-mobile.less',
                        'less/mobile.plone.less', 'less/mobile.less'],
                dest : '../desktop/mobile.min.css'
            },
        },

        watch : {
            recess : {
                files : [ 'less/*.less' ],
                tasks : [ 'dist-css' ]
            },
            concat : {
                files : [ 'js/*.js', 'js/custom/*.js' ],
                tasks : [ 'dist-js' ]
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

    // JS distribution task.
    grunt.registerTask('install', [ 'bower:install' ]);
    // JS distribution task.
    grunt.registerTask('dist-js', [ 'concat:desktopjs', 'concat:mobilejs',
            'uglify' ]);

    // CSS distribution task.
    grunt
            .registerTask('dist-css', [ 'recess', 'concat:desktopcss',
                    'concat:mobilecss', 'concat:mobilemincss',
                    'concat:desktopmincss' ]);

    // Fonts distribution task.
    // grunt.registerTask('dist-fonts', ['copy']);

    // Full distribution task.
    grunt.registerTask('dist', [ 'copy', 'dist-css', 'dist-js' ]);

    // Default task.
    grunt.registerTask('default', [ 'install', 'dist']);

};
