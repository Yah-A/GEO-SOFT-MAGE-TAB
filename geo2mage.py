import argparse
import os
from dateutil.relativedelta import relativedelta
import urllib.request as urllib2
import xml.etree.ElementTree as ET
import ftplib, datetime, sys
import gzip
import shutil


def obtaindate(userin):
    # isValid=False
    # while not isValid:
        try:  # strptime() throws an exception if the input doesn't match the pattern
            d = datetime.datetime.strptime(userin, "%d/%m/%Y").date()
            # print("You entered:",d)
            # isValid=True
            return d
        except:
            print("Date is NOT in the right format, please use \"dd/mm/yyyy\" and try again!\n")
            sys.exit(1)
    # return d


def askme(question):
    approve = input(question)
    if not approve or approve[0].lower() != 'y':
        print('As you like. Come back soon :)')
        sys.exit(0)


# Taking instance from ArgumentParser() class
parser = argparse.ArgumentParser()

parser.add_argument("keyword", type=str,
                    help="the Keyword(s) to Search for it in the GEO Database")
parser.add_argument("-fp", type=str, default=os.getcwd(),
                    help="the Path required to save the downloaded files, Default = Current Working Directory")
parser.add_argument("-sd", type=str,
                    help="the Start Date of the Submission Period You Choose for Your Keyword (Date format: dd/mm/yyyy)")
parser.add_argument("-ed", type=str,
                    help="the End Date of the Submission Period You Choose for Your Keyword (Date format: dd/mm/yyyy)")


args = parser.parse_args()

kw = args.keyword
fp = args.fp
# Validating the path entered
if fp:
    if not os.path.exists(fp) or fp[-1] == "\\" or fp[-1] == "/":
        print("The path is invalid or not created yet, please enter a valid path or create this directory first")
        sys.exit(0)
    else:
        os.chdir(fp.replace("\\", "\\""\\"))
# Validating the start/end dates entry and handling the exception of entering and end date without a start date and
# entering a start date greater than end date
if args.ed:
    if not args.sd:
        print("You can't enter an End Date without a Start Date, You should enter a Start Date. Try Again!!!")
        sys.exit(1)
if args.sd:
    sd = obtaindate(args.sd)
    if not args.ed:
        print ("***The End Date will be set as the current date (" + str(datetime.date.today()) + ")***")
        ed = datetime.date.today()
    else:
        ed = obtaindate(args.ed)

        if sd > ed:
            print("You've entered an invalid start/end date, start date should be Before end date!")
            print("Try Again!!!")
            sys.exit(1)
else:
    print("You Entered no Start/End Dates, hence search will be performed on the "
          "LAST 6 MONTHS as default, from {} to {} ...".format(datetime.date.today()-relativedelta(months=+6),datetime.date.today()))
    sd = datetime.date.today()-relativedelta(months=+6)
    ed = datetime.date.today()

# Reviewing the entered parameters
print("\nThese are the parameters of your query:\n")
print("keyword =", kw)
print("start date =", sd)
print("end date =", ed)
print("path =", fp + "\n")


askme('Would you like to proceed with these parameters?: [y/N]')

# We can use this in the final report
# print(en_dt - st_dt)

response = urllib2.urlopen('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term={0}[ETYP]+AND+'
                           '%22{1}%22[PDAT]+:+%22{2}%22[PDAT][Filter]&retmax=10000&usehistory=y'.format(kw, sd, ed))
data = response.read()
# print ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term={0}[ETYP]+AND+%22{1}%22[PDAT]+:"
#      "+%22{2}%22[PDAT][Filter]&retmax=10000&usehistory=y".format(kw,sd,ed))
# print(data)
filename = "IDs.txt"
file_ = open(filename, 'w')
# To build a tree out of a continuous string
tree = ET.fromstring(data)
IDs = []

records_no = tree[0].text
max_rec = tree[1].text
print("No. of records found =", records_no)
print("Max no. of records retrieved =", max_rec)
print("The query IDs/accession numbers has been downloaded to IDs.txt in", fp)

askme('These are the basic search results, would you like to start downloading the SOFT files?: [y/N]')

# print(tree)
# x=tree.iter('WebEnv')
# print(x)
for node in tree.iter('IdList'):
    # print('\n')
    # print(node.iter())
    # print(node.tag)
    counter = 0
    for elem in node.iter():
        # this condition is to eliminate the first unwanted empty result where node.tag = elem.tag = 'IdList'
        if elem.tag != node.tag:
            print(node.tag)
            print(elem.tag)
            # print("{}".format(elem.text))
            print(elem.text)
            file_.write(elem.text+'\n')
            IDs.append(elem.text)
            counter += 1
            print(counter)
            # print(node.tag)
file_.close()



def log(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %T")
    print('[-- {} --] {}'.format(timestamp, msg), file=sys.stderr)


for ID in IDs:
    server = 'ftp.ncbi.nlm.nih.gov'
    directory = 'geo/series/{0}{1}nnn/{0}{2}/soft'.format(kw, ID[3:6], ID[3:])

    soft = '{}{}_family.soft.gz'.format(kw, ID[3:])
    soft2 = '{}{}_family.soft'.format(kw, ID[3:])
    log("connecting to server")
    ftp = ftplib.FTP(server)
    ftp.login()

    log("changing to directory: {}".format(directory))
    ftp.cwd(directory)
    ftp.retrlines('LIST')

    os.makedirs(ID)
    os.chdir(ID)

    log("starting to download: {}".format(soft))
    ftp.retrbinary("RETR {}".format(soft), open(soft, 'wb').write)

    with gzip.open(soft, 'rb') as f_in:
        with open(soft2, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(soft)
    os.chdir(fp.replace("\\", "\\""\\"))

    log("finished download")
    ftp.quit()


