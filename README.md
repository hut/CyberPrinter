# CyberPrinter

CyberPrinter is a tool to convert image files to TransferSim programs for
spotters.

## Dependencies

*  python
* PIL library

## Example Usage

`./cyberprinter.py igem_spotter_template.png`

The output is:

```
mtp = MTP_Sys
group = Katja_2
resetWells
resetSpots
t A1   13:16,13:15 26:30,13:15 12,13:16 17:18,13:19 2:5,13:21 11,13:26 23:25,13:26 34:36,13:26 44:46,13:26 19,14:19 10,14:25 9,15:24 15:16,18:19 26:30,19:20 40,19:23 39,20:24 41,20:24 38,21:25 42,21:25 19,22:24 18,22:25 37,22:26 43,22:26 12,23:26
end



mtp = MTP_Sys
group = Katja_2
resetWells
resetSpots
t A1   17,23:26 2:5,24:26 13:16,24:26 26:30,24:26
end
```
  
which are two programs that have to be successively to produce the image with
the spotter.  The program may be used in combination with the provided IGEM.npw
file.
