import os.path

def get_new_file_path(base_path, suffix="_BF"):
    dir_path = os.path.dirname(base_path)
    file_name = os.path.basename(base_path)
    new_file_name = f"{file_name.split(".")[-2]}{suffix}.{file_name.split(".")[-1]}"
    return os.path.join(dir_path, new_file_name)


def scan_border_filter(file_path, borders_dict):
    new_file_path = get_new_file_path(file_path)

    with open(file_path, "rt") as file_read:
        with open(new_file_path, "w") as file_write:
            for line in file_read:
                line = line.strip().split()
                x = float(line[0])
                y = float(line[1])
                if borders_dict["min_x"] < x < borders_dict["max_x"]:
                    if borders_dict["min_y"] < y < borders_dict["max_y"]:
                        point = (f"{x} {y} {float(line[2])}\n")
                                 # f"{int(line[3])} {int(line[4])} {int(line[5])}\n")
                        file_write.write(point)


if __name__ == "__main__":

    FILE_NAME = os.path.join("..", "src", "осыпь_02.txt")

    BORDERS_DICT = {"min_x": 2886,
                    "max_x": 2962,
                    "min_y": 10786,
                    "max_y": 10862,
                    }

    scan_border_filter(FILE_NAME, BORDERS_DICT)
    # print(get_new_file_path(FILE_NAME))