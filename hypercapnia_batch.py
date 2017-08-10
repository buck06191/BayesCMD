from batch_data_creation import Batch
from datetime import datetime
import os
import sys
import distutils
import argparse
from bayescmd.util import findBaseDir
BASEDIR = findBaseDir('BayesCMD')

model_name = 'BS'
inputs = ['Pa_CO2', 'P_a', 'SaO2sup']  # Input variables
priors = {"Vol_mit": ['uniform', [0.02, 0.12]],
          'r_t': ['uniform', [0.01, 0.03]],
          'r_m': ['uniform', [0.01, 0.04]],
          'r_0': ['uniform', [0.007, 0.0175]],
          'cytox_tot_tis': ['uniform', [0.0025, 0.009]]
          }
test_priors = {"Vol_mit": ['uniform', [0.088, 0.09]],
          'r_t': ['uniform', [0.0165, 0.017]],
          'r_m': ['uniform', [0.0315, 0.035]],
          'r_0': ['uniform', [0.012, 0.0124]],
          'cytox_tot_tis': ['uniform', [0.00616, 0.0064]]
          }
outputs = ['Vmca', 'CCO']



def process(run_length, input_file, workdir):
    batchWriter = Batch(model_name,
                        priors,
                        inputs,
                        outputs,
                        run_length,
                        input_file,
                        workdir)

    batchWriter.definePriors()
    batchWriter.batchCreation(zero_flag=[0, 1])

if __name__ == '__main__':
    ap = argparse.ArgumentParser('Choose model to batch run:')
    ap.add_argument('input_file', metavar="INPUT_FILE", help='choice of model')
    ap.add_argument('run_length', metavar='RUN_LENGTH', type=int,
                    help='number of times to run the model')

    args = ap.parse_args()
    now = datetime.now().strftime('%H%MT%d%m%y')

    workdir = os.path.join(BASEDIR, 'build', 'batch', model_name, now)
    distutils.dir_util.mkpath(workdir)
    process(args.run_length, args.input_file, workdir)