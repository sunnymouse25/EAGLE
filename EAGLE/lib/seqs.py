from Bio.Seq import Seq

from EAGLE.lib.general import filter_list, get_un_fix


def seq_from_fasta(fasta_path, seq_id, ori=+1, start=1, end=-1):
    fasta_dict = load_fasta_to_dict(fasta_path)
    if end == -1:
        end = len(fasta_dict[seq_id])
    if start < 0:
        start = len(fasta_dict[seq_id]) + start + 1
    if end >= start:
        if ori > 0:
            return fasta_dict[seq_id][start-1: end]
        else:
            return str(Seq(fasta_dict[seq_id][start-1: end]).reverse_complement())
    else:
        if ori > 0:
            return fasta_dict[seq_id][end-1: start]
        else:
            return str(Seq(fasta_dict[seq_id][end-1: start]).reverse_complement())


def load_fasta_to_dict(fasta_path):
    fasta_dict = dict()
    seq_list = list()
    title = None
    fasta_f = open(fasta_path)
    for line_ in fasta_f:
        line = None
        line = line_.strip()
        if not line:
            continue
        if line[0] == ">":
            if title:
                fasta_dict[title] = "".join(seq_list)
                seq_list = list()
                title = None
            title = line[1:]
        else:
            seq_list.append(line)
    if title:
        fasta_dict[title] = "".join(seq_list)
        seq_list = list()
        title = None
    return fasta_dict


def dump_fasta_dict(fasta_dict, fasta_path, overwrite=True):
    if overwrite:
        fasta_f = open(fasta_path, 'w')
    else:
        fasta_f = open(fasta_path, 'a')
    for seq_id in fasta_dict.keys():
        fasta_f.write(">"+seq_id+"\n")
        fasta_f.write(fasta_dict[seq_id]+"\n")
    fasta_f.close()


def reduce_seq_names(fasta_dict, num_letters=10, num_words=4):
    if num_letters < 6:
        print("Number of letters must be at least 6")
        return 1
    if num_words < 2:
        print("Number of words must be at least 2")
        return 1
    splitters_repl = {"_": " ",
                      "\t": " ",
                      ",": " ",
                      ";": " ",
                      ".": " ",
                      ":": " ",
                      "|": " ",
                      "/": " ",
                      "\\": " "}
    parts_size_list = _get_part_size_list(num_letters, num_words)
    reduced_fasta_dict = dict()
    seq_names_dict = dict()
    for seq_name in fasta_dict.keys():
        if len(seq_name) <= num_letters:
            prepared_seq_name = None
            prepared_seq_name = seq_name+"".join("_" for i in range(num_letters-len(seq_name)))
            seq_names_dict[prepared_seq_name] = seq_name
            reduced_fasta_dict[prepared_seq_name] = fasta_dict[seq_name]
            continue
        reduced_seq_name = None
        seq_name_list = filter_list("".join([splitters_repl.get(s, s) for s in seq_name]).split())
        parts = list()
        for i in range(num_words):
            try:
                parts.append(seq_name_list[i][:parts_size_list[i]])
            except IndexError:
                break
        reduced_seq_name = "".join(parts)
        res_len = num_letters - len(reduced_seq_name)
        un_num = 0
        un_fix = get_un_fix(un_num, res_len)
        while seq_names_dict.get(reduced_seq_name+un_fix, None):
            un_fix = None
            un_num += 1
            un_fix = get_un_fix(un_num, res_len)
        reduced_fasta_dict[reduced_seq_name+un_fix] = fasta_dict[seq_name]
        seq_names_dict[reduced_seq_name+un_fix] = seq_name
    return reduced_fasta_dict, seq_names_dict


def _get_part_size_list(num_letters, num_words):
    if num_letters == 6:
        return [2, 3]
    if num_letters == 7:
        if num_words >= 3:
            return [2, 3, 1]
        else:
            return [2, 3]
    if num_letters == 8:
        if num_words >= 4:
            return [2, 3, 1, 1]
        elif num_words == 3:
            return [3, 3, 1]
        else:
            return [3, 3]
    if num_letters == 9:
        if num_words >= 4:
            return [3, 3, 1, 1]
        elif num_words == 3:
            return [3, 3, 1]
        else:
            return [3, 4]
    if num_letters == 10:
        if num_words >= 4:
            return [3, 4, 1, 1]
        elif num_words == 3:
            return [3, 4, 1]
        else:
            return [4, 4]
    if num_letters >= 11:
        if num_words >= 4:
            return [3, 4, 1, 1]
        elif num_words == 3:
            return [4, 4, 1]
        else:
            return [4, 5]