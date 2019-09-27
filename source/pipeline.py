import os, glob, random
from tqdm import tqdm
import joblib


class Pipeline:
    def __init__(
        self, load_dest, save_dest, old_extension=None, new_extension=None, shuffle=True
    ):

        self.save_dest = save_dest
        self.load_dest = load_dest
        self.new_extension = new_extension
        self.old_extension = old_extension

        os.system(f"mkdir -p {save_dest}")

        old_glob = f"*.{old_extension}" if old_extension else "*"
        new_glob = f"*.{new_extension}" if new_extension else "*"

        F_IN = glob.glob(os.path.join(load_dest, old_glob))
        F_OUT = glob.glob(os.path.join(save_dest, new_glob))

        F_IN = sorted(F_IN)

        if shuffle:
            random.shuffle(F_IN)

        F_OUT = set(F_OUT)
        self.ITR = [f for f in F_IN if self.get_output_file(f) not in F_OUT]

    def __len__(self):
        return len(self.ITR)

    def get_output_file(self, f):
        base = os.path.basename(f)
        if self.new_extension:
            base = base.split(".")[:-1]
            base.append(f"{self.new_extension}")

            base = ".".join(base)

            return os.path.join(self.save_dest, base)

    def slow_call(self, func):

        for f0 in tqdm(self.ITR):
            f1 = self.get_output_file(f0)

            if os.path.exists(f1):
                continue

            func(f0, f1)

            # if func(f0, f1) is False:
            #    print("REMOVING", f0)
            #    os.remove(f0)

    def __call__(self, func, CORES=-1):

        if CORES == 1:
            self.slow_call(func)
            return True

        dfunc = joblib.delayed(func)
        with joblib.Parallel(CORES) as MP:
            MP(dfunc(f, self.get_output_file(f)) for f in tqdm(self.ITR))
