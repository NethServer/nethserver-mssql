# nethserver-mssql
NethServer and Microsoft SQL Server integration.

When installed the module generates a default configuration as follow:
* Auto-generated SA password saved in `/var/lib/nethserver/secrets/mssql`
* Create default MsSQL databases (`master`, `model`, `msdb`, `tempdb`)
* Allow access to SQL service from Green network on default port 1433

User can change access network from Cockpit Services page or from Firewall section.

Database example:

    mssql-server=service
        ProductId=express
        ProductKey=
        TCPPort=1433
        access=green
        status=enabled


Events and actions
==================

`nethserver-mssql-upadte`: initialize default database.

`nethserver-mssql-save`: configure Microsoft repository, download the packages and install them. To complete this action `ProductId` is mandatory. To use `ProductKey` configure ProductId with 'key' value and then insert product key in `ProductKey` prop. You can do this configuration also from Cockpit interface.

`nethserver-mssql-change-password`: change SA password in /var/lib/nethserver/secrets/mssql and also in master SQL db.

`pre-backup-data`: dump and save tables in backup dir. They will be saved with backup-data execution.

`post-backup-data`: clean mssql local backup data dir.

`post-restore-config`: reinstall packages with restored cofniguration.

`post-restore-data`: restore tables from backup-data and then delete .bak file from local dir (not from backup).


Cockpit interface
=================

From Cockpit interface you can:
* configure repo and download initial package (`nethserver-mssql-save`)
* view and change SA password
* create a new database
* change SQL Server edition
