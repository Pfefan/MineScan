import os
import anvil
from multiprocessing import Pool
from collections import Counter
import argparse

class Blockcount():
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description='Count the total count of Blocks in a Minecraft world')
        self.parser.add_argument('--path', metavar='N', type=str, nargs='+',
                            help='the path to the world region files')

    def count_blocks(self, region_file):
        block_counts = Counter()
        region = anvil.Region.from_file(region_file)

        for x in range(32):
            for z in range(32):
                try:
                    chunk = anvil.Chunk.from_region(region, x, z)
                    for block in anvil.Chunk.stream_chunk(chunk):
                        if block.id != 'air' and block.id != 0:
                            block_counts[block.id] += 1
                except:
                    pass
        return block_counts

    def main(self):
        args = self.parser.parse_args()
        region_filepath = "/".join(args.path)
        filenames = os.listdir(region_filepath + "/")
        print(filenames)

        del self.parser

        with Pool(processes=11) as pool:
            results = pool.map(self.count_blocks, [region_filepath + "/" + filename for filename in filenames])
            total_counts = Counter()
            for result in results:
                total_counts += result
            print(f"Block counts in the region: {dict(total_counts)}")

if __name__ == "__main__":
    blockcount = Blockcount()
    blockcount.main()
