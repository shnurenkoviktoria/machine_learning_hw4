import matplotlib.pyplot as plt
import numpy as np
from keras.datasets import mnist
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def preprocess_data(x):
    x_flat = x.reshape(x.shape[0], -1) / 255.0
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x_flat)
    return x_scaled


def calculate_cluster_accuracy(y_true, y_pred, k):
    cluster_labels = []
    for i in range(k):
        true_labels = y_true[y_pred == i]
        if len(true_labels) > 0:
            most_common_label = np.argmax(np.bincount(true_labels))
            cluster_labels.append(most_common_label)

    correct_predictions = np.sum(y_pred == np.array(cluster_labels)[y_pred])
    accuracy = correct_predictions / len(y_true)
    return accuracy


def visualize_clusters(x, y_pred, k):
    fig, axs = plt.subplots(k, 10, figsize=(15, 8))
    plt.suptitle(f"K-Means Clustering with k={k}")

    for i in range(k):
        cluster_samples = x[y_pred == i][:10]
        for j in range(10):
            axs[i, j].imshow(cluster_samples[j], cmap=plt.cm.gray)
            axs[i, j].axis("off")

    plt.show()


def main():
    (x_train, y_train), (_, _) = mnist.load_data()
    x_train_scaled = preprocess_data(x_train)

    k_values = [4, 8, 10, 12]

    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=20, max_iter=500)
        y_pred = kmeans.fit_predict(x_train_scaled)

        visualize_clusters(x_train, y_pred, k)

        accuracy = calculate_cluster_accuracy(y_train, y_pred, k)
        print(f"Accuracy for k={k}: {accuracy:.4%}")


if __name__ == "__main__":
    main()
