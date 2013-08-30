/* jshint node: true */

module.exports = function(grunt) {
  "use strict";

  // Project configuration.
  grunt.initConfig({

    // Metadata.
    pkg: grunt.file.readJSON('package.json'),
    banner: '/**\n' +
              '* RCSE theme by Makina-Corpus\n' +
              '*/\n',

    // Task configuration.
    copy: {
        desktopfont: {expand: true,
            cwd: 'app/bower_components/font-awesome/',
            src:['font/**',],
            dest: '../desktop/'},
	    mobilefont: {expand: true,
	        cwd: 'app/bower_components/font-awesome/',
	        src:['font/**',],
	        dest: '../mobile/'}
    },
    concat: {
      options: {
        banner: '<%= banner %>',
        stripBanners: false
      },
      desktopjs: {
        src: [
          'app/bower_components/jquery/jquery.js',
          'app/bower_components/bootstrap/dist/js/bootstrap.js',
          'app/bower_components/picturefill/picturefill.js',
          'js/custom/jquery.oembed.js',
          'js/custom/comments.js',
	  'js/custom/cookie_functions.js',
          'js/theme-common.js',
          'js/theme-desktop.js'],
        dest: '../desktop/js/desktop.js'
      },
      mobilejs: {
       src: [
          'app/bower_components/jquery/jquery.js',
          'app/bower_components/jquery-mobile-bower/js/jquery.mobile-1.3.2.js',
          'app/bower_components/picturefill/picturefill.js',
          'js/custom/jquery.oembed.js',
          'js/custom/comments.js',
	  'js/custom/cookie_functions.js',
          'js/custom/jquery.mobile.plone.js',
          'js/theme-common.js',
          'js/theme-mobile.js'],
         dest: '../mobile/js/mobile.js'
      },
      desktopcss:{
    	  src: ['app/bower_components/bootstrap/dist/css/bootstrap.min.css',
    	        'app/bower_components/bootstrap/dist/css/bootstrap-theme.min.css',
    	        'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
    	        'app/bower_components/font-awesome/css/font-awesome.min.css',
    	        'less/desktop.min.css'],
    	  dest: '../desktop/css/desktop.min.css'
      },
      mobilecss: {
    	  src: [
			'app/bower_components/jquery-mobile-bower/css/jquery.mobile.structure-1.3.2.min.css',
			'app/bower_components/jquery-mobile-bower/css/jquery.mobile.theme-1.3.2.min.css',
			'app/bower_components/mediaelement/build/mediaelementplayer.min.css',
			'less/mobile.min.css'],
	        dest: '../mobile/css/mobile.min.css'
      }
    },

    uglify: {
      desktopjs: {
	      options: {
	            compress: true
	        },
          src: ['../desktop/js/desktop.js'],
          dest: '../desktop/js/desktop.min.js'
      },
      mobilejs: {
	      options: {
	            compress: true
	        },
          src: ['../mobile/js/mobile.js'],
          dest: '../mobile/js/mobile.min.js'
      }
    },

    recess: {
      desktopless: {
	      options: {
	        compile: true, compress: true
	      },
          src: ['less/desktop.plone.less',
                'less/desktop.less'],
          dest: 'less/desktop.min.css'
      },
      mobileless: {
	      options: {
	        compile: true, compress: true
	      },
          src: ['less/font-awesome-mobile.less',
                'less/mobile.plone.less',
                'less/mobile.less'],
          dest: 'less/mobile.min.css'
      },
    },

    watch: {
      recess: {
        files: ['less/*.less'],
        tasks: ['dist-css']
      },
      concat: {
        files: ['js/*.js'],
        tasks: ['dist-js']
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

  // JS distribution task.
  grunt.registerTask('dist-js', ['concat:desktopjs', 'concat:mobilejs', 'uglify']);

  // CSS distribution task.
  grunt.registerTask('dist-css', ['recess', 'concat:desktopcss', 'concat:mobilecss']);

  // Fonts distribution task.
//  grunt.registerTask('dist-fonts', ['copy']);

  // Full distribution task.
  grunt.registerTask('dist', ['copy', 'dist-css', 'dist-js']);

  // Default task.
  grunt.registerTask('default', ['dist']);

};