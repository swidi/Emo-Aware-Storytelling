import sklearn.metrics
import sys

model_file = open(sys.argv[1], "r")
anno_file = open(sys.argv[2], "r")

model = model_file.read().split()
anno = anno_file.read().split()

classes = {"Joy Joy Suspense":1, "Suspense Suspense Vitality":2, "Humor Annoyance Humor":3}

print(sklearn.metrics.f1_score(model, anno, average='micro'))
print(sklearn.metrics.classification_report(model, anno,target_names=classes.keys()))
