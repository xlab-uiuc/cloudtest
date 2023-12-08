# cloudtest

**Note**: If it ever comes down to making this repo public, disable all the cloud connection strings first. 

## Important gdocs

Paper Structure: https://docs.google.com/document/d/174mVS2f-TuKVkzjHWpWF9JfGp2lfimBBnZDOxxTW-oc/edit

**Discrepancies from fuzzing:**

Azure Storage discrepancies: https://docs.google.com/document/d/1fD_UqEUrwEhOCsCi0fSutc2H0vTtOYZssaGbIzPCJ1M/edit

S3 discrepancies: https://docs.google.com/document/d/13ey5x3MjERzZ_6q_HoPwSgeLwClctjpV_xlWSwI1TDs/edit

DynamoDB discrepancies: https://docs.google.com/document/d/1-_YeRWH5hWmCvyxt_YKEv4ASqzOcClgcF9FwmaQkG78/edit

Breakdown in a spreadsheet: https://docs.google.com/spreadsheets/d/1O_uZWFwpAwJgstAHOwyUFsPpMcgmq9fbrXigo7VfgdA/edit?pli=1#gid=804341594

**Application tests:**

Application discrepancies RCA: https://docs.google.com/document/d/1OIFc5jGdbZp6-gEaD0sb-fWSC1EzsbaHK1XNi5RYdA0/edit?usp=sharing

**Bugs reported:**

Azurite:
- [Copy Blob - 500](https://github.com/Azure/Azurite/issues/1954#issue-1697046568)
- [Put Block List - 500](https://github.com/Azure/Azurite/issues/1955#issue-1697049378)
- [Undelete Container](https://github.com/Azure/Azurite/issues/2318)
- [Upload Blob from URL](https://github.com/Azure/Azurite/issues/2319)
- 
Azure Storage:
- 2 Bugs of the following can be reproduced with the SDK: https://www.notion.so/Azure-Blob-bugs-e4785c99d2d947b3977245e52107448a

**API specification constraints breakdown:**

Azure Blob: https://docs.google.com/document/d/1MZBO1i73AIsV_2c58lC8FB_4MRdXAAMRCG__e-vz0OA/edit

**Cost Analysis:**

Gdoc for cost savings breakdown: https://docs.google.com/document/d/1In_lYeZbLrcmigNxgcLyRRFfGRnTUyxRg99xhfKNYcY/edit

Notebook for cost savings calculations: https://colab.research.google.com/drive/1md3ra322ytDH_MxMOcGXMixhpqcjl3TH?usp=sharing
