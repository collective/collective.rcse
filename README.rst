Introduction
============

This is project which aim to be a complete rewrite of cyn.in.

RCSE is french acronyme for "Réseau Collaboratif et Social d'Entreprises"
which means Social and Collaborative Network of Companies.

Features
========

* Mobile first
* Collaborative editing using etherpad
* Group based workflow (a group == a workspace)
* Oembed support (consumer & provider)
* Audio repository
* Blog support
* Calendar of events
* Discussion boards
* File repository
* Image galleries
* Video libraries

* Favoriting content
* Like/dislike content
* Tag content

* Customizable dashboards on group level
* Fast, Full Text Search Engine

Technologies
============

* HTML5 + CSS3 web based user interface
* jQuery_
* `jQuery Mobile`_
* `Bootstrap 3`_
* `CKEditor 4`_
* Plone_

.. _jQuery: http://jquery.com
.. _`jQuery Mobile`: http://jquerymobile.com
.. _Plone: http://plone.org
.. _`CKEditor 4`: http://ckeditor.com
.. _`Bootstrap 3`: http://getbootstrap.com

How to install
==============

This Project should be installed using the provided buildout.

Badges
------

.. image:: https://pypip.in/v/collective.rcse/badge.png
    :target: https://crate.io/packages/collective.rcse/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/collective.rcse/badge.png
    :target: https://crate.io/packages/collective.rcse/
    :alt: Number of PyPI downloads

.. image:: https://secure.travis-ci.org/collective/collective.rcse.png
    :target: http://travis-ci.org/#!/collective/collective.rcse

.. image:: https://coveralls.io/repos/collective/collective.rcse/badge.png?branch=master
    :alt: Coverage
    :target: https://coveralls.io/r/collective/collective.rcse




Dependencies
------------


.. list-table:: RCSE Dependencies
   :widths: 10 10 10 10
   :header-rows: 1

   * - Name
     - Version
     - Tests
     - Tests Coverage
   * - cioppino.twothumbs
     - |cioppino.twothumbs.v|
     - |cioppino.twothumbs.t|
     - |cioppino.twothumbs.c|
   * - collective.etherpad
     - |collective.etherpad.v|
     - |collective.etherpad.t|
     - |collective.etherpad.c|
   * - collective.favoriting
     - |collective.favoriting.v|
     - |collective.favoriting.t|
     - |collective.favoriting.c|
   * - collective.history
     - |collective.history.v|
     - |collective.history.t|
     - |collective.history.c|
   * - collective.localrolesdatatables
     - |collective.localrolesdatatables.v|
     - |collective.localrolesdatatables.t|
     - |collective.localrolesdatatables.c|
   * - collective.mediaelementjs
     - |collective.mediaelementjs.v|
     - |collective.mediaelementjs.t|
     - |collective.mediaelementjs.c|
   * - collective.memberdatatables
     - |collective.memberdatatables.v|
     - |collective.memberdatatables.t|
     - |collective.memberdatatables.c|
   * - collective.oembed
     - |collective.oembed.v|
     - |collective.oembed.t|
     - |collective.oembed.c|
   * - collective.picturefill
     - |collective.picturefill.v|
     - |collective.picturefill.t|
     - |collective.picturefill.c|
   * - collective.polls
     - |collective.polls.v|
     - |collective.polls.t|
     - |collective.polls.c|
   * - collective.portlet.embed
     - |collective.portlet.embed.v|
     - |collective.portlet.embed.t|
     - |collective.portlet.embed.c|
   * - collective.portlet.favoriting
     - |collective.portlet.favoriting.v|
     - |collective.portlet.favoriting.t|
     - |collective.portlet.favoriting.c|
   * - collective.portlet.localusers
     - |collective.portlet.localusers.v|
     - |collective.portlet.localusers.t|
     - |collective.portlet.localusers.c|
   * - collective.portlet.oembed
     - |collective.portlet.oembed.v|
     - |collective.portlet.oembed.t|
     - |collective.portlet.oembed.c|
   * - collective.readitlater
     - |collective.readitlater.v|
     - |collective.readitlater.t|
     - |collective.readitlater.c|
   * - collective.themeswitcher
     - |collective.themeswitcher.v|
     - |collective.themeswitcher.t|
     - |collective.themeswitcher.c|
   * - collective.transcode.star
     - |collective.transcode.star.v|
     - X
     - X
   * - collective.watcherlist
     - |collective.watcherlist.v|
     - |collective.watcherlist.t|
     - |collective.watcherlist.c|
   * - collective.whathappened
     - |collective.whathappened.v|
     - |collective.whathappened.t|
     - |collective.whathappened.c|
   * - collective.z3cform.html5widgets
     - |collective.z3cform.html5widgets.v|
     - |collective.z3cform.html5widgets.t|
     - |collective.z3cform.html5widgets.c|



License
=======

The project is under GPLv2.

Credits
=======

Companies
---------

* `Planet Makina Corpus <http://www.makina-corpus.org>`_
* `Contact Makina Corpus <mailto:python@makina-corpus.org>`_

People
------

- JeanMichel FRANCOIS aka toutpt <toutpt@gmail.com>
- Gagaro <gagaro42@gmail.com>



.. |cioppino.twothumbs.v| image:: https://pypip.in/v/cioppino.twothumbs/badge.png
   :target: https://crate.io/packages/cioppino.twothumbs
.. |cioppino.twothumbs.t| image:: https://secure.travis-ci.org/collective/cioppino.twothumbs.png
   :target: http://travis-ci.org/collective/cioppino.twothumbs
.. |cioppino.twothumbs.c| image:: https://coveralls.io/repos/collective/cioppino.twothumbs/badge.png?branch=master
   :target: https://coveralls.io/r/collective/cioppino.twothumbs

.. |collective.etherpad.v| image:: https://pypip.in/v/collective.etherpad/badge.png
   :target: https://crate.io/packages/collective.etherpad
.. |collective.etherpad.t| image:: https://secure.travis-ci.org/collective/collective.etherpad.png
   :target: http://travis-ci.org/collective/collective.etherpad
.. |collective.etherpad.c| image:: https://coveralls.io/repos/collective/collective.etherpad/badge.png?branch=master
   :target: https://coveralls.io/r/collective/collective.etherpad

.. |collective.favoriting.v| image:: https://pypip.in/v/collective.favoriting/badge.png
   :target: https://crate.io/packages/collective.favoriting
.. |collective.favoriting.t| image:: https://secure.travis-ci.org/collective/collective.favoriting.png
   :target: http://travis-ci.org/collective/collective.favoriting
.. |collective.favoriting.c| image:: https://coveralls.io/repos/collective/collective.favoriting/badge.png?branch=master
   :target: https://coveralls.io/r/collective/collective.favoriting

.. |collective.history.v| image:: https://pypip.in/v/collective.history/badge.png
   :target: https://crate.io/packages/collective.history
.. |collective.history.t| image:: https://secure.travis-ci.org/collective/collective.history.png
   :target: http://travis-ci.org/collective/collective.history
.. |collective.history.c| image:: https://coveralls.io/repos/collective/collective.history/badge.png?branch=master
   :target: https://coveralls.io/r/collective/collective.history

.. |collective.localrolesdatatables.v| image:: https://pypip.in/v/collective.localrolesdatatables/badge.png
   :target: https://crate.io/packages/collective.localrolesdatatables
.. |collective.localrolesdatatables.t| image:: https://secure.travis-ci.org/collective/collective.localrolesdatatables.png
   :target: http://travis-ci.org/collective/collective.localrolesdatatables
.. |collective.localrolesdatatables.c| image:: https://coveralls.io/repos/collective/collective.localrolesdatatables/badge.png?branch=master
   :target: https://coveralls.io/r/collective/collective.localrolesdatatables

.. |collective.mediaelementjs.v| image:: https://pypip.in/v/collective.mediaelementjs/badge.png
   :target: https://crate.io/packages/collective.mediaelementjs
.. |collective.mediaelementjs.t| image:: https://secure.travis-ci.org/collective/collective.mediaelementjs.png
   :target: http://travis-ci.org/collective/collective.mediaelementjs
.. |collective.mediaelementjs.c| image:: https://coveralls.io/repos/collective/collective.mediaelementjs/badge.png?branch=master
   :target: https://coveralls.io/r/collective/collective.mediaelementjs

.. |collective.memberdatatables.v| image:: https://pypip.in/v/collective.memberdatatables/badge.png
   :target: https://crate.io/packages/collective.memberdatatables
.. |collective.memberdatatables.t| image:: https://secure.travis-ci.org/collective/collective.memberdatatables.png
   :target: http://travis-ci.org/collective/collective.memberdatatables
.. |collective.memberdatatables.c| image:: https://coveralls.io/repos/collective/collective.memberdatatables/badge.png?branch=master
   :target: https://coveralls.io/r/collective/collective.memberdatatables

.. |collective.oembed.v| image:: https://pypip.in/v/collective.oembed/badge.png
   :target: https://crate.io/packages/collective.oembed
.. |collective.oembed.t| image:: https://secure.travis-ci.org/collective/collective.oembed.png
   :target: http://travis-ci.org/collective/collective.oembed
.. |collective.oembed.c| image:: https://coveralls.io/repos/collective/collective.oembed/badge.png?branch=master
   :target: https://coveralls.io/r/collective/collective.oembed

.. |collective.picturefill.v| image:: https://pypip.in/v/collective.picturefill/badge.png
   :target: https://crate.io/packages/collective.picturefill
.. |collective.picturefill.t| image:: https://secure.travis-ci.org/collective/collective.picturefill.png
   :target: http://travis-ci.org/collective/collective.picturefill
.. |collective.picturefill.c| image:: https://coveralls.io/repos/collective/collective.picturefill/badge.png?branch=master
   :target: https://coveralls.io/r/collective/collective.picturefill

.. |collective.polls.v| image:: https://pypip.in/v/collective.polls/badge.png
   :target: https://crate.io/packages/collective.polls
.. |collective.polls.t| image:: https://secure.travis-ci.org/collective/collective.polls.png
   :target: http://travis-ci.org/collective/collective.polls
.. |collective.polls.c| image:: https://coveralls.io/repos/collective/collective.polls/badge.png?branch=master
   :target: https://coveralls.io/r/collective/collective.polls

.. |collective.portlet.embed.v| image:: https://pypip.in/v/collective.portlet.embed/badge.png
   :target: https://crate.io/packages/collective.portlet.embed
.. |collective.portlet.embed.t| image:: https://secure.travis-ci.org/collective/collective.portlet.embed.png
   :target: http://travis-ci.org/collective/collective.portlet.embed
.. |collective.portlet.embed.c| image:: https://coveralls.io/repos/collective/collective.portlet.embed/badge.png?branch=master
   :target: https://coveralls.io/r/collective/collective.portlet.embed

.. |collective.portlet.favoriting.v| image:: https://pypip.in/v/collective.portlet.favoriting/badge.png
   :target: https://crate.io/packages/collective.portlet.favoriting
.. |collective.portlet.favoriting.t| image:: https://secure.travis-ci.org/collective/collective.portlet.favoriting.png
   :target: http://travis-ci.org/collective/collective.portlet.favoriting
.. |collective.portlet.favoriting.c| image:: https://coveralls.io/repos/collective/collective.portlet.favoriting/badge.png?branch=master
   :target: https://coveralls.io/r/collective/collective.portlet.favoriting

.. |collective.portlet.localusers.v| image:: https://pypip.in/v/collective.portlet.localusers/badge.png
   :target: https://crate.io/packages/collective.portlet.localusers
.. |collective.portlet.localusers.t| image:: https://secure.travis-ci.org/collective/collective.portlet.localusers.png
   :target: http://travis-ci.org/collective/collective.portlet.localusers
.. |collective.portlet.localusers.c| image:: https://coveralls.io/repos/collective/collective.portlet.localusers/badge.png?branch=master
   :target: https://coveralls.io/r/collective/collective.portlet.localusers

.. |collective.portlet.oembed.v| image:: https://pypip.in/v/collective.portlet.oembed/badge.png
   :target: https://crate.io/packages/collective.portlet.oembed
.. |collective.portlet.oembed.t| image:: https://secure.travis-ci.org/collective/collective.portlet.oembed.png
   :target: http://travis-ci.org/collective/collective.portlet.oembed
.. |collective.portlet.oembed.c| image:: https://coveralls.io/repos/collective/collective.portlet.oembed/badge.png?branch=master
   :target: https://coveralls.io/r/collective/collective.portlet.oembed

.. |collective.readitlater.v| image:: https://pypip.in/v/collective.readitlater/badge.png
   :target: https://crate.io/packages/collective.readitlater
.. |collective.readitlater.t| image:: https://secure.travis-ci.org/collective/collective.readitlater.png
   :target: http://travis-ci.org/collective/collective.readitlater
.. |collective.readitlater.c| image:: https://coveralls.io/repos/collective/collective.readitlater/badge.png?branch=master
   :target: https://coveralls.io/r/collective/collective.readitlater

.. |collective.themeswitcher.v| image:: https://pypip.in/v/collective.themeswitcher/badge.png
   :target: https://crate.io/packages/collective.themeswitcher
.. |collective.themeswitcher.t| image:: https://secure.travis-ci.org/collective/collective.themeswitcher.png
   :target: http://travis-ci.org/collective/collective.themeswitcher
.. |collective.themeswitcher.c| image:: https://coveralls.io/repos/collective/collective.themeswitcher/badge.png?branch=master
   :target: https://coveralls.io/r/collective/collective.themeswitcher

.. |collective.transcode.star.v| image:: https://pypip.in/v/collective.transcode.star/badge.png
   :target: https://crate.io/packages/collective.transcode.star

.. |collective.watcherlist.v| image:: https://pypip.in/v/collective.watcherlist/badge.png
   :target: https://crate.io/packages/collective.watcherlist
.. |collective.watcherlist.t| image:: https://secure.travis-ci.org/collective/collective.watcherlist.png
   :target: http://travis-ci.org/collective/collective.watcherlist
.. |collective.watcherlist.c| image:: https://coveralls.io/repos/collective/collective.watcherlist/badge.png?branch=master
   :target: https://coveralls.io/r/collective/collective.watcherlist

.. |collective.whathappened.v| image:: https://pypip.in/v/collective.whathappened/badge.png
   :target: https://crate.io/packages/collective.whathappened
.. |collective.whathappened.t| image:: https://secure.travis-ci.org/collective/collective.whathappened.png
   :target: http://travis-ci.org/collective/collective.whathappened
.. |collective.whathappened.c| image:: https://coveralls.io/repos/collective/collective.whathappened/badge.png?branch=master
   :target: https://coveralls.io/r/collective/collective.whathappened

.. |collective.z3cform.html5widgets.v| image:: https://pypip.in/v/collective.z3cform.html5widgets/badge.png
   :target: https://crate.io/packages/collective.z3cform.html5widgets
.. |collective.z3cform.html5widgets.t| image:: https://secure.travis-ci.org/collective/collective.z3cform.html5widgets.png
   :target: http://travis-ci.org/collective/collective.z3cform.html5widgets
.. |collective.z3cform.html5widgets.c| image:: https://coveralls.io/repos/collective/collective.z3cform.html5widgets/badge.png?branch=master
   :target: https://coveralls.io/r/collective/collective.z3cform.html5widgets
