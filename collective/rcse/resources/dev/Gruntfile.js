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
    concat: {
      options: {
        banner: '<%= banner %>',
        stripBanners: false
      },
      desktop: {
        src: [
          'js/jquery.js',
          'js/jquery.oembed.js',
          'js/comments.js',
          'js/picturefill.min.js',
          'bootstrap/js/transition.js',
          'bootstrap/js/alert.js',
          'bootstrap/js/button.js',
          'bootstrap/js/carousel.js',
          'bootstrap/js/collapse.js',
          'bootstrap/js/dropdown.js',
          'bootstrap/js/modal.js',
          'bootstrap/js/tooltip.js',
          'bootstrap/js/popover.js',
          'bootstrap/js/scrollspy.js',
          'bootstrap/js/tab.js',
          'bootstrap/js/affix.js',
          'js/theme-common.js',
          'js/theme-desktop.js'
        ],
        dest: '../desktop/theme-desktop.js'
      },
      mobile: {
       src: [
    	  'js/jquery.js',
          'js/jquery.oembed.js',
          'js/comments.js',
          'js/picturefill.min.js',
          'jquerymobile/jquery.mobile.js',
          'js/jquery.mobile.plone.js',
          'js/theme-common.js',
          'js/theme-mobile.js'
         ],
         dest: '../mobile/theme-mobile.js'
      }
    },

    uglify: {
      desktop: {
	      options: {
	            compress: true
	        },
          src: ['../desktop/theme-desktop.js'],
          dest: '../desktop/theme-desktop.min.js'
      },
      mobile: {
	      options: {
	            compress: true
	        },
          src: ['../mobile/theme-mobile.js'],
          dest: '../mobile/theme-mobile.min.js'
      }
    },

    recess: {
      desktop: {
	      options: {
	        compile: true//, compress: true
	      },
          src: ['bootstrap/less/bootstrap.less',
                'fontawesome/less/font-awesome.less',
                'less/desktop.plone.less',
                'less/desktop.less'],
          dest: '../desktop/theme-desktop.min.css'
      },
      mobile: {
	      options: {
	        compile: true, compress: true
	      },
          src: ['jquerymobile/jquery.mobile.structure.less',
                'jquerymobile/theme/jquery.mobile.theme.min.less',
                'fontawesome/less/font-awesome-mobile.less',
                'less/mobile.plone.less',
                'less/mobile.less'],
          dest: '../mobile/theme-mobile.min.css'
      }
    },

    watch: {
      recess: {
        files: ['less/*.less', 'libs/less/*.less'],
        tasks: ['recess']
      },
      concat: {
        files: ['js/*.js', 'libs/js/*.js'],
        tasks: ['concat', 'uglify']
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
  grunt.registerTask('dist-js', ['concat', 'uglify']);

  // CSS distribution task.
  grunt.registerTask('dist-css', ['recess']);

  // Fonts distribution task.
//  grunt.registerTask('dist-fonts', ['copy']);

  // Full distribution task.
  grunt.registerTask('dist', ['dist-css', 'dist-js']);

  // Default task.
  grunt.registerTask('default', ['dist']);

};