#Creator: Rob Hird
#Date: Dec 2018
#Description: Test Case to verify indexes.conf

from modules import verify_indexes_module
import sys 
sys.dont_write_bytecode = True
perf = "perf"
prod = "prod"
def main():
    # verify_indexes_module.run(perf)
    # verify_indexes_module.run(prod)
    print("hello")

if __name__ == '__main__':
    main()