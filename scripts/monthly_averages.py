import argparse
import sys
import csv
from datetime import datetime

csv.field_size_limit(sys.maxsize)

def main():
    parser = argparse.ArgumentParser(description = "Usage: monthly_averages.py -i <the input csv file> [-o <output file>]")

    parser.add_argument("-i", required=True, help="input csv file")
    parser.add_argument("-o", help="output csv file")

    args = parser.parse_args()

    if args.o is None:
        out = sys.stdout
    else:
        out = open(args.o, "w", newline = "")

    avgs = {}

    with open(args.i, newline="") as f:
        reader = csv.reader(f)    
        headers = next(reader)

        #indices
        index_time1 = headers.index("Created Date")
        index_time2 = headers.index("Closed Date")
        index_zip = headers.index("Incident Zip")    

        for row in reader:
            time1_str = row[index_time1]
            time2_str = row[index_time2]
            zipcode = row[index_zip]

            if time1_str and time2_str:
                try:
                    format = "%m/%d/%Y %I:%M:%S %p"
                    created_time = datetime.strptime(time1_str, format)
                    closed_time = datetime.strptime(time2_str, format)

                    if closed_time >= created_time:
                        difference = (closed_time - created_time).total_seconds()
                        response_time = difference / 3600.0

                        month = closed_time.month
                        key = (zipcode, month)

                        if key in avgs:
                            total, count = avgs[key]
                            avgs[key] = (total + response_time, count + 1)
                        else:
                            avgs[key] = (response_time, 1)

                except ValueError:
                    continue
            
    print("zipcode, month, monthly response-time average", file=out)

    for key, (total, count) in avgs.items():
        monthly_avg = total / count
        z = key[0]
        m = key[1]
        print(str(z) + "," + str(m) + "," + str(monthly_avg), file=out)

   
    if out is not sys.stdout:
        out.close()     

if __name__ == "__main__":
    main()
