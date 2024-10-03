.. _pipeline:

Pipeline
========

.. warning::
    Pour que Pinpin fonctionne correctement, le pipeline doit être respecté. Si un fichier est mal renommé, Pinpin ne le reconnaîtra pas ou, dans le pire des cas, ne fonctionnera pas du tout.

Voici la structure des répertoires parents d'un film ESMA Montpellier :

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

Lorsque vous créez votre projet, Pinpin copie ce répertoire **.pinpin_data** à la racine du projet :

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

Les assets sont classés selon ces catégories :

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

Pour chaque asset, les dossiers sont classés par nom, par logiciel et par département :

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

Par exemple, le dossier **maya** est un projet maya, avec ces départements : modeling (geo), lookdev (ldv), rigging (rig) :

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

Voici un exemple de nomenclature d'un fichier d'asset :

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

* CDS : préfixe correspondant au titre du film en 3 lettres majuscules.
* chr : abréviation du type d'asset en trois lettres minuscules.
* marcel : nom de l'asset.
* geo : abréviation du département en trois lettres minuscules.
* E : abréviation de *Edit* parce que l'asset est en édition.
* 001 : incrément.
* .ma : extension de fichier.

------------

Sequence
--------

Voici un exemple de nomenclature de fichier de séquence :

* CDS_seq010_masterLayout_E_001.ma

------------

Shot
----

Voici un exemple de nomenclature de shot :

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
    Un fichier publié ne doit pas contenir de références.
    Pinpin publie automatiquement un asset en important les références.

.. tip::
    Avant de publier un asset, assurez-vous que vous avez supprimé tous les namespaces inutiles.

Le répertoire publish est divisé en plusieurs répertoires :

.. list-table::

   * - **asset**
   * - **sequence**
   * - **shot**

Asset publish
^^^^^^^^^^^^^

Le répertoire des assets publiés est divisé en plusieurs répertoires :

.. list-table::

   * - **01_character**
   * - **02_prop**
   * - **03_item**
   * - **04_enviro**
   * - **05_module**
   * - **06_diorama**
   * - **07_fx**
   * - **08_camera**

Chaque répertoire de type d'asset est divisé en plusieurs répertoires :

.. list-table::

   * - **clo** 
   * - **geo**
   * - **grm**
   * - **ldv** 
   * - **rig**

Voici un exemple d'arborescence de fichiers publiés :

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

Voici un exemple de nomenclature d'un fichier de cache :

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

Voici un exemple de nomenclature de séquence de fichiers de cache :

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

Voici un exemple de hiérarchie de fichiers de cache pour une prise de vue :

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