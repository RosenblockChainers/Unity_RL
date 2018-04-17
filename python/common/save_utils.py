import os
import tensorflow as tf

from tensorflow.python.tools import freeze_graph


def save_model(folder_name, t=0):
    save_path = folder_name + '/model-' + str(t) + '.cptk'
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    saver = tf.train.Saver()
    result = saver.save(tf.keras.backend.get_session(), save_path)
    tf.train.write_graph(tf.keras.backend.get_session().graph, folder_name,
                         'raw_graph_def.pb', as_text=False)
    print('Successfully saved: {0}'.format(result))


def load_model(folder_name):
    ckpt = tf.train.get_checkpoint_state(
        os.path.dirname(folder_name + '/model.ckpt'))
    if ckpt:
        model_path = ckpt.model_checkpoint_path
        saver = tf.train.Saver()
        saver.restore(tf.keras.backend.get_session(), model_path)
        print('Successfully loaded: {0}'.format(ckpt.model_checkpoint_path))
    else:
        print('Training new network')


def export_graph(folder_name, env_name, run_id):
    ckpt = tf.train.get_checkpoint_state(folder_name)
    freeze_graph.freeze_graph(
        input_graph=folder_name + '/raw_graph_def.pb',
        input_binary=True,
        input_checkpoint=ckpt.model_checkpoint_path,
        output_node_names="action",
        output_graph=folder_name + '/' + env_name + '_' + run_id + '.bytes',
        clear_devices=True,
        initializer_nodes="",
        input_saver="",
        restore_op_name="save/restore_all",
        filename_tensor_name="save/Const:0")
