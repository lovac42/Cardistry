# Cardistry: Dynamically Add New Cards

## About:
This addon adjusts how many new card will be dealt out during review depending on the current outstanding number of young and learning cards in a given deck. It will increase or decrease the daily limit as cards matures or lapses. This ensures that a user will not be juggling more than (n) amount of young/learning cards in a given period.


Please note that parent's new card limit must be larger than child's subdeck limit as Anki enforces parent deck limits first.


## Configs:
Enable using deck menu options.  

<img src="https://github.com/lovac42/Cardistry/blob/master/screenshots/deckmenu.png?raw=true">

<img src="https://github.com/lovac42/Cardistry/blob/master/screenshots/forecast.png?raw=true">


## Bug warnings:
On later version of Anki ~2.1.33, you may get a warning: `bug: fillNew()`. This is not a bug. You are receiving this warning because this addon cutoff and prevented the reviewer from doing any more cards. There isn't an easy way to prevent or change this warning message... Given how Anki is coded...
