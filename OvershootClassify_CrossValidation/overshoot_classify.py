
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import input_data
import tensorflow as tf

PERCENT = 0.8
TRAIN_TIMES = 20


def main(_):
    # Import data
    all_data = input_data.read_data_set()

    # Create the model
    x = tf.placeholder(tf.float32, [None, 40])
    W = tf.Variable(tf.zeros([40, 9]))
    b = tf.Variable(tf.zeros([9]))
    y = tf.matmul(x, W) + b

    # Define loss and optimizer
    y_ = tf.placeholder(tf.float32, [None, 9])
    cross_entropy = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

    sess = tf.InteractiveSession()
    
    # Train
    print('\nTraining classification of overshoot...')
    print('  Condition: percent of train dataset {} , train times {}'.format(
        PERCENT, TRAIN_TIMES))

    accuracy_result = []
    for _ in range(TRAIN_TIMES):
        tf.global_variables_initializer().run()
        data_set = all_data.next_shuffle(PERCENT)
        
        for _ in range(1000):
            batch_xs, batch_ys = data_set[0]
            sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

        # Test trained model
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        accuracy_result.append(sess.run(accuracy, feed_dict={x: data_set[1][0],
                                            y_: data_set[1][1]}))
        print('  accuracy: {}'.format(accuracy_result[-1]))

    print('  average accuracy:{}'.format(sum(accuracy_result) / len(accuracy_result)))


if __name__ == '__main__':
    tf.app.run(main=main, argv=[sys.argv[0]])
