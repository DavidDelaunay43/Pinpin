.. _pipeline:

Pipeline
========

.. warning::
    To ensure that Pinpin works properly, the pipeline must be respected. If a file is incorrectly renamed, Pinpin will not recognise it, or in the worst case, will not work at all.

Here is the structure of the parent directories of an ESMA Montpellier film:

* <FILM_NAME>
    * **.pinpin_data**
    * 04_asset
    * 05_sequence
    * 06_shot
    * 07_comp
    * 08_editing
    * 09_publish
    * 10_texture
    * 11_cache

When you set your project, Pinpin will copy this directory to the root of the project :

* **.pinpin_data**
    * **preview**
    * **icon**
    * **file_data.json**
    * **prefix.json**
    * **variants.json**

Assets are sorted by these categories :

* 04_asset
    * 01_character **chr** *animated character*
    * 02_prop **prp** *animated object*
    * 03_item **itm** *static object*
    * 04_enviro **env** *location, outdoor or indoor environment*
    * 05_module **mod** *assembly of items, whether in an enviro*
    * 06_diorama **drm** *assembly test scene*
    * 07_fx **fx** *reusable fx (volume, fluid, grass...)*
    * 08_camera **cam** camera rig*

For each asset, the departments are sorted by name, software and department :

* 01_character
    * <charName>
        * houdini
        * mari
        * marvelous
        * maya 
        * substance
        * zbrush 

The folder **maya** is a maya project, with these departments : modeling (geo), lookdev (ldv), rigging (rig) :

* <charName>
    * maya 
        * scenes
            * geo
            * ldv
            * rig
        * workspace.mel

Here is an example of an asset file nomenclature :

* geo
    * <PREFIX>_<assetType>_<assetName>_<department>_<step>_<increment>.<extension>
    * CDS_chr_marcel_geo_E_001.ma

* CDS : prefix corresponding to the title of the film in 3 capital letters.
* chr : abbreviation of the asset type in three lower case letters.
* marcel : asset name.
* geo : abbreviation of the department in three lower case letters.
* E : abbreviation for *Edit* because the asset is in edition.
* 001 : increment.
* .ma : file extension.