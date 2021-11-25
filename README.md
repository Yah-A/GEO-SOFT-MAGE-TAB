# GEO-SOFT-MAGE-TAB
A program to query GEO database, download the soft files of the results, and generate MAGE-TAB files format
This project was a course project in a Bioinformatics Diploma, Nile University (2019)

Project 6: GEO Import:

ArrayExpress is a repository for manually curated functional genomics experiments.
Nevertheless, ArrayExpress also tend to be single shop for all functional genomics
experiments. This is done by importing experiments submitted to GEO. The main
challenge is data formats. ArrayExpress has founded MAGE-TAB data format to

store and represent experiments in a human readable format that can be viewed
using excel. On the other hand, GEO are using their own format called soft.
Write a software that:
1. Collect and download experiments/series soft format using NCBI Rest API.
2. Convert Softfile to MAGE tab formats.
3. MAGE-TAB consists of 2 tab-delimited files IDF and SDRF.
Your program should accept the following inputs:
1. Query to NCBI. This query should be run against the GEO Datasets -
db_id=gds -
2. Start and end date for the query. Default values will be released in the
last 6 months.
3. Working directory where GEO and MAGE-TAB files will be stored.
Output of your program:
1. Create folder for each experiment that contains the downloaded SOFT
file from GEO and the generated MAGE-TAB files.
2. Detailed report for all experiment downloaded including execution time,
and number of experiment downloaded. (be creative in generating the
report and make it informative as you can using charts whenever
possible)
Important Notes:
1. You can use any third-party library, tool, or public service. Just state this in
your code and report and list the functions or endpoints you used.
2. GEO’s soft files can be compressed, you need to work on these
compressed files.
3. MAGE-TAB format can be little bit tricky, so read the specifications
carefully and study some examples from ArrayExpress website.
4. Important links:
a. https://www.ncbi.nlm.nih.gov/geo/info/geo_paccess.html
b. https://www.ebi.ac.uk/arrayexpress/help/magetab_spec.html
c. https://www.ncbi.nlm.nih.gov/geo/info/download.html
