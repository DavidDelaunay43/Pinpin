.. _pipeline:
Pipeline
========

.. warning::
    To ensure that Pinpin works properly, the pipeline must be respected. If a file is incorrectly renamed, Pinpin will not recognise it, or in the worst case, will not work at all.

Here is the structure of the parent directories of an ESMA Montpellier film:

* <filmName>
    * **.pinpin_data**
        * **preview**
        * **file_data.json**
        * **prefix.json**
        * **variants.json**
    * 04_asset
        * 01_character
        * 02_prop
        * 03_item
        * 04_enviro
        * 05_module
        * 06_diorama
        * 07_fx
        * 08_camera
    * 05_sequence
    * 06_shot
    * 07_comp
    * 08_editing
    * 09_publish
        * asset 
            * 01_character
                * geo 
                * ldv 
                * rig 
                * cloth
            * 02_prop
                * geo 
                * ldv 
                * rig 
                * cloth
            * 03_item
                * geo 
                * ldv 
            * 04_enviro
                * geo 
                * ldv 
            * 05_module
                * ldv
            * 06_diorama
            * 07_fx
            * 08_camera
                * rig
        * sequence 
        * shot
    * 10_texture
    * 11_cache
