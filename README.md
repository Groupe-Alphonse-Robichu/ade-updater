# ade-updater

## How to install

Simply `git clone` this repository, `cd` at the root of the repository and install the requirements :
```
$ pip3 install -r requirements.txt
```

Make sure your version of Python is 3.6 or above.

## How to use

```
$ ./updateAde -h
usage : ./updateAde.py --createGroup <group_name>
        ./updateAde.py --createCal <group_name> <cal_name>
        ./updateAde.py [-n] --update
        ./updateAde.py [-n] --all
        ./updateAde.py [-n] --remaining
```

First, you need to create a calendar group :
```
./updateAde.py --createGroup MyGroup
```

Then, you add at least one calendar in this group :
```
./updateAde.py --createCal MyGroup MyCal
```

Once this is done,  you can proceed to the configration of the calendar(s) via the `live.json` file :
```
{
    "MyGroup": {
		"source": "MySource",
		"project_id": "22",
		"resources": [1, 2, 3],
		"dest_folder": "/tmp/ade",
		"start": "2022-01-28",
		"limit": "2022-06-10",
		"alert": "https/discord.com/api/webhooks/...",
		"ignore": [],
		"translate": {},
		"calendars": {
            "MyCal" : {
		        "resources": [4],
		        "notify": "https/discord.com/api/webhooks/...",
		        "update": "never",
		        "week": ""
            }
        }
    }
}
```

The `source` refers to an entry in `sources.json`, being a template URL with the fields `{project}`, `{resources}`, `{start}` and `{end}` to be completed by the script.

You can find the `project_id` and the `resources` in your ADE by selecting Export > Generate URL. Note that resources can be defined at the calendar level or at the group level, in which case they will be shared by all calendars of this group.

The `start` and `limit` dates are very important, they define the date at which the interesting events in the calendar begin and the date at which they stop. The group will be archived when the `limit` date is reached.

The `translate` and `ignore` collections are empty for now. The first will fill when you fetch data, the names provided by the ADE will be the keys of the object and the values will be `null` by default. Change it to something else to change the name of every event with this name. The `ignore` field is a list of names of events you want to ignore (translation doesn't apply here, these must be the original names provided by the ADE).

It is then recommanded to run the script with the `--all` argument to discover as many event names as possible. It will fetch all the events from the beginning of the calendar to the expiry date. Every time the script is run and at least one unergistered event name is discovered, it will send a message on the `alert` Discord webhook. You can use the `-n` option to prevent the script from using the Discord webhook but print additional info in the console.

You can then setup a crontab to run the script every day or so with the `--update` option. On every saturday it will fetch the calendar for the next week, and each time you call it again during the week it will check if events have been added, deleted or modified. 
```cron
1 0 * * * /path/to/script/updateAde.py --update
```

You can also run the script with the `--remaining` option to see all the events remaining before the end of the calendar.
