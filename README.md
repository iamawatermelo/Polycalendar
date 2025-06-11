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

![An image showing how Polycalendar has combined two calendars](/demo.png)

## How do I use it?

Install Polycalendar:

```sh
pip install git+https://github.com/iamawatermelo/Polycalendar
```

Write a config file (but with your own ICS files):

> [!TIP]
> You can use something like `file:///home/sarah/Downloads/basic.ics` to
> reference something on your drive.

```kdl
// file.kdl

calendar "public" {
    source "https://calendar.google.com/calendar/ical/me%40polycalendar.srh.dog/public/basic.ics" { 
        transform "polycalendar/null" dummy=0
    }
    
    source "https://calendar.google.com/calendar/ical/work%40polycalendar.srh.dog/public/basic.ics" {
        transform "polycalendar/null" dummy=0
    }
    
    transform "polycalendar/null" dummy=0
}
```

> [!NOTE]
> Due to a downstream bug with the configuration language, each source
> must have at least one transformation and each source must have
> one configuration entry.
> 
> You can use `polycalendar/null` for now.
> ```
> transform "polycalendar/null" dummy=0
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