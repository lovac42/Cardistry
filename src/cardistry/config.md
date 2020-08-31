# Cardistry
Dynamically Adjust New Cards

## matured_ivl:
All intervals below this value is a young card.  
A good number to set is 21 or 100.  
Set to 9999 to remove limit.

## scan_days:
Days to scan ahead.  
Using a multiple of 5x or 10x would make the calculations easier.  
Set to 9999 to remove limit.

## scan_ease:
All ease values equal to or below this value will be counted as difficult.  
Default starting ease is set to 2500.  
Set to 9999 to remove limit.

## inc_filtered_decks:
true or false (lower cased letters).  
Cards moved to a filtered deck uses different id's and will screw the calculations.
