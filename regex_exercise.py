import gzip
import re
from Bio import SeqIO
import csv

log_lines = [
    "2024-01-15 10:02:11 INFO Server started on port 8080",
    "2024-01-15 10:03:47 ERROR Failed to connect to database",
    "2024-01-16 08:15:00 WARNING Disk usage at 85%",
    "2024-01-16 14:22:39 ERROR Timeout while fetching https://example.com/api",
    "2024-01-17 09:00:05 INFO User admin logged in from 192.168.1.10",
    "2024-01-17 11:41:18 DEBUG Cache cleared successfully",
    "2024-01-18 03:12:56 ERROR Connection refused from 192.168.1.55",
    "2024-01-18 23:59:02 INFO Backup completed in 42s",
]



for i in range(len(log_lines)):
    a = re.match("2024-01-16", log_lines[i])
    b = re.search("ERROR|WARNING", log_lines[i])
    c = re.search(r"(.{1,3}\.){2,4}.+", log_lines[i]) # pridat ze se jedna o cislo \d
    d = re.search(r"in .+s$", log_lines[i])
    e = re.search("http://|https://", log_lines[i])
    #print(c)

#print(re.match(r""))


# TASK 2
def reverse_complement(seq):
    complement = str.maketrans("ACGT", "TGCA")
    reverse_complement = seq.translate(complement)[::-1]
    return reverse_complement
#print(reverse_complement("ATAG"))

class SequencingRead:
    def __init__(self, read_id, sequence):
        self.read_id = read_id
        self.sequence = sequence


    def matches_mid_pair(self, forward_mid, reverse_mid) -> bool:
        pattern = re.compile(rf"^{forward_mid}.*{reverse_complement(reverse_mid)}$")
        return bool(pattern.match(self.sequence))

    def trim_mid_pair(self, forward_mid, reverse_mid) -> str | None:
        if self.matches_mid_pair(forward_mid, reverse_mid) == True:
            seq_crop = re.sub(forward_mid, "", self.sequence)
            seq_cropped = re.sub(reverse_complement(reverse_mid), "", seq_crop)
            return seq_cropped
        else:
            return None

    def describe(self) -> str:
        return f"{type(self).__name__} {self.sequence}"

r1 = SequencingRead("demo_1", "AGCTTCGA" + "N" * 20 + reverse_complement("TGCAGGTC"))
print(r1.describe())
print(r1.matches_mid_pair("AGCTTCGA", "TGCAGGTC"))  # True
print(r1.matches_mid_pair("CGATCGAT", "GCTAGCTA"))  # False
print(r1.trim_mid_pair("AGCTTCGA", "TGCAGGTC"))     # 20 x "N"



#install Biopython
# TASK 3

class Demultiplexer:
    def __init__(self, fasta_path, mid_table_path):
        self.reads = []

        with gzip.open(fasta_path, "rt") as handle:
            for record in SeqIO.parse(handle, "fasta"):
                self.reads.append(
                    SequencingRead(record.id, str(record.seq))
                )

        self.mids = []

        with open(mid_table_path, "r", newline="") as handle:
            reader = csv.DictReader(handle, delimiter=";")
            for row in reader:
                label = f"{row['SampleID']}_{row['Description']}"
                forward_mid = row["FBarcodeSequence"]
                reverse_mid = row["RBarcodeSequence"]
                self.mids.append((label, forward_mid, reverse_mid))

        self.assigned = {label: [] for label, _, _ in self.mids}
        self.unassigned = []


    def assign_reads(self):


    def report(self) -> str:


    def write_fasta(self, output_dir):



demux = Demultiplexer("fishes.fna.gz", "fishes_MIDs.csv")
demux.assign_reads()
print(demux.report())
demux.write_fasta("demux_output")