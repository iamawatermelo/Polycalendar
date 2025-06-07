<h1>
    <picture height="64">
        <source
            srcset="polycalendar-light.svg"
            media="(prefers-color-scheme: dark)"
        />
        <source
            srcset="polycalendar-dark.svg"
            media="(prefers-color-scheme: light), (prefers-color-scheme: no-preference)"
        />
        <img src="polycalendar-dark.svg" height="64" alt="Trusty logo" />
    </picture>
</h1>

Polycalendar is a calendar tool to synthesise, publish and view multiple
different calendars.

## How do I use it?

Write a config file:

```kdl
// file.kdl

calendar "public" {
    source "https://calendar.google.com/calendar/ical/me%40polycalendar.srh.dog/public/basic.ics" { 
        transform "polycalendar/filter" {
            include "name"
            include "location"
            
            set "color" value="turquoise"
        }
    }
    
    source "https://calendar.google.com/calendar/ical/work%40polycalendar.srh.dog/public/basic.ics" {
        transform "polycalendar/redact" {
            description "Busy"
            padding (minutes)10
            delete_overlaps true
        }
        
        transform "polycalendar/filter" {
            set "color" value="red"
        }
    }
    
    transform "polycalendar/truncate" {
        beginning date="now"
        end date="now" offset=(weeks)4
    }
}
```

> [!NOTE]
> Due to a downstream bug with the configuration language, each source
> must have at least one transformation and each source must have
> one configuration entry.
> 
> You can use `polycalendar/null` for now.
> ```
> transformation "polycalendar/null" dummy=0
> ```

Run:

```
polycalendar serve file.kdl
```

to run a web server, or

```
polycalendar execute file.kdl
```

to build your calendar and assemble it into an ICS file.