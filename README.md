# auth0-cli-utilities
Random Auth0 command line tools.

## Setup

These tools use the [Auth0 Python SDK](https://github.com/auth0/auth0-python).
Start with the usual [virtualenv](https://virtualenv.pypa.io/en/latest/#)
stuff.

```
$ mkdir ~/virtualenv/auth0
$ virtualenv ~/virtualenv/auth0
$ source ~/virtualenv/auth0/bin/activate
$ pip install -r requirements
$ python test.py
```

`test.py` will dump the configuration for your tenant's connections if
everything is working correctly.

## `db_backup.py`

This script is supposed to back up your Auth0 hosted user databases. It is
probably a Bad Idea. It hasn't been tested against large environments and may
need modification to avoid hitting Auth0 rate limits. I don't imagine this
scales well at all for large user databases.

Auth0 doesn't provide a means to backup your databases. You used to be able to
download your entire database by paging through the results of a query against
the `/users` endpoint that returned all user profiles, but those queries are
now limited to 1,000 results.

You can use the `/jobs` endpoint to submit a job to download your entire user
database. Unfortunately, you need to explicitly specify every attribute that
you want to back up. If you don't explicitly specify any attributes, you will
get a default set that excludes your `user_metadata` and `app_metadata`. On the
other hand, if you explicitly specify even one attribute, you must specify them
all.

This script uses the `/jobs` endpoint to download a default export job of your
user databases in CSV format. Then it iterates through the results of that
file, querying the `/users` endpoint for each user from the export job, one at
a time. I told you it was probably a Bad Idea.

### Other Solutions

These are probably much better ideas!

#### Export Jobs

This is probably the simplest solution. Maintain an up to date export job
import file that explicitly specifies all the attributes you want to back up.
This might be difficult in an environment where your `user_metadata` and
`app_metadata` are changing rapidly due to ongoing development, but it is the
most efficient and probably the recommended option.

```
{
    "connection_id": "con_ABC123",
    "format": "json",
    "fields": [
        {
            "name": "username"
        },
        {
            "name": "email"
        },
        {
            "name": "user_metadata.preferred_language",
            "export_as": "preferred_language"
        },
        {
            "name": "app_metadata.customer_id",
            "export_as": "customer_id"
        },
        .
        .
        .
```

#### Backup Groups

When your users register, assign them to a "backup group", and limit every
backup group to 1,000 members. Name the groups algorithmically so you can then
write a script to run a query against each backup group via the `/users`
endpoint. You can then page through the results of each query, eventually
backing up all your backup groups.

```
{
  "app_metadata": {
    "backup_group": "AAA001"
  }
}
```

## `list_metadata_fields.py`

A work in progress. Largely a copy of the `db_backup.py` script, but this one
is intended to provide a list of all the unique keys in your `user_metadata`
and `app_metadata`. Useful for checking your metadata fields for typos or new
fields that someone has snuck in.

## `getcxnid.py`

Returns the connection ID for the specified connection.

```
$ python getcxnid.py -c "Username-Pssword-Authentication"
```

