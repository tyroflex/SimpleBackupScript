# SimpleBackupUtils
Simple Backup Script I use to upload and store media in S3 Deep Glacier for cost efficient backup.

This is a very simple script that uses AWS's Boto3 Library on Python to access and upload data to the S3 Buckets.

The script is not designed to be able to resume interrupted upload despite AWS's Multipart Upload allowing it.

TODO:
- Allow the script to resume when interrupted.
- Remake the entire script in C# before adding more functionality.
