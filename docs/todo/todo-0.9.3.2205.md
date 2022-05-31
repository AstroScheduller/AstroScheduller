# AstroScheduller Todo

### Type I Todo (w/ steps in details)

 - [x] schedule_edit.item() find by index

      - [x] schedule.plot() display the index of each object on the figure

           (E.g. for "B1740-28", display "41. B1740-28" instead of simply "B1740-28". )

      - [x] schedule_edit.item() find by index

           Example:

           ```python
           schedule.item(index = 41)
           ```

 - [x] Compatible with Astropy

      - [x] Add Objects from [Astropy SkyCoords](https://docs.astropy.org/en/stable/coordinates/index.html)
        
        Example: 
        
        ```python
        schedule.add_object(
        	astropy.SkyCoord(ra=10.68458*u.degree, dec=41.26917*u.degree)
        )
        ```
        
      - [x] Add TimeObject from [Astropy Time](https://docs.astropy.org/en/stable/time/index.html)

        Example:

        ```python
        schedule.s.set_duration(
          begin = Time('2010-01-01T00:00:00', format='isot', scale='utc'), 
          end = Time('2010-01-01T12:00:00', format='isot', scale='utc'), 
          format = "astropy"
        )
        ```



### Type II Todo (w/o steps in detail & to bo discussed)

 - [x] Optimize sch.set_xxx() functions. Instead of always update all parameters, users can use the function to update one of parameter, such that: 

   ```python
   sch.set_elevation(minimal = 10, maximal = 80)
   
   # To update minimal elevation into 20 deg. 
   # In current version: 
   sch.set_elevation(minimal = 20, maximal = 80)
   # Expected in future versions:
   sch.update_elevation(minimal = 20)
   
   # Or maybe we can redesign those function as: 
   sch.set.elevation(minimal = 20, maximal = 80)
   sch.update.elevation(minimal = 20)
   sch.update.elevation(minimal = 30)
   ```

 - [-] Escape from Moon and other celestial objects. Set the default value of those objects as their angular size instead of 0. 

   ```python
   sch.set_escape(sun = 5, moon = 2)
   ```

   

 - [x] Pre-built versions of AstroSchedullerGo Module for more platforms. 

 - [ ] Documentations & Wikis

 - [ ] A User-friendly GUI
