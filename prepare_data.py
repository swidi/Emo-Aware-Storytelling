# Copyright 2019 The Texar Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Preprocesses raw data and produces TFRecord files
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import texar as tx

from data_utils import processor
#from Reinforcement import rl_data_utils_x4_128_inference_v3 as data_utils # used for extra evaluation experiment to generate stories with various arcs and same title
from data_utils import rl_data_utils_128 as data_utils # used for processing comet data for label finetune generationi

# pylint: disable=invalid-name, too-many-locals, too-many-statements

flags = tf.flags

FLAGS = flags.FLAGS
flags.DEFINE_string(
    "data_dir", 'data',
    "The directory of raw data, wherein data files must be named as "
    "'train_[x1,x4].txt', 'dev_[x1,x4].txt', or 'test_[x1,x4].txt'.")
flags.DEFINE_integer(
    "max_seq_length", 128,
    "The maxium length of sequence, longer sequence will be trimmed.")
flags.DEFINE_string(
    "tfrecord_output_dir", None,
    "The output directory where the TFRecord files will be generated. "
    "By default it is set to be the same as `--data_dir`.")
flags.DEFINE_string(
    "pretrained_model_dir", "gpt2_pretrained_models/model_345M",
    "The directory of pretrained model.")


tf.logging.set_verbosity(tf.logging.INFO)


def prepare_data():
    """
    Builds the model and runs.
    """
    data_dir = FLAGS.data_dir
    if FLAGS.tfrecord_output_dir is None:
        tfrecord_output_dir = data_dir
    else:
        tfrecord_output_dir = FLAGS.tfrecord_output_dir
    tx.utils.maybe_create_dir(tfrecord_output_dir)

    # Creates a data pre-processor for, e.g., BPE encoding
    proc = processor.get_encoder(FLAGS.pretrained_model_dir)

    # Produces TFRecord files
    data_utils.prepare_TFRecord_data_v2(
        data_dir=data_dir,
        max_seq_length=FLAGS.max_seq_length,
        encoder=proc,
        output_dir=tfrecord_output_dir)


def main():
    """Data preparation.
    """
    prepare_data()


if __name__ == "__main__":
    main()
