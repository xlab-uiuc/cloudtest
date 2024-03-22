# Discrepancy Reports and Status

### Azurite: 

**Total Discrepancies**: 34, **Reported**: 5, **Confirmed**: 5, **Fixed**: 2 
**Total Bugs**: 3, **Reported**: 1, **Confirmed**: 1, **Fixed**: 0

### Localstack: 

**Total Discrepancies**: 64, **Reported**: 5, **Confirmed**: 1, **Fixed**: 1 (+3*)  
**Total Bugs**: 7, **Reported**: 6, **Confirmed**: 6, **Fixed**: 5

## Azurite Discrepancy Report:

| REST API | Link | Status |
| -------- | -------- | -------- |
| copy_blob | [Azurite/issues/1954](https://github.com/Azure/Azurite/issues/1954) | Fixed |
| put_block_list | [Azurite/issues/1955](https://github.com/Azure/Azurite/issues/1955#issue-1697049378) | Fixed |
| undelete_container | [Azurite/issues/2318](https://github.com/Azure/Azurite/issues/2318) | Fixed* |
| upload_blob_from_url | [Azurite/issues/2319](https://github.com/Azure/Azurite/issues/2319)| Fixed | 
| list_container_api | [Azurite/issues/2320](https://github.com/Azure/Azurite/issues/2320) | Confirmed | 

## LocalStack Discrepancy (BUGS) Report:

| REST API | Link | Status |
| -------- | -------- | -------- |
| GetObjectRetention |  [LocalStack/issues/10331](https://github.com/localstack/localstack/issues/10331)  | Fixed* |
| DeleteObjectTagging |  [LocalStack/issues/10330](https://github.com/localstack/localstack/issues/10330)  | Fixed* |
| RestoreObject |  [LocalStack/issues/10332](https://github.com/localstack/localstack/issues/10332)  | Fixed* |
| CopyObject |  [LocalStack/issues/10328](https://github.com/localstack/localstack/issues/10328)  | Fixed |
| SelectObjectContent |  [LocalStack/issues/10329](https://github.com/localstack/localstack/issues/10329)  | Fixed |

## DynamoDB Discrepancy (BUGS) Report:

| REST API | Link | Status |
| -------- | -------- | -------- |
| DeleteTable & ListGlobalTables |  [LocalStack/issues/10376](https://github.com/localstack/localstack/issues/10376)  | Confirmed |

## Azurite (BUGS) Report:

| REST API | Link | Status |
| -------- | -------- | -------- |
| set_container_access_policy |  [Azurite/issues/10376](https://github.com/Azure/Azurite/issues/2378)  | Confirmed |

<br>
*Already fixed in the latest version of the Emulator. We don't claim the fix.
