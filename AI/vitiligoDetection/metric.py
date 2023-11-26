import tensorflow as tf
from tensorflow.keras.models import load_model
import tensorflow_model_analysis as tfma

model = load_model("models/imageclassifier")

# Define your metrics
metrics = [
   tf.keras.metrics.AUC(name='auc', num_thresholds=10000),
   tf.keras.metrics.Accuracy(name='accuracy', num_thresholds=10000),
   tf.keras.metrics.Precision(name='precision', num_thresholds=10000),
   tf.keras.metrics.Recall(name='recall', num_thresholds=10000),
   tf.keras.metrics.AUC(name='auc', num_thresholds=10000),
]

# Convert metrics to TFMA specs
metrics_specs = tfma.metrics.specs_from_metrics(metrics)

# Run model analysis
eval_result = tfma.run_model_analysis(
   eval_shared_model=model,
   data_location="./data",
   output_path="./output",
   metrics_specs=metrics_specs)

