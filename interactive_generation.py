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
"""Example of building OpenAI GPT-2 language model for interactive emotion-aware story generation.
"""

import importlib
import random
import re
import numpy as np
import tensorflow as tf
import texar as tx

from data_utils import model_utils, processor

# pylint: disable=invalid-name, too-many-locals, too-many-statements, no-member
# pylint: disable=too-many-branches

flags = tf.flags

FLAGS = flags.FLAGS

flags.DEFINE_string("checkpoint", None,
                    "Model checkpoint to load model weights from. Use "
                    "`--pretrain_checkpoint` instead if loading OpenAI "
                    "pretrained checkpoint.")
flags.DEFINE_string("pretrain_checkpoint", None,
                    "OpenAI pretrained model checkpoint. Ignored if "
                    "'--checkpoint' is specified.")
flags.DEFINE_string("pretrained_model_dir", None,
                     "The directory of pretrained model, for loading "
                     "vocabuary, etc.")
flags.DEFINE_integer("seed", None, "Random seed.")
flags.DEFINE_integer("nsamples", 1, "The number of samples per input.")
flags.DEFINE_integer("max_decoding_length", 128,
                     "The maximun length of generated text.")
flags.DEFINE_integer("batch_size", 1, "The batch size of input.")
flags.DEFINE_integer("poem_batch_size", 1, "The batch size of input.")
flags.DEFINE_float("temperature", 0.7,
                   "Softmax temperature for top-k sample decoding. Must be "
                   "strictly greater than 0. Defaults to 0.7.")
flags.DEFINE_integer("top_k", 40,
                     "The number of top most likely candidates from a vocab "
                     "distribution.")
flags.DEFINE_boolean("is_interactive", False, "Interactive mode or not.")
flags.DEFINE_boolean("is_eval", False, "Evaluation mode or not.")
flags.DEFINE_integer("eval_poems_per_arc", 20, "The amount of poems to generate per emotion arc")
flags.DEFINE_string("config_type", "texar",
                    "The configuration file type. Set to 'json' if the GPT-2 "
                    "config file is in the same type of the official GPT-2 "
                    "config file. Set to 'texar' if GPT-2 config file is in "
                    "Texar type.")
flags.DEFINE_string("config_model", "configs.config_model_117M",
                    "The model configuration file to configure the model. "
                    "The config file type is define by the 'config_type',"
                    "it be of texar type or json type."
                    "For '--config_type=json', set the json config file path"
                    "like: '--config_model gpt2_pretrained_models/model_117M/"
                    "hparams.json';"
                    "For '--config_type=texar', set the texar config file "
                    "like: '--config_model configs.config_model_117M'.")

eval_arcs = ["Joy Joy Sadness", "Humor Annoyance Humor", "Suspense Suspense Vitality"]
eval_title = "my heart will go on" 

def normalize_stanza(stanza):
    stanza = stanza[:stanza.find('<|endoftext|>')].strip() if '<|endoftext|>' in stanza else stanza
    stanza = stanza.replace("|", "")
    stanza = stanza.strip()
    # Insert a linebreak BEFORE capital words (except I)
    stanza = re.sub(r"([A-HJ-Z]|I\w)", r"\n\1", stanza)
    if stanza[0] == '\n':
        stanza = stanza[1:]
    return stanza

def normalize_emo(emo):
    emo = emo.capitalize()
    if emo == "Beauty":
        emo = "Joy"
    if emo == "Sublime":
        emo = "Awe"
    return  emo + " " + emo + " " + emo

def main(_):
    """
    Builds the model and runs
    """
    np.random.seed(FLAGS.seed)
    tf.set_random_seed(FLAGS.seed)

    nsamples = FLAGS.nsamples
    batch_size = FLAGS.batch_size
    max_decoding_length = FLAGS.max_decoding_length

    # Load GPT-2 model configuration
    if FLAGS.config_type == "json":
        gpt2_config = model_utils.transform_gpt2_to_texar_config(
            FLAGS.config_model)
    elif FLAGS.config_type == "texar":
        gpt2_config = importlib.import_module(
            FLAGS.config_model)
    else:
        raise ValueError("Unknown config_type.")

    assert max_decoding_length <= gpt2_config.position_size, (
        "max_decoding_length should not be greater than position size")
    assert nsamples % batch_size == 0, (
        "nsamples must be dividable by batch_size")

    # Create a data pre-processor for, e.g., BPE encoding
    proc = processor.get_encoder(
        FLAGS.pretrained_model_dir)

    context = tf.placeholder(tf.int32, [batch_size, None])
    context_length = tf.placeholder(tf.int32, [batch_size])

    end_token = proc.encoder["<|endoftext|>"]
    if FLAGS.is_interactive:
        start_tokens = context[:, 0]
    else:
        start_tokens = tf.fill([batch_size], end_token)

    # Build the GPT-2 model
    word_embedder = tx.modules.WordEmbedder(
        vocab_size=gpt2_config.vocab_size,
        hparams=gpt2_config.embed)

    pos_embedder = tx.modules.PositionEmbedder(
        position_size=gpt2_config.position_size,
        hparams=gpt2_config.pos_embed)

    def _embedding_fn(x, y):
        # `x` is token ids, `y` is time steps
        return word_embedder(x) + pos_embedder(y)

    helper = tx.modules.TopKSampleEmbeddingHelper(
        embedding=_embedding_fn,
        start_tokens=start_tokens,
        end_token=end_token,
        top_k=FLAGS.top_k,
        softmax_temperature=FLAGS.temperature)
    output_layer = tf.transpose(word_embedder.embedding, (1, 0))

    decoder = tx.modules.TransformerDecoder(
        vocab_size=gpt2_config.vocab_size,
        output_layer=output_layer,
        hparams=gpt2_config.decoder)

    with tf.Session() as sess:
        # Generate continuations of context
        lm_output, _ = decoder(
            context=context,
            context_sequence_length=context_length,
            max_decoding_length=max_decoding_length,
            helper=helper,
            mode=tf.estimator.ModeKeys.PREDICT)

        # Load model checkpoint
        if FLAGS.checkpoint:
            tf.logging.info("Restore from {}".format(FLAGS.checkpoint))
            saver = tf.train.Saver()
            saver.restore(sess, FLAGS.checkpoint)
        elif FLAGS.pretrain_checkpoint:
            model_utils.init_gpt2_checkpoint(
                sess, FLAGS.pretrain_checkpoint)
        print("\nFinished loading\n")

        if FLAGS.is_interactive:
            # Enter interactive mode
            while True:
                story_title = input("Please enter a title! or q to exit >>> ")
                if story_title == "q":
                    break
                emotion_arc_poem = input("Please enter a sequence of emotions, one for each stanza. Choose from: Beauty, Joy, Vitality, Humor, Uneasiness, Sadness, Suspense, Annoyance, Nostalgia, Awe, Sublime. Beauty/Joy and Awe/Sublime refer to the same emotion internally.\n>>> ")
                if emotion_arc_poem == "q":
                    break
                # raw_text = raw_text + " | "

                while not story_title:
                    print("Input should not be empty!")
                    story_title = input("Please enter a title! or q to exit >>> ")
                    emotion_arc_poem = input("Please enter a sequence of three emotions separated by space from joy, anger, sadness, fear, neutral! or q to exit >>> ")

                for _ in range(FLAGS.poem_batch_size):
                    for emotion in emotion_arc_poem.split():
                        emotion_arc = normalize_emo(emotion)
                        print(emotion_arc)
                        raw_text = " <$> ".join((emotion_arc, story_title))
                        print(raw_text)
                        context_tokens = proc.encode(raw_text)
    
                        feed_dict = {
                            context: [context_tokens for _ in range(batch_size)],
                            context_length:
                                [len(context_tokens) for _ in range(batch_size)],
                            tx.context.global_mode(): tf.estimator.ModeKeys.PREDICT
                        }
                        generated = 0
                        for _ in range(nsamples // batch_size):
    
                            output = sess.run(lm_output, feed_dict=feed_dict)
    
                            sample_id = output.sample_id
                            for i in range(batch_size):
                                si = sample_id[i][len(context_tokens):]
                                s_text = proc.decode(si)
                                s_text = normalize_stanza(s_text)
                                print(s_text)
                    # end of poem
                    print("=" * 80)
        elif FLAGS.is_eval:
            eval_arcs_total = []
            for arc in eval_arcs:
                for _ in range(FLAGS.eval_poems_per_arc):
                    eval_arcs_total.append(arc)
            random.shuffle(eval_arcs_total)

            eval_arcs_file = open("eval_arcs.txt", "w")
            poems_file = open("eval_poems.txt", "w")
            for arc in eval_arcs_total:
                eval_arcs_file.write(arc + "\n")

            for emotion_arc_poem in eval_arcs_total:
                story_title = eval_title
                for emotion in emotion_arc_poem.split():
                    emotion_arc = normalize_emo(emotion)
                    print("Generating: " + story_title + " / " + emotion_arc)
                    raw_text = " <$> ".join((emotion_arc, story_title))
                    context_tokens = proc.encode(raw_text)

                    feed_dict = {
                        context: [context_tokens for _ in range(batch_size)],
                        context_length:
                            [len(context_tokens) for _ in range(batch_size)],
                        tx.context.global_mode(): tf.estimator.ModeKeys.PREDICT
                    }
                    generated = 0
                    for _ in range(nsamples // batch_size):

                        output = sess.run(lm_output, feed_dict=feed_dict)

                        sample_id = output.sample_id
                        for i in range(batch_size):
                            si = sample_id[i][len(context_tokens):]
                            s_text = proc.decode(si)
                            s_text = normalize_stanza(s_text)
                            print(s_text)
                            print()
                            poems_file.write(s_text + "\n\n")
                    # end of poem
                print("=" * 80)
                poems_file.write("="*80+"\n")

if __name__ == "__main__":
    tf.app.run()
