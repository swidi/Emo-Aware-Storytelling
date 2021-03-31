import tensorflow as tf

tf.enable_eager_execution()

raw_dataset = tf.data.TFRecordDataset("data/dev.tf_record")
for raw_record in raw_dataset.take(5):
    example = tf.train.Example()
    example.ParseFromString(raw_record.numpy())
    print(example)
