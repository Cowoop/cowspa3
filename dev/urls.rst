Scheme
======
/<otype>/#[<id>/]<action>[/<section>]

Member
======

::

    (+) Works with sugarskull and flask
    (-) Bigger page and slightly complex search/other sections
    (+) Simple/RESTish URLs

- /members/#new [ member.new ]
- /members/#22 [ member.info(22) ]
- /members/#22/edit/contact [ member.update(22, ..) ]
- /members/#me 

Location
========
- /bizplaces/ [List all the Locations]
- /bizplaces/#4 [Show details of Location with ID 4]
- /bizplaces/#4/edit/
- /bizplaces/new
- /bizplaces/#4/tariffs/

Tariffs
=======
- /tariffs/ [ list of tariffs ] # context-specific
- /tariffs/#24/
- /tariffs/#24/edit/

Other options considered
========================
Scheme used for 0.3
-------------------

::

    (+) Works with sugarskull and flask  (current scheme)
    (-) Ugly bugprone URLs

- /members/new [ member.new ]
- /members/edit/#22 [ member.info(22) ]
- /members/edit/#22/edit/contact [ member.update(22, ..) ]

More RESTlike Option
--------------------
::

    (-) Does not work with sugarskull and flask
    (+) Simple/More RESTish URLs

- /members/new [ member.new ]
- /members/22 [ member.info(22) ]
- /members/22/edit/contact [ member.update(22, ..) ]
