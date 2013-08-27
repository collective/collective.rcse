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
    clean: {
      dist: ['dist']
    },

    concat: {
      options: {
        banner: '<%= banner %>',
        stripBanners: false
      },
      bootstrap: {
        src: [
          'js/jquery.js',
          'js/jquery.oembed.js',
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
          'js/theme.js'
        ],
        dest: '../desktop/theme.js'
      }
    },

    uglify: {
      options: {
            compress: true
        },
        build: {
          src: ['../desktop/theme.js'],
          dest: '../desktop/theme.min.js'
      }
    },

    recess: {
      options: {
        compile: true
      },
      min: {
        options: {
          compress: true
        },
        src: ['less/theme.less', 'fontawesome/less/font-awesome.less'],
        dest: '../desktop/theme.min.css'
      },
    },

    watch: {
      recess: {
        files: 'less/*.less',
        tasks: ['recess']
      },
      concat: {
        files: 'js/*.js',
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