
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import input_data
import tensorflow as tf

PERCENT = 0.8
TRAIN_TIMES = 10


def addLayer(inputData,inSize,outSize,activity_function = None):  
    Weights = tf.Variable(tf.random_normal([inSize,outSize]))   
    basis = tf.Variable(tf.zeros([1,outSize])+0.1)    
    weights_plus_b = tf.matmul(inputData,Weights)+basis  
    if activity_function is None:  
        ans = weights_plus_b  
    else:  
        ans = activity_function(weights_plus_b)  
    return ans  


def main(_):
    # Import data
    all_data = input_data.read_data_set()

    xs = tf.placeholder(tf.float32,[None,80])   
    ys = tf.placeholder(tf.float32,[None,9])  

    l1 = addLayer(xs,80,80,activity_function=tf.nn.sigmoid) 
    l2 = addLayer(l1,80,9,activity_function=tf.nn.sigmoid)  

    loss = tf.reduce_mean(tf.reduce_sum(tf.square((ys-l2)),reduction_indices = [1]))

    train = tf.train.GradientDescentOptimizer(0.1).minimize(loss) 

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
            sess.run(train, feed_dict={xs: batch_xs, ys: batch_ys})

        # Test trained model
        correct_prediction = tf.equal(tf.argmax(l2, 1), tf.argmax(ys, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        accuracy_result.append(sess.run(accuracy, feed_dict={xs: data_set[1][0],
                                            ys: data_set[1][1]}))
        print('  accuracy: {}'.format(accuracy_result[-1]))

    print('  average accuracy:{}'.format(sum(accuracy_result) / len(accuracy_result)))


if __name__ == '__main__':
    tf.app.run(main=main, argv=[sys.argv[0]])
