### BEST MODEL ###

# This script contains results related to the best model obtained after hyperparameter tuning - LightGBM tuned with 'balanced_accuracy' score.
# It has the code to obtain the figures presented in the web app (ROC curves, confusion matrix, feature importance bar chart).
# After training the model, we use pickle to store the model in order to make predicitons (labelling) using new data in the app.
# Finally, the script contains a code to generate a csv file with data to test in the app for the predictions.



### Imports
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from lightgbm import LGBMClassifier
from sklearn.preprocessing import label_binarize
from sklearn.metrics import auc, roc_curve, confusion_matrix
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from utils.model_datatransforms import *



### Data Loading

df = pd.read_parquet('data/pred_model_data_full.parquet')

conditions = df['noise_event_laeq_primary_detected_class'].isin(['Music non-amplified', 'Nature elements - Wind', 'Unsupported'])
df.loc[conditions, 'noise_event_laeq_primary_detected_class'] = 'Other'

df.noise_event_laeq_primary_detected_class.value_counts()



X = df.drop(columns=['noise_event_laeq_primary_detected_class']) 

le = LabelEncoder()
y = le.fit_transform(df[['noise_event_laeq_primary_detected_class']])

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=1)



### Pipeline
pipeline = Pipeline(steps=[
    ('day_period_handler',
     DayPeriodHandler()
     ),
    ('month_handler',
     MonthHandler(strategy='month')
     ),
    ('day_of_the_week_handler',
     DayoftheWeekHandler(strategy='full')
     ),
    ('column_dropper',
     ColumnDropper(columns_to_drop=[
    'date', 
    'hour',
    'minute',
    'second',
    'noise_event_laeq_model_id',
    'noise_event_laeq_primary_detected_certainty'
    ])
     ),
    ('custom_encoder',
     CustomEncoder(
        columns=['#object_id', 'day_period', 'month', 'weekday'],
        strategy='one_hot'
        )
     ),
    ('pca',
     PCATransformer(
        n_components=7,
        columns=[
            'lamax', 'laeq', 'lceq', 'lcpeak',
            'lamax_shift_t-_1', 'laeq_shift_t-_1', 'lceq_shift_t-_1',
            'lcpeak_shift_t-_1', 'lamax_shift_t-_2', 'laeq_shift_t-_2',
            'lceq_shift_t-_2', 'lcpeak_shift_t-_2', 'lamax_shift_t-_3',
            'laeq_shift_t-_3', 'lceq_shift_t-_3', 'lcpeak_shift_t-_3',
            'lamax_shift_t-_4', 'laeq_shift_t-_4', 'lceq_shift_t-_4',
            'lcpeak_shift_t-_4', 'lamax_shift_t-_5', 'laeq_shift_t-_5',
            'lceq_shift_t-_5', 'lcpeak_shift_t-_5'
        ])
     ),
     ('lightgbm', LGBMClassifier(random_state=42, class_weight='balanced', num_leaves=25, n_estimators=80, min_child_samples=11, learning_rate=0.06))
])


pipeline.fit(X_train, y_train)


### Feature Importance
lgb_model = pipeline.named_steps['lightgbm']

# Get feature importance values and the list of feature names in the same order
feature_importance = lgb_model.feature_importances_
feature_names = pipeline.named_steps['lightgbm'].feature_name_

# Create a list of tuples (feature name, feature importance)
feature_importance_tuples = list(zip(feature_names, feature_importance))

# Sort the list by feature importance
feature_importance_tuples.sort(key=lambda x: x[1], reverse=False)

# Extract the sorted feature names and importances
sorted_feature_names = [tup[0] for tup in feature_importance_tuples]
sorted_feature_importance = [tup[1] for tup in feature_importance_tuples]

# Calculate the bar width
bar_width = 0.7

# Calculate the positions of the bars
bar_positions = np.arange(len(sorted_feature_importance))

# Plot the bar chart
plt.figure(figsize=(8, 10))
plt.barh(bar_positions, sorted_feature_importance, align='center', height=bar_width)
plt.yticks(bar_positions, sorted_feature_names)

# Increase the separation between y-axis tick labels
plt.gca().set_yticks(bar_positions)
plt.gca().set_yticklabels(sorted_feature_names)

plt.xlabel('Importance')
plt.ylabel('Features')
plt.title('Feature Importance')
plt.tight_layout()
plt.savefig("assets/feature_importance.png", bbox_inches='tight')
plt.close()


### Make predictions
y_pred = pipeline.predict(X_test)
y_pred_proba = pipeline.predict_proba(X_test)


### Plot ROC curves for each class (OvR)
n_classes = 5
true_labels = y_test 

# Binarize the true labels
binarized_labels = label_binarize(true_labels, classes=np.unique(true_labels))

# Compute ROC curve and ROC area for each class
fpr = dict()
tpr = dict()
roc_auc = dict()

for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(binarized_labels[:, i], y_pred_proba[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

# Plot ROC curve for each class
plt.figure(figsize=(8, 6))
colors = ['blue', 'red', 'green', 'yellow', 'orange'] 

for i, color in zip(range(n_classes), colors):
    plt.plot(fpr[i], tpr[i], color=color, lw=2, label='ROC curve of class {0} (area = {1:0.2f})'.format(i, roc_auc[i]))

plt.plot([0, 1], [0, 1], 'k--', lw=2)  # Plot diagonal line for reference
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.savefig('assets/ROC_curves.png',bbox_inches='tight')
plt.close() 



### Confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Define the class labels
classes = list(le.classes_)

cm_df = pd.DataFrame(cm,
                     index = classes, 
                     columns = classes)

plt.figure(figsize=(8,6))
ax = sns.heatmap(cm_df, annot=True, fmt='.0f')
plt.title('Confusion Matrix')
plt.ylabel('Actual Values')
plt.xlabel('Predicted Values')

# Adjust the alignment of the tick labels
plt.xticks(rotation=45)

plt.savefig('assets/confusion_matrix.png', bbox_inches='tight')
plt.close()



### Save the best model using pickle
filename = 'best_model.pkl'
pickle.dump(pipeline, open(filename, 'wb'))


### Choose a percentage of the test set to use in the app for the predictions
percentage = 0.25 
sampled_df = X_test.sample(frac=percentage, random_state=42)
sampled_df.to_csv('sampled_data.csv', index=False)