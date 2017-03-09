# contribution-spy
Python 3.x script to log when the number of a user's contribution changes

### Fork info
This repository is a fork of [contribution-spy](https://github.com/leots/contribution-spy) by [**@leots**](https://github.com/leots).

The `push-notifications` branch is a Python 3.x version of that script, with the [Notifications](#Notifications) feature, a JSON file for configuration, and improved error handling.

### Setting it up
1. Make sure you have [Python 3.x](https://www.python.org/) installed
2. For Python < 3.4, you need to install [pip](https://pip.pypa.io/en/stable/installing/) manually
3. Rename `config.json.template` to `config.json`
4. Replace these values:

    | Value to replace              | Replace it with                                   | Example value         |
    | ----------------------------- | ------------------------------------------------- | --------------------- |
    | `GITHUB_USERNAME_TO_SPY`      | the GitHub username of the user you want to spy   | "leots"               |
    | `PATH_TO_CSV_LOG_FILE`        | the path to the CSV log file                      | "contributions.csv"   |
    | `YOUR_PUSHOVER_USER_KEY`      | your Pushover User Key                            | —                     |
    | `YOUR_PUSHOVER_API_TOKEN`     | your Pushover API Token/Key                       | —                     |

5. From the script directory, run `pip install -r requirements.txt`
6. Finally, run the script `python contribution-spy.py`
    (or pass `yes` as an argument `python contribution-spy.py yes`, to enable the Notifications feature)

### Notifications
You can set this script to send push notifications whenever the specified user makes a contribution on GitHub. To enable this feature, run this script like this `python contributions-spy.py yes`

We use the [Pushover](https://pushover.net/) notification service. You will have to purchase your own license for your devices and set your [user key](config.json#L4) and [API token](config.json#L5) in the `config.json` file

### Notes
- The code that gets the number of contributions is from [ghb-contributions](https://github.com/keith/ghb/blob/master/src/ghb-contributions) by [**@keith**](https://github.com/keith)
- The Notifications feature, `config.json` and improved error handling were contributed by [**@dn0z**](https://github.com/dn0z)

### License
[contribution-spy](https://github.com/leots/contribution-spy) is licensed under the [MIT License](LICENSE)
