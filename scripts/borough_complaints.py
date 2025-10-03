import argparse
import sys
import csv

csv.field_size_limit(sys.maxsize)

def main():
    parser = argparse.ArgumentParser(description= "Usage: borough_complaints.py -i <the input csv file> -s <start date> -e <end date> [-o <output file>]")
    
    # define all arguments
    parser.add_argument("-i", required=True, help="input csv file")
    parser.add_argument("-s", required=True, help="start date")
    parser.add_argument("-e", required=True, help="end date")
    parser.add_argument("-o", help="output file")

    args = parser.parse_args()

    if args.o == None:
        out = sys.stdout
    else:
        out = open(args.o, "w", newline="")

    counts = {}
    mon_s, day_s, ye_s = (args.s).split("/")
    mon_s = int(mon_s)
    day_s = int(day_s)
    mon_e, day_e, ye_e = (args.e).split("/")
    mon_e = int(mon_e)
    day_e = int(day_e)        

    with open(args.i, newline="") as f:
        reader = csv.reader(f)    
        headers = next(reader)

        #indices
        ci = headers.index("Complaint Type")
        bi = headers.index("Borough")
        di = headers.index("Closed Date")

        for row in reader:
            try:
                c_type = row[ci]
                brgh = row[bi]
                date = row[di].split()[0]
            except IndexError:
                continue   

            month, day, year = date.split("/")
            month = int(month)
            day = int(day)
            if not date:
                continue

            if (mon_s, day_s) <= (month, day) <= (mon_e, day_e):
                key = (c_type, brgh)
                if key in counts:
                    counts[key] += 1
                else:
                    counts[key] = 1

    print("complaint type, borough, count", file=out)

    for key, count in counts.items():
        complaint = key[0]
        borough = key[1]
        print(complaint + ", " + borough + ", " + str(count), file=out)                     

    if out != sys.stdout:
        out.close()

if __name__ == "__main__":
    main()
