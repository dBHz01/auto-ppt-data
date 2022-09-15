import os
from shutil import copyfile
from dp_insts import PEOPLE

DST_BASE_DIR = "CNET-imgs"

if __name__ == "__main__":
    for people in PEOPLE:
        for dir in os.listdir(people):
            label = dir.split("-")[1]
            pathname = os.path.join(people, dir, "content.json")
            # img_names = []
            # for img in os.listdir(pathname):
            #     try:
            #         img_names.append((int(img.split("-")[0]), img))
            #     except Exception:
            #         print(img)
            # img_names.sort(key=lambda x : x[0])
            src_path = os.path.join(people, dir, "content.json")
            dst_path = os.path.join(DST_BASE_DIR, people, label + "-content.json")
            print(people, dst_path)
            if not os.path.exists(os.path.join(DST_BASE_DIR, people)):
                os.mkdir(os.path.join(DST_BASE_DIR, people))
            copyfile(src_path, dst_path)
