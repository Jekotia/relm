Relm has been designed in a manner which makes expanding its capabilities with new Notification types, Storage types, and Sources fairly easy.

# Sources

Let's use SourceForge as an example as we look over the process.

Every time Relm is run, there will be some sort of usage of sources, even if it doesn't attempt to communicate. 

# Notifications



# Storage

Let's use `mysql` as an example as we look over the process.

When Relm is run with any arguments that call for a storage read or write, those operations will be handled by relm.storage.read and relm.storage.write. When one of these <u>functions</u> are called, they look to the config and then call another <u>function</u> based on the value of `['STORAGE']['type']` .

```python
run = 'self.storage.r.' + self.config['STORAGE']['type'] + '(self)'
return eval(run)
```

## Existing Code

In addition to the work on the enhancement itself, only five small modifications to existing code would be required to add MySQL support:

- In `functions/relm/core/config.py`
  - Add MySQL configuration values to the default config generated
- In `functions/relm/storage/d/__init__.py`
  - Add the line `from functions.relm.storage.d.mysql import func_mysql as mysql` 
- In `functions/relm/storage/r/__init__.py`
  - Add the line `from functions.relm.storage.r.mysql import func_mysql as mysql ` 
- In `functions/relm/storage/w/__init__.py`
  - Add the line `from functions.relm.storage.w.mysql import func_mysql as mysql`

## New Code

Three files are required:

- `functions/relm/storage/d/mysql.py`

  This function needs to:

  - Accept
  - Return

- `functions/relm/storage/r/mysql.py`

  This <u>function</u> needs to:

  - Accept the argument `self`
  - Return either the contents of the storage entry as a string, or the Boolean False if no entry exists

- `functions/relm/storage/w/mysql.py`

  This <u>function</u> needs to:

  - Accept the arguments `self` and `data`
  - Return either Boolean True or False, based on if the write was successful

Both files should use the dictionary `self.current` to inform themselves what the current task is, and do their own exception handling.