import numpy as np
import tensorflow as tf

from models.core.model_base import ModelBase


class LinearNet(ModelBase):
    def __init__(self, d):
        super().__init__()
        self.d = d
        # input state
        self.state_in = tf.placeholder(dtype=tf.float32,
                                       shape=[1, d],
                                       name='vector_observation')
        # model
        self.model = tf.keras.models.Sequential()
        self.model.add(tf.keras.layers.Dense(1, input_dim=d, use_bias=False))
        # output action
        self.output = self.model(self.state_in)
        self.output = tf.reshape(self.output, [])
        self.output = tf.cond(tf.less(self.output, 0),
                              lambda: tf.constant(0),
                              lambda: tf.constant(1))
        # cast output to tf.int64
        self.output = tf.reshape(self.output, [1, 1])
        self.output = tf.cast(self.output, tf.int64, name='action')

    def take_action(self, info):
        return self.output.eval(
            feed_dict={self.state_in: info.vector_observations})

    def update_param(self, new_param):
        new_weights = []
        size = 0
        for w in self.model.get_weights():
            new_w = new_param[size:size + w.size]
            new_w = np.reshape(new_w, w.shape)
            size += w.size
            new_weights.append(new_w)
        self.model.set_weights(new_weights)

    def param_vector(self):
        w = self.model.get_weights()[0]
        weights = np.reshape(w, (w.size, 1))
        for i in range(1, len(self.model.get_weights())):
            w = self.model.get_weights()[i]
            weights = np.vstack((weights, np.reshape(w, (w.size, 1))))
        return weights
