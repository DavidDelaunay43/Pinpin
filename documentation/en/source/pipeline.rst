.. _pipeline:

Pipeline
========

.. warning::
    To ensure that Pinpin works properly, the pipeline must be respected. If a file is incorrectly renamed, Pinpin will not recognise it, or in the worst case, will not work at all.

Here is the structure of the parent directories of an ESMA Montpellier film:

.. list-table::

    * - **.pinpin_data**
    * - **00_managment**
    * - **01_externalData**
    * - **02_ressources**
    * - **03_preprod**
    * - **04_asset**
    * - **05_sequence**
    * - **06_shot**
    * - **07_comp**
    * - **08_editing**
    * - **09_publish**
    * - **10_texture**
    * - **11_cache**
    * - **12_test**
    * - **13_jury**
    * - **14_com**

When you set your project, Pinpin will copy this directory **.pinpin_data** to the root of the project:

.. list-table::

    * - **preview**
      - contains png thumbnails of files
    * - **icons**
      - contains asset icons (optionnal)
    * - file_data.json
      - comments associated with the files 
    * - prefix.json
      - prefix of the project (optionnal)
    * - variants.json
      - variants for publish asset (optionnal)

------------

Asset
-----

Assets are sorted by these categories:

.. list-table::
   :header-rows: 1

   * - Asset type
     - Abbreviation
     - Description
   * - 01_character
     - **chr**
     - *animated character*
   * - 02_prop
     - **prp**
     - *animated object*
   * - 03_item
     - **itm**
     - *static object*
   * - 04_enviro
     - **env**
     - *location, outdoor or indoor environment*
   * - 05_module
     - **mod**
     - *assembly of items, whether in an enviro*
   * - 06_diorama
     - **drm**
     - *assembly test scene*
   * - 07_fx
     - **fx**
     - *reusable fx (volume, fluid, grass...)*
   * - 08_camera
     - **cam**
     - *camera rig*

For each asset, the folders are sorted by name, software and department:

.. list-table::
    :header-rows: 1

    * - Asset type
      - Asset name
      - Software project
    * - **01_character**
      - **marcel**
      - **houdini**
    * - 
      - 
      - **mari**
    * - 
      - 
      - **marvelous**
    * - 
      - 
      - **maya**
    * - 
      - 
      - **substance**
    * - 
      - 
      - **zbrush**

For example, the folder **maya** is a maya project, with these departments : modeling (geo), lookdev (ldv), rigging (rig):

.. list-table::
    :header-rows: 1

    * - Asset name
      - Software project
      - Software folder
      - Department
    * - **marcel**
      - **maya**
      - **scenes**
      - **geo**
    * - 
      - 
      - 
      - **ldv**
    * - 
      - 
      - 
      - **rig**
    * - 
      - 
      - workspace.mel
      - 

Here is an example of an asset file nomenclature:

* CDS_chr_marcel_geo_E_001.ma

.. list-table:: 
   :header-rows: 1

   * - PREFIX
     - assetType
     - assetName
     - department
     - step
     - increment
     - extension
   * - CDS
     - chr
     - marcel
     - geo
     - E
     - 001
     - .ma
   * - CDS
     - chr
     - marcelBob
     - geoLo
     - E
     - 004
     - .ma

* CDS : prefix corresponding to the title of the film in 3 capital letters.
* chr : abbreviation of the asset type in three lower case letters.
* marcel : asset name.
* geo : abbreviation of the department in three lower case letters.
* E : abbreviation for *Edit* because the asset is in edition.
* 001 : increment.
* .ma : file extension.

------------

Sequence
--------

Here is an example of a sequence file nomenclature:

* CDS_seq010_masterLayout_E_001.ma

------------

Shot
----

Here is an example of a shot file nomenclature:

* CDS_seq010_sh010_anim_E_001.ma

.. list-table:: 
   :header-rows: 1

   * - PREFIX
     - sequenceNum
     - shotNum
     - department
     - step
     - increment
     - extension
   * - CDS
     - seq010
     - sh010
     - anim
     - E
     - 001
     - .ma
   * - CDS
     - seq010
     - sh010
     - confo
     - E
     - 001
     - .ma
   * - CDS
     - seq010
     - sh010
     - cloth
     - E
     - 001
     - .ma
   * - CDS
     - seq010
     - sh010
     - fx
     - E
     - 001
     - .ma
   * - CDS
     - seq010
     - sh010
     - layout
     - E
     - 001
     - .ma
   * - CDS
     - seq010
     - sh010
     - lighting
     - E
     - 001
     - .ma
   * - CDS
     - seq010
     - sh010
     - render
     - E
     - 001
     - .ma

------------

Publish
-------

.. important::
    A published file must not contain any references.
    Pinpin automatically publishes an asset by importing the references.

.. tip::
    Before publishing an asset, make sure you have removed any unnecessary namespaces.

The publish directory is divided into these directories:

.. list-table::

   * - **asset**
   * - **sequence**
   * - **shot**

Asset publish
^^^^^^^^^^^^^

The asset publish directory is divided into these directories:

.. list-table::

   * - **01_character**
   * - **02_prop**
   * - **03_item**
   * - **04_enviro**
   * - **05_module**
   * - **06_diorama**
   * - **07_fx**
   * - **08_camera**

Each asset type directory is divided in to these directories:

.. list-table::

   * - **clo** 
   * - **geo**
   * - **grm**
   * - **ldv** 
   * - **rig**

Here is an example of a published file tree:

.. list-table:: 
   :header-rows: 1

   * - department directory
     - publish file
     - old publish file
    
   * - **geo**
     - CDS_chr_chauvesouris_geo_P.ma
     - 
   * - 
     - CDS_chr_marcel_geo_P.ma
     - 
   * - 
     - CDS_chr_marcelBob_geo_P.ma
     - 
   * - 
     - CDS_chr_petru_geo_P.ma
     -
   * - 
     - **OLD**
     - CDS_chr_chauvesouris_geo_P_001.ma
   * - 
     - 
     - CDS_chr_chauvesouris_geo_P_002.ma
   * - 
     - 
     - CDS_chr_marcel_geo_P_001.ma
   * - 
     - 
     - CDS_chr_marcelBob_geo_P_001.ma
   * - 
     - 
     - CDS_chr_petru_geo_P_001.ma
   
   * - **ldv**
     - CDS_chr_chauvesouris_ldv_P.ma
     -
   * -
     - CDS_chr_marcel_ldv_P.ma
     -
   * -
     - CDS_chr_marcelBob_ldv_P.ma
     -
   * -
     - CDS_chr_petru_ldv_P.ma
     -
   * - 
     - **OLD**
     - 
   
   * - **rig**
     - CDS_chr_chauvesouris_rig_P.ma
     -
   * -
     - CDS_chr_marcel_rig_P.ma
     -
   * -
     - CDS_chr_marcelBob_rig_P.ma
     -
   * -
     - CDS_chr_petru_rig_P.ma
     -
   * - 
     - **OLD**
     - 

-----

Cache
-----

Here is an example of a cache file nomenclature:

* CDS_seq020_sh030_marcel_anim.abc
* CDS_seq020_sh030_bottle_anim.abc

.. list-table:: 
   :header-rows: 1

   * - PREFIX
     - sequenceNum
     - shotNum
     - character | prop
     - department
     - extension
   * - CDS
     - seq020
     - sh030
     - marcel
     - anim
     - .abc
   * - CDS
     - seq020
     - sh030
     - bottle
     - anim
     - .abc 

Here is an example of a cache file sequence nomenclature:

* CDS_seq020_sh030_smoke_fx.1001.vdb
* CDS_seq020_sh030_smoke_fx.1002.vdb
* CDS_seq020_sh030_smoke_fx.1003.vdb
* CDS_seq020_sh030_smoke_fx.1004.vdb

.. list-table:: 
   :header-rows: 1

   * - PREFIX
     - sequenceNum
     - shotNum
     - effect
     - department (fx)
     - frame number
     - extension
   * - CDS
     - seq020
     - sh030
     - smoke
     - fx
     - 1001
     - .vdb
   * - CDS
     - seq020
     - sh030
     - smoke
     - fx
     - 1002
     - .vdb
   * - CDS
     - seq020
     - sh030
     - smoke
     - fx
     - 1003
     - .vdb
   * - CDS
     - seq020
     - sh030
     - smoke
     - fx
     - 1004
     - .vdb

Here is an example of a cache file hierarchy for a shot:

.. list-table:: 
   :header-rows: 1

   * - **cache directory**
     - **sequence directory**
     - **shot directory**
     - cache file | **folder**
     - sequence cache file
   * - **11_cache**
     - **seq020**
     - **sh030**
     - CDS_seq020_sh030_bottle_anim.abc
     -
   * - 
     - 
     - 
     - CDS_seq020_sh030_marcel_anim.abc
     -  
   * - 
     - 
     - 
     - **CDS_seq020_sh030_smoke_fx**
     - CDS_seq020_sh030_smoke_fx.1001.vdb
   * - 
     - 
     - 
     -
     - CDS_seq020_sh030_smoke_fx.1002.vdb
   * - 
     - 
     - 
     -
     - CDS_seq020_sh030_smoke_fx.1003.vdb
   * - 
     - 
     - 
     -
     - CDS_seq020_sh030_smoke_fx.1004.vdb