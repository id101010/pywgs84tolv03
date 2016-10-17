# pywgs84tolv03 converter script

This is a github mirror for the swisstopo ch1903 converter script written by me. You can find the script and ports to several other languages at: 

https://www.swisstopo.admin.ch/internet/swisstopo/en/home/products/software/products/skripts.html

It seems like the above site is (temporary?) not available anymore. 


## Example use

```python
''' Example usage for the GPSConverter class.'''

converter = GPSConverter()

# Coordinates
wgs84 = [46.95108, 7.438637, 0]
lv03  = []

# Convert WGS84 to LV03 coordinates
lv03 = converter.WGS84toLV03(wgs84[0], wgs84[1], wgs84[2])

print "WGS84: "
print wgs84
print "LV03: "
print lv03
```
