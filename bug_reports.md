# Bug Report

## Bugs reported

**Total Bugs**: 10, **Reported**: 7*, **Confirmed**: 7, **Fixed**: 5

| REST API | Service | Link | Status |
| -------- | -------- |-------- | -------- |
| CopyObject | LocalStack |  [LocalStack/issues/10328](https://github.com/localstack/localstack/issues/10328)  | Fixed |
| SelectObjectContent | LocalStack | [LocalStack/issues/10329](https://github.com/localstack/localstack/issues/10329)  | Fixed |
| DeleteObjectTagging | LocalStack | [LocalStack/issues/10330](https://github.com/localstack/localstack/issues/10330)  | Fixed |
| GetObjectRetention | LocalStack | [LocalStack/issues/10331](https://github.com/localstack/localstack/issues/10331)  | Fixed |
| RestoreObject | LocalStack | [LocalStack/issues/10332](https://github.com/localstack/localstack/issues/10332)  | Fixed |
| DeleteTable & ListGlobalTables | LocalStack |  [LocalStack/issues/10376](https://github.com/localstack/localstack/issues/10376)  | Confirmed |
| set_container_access_policy | Azurite | [Azurite/issues/2378](https://github.com/Azure/Azurite/issues/2378)  | Confirmed |

*The remaining 3 bugs were not reported because they were fixed already in the latest version of the emulator.

## Discrepancies reported

**Total Discrepancies**: 94, **Reported**: 5, **Confirmed**: 5, **Fixed**: 4

We also reported some of the discrepancies which the emulator developers found crucial as they quickly addressed them.

| REST API | Service | Link | Status |
| -------- | -------- | -------- | -------- |
| copy_blob | Azurite | [Azurite/issues/1954](https://github.com/Azure/Azurite/issues/1954) | Fixed |
| put_block_list | Azurite | [Azurite/issues/1955](https://github.com/Azure/Azurite/issues/1955#issue-1697049378) | Fixed |
| undelete_container | Azurite | [Azurite/issues/2318](https://github.com/Azure/Azurite/issues/2318) | Fixed |
| upload_blob_from_url | Azurite | [Azurite/issues/2319](https://github.com/Azure/Azurite/issues/2319)| Fixed |
| list_container_api | Azurite | [Azurite/issues/2320](https://github.com/Azure/Azurite/issues/2320) | Confirmed |
