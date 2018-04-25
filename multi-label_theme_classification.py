import os
import json

config_directory = "theme_config.json"

config = json.loads(open(config_directory).read())
data_directory = config["data_directory"]
fasttext_directory = config["fasttext_directory"]
pretrained_model_directory = config["pretrained_model_directory"]
raw_result_filename = config["raw_result_filename"]
result_filename = config["result_filename"]
mode = config["mode"]
k = config["k"]
threshold = config["threshold"]

num_labels = 19

cmd = "%s predict-prob %s %s %s > %s" %(fasttext_directory, pretrained_model_directory, data_directory, str(num_labels), raw_result_filename)
os.system(cmd)

result = []
with open(raw_result_filename) as f:
    for l in f.readlines():
        llist = l.split(" ")
        temp = []
        for eind in range(len(llist) / 2):
            temp.append((llist[eind * 2][9:], float(llist[eind * 2 + 1])))
        temp.sort(key=lambda x: x[1], reverse=True)
        result.append(temp)

with open(result_filename, "w") as f:
    if mode == "topk":
        for line in result:
            temp_str = []
            for idx in range(k):
                temp_str.append(line[idx][0])
            temp_str = ",".join(temp_str)
            f.write(temp_str)
            f.write("\n")
    elif mode == "threshold":
        for line in result:
            temp_str = []
            for label, score in line:
                if score >= threshold:
                    temp_str.append(label)
                else:
                    break
            temp_str = ",".join(temp_str)
            f.write(temp_str)
            f.write("\n")
